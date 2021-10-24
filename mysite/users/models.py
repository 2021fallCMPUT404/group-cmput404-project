from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
import uuid
from django import forms	
from django.forms.widgets import Textarea
# Create your models here.

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
	profileImage = None
	github = None
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Inbox(models.Model):
	type = 'inbox'
	author = models.ForeignKey(User, on_delete=models.CASCADE)