from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
import uuid
import datetime

# Create your models here.
'''
class User(AbstractUser):
    pass
'''


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return 'images/users/user_{0}/{1}'.format(instance.user.id, filename)


'''
class displayName(models.Model):
    displayName = models.CharField(max_length=64,
                                   primary_key=True,
                                   unique=True)

    def __str__(self):
        return self.displayName
'''


class MyUUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # other fields

    def __str__(self):
        return self.id


class User_Profile(models.Model):
    type = "author"
    #displayName = models.ForeignKey('displayName',blank=True, null=True,on_delete=models.CASCADE)
    #id = models.ForeignKey('MyUUIDModel', on_delete=models.CASCADE)
    displayName = models.CharField(max_length=64,
                                   primary_key=True,
                                   unique=True,
                                   default=uuid.uuid4)
    bio = models.CharField(max_length=256, unique=False)
    url = models.URLField(
        unique=True,
        default="https://github.com/2021fallCMPUT404/group-cmput404-project")
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    '''
    profile_picture = models.ImageField(upload_to=user_directory_path)
    created_date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.displayName, self.bio, self.url, self.profile_picture, self.create_date


'''
class Inbox(models.Model):
    type = 'inbox'
    author = models.ForeignKey(User, on_delete=models.CASCADE)
'''
'''
class edit_history(models.Model):
    name = models.ForeignKey(User_Profile, on_delete=models.DO_NOTHING)
    edit_date = models.DateField()

    def __str__(self):
        return self.edit_date
'''