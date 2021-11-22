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

  path('select_github_activity/', views.select_github_activity, name='select_github_activity'),
  path('request_post_list', views.request_post_list, name = 'request_post_list'),
  path('request_post/<int:id>', views.request_post, name = 'request_post'),
  path('create_new_post', views.create_new_post, name = 'create_new_post'),
  path('manage_user_post/<int:user_id>', views.manage_user_post, name='manage_user_post'),
  path('crud_post/<int:id>', views.crud_post, name = 'crud_post'),
  path('manage_post_comment/<int:post_id>', views.manage_post_comment, name = 'manage_post_comment'),
  path('crud_comment/<int:comment_id>', views.crud_comment, name='crud_comment'),
  path('manage_post_like/<int:post_id>', views.manage_post_like, name = 'manage_post_like'),
  path('crud_like/<int:like_id>', views.crud_like, name='crud_like')

]
