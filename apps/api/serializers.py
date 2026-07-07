from rest_framework import serializers
from apps.news.models import Article, Category, Tag, Like, Bookmark
from apps.comments.models import Comment
from apps.accounts.models import User
from apps.newsletter.models import Subscriber


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio',
                  'avatar', 'role', 'website', 'twitter_handle', 'facebook_url',
                  'linkedin_url', 'date_joined']
        read_only_fields = ['id', 'role', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'icon', 'article_count', 'is_active']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class ArticleListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'summary', 'featured_image', 'category_name',
                  'category_slug', 'author_name', 'author_username', 'status',
                  'is_featured', 'is_breaking', 'is_trending', 'views_count',
                  'likes_count', 'reading_time', 'published_at', 'created_at']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'summary', 'content', 'featured_image',
                  'featured_image_alt', 'category', 'tags', 'author', 'status',
                  'is_featured', 'is_breaking', 'is_trending', 'is_editor_pick',
                  'views_count', 'likes_count', 'reading_time', 'comment_count',
                  'meta_title', 'meta_description', 'published_at', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'parent', 'content', 'is_approved',
                  'likes_count', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'is_approved', 'likes_count', 'created_at']

    def get_replies(self, obj):
        if obj.is_parent:
            replies = Comment.objects.filter(parent=obj, is_approved=True)
            return CommentSerializer(replies, many=True).data
        return []

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookmarkSerializer(serializers.ModelSerializer):
    article = ArticleListSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'article', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class NewsletterSubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()
