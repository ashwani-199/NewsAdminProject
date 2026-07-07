from django.contrib import admin
from apps.core.models import WebsiteSettings, ContactMessage, FAQ, Career, CareerApplication


@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_tagline', 'contact_email', 'contact_phone']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark selected as read'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'employment_type', 'is_active', 'application_deadline']
    list_filter = ['employment_type', 'is_active']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'career', 'created_at']
