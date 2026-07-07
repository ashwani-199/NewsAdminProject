from django.contrib import admin
from apps.advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'order', 'is_active', 'clicks_count', 'impressions_count', 'start_date', 'end_date']
    list_filter = ['position', 'is_active']
    search_fields = ['title']
    list_editable = ['order', 'is_active']
