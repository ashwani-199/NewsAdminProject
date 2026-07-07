from django import template
from apps.news.models import Article, Category

register = template.Library()


@register.simple_tag
def get_popular_articles(count=5):
    return Article.objects.filter(status='published').order_by('-views_count')[:count]


@register.simple_tag
def get_categories():
    return Category.objects.filter(is_active=True)


@register.simple_tag
def get_trending_articles(count=5):
    return Article.objects.filter(status='published', is_trending=True)[:count]


@register.filter
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value


@register.filter
def file_size(value):
    if value < 1024:
        return f'{value} B'
    elif value < 1024 * 1024:
        return f'{value / 1024:.1f} KB'
    return f'{value / (1024 * 1024):.1f} MB'
