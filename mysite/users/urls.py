from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static

app_name = 'users'

urlpatterns = [
    path('', views.UserList, name='homepage'),
    path('<int:User_id>/', views.userGet, name='placeholder'),
    path('users_test', views.index, name='index'),
    path('create_user/', views.create_user_view, name='create_user'),
    path('<int:User_id>/posts/', views.user_post_view, name='view_user_posts'),
    path('user_login/', views.login_view, name='user_login'),
    path('register/', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('user_home_page', views.user_home_page_view, name='user_home_page'),
    path('<int:User_id>/followers/', views.follow_list, name='view_followers'),
    path('<int:User_id>/followers/<int:Foreign_id>/', views.follow_crud, name='crud_followers'),
    path('requests/send-request/<int:User_id>/', views.send_friend_request, name='send_friend_request'),
    path('requests/accept-request/<int:User_id>/', views.accept_friend_request, name='accept_request'),
    path("requests/deny-request/<int:User_id>/", views.reject_friend_request, name='reject_request'),
    path("requests/view-request/<int:User_id>/", views.view_friend_requests, name='view_requests'),
    path("requests/request-page/", views.send_request_page, name='request_page'),
    path("api/", views.apiOverview, name='api_overview'),
    #path("api/Users/", views.UserList, name='api_user'),
    path('edit_user_profile',
         views.edit_user_profile_view,
         name='edit_user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)