from django.urls import path
from apps.news import views

app_name = 'news'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('author/<int:pk>/', views.AuthorView.as_view(), name='author'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('search-suggestions/', views.SearchSuggestionsView.as_view(), name='search_suggestions'),
    path('like/<int:pk>/', views.LikeArticleView.as_view(), name='like_article'),
    path('bookmark/<int:pk>/', views.BookmarkArticleView.as_view(), name='bookmark_article'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('disclaimer/', views.DisclaimerView.as_view(), name='disclaimer'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('careers/', views.CareersView.as_view(), name='careers'),
]
