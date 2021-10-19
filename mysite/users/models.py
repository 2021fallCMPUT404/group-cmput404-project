from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
import uuid
# Create your models here.

class User(AbstractUser):
	pass

class User_Profile(models.Model):
	type = "author"
	id = uuid.uuid4()
	host = None
	displayName = models.CharField(max_length=60)
	profileImage = None
	github = None
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Inbox(models.Model):
	type = 'inbox'
	author = models.ForeignKey(User, on_delete=models.CASCADE)