from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [path('', views.index, name='index')]
