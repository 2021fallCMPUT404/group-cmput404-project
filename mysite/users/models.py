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

def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class User(AbstractUser):
	pass

class displayName(models.Model):
    displayName = models.CharField(max_length = 32, unique = True)

    def __str__(self):
        return self.displayName

class MyUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # other fields

    def __str__(self):
	    return self.id

class User_Profile(models.Model):
    type = "author"

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')
    host = None
    displayName = models.CharField(max_length=60, blank=True)
    profileImage = models.ImageField(
        upload_to='profile_picture',
        blank=True,
        default='profile_picture/default_picture.png')
    github = models.URLField(
        blank=True,
        default="https://github.com/2021fallCMPUT404/group-cmput404-project")

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=256, unique=False)
    user_posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)


class Inbox(models.Model):
    type = 'inbox'
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class UserFollows(models.Model):
    actor = models.ForeignKey(User_Profile, related_name="following", on_delete=models.CASCADE, default='')
    object = models.ForeignKey(User_Profile, related_name="followers", on_delete=models.CASCADE, default='')

class FriendRequest(models.Model):
    type = "Follow"
    actor = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name="actor", default='')
    object = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name="object", default='')

    def summary(self):
        return '{} wants to follow {}'.format(self.actor.displayName, self.object.displayName)

	type = "author"
	host = None
	displayName = models.ForeignKey(displayName, primary_key=True, on_delete=models.CASCADE, related_name = "username")
	id = models.ForeignKey(MyUUIDModel, on_delete=models.CASCADE)
	profileImage = None
	github = None
	bio = models.CharField(max_length = 256, unique = False, default="egg dog")
	url = models.URLField(unique = True, default = "https://github.com/2021fallCMPUT404/group-cmput404-project")
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(upload_to = user_directory_path, default = "image/users/egg_dog.jpeg")
	def __str__(self):
		return self.bio

class Inbox(models.Model):
	type = 'inbox'
	author = models.ForeignKey(User, on_delete=models.CASCADE)


class edit_history(models.Model):
    name = models.ForeignKey(User_Profile, on_delete=models.DO_NOTHING)
    edit_date = models.DateField()

    def __str__(self):
        return self.edit_date
