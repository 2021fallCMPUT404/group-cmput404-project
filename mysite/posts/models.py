from django.db import models
from django.conf import settings
from django.db.models.fields.json import JSONField
#from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from users.models import User
import uuid
from django.urls import reverse


class Post(models.Model):
    
    CONTENT = (
		('text/markdown', 'Markdown'),
		('text/plain','Plaintext'),
	)

    VISIBILITY = (
		('PUBLIC', 'Public'),
		('FRIENDS', 'Friends'),
		('PRIVATE', 'My Eyes Only')
    )

    type = 'post'
    title = models.TextField( max_length=100, blank=True )
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shared_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    related_name='+')

    published = models.DateTimeField(auto_now_add=True)
    unlisted = models.BooleanField(default=False)
    visibility=models.CharField(max_length=20, choices=VISIBILITY, default=VISIBILITY[0][0], null=False)
    visible=None
    description = models.CharField(max_length=500, null =True)
    contentType = models.CharField(max_length=20, choices=CONTENT, default=CONTENT[1][0],null=False)
    originalPost = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, editable =False)
    like = models.ManyToManyField(User, related_name='posts_likes')

    def get_absolute_url(self):
        return reverse('post_placeholder', args=[str(self.id)])

    def __str__(self):
        return self.title
    def is_shared_post(self):
        return self.shared_user != None


class Comment(models.Model):
    #name of the user (primary key problem)
    type = 'comment'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name="comments")
    #author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               #on_delete=models.CASCADE,
                               #blank=True,
                               #null=True)
    author = JSONField(null=True, blank=True)
    comment_body = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='comments_likes')
    class Meta:
        ordering = ['comment_created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment_body, self.author)


class Like(models.Model):

    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name='likes',
                             on_delete=models.CASCADE)


class Share(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True,related_name="shares")
    shared_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    shared_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['shared_on', 'shared_user']

    def __str__(self):
        return 'Shared by {}'.format(self.author)


class Node(models.Model):
    team_id = models.IntegerField(null=True) #Added in case we need to do specific parsing for a team
    users = models.URLField()
    posts = models.URLField()
    username = models.TextField()
    password = models.TextField()
