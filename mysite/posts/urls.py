from django.urls import include, path
from . import views

app_name = 'posts'

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
  path('upload_post', views.upload_post, name = 'upload_post'),
  path('request_post_list', views.request_post_list, name = 'request_post_list'),

]
