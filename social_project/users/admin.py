from django.contrib import admin
from users.models import username, user_profile, edit_history
# Register your models here.

admin.site.register(username)
admin.site.register(user_profile)
admin.site.register(edit_history)