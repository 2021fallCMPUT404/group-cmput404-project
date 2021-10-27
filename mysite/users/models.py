from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.http import HttpResponse
import uuid
from django import forms
from django.forms.widgets import Textarea
import datetime


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return 'images/users/user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.


#TODO: MERGE USER_PROFILE INTO USER
class User(AbstractUser):
    pass


class Create_user(forms.Form):
    username = forms.CharField(initial='')
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


class User_Profile(models.Model):
    type = "author"
    #id = uuid.uuid4()
    host = None
    displayName = models.CharField(max_length=60)
    profileImage = models.ImageField(upload_to=user_directory_path)
    github = models.URLField(
        unique=True,
        default="https://github.com/2021fallCMPUT404/group-cmput404-project")
    #followers = models.ManyToManyField("self", blank=True, related_name='followers')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=256, unique=False)

class Inbox(models.Model):
    type = 'inbox'
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class UserFollows(models.Model):
    actor_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    object_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

class FriendRequest(models.Model):
    '''
    def __init__(self, actor: User, object: User):
        self.type = "Follow"
        self.actor = actor
        self.object = object
        self.summary = "{} wants to follow {}"

    def accept_request(self):
        actor_profile = User_Profile.get(self.actor.pk)
        object_profile = User_Profile.get(self.object.pk)
        actor_profile.Followers.add(self.object)
        object_profile.FOllowers.add(self.actor)

        return
    
    def reject_request():
        return None
    '''
    type = "Follow"
    actor = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name="actor", default='')
    object = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name="object", default='')

    def summary(self):
        return '{} wants to follow {}'.format(self.actor.displayName, self.object.displayName)