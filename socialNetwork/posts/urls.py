from django.urls import include, path
from . import views


urlpatterns = [
  path('', views.PostView.as_view(), name='post')
]