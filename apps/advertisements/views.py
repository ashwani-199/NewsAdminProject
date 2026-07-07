from django.shortcuts import get_object_or_404, redirect
from django.views import View
from apps.advertisements.models import Advertisement


class AdClickView(View):
    def get(self, request, pk):
        ad = get_object_or_404(Advertisement, pk=pk, is_active=True)
        ad.clicks_count += 1
        ad.save(update_fields=['clicks_count'])
        return redirect(ad.url or '/')
