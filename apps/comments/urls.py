from django.urls import path
from apps.comments import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:article_id>/', views.AddCommentView.as_view(), name='add_comment'),
    path('reply/<int:comment_id>/', views.AddReplyView.as_view(), name='add_reply'),
    path('edit/<int:pk>/', views.EditCommentView.as_view(), name='edit_comment'),
    path('delete/<int:pk>/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('report/<int:pk>/', views.ReportCommentView.as_view(), name='report_comment'),
    path('like/<int:pk>/', views.LikeCommentView.as_view(), name='like_comment'),
]
