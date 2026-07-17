from django.contrib import admin
from apps.core.models import WebsiteSettings, ContactMessage, FAQ, Career, CareerApplication


@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_tagline', 'contact_email', 'contact_phone']
    fieldsets = (
        ('Site Info', {'fields': ('site_name', 'site_tagline', 'site_logo', 'site_favicon')}),
        ('Contact', {'fields': ('contact_email', 'contact_phone', 'address')}),
        ('Footer & Social', {'fields': ('footer_text', 'copyright_text', 'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url', 'telegram_url', 'whatsapp_number')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
        ('Analytics & Maps', {'fields': ('google_analytics_id', 'google_maps_api_key')}),
    )


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
