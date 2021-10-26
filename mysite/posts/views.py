from django.shortcuts import get_object_or_404, render, redirect
from . import views
from django.http import HttpResponse, Http404
from django.template import loader
from django.utils import timezone
from .models import Post, Comment, Like
from .forms import ShareForm
from .models import Post
from django.views.generic import CreateView
# Create your views here.


def post(request, Post_id):
    post = get_object_or_404(Post, Post_id=Post_id)
    share_form = ShareForm()
    return render(request, 'Posts/post.html', {'post':post})
    #output = "Post text is: {}, Post date is: {}, Post id is: {}, Post author is: {}".format(post.text, post.pub_date,post.id, post.author)
    #return HttpResponse(output)

def placeholder(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    template = loader.get_template('posts/placeholder.html')
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
	return render(request, 'templates/Make_Posts/make_post.html', {'form':form})

def delete_post(request,pid):
    post = Post.objects.get(Post_id=pid)
    if request.user== post.user_name:
        Post.objects.get(Post_id=pid).delete()
    return redirect('home')

class SharedPostView(View):
  def post(self, request, pid, *args, **kwargs):
    original_post = Post.objects.get(Post_id=pid)
    form = ShareForm(request.POST)
    if form.is_valid():
    new_post = Post(
      shared_body = self.request.POST.get('body'),
      body = original_post.body,
      author = original_post.author,
      created_on = original_post.created_on,
      shared_on = timezone.now(),
      shared_user = request.user
    )
    new_post.save()
    '''
    for img in original_post.image.all():
      new_post.image.add(img),
    new_post.save()
    '''
    return redirect('home')

class addPost(CreateView):
    model = Post
    template_name = 'addPost.html'
    fields = '__all__'
    
