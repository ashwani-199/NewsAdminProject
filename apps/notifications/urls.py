from django.urls import path
from apps.notifications import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications'),
    path('mark-read/<int:pk>/', views.MarkNotificationRead.as_view(), name='mark_read'),
    path('mark-all-read/', views.MarkAllRead.as_view(), name='mark_all_read'),
    path('unread-count/', views.UnreadCountView.as_view(), name='unread_count'),
]
