from django.contrib import admin
from django.utils.html import format_html
from apps.news.models import Category, Tag, Article, ArticleImage, Like, Bookmark


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'total_articles', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'image', 'icon')}),
        ('SEO', {'fields': ('meta_title', 'meta_description')}),
        ('Settings', {'fields': ('is_active', 'order')}),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'is_featured', 'is_breaking',
                    'is_trending', 'views_count', 'published_at']
    list_filter = ['status', 'is_featured', 'is_breaking', 'is_trending', 'is_editor_pick',
                   'category', 'created_at']
    search_fields = ['title', 'summary', 'content', 'author__username', 'author__email']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured', 'is_breaking', 'is_trending']
    inlines = [ArticleImageInline]
    date_hierarchy = 'published_at'
    readonly_fields = ['views_count', 'likes_count', 'reading_time', 'preview_image']
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'summary', 'content', 'category', 'tags')}),
        ('Media', {'fields': ('featured_image', 'featured_image_alt', 'preview_image')}),
        ('Author & Status', {'fields': ('author', 'status', 'published_at', 'scheduled_at')}),
        ('Featured Sections', {'fields': ('is_featured', 'is_breaking', 'is_trending', 'is_editor_pick', 'is_pinned')}),
        ('Comments', {'fields': ('allow_comments',)}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
        ('Stats', {'fields': ('views_count', 'likes_count', 'reading_time')}),
    )

    def preview_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.featured_image.url)
        return '-'
    preview_image.short_description = 'Preview'

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'article__title']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'article__title']
