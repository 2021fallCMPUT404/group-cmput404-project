from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Post



class PostView(View):
    def get_posts(self,request, post_id,*args, **kwargs):
            posts = Post.objects.all().order_by('-pub_date')
            
            context = {
                'postList':posts,
            }
            return render(request,'posts/index.html', context)

