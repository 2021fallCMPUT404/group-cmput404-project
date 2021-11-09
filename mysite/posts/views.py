from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, AnonymousUser
from . import views
from django.urls.base import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from .models import Post, Comment, Like, Share
from .forms import ShareForm,CommentForm
from .models import Post
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

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




class addPost(CreateView):
    model = Post
    template_name = 'posts/addPost.html'
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
    template_name = 'posts/editPost.html'
    fields = ['text', 'image']


class deletePost(DeleteView):
    model = Post
    template_name = 'posts/deletePost.html'
    success_url = reverse_lazy('post')

class SharedPostView(View):
    def get(self, request, pk):
        post_object = get_object_or_404(Post, pk=pk)
        current_user = request.user
        if current_user == AnonymousUser:
            return HttpResponseRedirect(reverse('post_placeholder', args=(str(current_user), post_object.ID)))


        sharedPost = Post.objects.create(
            text=post_object.text,
            #images=post_object.images,
            pub_date=post_object.pub_date,
            author=post_object.author,
            shared_user=current_user,
            original_post=post_object
            ).save()
        return HttpResponseRedirect(reverse('index'))
