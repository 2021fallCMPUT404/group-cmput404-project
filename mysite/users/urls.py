from django.urls import path
from . import views

urlpatterns = [
  path('', views.homepage, name='homepage'),
  path('<int:User_id>/', views.placeholder, name='placeholder'),
  path('users_test', views.index, name='index'),
  path('create_user/', views.create_user_view, name='create_user')
]