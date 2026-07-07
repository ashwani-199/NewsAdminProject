from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('author/', views.AuthorDashboardView.as_view(), name='author_dashboard'),
    path('author/articles/', views.AuthorArticlesView.as_view(), name='author_articles'),
    path('author/articles/create/', views.CreateArticleView.as_view(), name='create_article'),
    path('author/articles/edit/<slug:slug>/', views.EditArticleView.as_view(), name='edit_article'),
    path('author/articles/delete/<int:pk>/', views.DeleteArticleView.as_view(), name='delete_article'),
    path('author/stats/', views.AuthorStatsView.as_view(), name='author_stats'),
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/users/', views.AdminUsersView.as_view(), name='admin_users'),
    path('admin/authors/', views.AdminAuthorsView.as_view(), name='admin_authors'),
    path('admin/articles/', views.AdminArticlesView.as_view(), name='admin_articles'),
    path('admin/comments/', views.AdminCommentsView.as_view(), name='admin_comments'),
    path('admin/categories/', views.AdminCategoriesView.as_view(), name='admin_categories'),
    path('admin/subscribers/', views.AdminSubscribersView.as_view(), name='admin_subscribers'),
    path('admin/messages/', views.AdminMessagesView.as_view(), name='admin_messages'),
    path('admin/settings/', views.AdminSettingsView.as_view(), name='admin_settings'),
    path('admin/contacts/', views.AdminContactMessagesView.as_view(), name='admin_contacts'),
]
