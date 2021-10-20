from django.shortcuts import get_object_or_404, render
from . import views
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Post
# Create your views here.


def post(request, Post_id):
    post = get_object_or_404(Post, pk=Post_id)
    return render(request, 'Posts/post.html', {'post':post})
    #output = "Post text is: {}, Post date is: {}, Post id is: {}, Post author is: {}".format(post.text, post.pub_date,post.id, post.author)
    #return HttpResponse(output)

def placeholder(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    template = loader.get_template('Posts/placeholder.html')
    #output = '\n'.join([q.text for q in latest_post_list])
    print(latest_post_list)
    context = {
        'latest_post_list': latest_post_list
    }
    return HttpResponse(template.render(context, request))