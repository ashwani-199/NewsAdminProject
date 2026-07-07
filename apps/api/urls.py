from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.api import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='api_article')
router.register(r'categories', views.CategoryViewSet, basename='api_category')
router.register(r'tags', views.TagViewSet, basename='api_tag')
router.register(r'comments', views.CommentViewSet, basename='api_comment')
router.register(r'authors', views.AuthorViewSet, basename='api_author')
router.register(r'bookmarks', views.BookmarkViewSet, basename='api_bookmark')

app_name = 'api'

urlpatterns = [
    path('auth/', include('apps.api.auth_urls')),
    path('search/', views.SearchAPIView.as_view(), name='api_search'),
    path('newsletter/subscribe/', views.NewsletterSubscribeAPIView.as_view(), name='api_newsletter_subscribe'),
    path('trending/', views.TrendingArticlesAPIView.as_view(), name='api_trending'),
    path('breaking/', views.BreakingNewsAPIView.as_view(), name='api_breaking'),
    path('featured/', views.FeaturedArticlesAPIView.as_view(), name='api_featured'),
    path('', include(router.urls)),
]
