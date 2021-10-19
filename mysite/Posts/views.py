from django.shortcuts import render
from . import views
from django.http import HttpResponse
from .models import Post
# Create your views here.

def post(request):
    return HttpResponse("Placeholder post")

def placeholder(request, Post_id):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.text for q in latest_post_list])
    return HttpResponse(output)