from django.urls import path
from . import views


urlpatterns = [
    path('', views.APIRoot.as_view(), name = 'root'),
    path('posts/', views.PostEndpoint.as_view(), name = 'post-endpoint'),
    path('posts/<int:pk>/', views.PostDetailedEndpoint.as_view(), name = 'detailed-post'),
    path('comments/', views.CommentEndpoint.as_view(), name = 'comment-endpoint'),
    path('like/<int:pk>/', views.LikeEndpoint.as_view(), name = 'like-endpoint'),
    path('dislike/<int:pk>/', views.DislikeEndpoint.as_view(), name = 'dislike-endpoint')
]