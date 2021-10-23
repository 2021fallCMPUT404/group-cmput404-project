from django.db import models
from users.models import User
import uuid

# Create your models here.

class Post(models.Model):
    type = 'post'
    id = uuid.uuid4()
    text = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    visibility =None



class Comment(models.Model):     
	post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
	username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
	comment = models.CharField(max_length=200)
	comment_date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
	user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

class Share(models.Model):
        user = models.ForeignKey(User, related_name='shares', on_delete=models.CASCADE)
        post = models.ForeignKey(Post, related_name='shares', on_delete=models.CASCADE)
        
