from django.urls import path
from apps.advertisements import views

app_name = 'ads'

urlpatterns = [
    path('click/<int:pk>/', views.AdClickView.as_view(), name='ad_click'),
]
