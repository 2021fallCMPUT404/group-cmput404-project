from django.urls import include, path
from . import views


urlpatterns = [
  path('', views.post, name='post'),
  path('<int:Post_id>/', views.placeholder, name='post_placeholder')
]