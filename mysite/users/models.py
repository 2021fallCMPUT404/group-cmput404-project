from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
import uuid
# Create your models here.

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
	host = None
	displayName = models.ForeignKey(displayName, on_delete=models.CASCADE, related_name = "username")
	id = models.ForeignKey(MyUUIDModel, primary_key=True, on_delete=models.CASCADE)
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