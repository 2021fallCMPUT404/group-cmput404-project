from django.shortcuts import render
from . import views
from django.http import HttpResponse
from .models import Post
# Create your views here.

def post(request, Post_id):
    post = Post.objects.get(pk=Post_id)
    output = "Post text is: {}, Post date is: {}, Post id is: {}, Post author is: {}".format(post.text, post.pub_date,post.id, post.author)
    return HttpResponse(output)

def placeholder(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    output = '\n'.join([q.text for q in latest_post_list])
    return HttpResponse(output)