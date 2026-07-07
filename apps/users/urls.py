from django.urls import path
from apps.users import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('bookmarks/', views.BookmarksView.as_view(), name='bookmarks'),
    path('history/', views.ReadingHistoryView.as_view(), name='reading_history'),
    path('comments/', views.MyCommentsView.as_view(), name='my_comments'),
    path('notifications/', views.UserNotificationsView.as_view(), name='notifications'),
    path('newsletter/', views.NewsletterSettingsView.as_view(), name='newsletter_settings'),
]
