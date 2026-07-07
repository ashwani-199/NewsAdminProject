from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.api import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='api_change_password'),
]
