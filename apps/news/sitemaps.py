from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.news.models import Article, Category


class ArticleSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Article.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['news:home', 'news:about', 'news:contact', 'news:privacy_policy',
                'news:terms', 'news:disclaimer', 'news:faq', 'news:careers']

    def location(self, item):
        return reverse(item)
