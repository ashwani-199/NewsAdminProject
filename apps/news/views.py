from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Q, F, Sum
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.urls import reverse
from apps.news.models import Article, Category, Tag, Like, Bookmark
from apps.comments.models import Comment
from apps.comments.forms import CommentForm
from apps.core.models import ContactMessage, WebsiteSettings


class HomeView(TemplateView):
    template_name = 'news/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['featured_articles'] = Article.objects.filter(
            status='published', is_featured=True
        ).select_related('author', 'category')[:5]

        context['latest_news'] = Article.objects.filter(
            status='published'
        ).select_related('author', 'category')[:12]

        context['breaking_news'] = Article.objects.filter(
            status='published', is_breaking=True
        ).select_related('author', 'category')[:5]

        context['trending_news'] = Article.objects.filter(
            status='published', is_trending=True
        ).select_related('author', 'category')[:6]

        context['editor_picks'] = Article.objects.filter(
            status='published', is_editor_pick=True
        ).select_related('author', 'category')[:4]

        context['most_viewed'] = Article.objects.filter(
            status='published'
        ).order_by('-views_count')[:6]

        context['categories'] = Category.objects.filter(is_active=True).annotate(
            article_count=Count('articles', filter=Q(articles__status='published'))
        )[:10]

        context['youtube_videos'] = Article.objects.filter(
            status='published'
        ).exclude(
            content__contains='youtube' 
        ).order_by('-published_at')[:6]

        settings = WebsiteSettings.objects.first()
        context['site_settings'] = settings

        return context


class CategoryView(ListView):
    model = Article
    template_name = 'news/category.html'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        return Article.objects.filter(
            status='published', category=self.category
        ).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagView(ListView):
    model = Article
    template_name = 'news/tag.html'
    paginate_by = 12

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Article.objects.filter(
            status='published', tags__name__iexact=self.tag.name
        ).select_related('author', 'category').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    slug_field = 'slug'

    def get_queryset(self):
        return Article.objects.filter(
            status='published'
        ).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object

        Article.objects.filter(pk=article.pk).update(views_count=F('views_count') + 1)

        context['comments'] = Comment.objects.filter(
            article=article, parent=None, is_approved=True
        ).select_related('user')[:50]

        context['comment_form'] = CommentForm()

        context['related_articles'] = Article.objects.filter(
            status='published',
            category=article.category
        ).exclude(pk=article.pk).select_related('author')[:4]

        context['prev_article'] = Article.objects.filter(
            status='published',
            published_at__lt=article.published_at
        ).order_by('-published_at').first()

        context['next_article'] = Article.objects.filter(
            status='published',
            published_at__gt=article.published_at
        ).order_by('published_at').first()

        context['tags'] = article.tags.all()

        if self.request.user.is_authenticated:
            context['user_liked'] = Like.objects.filter(
                user=self.request.user, article=article
            ).exists()
            context['user_bookmarked'] = Bookmark.objects.filter(
                user=self.request.user, article=article
            ).exists()

        return context


class AuthorView(ListView):
    model = Article
    template_name = 'news/author.html'
    paginate_by = 12

    def get_queryset(self):
        self.author = get_object_or_404(settings.AUTH_USER_MODEL, pk=self.kwargs['pk'])
        return Article.objects.filter(
            status='published', author=self.author
        ).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        context['total_articles'] = Article.objects.filter(
            author=self.author, status='published'
        ).count()
        context['total_views'] = Article.objects.filter(
            author=self.author, status='published'
        ).aggregate(total=Sum('views_count'))['total'] or 0
        return context


class SearchView(ListView):
    model = Article
    template_name = 'news/search.html'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '')
        tag = self.request.GET.get('tag', '')
        author = self.request.GET.get('author', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')

        articles = Article.objects.filter(status='published').select_related('author', 'category')

        if query:
            articles = articles.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(content__icontains=query) |
                Q(meta_keywords__icontains=query)
            )

        if category:
            articles = articles.filter(category__slug=category)

        if tag:
            articles = articles.filter(tags__name__iexact=tag)

        if author:
            articles = articles.filter(author__username__icontains=author)

        if date_from:
            articles = articles.filter(published_at__gte=date_from)

        if date_to:
            articles = articles.filter(published_at__lte=date_to)

        return articles.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class SearchSuggestionsView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if len(query) < 2:
            return JsonResponse({'results': []})

        articles = Article.objects.filter(
            status='published', title__icontains=query
        ).values('title', 'slug', 'featured_image')[:5]

        results = [
            {
                'title': a['title'],
                'url': reverse('news:article_detail', args=[a['slug']]),
                'image': a['featured_image'] or '',
            }
            for a in articles
        ]
        return JsonResponse({'results': results})


class LikeArticleView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'}, status=403)

        article = get_object_or_404(Article, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, article=article)

        if not created:
            like.delete()
            article.likes_count = max(0, article.likes_count - 1)
            article.save(update_fields=['likes_count'])
            return JsonResponse({'liked': False, 'count': article.likes_count})

        article.likes_count = Like.objects.filter(article=article).count()
        article.save(update_fields=['likes_count'])
        return JsonResponse({'liked': True, 'count': article.likes_count})


class BookmarkArticleView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'}, status=403)

        article = get_object_or_404(Article, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)

        if not created:
            bookmark.delete()
            return JsonResponse({'bookmarked': False})

        return JsonResponse({'bookmarked': True})


class AboutView(TemplateView):
    template_name = 'news/about.html'


class ContactView(View):
    template_name = 'news/contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not all([name, email, subject, message]):
            messages.error(request, 'All fields are required.')
            return render(request, self.template_name)

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Thank you! Your message has been sent.')
        return redirect('news:contact')


class PrivacyPolicyView(TemplateView):
    template_name = 'news/privacy_policy.html'


class TermsView(TemplateView):
    template_name = 'news/terms.html'


class DisclaimerView(TemplateView):
    template_name = 'news/disclaimer.html'


class FAQView(TemplateView):
    template_name = 'news/faq.html'


class CareersView(TemplateView):
    template_name = 'news/careers.html'



