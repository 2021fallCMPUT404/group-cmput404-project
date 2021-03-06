"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls import include, url
from users import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('post/', include('posts.urls')),
    path('author/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('users', include('users.urls')),
    url(r'^users_test$', views.index, name='index'),

    #path('', views.index, name='user_home_page'),
    path('users', include('users.urls')),
    path('login', include('users.urls')),
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('service/author/<int:author_id>/posts/<int:post_id>/comments/', views.post_comments_api.as_view(), name='comment_api'),
    path('authors/', views.UserList, name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
