from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from . import views
from django.http import HttpResponse, Http404
from django.template import loader
from django.utils import timezone
from .models import Post, Comment, Like
from .forms import ShareForm,CommentForm
from .models import Post
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from users.models import User_Profile
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .forms import addPostForm
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
# Create your views here.


def post(request, Post_id):
    post = get_object_or_404(Post, pk=Post_id)
    share_form = ShareForm()
    
    return render(request, 'posts/post.html', {'post':post})
    #output = "Post text is: {}, Post date is: {}, Post id is: {}, Post author is: {}".format(post.text, post.pub_date,post.id, post.author)
    #return HttpResponse(output)


def placeholder(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    template = loader.get_template('posts/placeholder.html')
    current_user=User.objects.get(id=request.user.id)
    authorized_posts=[]
    print(current_user)
    for p in latest_post_list:
        if   p.privacy==0:          #PUBLIC POST
            authorized_posts.append(p)
        elif p.privacy==1:          #PRIVATE POST
            if p.author==current_user:
                authorized_posts.append(p)

    #NEED FRIEND POST

    
    #output = '\n'.join([q.text for q in latest_post_list])
    #print(latest_post_list)
    
    context = {
        'latest_post_list': authorized_posts
    }
    
    return HttpResponse(template.render(context, request))


def delete_post(request, Post_id):
    post = Post.objects.get(pk=Post_id)
    print(request.user)
    if request.user == post.author:
        Post.objects.get(pk=Post_id).delete()
    return redirect('post')

#@csrf_exempt
def select_github_activity(request):
    #In this view, the webpage will allow user to observer all the recent activity on user profile.
    #The user will be allowed to select one activity and add it inot stream.
    the_user_profile = User_Profile.objects.get(user=request.user)
    github_username = the_user_profile.github
    
    #print(request.GET)
    if request.method == 'POST':
        user_profile = User_Profile.objects.get(user=request.user)
        
        github_data = request.POST['select_event']
        print(github_data)
        data_list = github_data.split(' ')
        event_type = data_list[0]
        
        content = ' '.join([data for data in data_list[1:]])
        github_activity_post = Post(title = event_type, text = content, author = request.user)
        github_activity_post.save()
        return render(request, 'users/user_home_page.html')
    else:        
        return render(request, 'posts/display_github_activities.html', context={'insert_github_username':github_username})


        



class addPost(CreateView):
    model = Post
    template_name  = 'posts/addPost.html'
    fields = '__all__'


class addComment(CreateView):
    model = Comment
    form_class=CommentForm
    template_name = 'posts/addComment.html'
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id=self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('post')


        
    
    
    
class updatePost(UpdateView):
    model = Post
    template_name  = 'posts/editPost.html'
    fields = ['title','text', 'image']



class deletePost(DeleteView):
    model = Post
    template_name = 'posts/deletePost.html'
    success_url = reverse_lazy('post')

class SharedPostView(UpdateView):
    model = Post
    template_name  = 'posts/sharePost.html'
    fields = ['shared_on','shared_user']