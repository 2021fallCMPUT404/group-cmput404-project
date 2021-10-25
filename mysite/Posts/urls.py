from django.urls import include, path
from . import views
from .views import SharedPostView


urlpatterns = [
  path('', views.placeholder, name='post'),
  path('<int:Post_id>/', views.post, name='post_placeholder'),
  path('<int:Post_id>/delete/', views.delete_post, name='delete-post')
  path('<int:Post_id>/share', SharedPostView.as_view(), name='share-post'),
  
]
