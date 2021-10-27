from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
import uuid
from django import forms
from django.forms.widgets import Textarea
import datetime
from posts.models import Post
'''
#TODO: MERGE USER_PROFILE INTO USER
class User(AbstractUser):
    pass
'''
def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return 'images/users/user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.



class Create_user(forms.Form):
    username = forms.CharField(initial='')
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


class User_Profile(models.Model):
    type = "author"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    host = None
    displayName = models.CharField(max_length=60, blank = True)
    profileImage = models.ImageField(upload_to='profile_picture', blank = True)
    github = models.URLField(
        unique=True,
        blank = True,
        default="https://github.com/2021fallCMPUT404/group-cmput404-project")

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=256, unique=False)
    user_posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

class Inbox(models.Model):
    type = 'inbox'
    author = models.ForeignKey(User, on_delete=models.CASCADE)

