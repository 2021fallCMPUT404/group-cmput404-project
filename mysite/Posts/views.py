from django.shortcuts import get_object_or_404, render, redirect
from . import views
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Post, Comment, Like
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

def create_post(request):
	user = request.user
	if request.method == "POST":
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			data.user_name = user
			data.save()
			messages.success(request, f'Posted Successfully')
			return redirect('home')
	else:
		form = NewPostForm()
	return render(request, 'Posts/Make_Posts/make_post.html', {'form':form})

def delete_post(request,pid):
    post = Post.objects.get(Post_id=pid)
    if request.user== post.user_name:
        Post.objects.get(Post_id=pid).delete()
    return redirect('home')
