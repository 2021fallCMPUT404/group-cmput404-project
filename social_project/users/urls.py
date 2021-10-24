from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users_test', views.index, name='index'),
    #path('create_user_form/', views.create_user_form, name='create_user_form')
]
