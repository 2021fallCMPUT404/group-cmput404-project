from django.urls import path
from . import views

urlpatterns = [
  path('', views.homepage, name='homepage'),
  path('<int:User_id>/', views.placeholder, name='placeholder'),
]