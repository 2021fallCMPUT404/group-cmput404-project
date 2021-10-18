from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('users', include('users.urls')),
    url(r'^$', views.index, name='index'),
    path('admin/', admin.site.urls),
]