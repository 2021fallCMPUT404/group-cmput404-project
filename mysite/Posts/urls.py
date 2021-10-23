from django.urls import include, path
from . import views


urlpatterns = [
  path('', views.placeholder, name='post'),
  path('<int:Post_id>/', views.post, name='post_placeholder')
]