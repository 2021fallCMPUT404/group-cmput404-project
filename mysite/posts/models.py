from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from users.models import User
import uuid
from django.urls import reverse



class Post(models.Model):

    PUBLIC=0
    PRIVATE=1
    # FREINDS=2    #Need friend system?

    Privacy=(
        (PUBLIC,"PUBLIC"),          
        (PRIVATE,"PRIVATE"),        #only shows to me
        #(FREINDS,"FRIENDS"),
        #(Unlisted,"Unlisted")
        
    )

    type = 'post'
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    shared_on = models.DateTimeField(blank=True, null=True)
    privacy=models.IntegerField(choices=Privacy,default=PUBLIC)
    visible=None



    def get_absolute_url(self):
        return reverse('post_placeholder', args=(str(self.id)))


class Comment(models.Model):
    #name of the user (primary key problem)
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True,related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    comment_body = models.TextField()
    comment_created= models.DateTimeField(auto_now_add=True)

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


