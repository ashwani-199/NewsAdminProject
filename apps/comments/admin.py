from django.contrib import admin
from apps.comments.models import Comment, CommentLike


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'content_preview', 'is_approved', 'is_reported', 'created_at']
    list_filter = ['is_approved', 'is_reported', 'created_at']
    search_fields = ['content', 'user__username', 'article__title']
    list_editable = ['is_approved']
    actions = ['approve_comments', 'reject_comments']

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'

    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
    reject_comments.short_description = 'Reject selected comments'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'created_at']
