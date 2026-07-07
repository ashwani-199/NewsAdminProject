from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.news.sitemaps import ArticleSitemap, CategorySitemap, StaticViewSitemap

sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.news.urls', namespace='news')),
    path('account/', include('apps.accounts.urls', namespace='account')),
    path('user/', include('apps.users.urls', namespace='users')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('comments/', include('apps.comments.urls', namespace='comments')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('newsletter/', include('apps.newsletter.urls', namespace='newsletter')),
    path('ads/', include('apps.advertisements.urls', namespace='ads')),
    path('api/', include('apps.api.urls', namespace='api')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', include('robots.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
