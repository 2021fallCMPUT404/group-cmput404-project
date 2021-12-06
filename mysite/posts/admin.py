from django.contrib import admin

from .models import Post,Comment, Node

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Node)