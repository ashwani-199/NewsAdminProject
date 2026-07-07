from django.contrib import admin
from apps.newsletter.models import Subscriber, Newsletter


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    actions = ['deactivate_subscribers']

    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscribers.short_description = 'Deactivate selected subscribers'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'is_sent', 'sent_at', 'created_at']
    list_filter = ['is_sent', 'created_at']
    search_fields = ['subject']
