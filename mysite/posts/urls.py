from django.urls import include, path
from . import views


urlpatterns = [
  path('feed', views.placeholder, name='feed'),
  path('addpost/', views.addPost.as_view(), name="addpost"),
  path('<int:pk>/comment/', views.addComment.as_view(), name="addcomment"),
  path('<int:Post_id>/', views.post, name='post_placeholder'),
  path('<int:pk>/edit/', views.updatePost.as_view(), name='editpost'),
  path('<int:pk>/delete-post/', views.deletePost.as_view(), name='deletepost'),
  path('<int:pk>/share/', views.SharedPostView.as_view(), name='sharepost'),
  path('likePost/<int:pk>/', views.likePost, name='likepost'),
  path('likeComment/<int:pk>/', views.likeComment, name='likecomment'),
]
