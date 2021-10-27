from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
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
    path('user_home_page', views.user_home_page_view, name='user_home_page')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)