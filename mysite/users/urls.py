from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<int:User_id>/', views.placeholder, name='placeholder'),
    path('users_test', views.index, name='index'),
    path('create_user/', views.create_user_view, name='create_user'),
    path('<int:User_id>/posts/', views.user_post_view, name='view_user_posts'),
    path('user_login/', views.login_view, name='user_login'),
    path('register/', views.register, name='register'),
    path('login', views.login_view, name='login'),
]