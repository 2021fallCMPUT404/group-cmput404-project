from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<int:User_id>/', views.placeholder, name='placeholder'),
    path('users_test', views.index, name='index'),
    path('create_user/', views.create_user_view, name='create_user'),
    path('<int:User_id>/posts/', views.user_post_view, name='view_user_posts'),
    path('requests/send-request/<int:User_id>/', views.send_friend_request, name='send_friend_request'),
    path('requests/accept-request/<int:User_id>/', views.accept_friend_request, name='accept_request'),
    path("requests/deny-request/<int:User_id>/", views.views.reject_friend_request, name='reject_request'),
    path("requests/view-request/<int:User_id>/", views.views.view_friend_requests, name='view_requests'),

    path('user_login/', views.login_view, name='user_login')
]