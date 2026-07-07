from django.db.models import Count, Q
from apps.news.models import Category, Article
from apps.advertisements.models import Advertisement
from apps.core.models import WebsiteSettings


def global_context(request):
    categories = Category.objects.filter(is_active=True).annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    )[:10]
    trending = Article.objects.filter(status='published', is_trending=True)[:5]
    breaking = Article.objects.filter(status='published', is_breaking=True)[:3]
    header_ads = Advertisement.objects.filter(position='header', is_active=True).first()
    sidebar_ads = Advertisement.objects.filter(position='sidebar', is_active=True)[:2]
    site_settings = None
    try:
        site_settings = WebsiteSettings.objects.first()
    except Exception:
        pass

    return {
        'nav_categories': categories,
        'trending_news': trending,
        'breaking_news': breaking,
        'header_ad': header_ads,
        'sidebar_ads': sidebar_ads,
        'site_settings': site_settings,
    }
