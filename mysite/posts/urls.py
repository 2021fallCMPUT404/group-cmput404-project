from django.urls import include, path
from . import views



urlpatterns = [
  path('', views.placeholder, name='post'),
  path('addpost/', views.addPost.as_view(), name="addpost"),
  path('<int:pk>/comment/', views.addComment.as_view(), name="addcomment"),
  path('<int:Post_id>/', views.post, name='post_placeholder'),
  path('<int:pk>/edit/', views.updatePost.as_view(), name='editpost'),
  path('<int:pk>/delete-post/', views.deletePost.as_view(), name='deletepost'),
  path('<int:pk>/share/', views.SharedPostView.as_view(), name='sharepost'),
  path('select_github_activity/', views.select_github_activity, name='select_github_activity'),
  path('request_post/<str:id>', views.request_post, name = 'request_post'),
  path('crud_post/<str:id>', views.crud_post, name = 'crud_post'),
  path('request_post_list', views.request_post_list, name = 'request_post_list'),
  #path('delete_post/<str:id>', views.delete_post, name = 'delete_post'),
  path('manage_post_comment/<str:post_id>', views.manage_post_comment, name = 'manage_post_comment'),
  path('create_new_post', views.create_new_post, name = 'create_new_post'),

]
