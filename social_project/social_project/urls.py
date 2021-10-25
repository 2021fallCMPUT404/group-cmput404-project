from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('users', include('users.urls')),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('create_user_profile',
         views.create_user_profile,
         name='create_user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
