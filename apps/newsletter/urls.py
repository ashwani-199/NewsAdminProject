from django.urls import path
from apps.newsletter import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<str:token>/', views.UnsubscribeView.as_view(), name='unsubscribe'),
]
