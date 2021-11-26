from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from rest_framework.authtoken import views as token_views

app_name = 'users'

urlpatterns = [
    path('', views.UserList, name='homepage'),
    path('userGet/<int:User_id>/', views.userGet, name='user_get'),
    path('userPost/<int:User_id>/', views.userPost, name='user_post'),
    path('users_test', views.index, name='index'),
    path('create_user/', views.create_user_view, name='create_user'),
    path('<int:User_id>/posts/', views.user_post_view, name='view_user_posts'),
    path('<int:User_id>/page/', views.get_user_page, name='get_user_page'),
    path('<int:User_id>/posts/<int:post_id>/comments', views.get_post_comments, name='get_post_comments'),
    path('user_login/', views.login_view, name='user_login'),
    path('register/', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('user_home_page', views.user_home_page_view, name='user_home_page'),
    path('display_token', views.display_token, name='display_token'),
    path('generate_token', views.generate_token, name='generate_token'),
    path('<int:User_id>/followers/',
         views.follow_list,
         name='view_followers_REST'),
    path('<int:User_id>/following/',
         views.following_list,
         name='view_following_GET'),
    path('<int:User_id>/view-followers/',
         views.view_followers,
         name='view_followers'),
    path('<int:User_id>/get-followers/<int:Foreign_id>/',
         views.get_follow,
         name='get_followers'),
     path('<int:User_id>/followers/<int:Foreign_id>/',
         views.follow_crud,
         name='crud_followers'),
    path('requests/send-request/<int:User_id>/',
         views.send_friend_request,
         name='send_friend_request'),
    path('requests/accept-request/<int:User_id>/',
         views.accept_friend_request,
         name='accept_request'),
    path("requests/deny-request/<int:User_id>/",
         views.reject_friend_request,
         name='reject_request'),
    path("requests/view-request/<int:User_id>/",
         views.view_friend_requests,
         name='view_requests'),
    path("requests/request-page/",
         views.send_request_page,
         name='request_page'),
    path("api/", views.apiOverview, name='api_overview'),
    #path("api/Users/", views.UserList, name='api_user'),
    path('edit_user_profile',
         views.edit_user_profile_view,
         name='edit_user_profile'),
     path('external-users/', views.view_t15_users, name='external_users'),
     path('external-users/t-03/users/', views.view_t3_users, name='t03_users'),
     path('external-users/t-03/posts/', views.view_t3_posts, name='t03_posts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)