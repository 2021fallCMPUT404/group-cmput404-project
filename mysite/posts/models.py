from django.db import models
from django.contrib.auth.models import User
from users.models import User
import uuid
from django.urls import reverse


class Post(models.Model):
    type = 'post'

    text = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    visibility = None


def get_absolute_url(self):
    return reverse('post_placeholder', args=(str(self.id)))


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             related_name='details',
                             on_delete=models.CASCADE)
    username = models.ForeignKey(User,
                                 related_name='details',
                                 on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    comment_date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name='likes',
                             on_delete=models.CASCADE)