from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from apps.news.models import Article, Category, Tag, Like, Bookmark
from apps.comments.models import Comment
from apps.accounts.models import User
from apps.newsletter.models import Subscriber
from apps.api.serializers import (
    UserSerializer, RegisterSerializer, CategorySerializer, TagSerializer,
    ArticleListSerializer, ArticleDetailSerializer, CommentSerializer,
    BookmarkSerializer, NewsletterSubscribeSerializer
)
from apps.api.permissions import IsAuthorOrReadOnly


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Account created successfully',
        }, status=status.HTTP_201_CREATED)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'error': 'Password too short'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed'})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True).annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).order_by('name')
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author', 'category').prefetch_related('tags')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'status', 'is_featured', 'is_breaking', 'is_trending', 'author']
    search_fields = ['title', 'summary', 'content', 'tags__name']
    ordering_fields = ['published_at', 'views_count', 'likes_count', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            return qs.filter(status='published')
        return qs

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        article = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, article=article)
        if not created:
            like.delete()
            article.likes_count = max(0, article.likes_count - 1)
            article.save(update_fields=['likes_count'])
            return Response({'liked': False, 'count': article.likes_count})
        article.likes_count += 1
        article.save(update_fields=['likes_count'])
        return Response({'liked': True, 'count': article.likes_count})

    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        article = self.get_object()
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)
        if not created:
            bookmark.delete()
            return Response({'bookmarked': False})
        return Response({'bookmarked': True})


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(role='journalist').annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    )
    serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_approved=True).select_related('user', 'article')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        article_id = self.request.query_params.get('article')
        if article_id:
            qs = qs.filter(article_id=article_id)
        return qs


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('article__author', 'article__category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchAPIView(generics.ListAPIView):
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if not query:
            return Article.objects.none()
        return Article.objects.filter(
            Q(status='published') &
            (Q(title__icontains=query) |
             Q(summary__icontains=query) |
             Q(content__icontains=query) |
             Q(tags__name__icontains=query))
        ).distinct().select_related('author', 'category')[:20]


class TrendingArticlesAPIView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    queryset = Article.objects.filter(status='published', is_trending=True)[:10]


class BreakingNewsAPIView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    queryset = Article.objects.filter(status='published', is_breaking=True)[:5]


class FeaturedArticlesAPIView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    queryset = Article.objects.filter(status='published', is_featured=True)[:6]


class NewsletterSubscribeAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = NewsletterSubscribeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            sub, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={'token': get_random_string(64)}
            )
            if not created and sub.is_active:
                return Response({'message': 'Already subscribed'})
            if not created:
                sub.is_active = True
                sub.save()
            return Response({'message': 'Subscribed successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
