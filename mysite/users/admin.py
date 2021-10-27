from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FriendRequest, User, UserFollows, User_Profile, Inbox
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(User_Profile)
admin.site.register(Inbox)
admin.site.register(FriendRequest)
admin.site.register(UserFollows)

