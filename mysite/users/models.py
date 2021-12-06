from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
import uuid
from django import forms
from django.forms.widgets import Textarea
import datetime
from posts.models import Post, Like, CommentLike#, InboxLike
from django.urls import reverse
import json


SITE_URL = "https://cmput404-socialdist-project.herokuapp.com"

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

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_profile')
    host = SITE_URL + '/'
    url = SITE_URL
    displayName = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=60, blank=True)
    first_name = models.CharField(max_length=69, blank=True)
    last_name = models.CharField(max_length=69, blank=True)
    profileImage = models.ImageField(
        upload_to='profile_picture',
        blank=True,
        default='profile_picture/default_picture.png')
    github = models.CharField(blank=True, default="", max_length=100)

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=256, unique=False)

    #user_posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return ', '.join((self.displayName, str(self.id), str(self.user.id)))

    def get_absolute_url(self):
        return SITE_URL + reverse('users:user_crud', args=[str(self.user.id)])


class Inbox(models.Model):
    type = 'inbox'
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ManyToManyField(Post, null=True, blank=True)
    follow = models.ManyToManyField("users.FriendRequest", null=True, blank=True)
    like = models.ManyToManyField(Like, null=True, blank=True)
    #comment_like = models.ManyToManyField(CommentLike, null=True, blank=True, on_delete=models.CASCADE)
    #inbox_like = models.ManyToManyField(InboxLike, null=True, blank=True, on_delete=models.CASCADE)


class UserFollows(models.Model):
    #followin
    '''
    actor = models.ForeignKey(User_Profile,
                              related_name="following",
                              on_delete=models.CASCADE,
                              default='')
    #Got followed
    object = models.ForeignKey(User_Profile,
                               related_name="followers",
                               on_delete=models.CASCADE,
                               default='')
    '''

    actor = models.JSONField(null=True, blank=True)
    object = models.JSONField(null=True, blank=True)

    #Creates new instance of Userfollow with the actor following the object
    #Parameters are User_Profile objects
    def create_user_follow(actor, object):
        UserFollows.objects.get_or_create(actor=actor, object=object)

    #The actor will stop following the object
    def delete_user_follow(actor, object):
        instance = UserFollows.objects.filter(actor=actor, object=object)
        if instance.exists():
            instance.delete()
        return None


class FriendRequest(models.Model):
    type = "Follow"
    '''
    actor = models.ForeignKey(User_Profile,
                              on_delete=models.CASCADE,
                              related_name="actor",
                              default='')
    object = models.ForeignKey(User_Profile,
                               on_delete=models.CASCADE,
                               related_name="object",
                               default='')
    '''

    actor = models.JSONField(null=True, blank=True)
    object = models.JSONField(null=True, blank=True)

    def create_friend_request(actor, object):
        '''Creates a friend request instance with the actor being the person who follows
        and the object is the person whom is being followed. The actor and object paramaters
        are user_profile objects.'''
        actor_json = serializers.serialize('json', [actor]).replace("[","").replace("]","")
        object_json = serializers.serialize('json', [object]).replace("[","").replace("]","")
        print(actor, object)
        print(actor_json, object_json)
        print(type(actor_json))
        if UserFollows.objects.filter(actor=object, object=actor).exists(
        ):  #Checks if the object is already following the actor
            # Returns so it doesn't create constant friend requests
            print("{} is already following {}".format(object.displayName,
                                                      actor.displayName))
            return
        f_request, created = FriendRequest.objects.get_or_create(actor=actor_json,
                                                                 object=object_json)
        print("Friend request created")
        print(f_request.summary())

        return f_request

    def summary(self):
        actor_json = json.loads(self.actor)['fields']
        object_json = json.loads(self.object)['fields']
        print("In summary: ", actor_json, object_json)
        return '{} wants to follow {}'.format(actor_json['displayName'],
                                              object_json['displayName'])
