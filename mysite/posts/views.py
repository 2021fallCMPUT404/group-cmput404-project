from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from . import views
from django.http import HttpResponse, Http404
from django.template import loader
from django.utils import timezone
from .models import Post, Comment, Like
from .forms import ShareForm, CommentForm
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from users.models import User_Profile
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .forms import addPostForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import CommentSerializer, LikeSerializer, PostSerializer
import json
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
# Create your views here.


def post(request, Post_id):
    post = get_object_or_404(Post, pk=Post_id)
    share_form = ShareForm()

    return render(request, 'posts/post.html', {'post': post})
    #output = "Post text is: {}, Post date is: {}, Post id is: {}, Post author is: {}".format(post.text, post.pub_date,post.id, post.author)
    #return HttpResponse(output)


def placeholder(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    template = loader.get_template('posts/placeholder.html')
    current_user = User.objects.get(id=request.user.id)
    authorized_posts = []
    print(current_user)
    for p in latest_post_list:
        if p.privacy == 0:  #PUBLIC POST
            authorized_posts.append(p)
        elif p.privacy == 1:  #PRIVATE POST
            if p.author == current_user:
                authorized_posts.append(p)

    #NEED FRIEND POST

    #output = '\n'.join([q.text for q in latest_post_list])
    #print(latest_post_list)

    context = {'latest_post_list': authorized_posts}

    return HttpResponse(template.render(context, request))


@api_view(['GET'])
def request_post_list(request):
    posts = Post.objects.all()
    posts_serializer = PostSerializer(posts, many=True)
    return Response(posts_serializer.data)


@api_view(['GET'])
def request_post(request, id):
    post = Post.objects.get(id=id)
    post_serializer = PostSerializer(post)
    return Response(post_serializer.data)


@api_view(['POST'])
def create_new_post(request):
    if request.method == 'POST':
        try:

            data = JSONParser().parse(request)
            post_serializer = PostSerializer(data=data)
            if post_serializer.is_valid():
                post_serializer.save()
                return JsonResponse(post_serializer.data,
                                    status=status.HTTP_201_CREATED)
            return JsonResponse(post_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE'])
def manage_user_post(request, user_id):
    if request.method == 'GET':
        try:
            related_user = User.objects.get(id=user_id)
            posts = Post.objects.filter(author=related_user)
            posts_serializer = PostSerializer(posts, many=True)
            return JsonResponse(posts_serializer.data, safe=False)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        try:
            related_user = User.objects.get(id=user_id)
            data = JSONParser().parse(request)
            post_serializer = PostSerializer(data=data)
            if post_serializer.is_valid():
                post_serializer.save()
                return JsonResponse(post_serializer.data,
                                    status=status.HTTP_201_CREATED)
            return JsonResponse(post_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            related_user = User.objects.get(id=user_id)
            posts = Post.objects.filter(author=related_user)
            for post in posts:
                post.delete()
            return JsonResponse({'message': 'Posts were deleted'},
                                status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def crud_post(request, id):

    #post_serializer = PostSerializer(data = request.data)
    if request.method == 'GET':
        try:
            post = Post.objects.get(id=id)
            post_serializer = PostSerializer(post)
            return JsonResponse(post_serializer.data)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            related_post = Post.objects.get(id=id)
            data = JSONParser().parse(request)
            post_serializer = PostSerializer(related_post, data=data)
            if post_serializer.is_valid():
                post_serializer.save()
                return JsonResponse(post_serializer.data)
            return JsonResponse(post_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            post = Post.objects.get(id=id)
            post.delete()
            return JsonResponse({'message': 'Post was deleted'},
                                status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE'])
def manage_post_comment(request, post_id):
    if request.method == 'GET':
        try:
            related_post = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post=related_post)
            comments_serializer = CommentSerializer(comments, many=True)
            return JsonResponse(comments_serializer.data, safe=False)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        try:
            related_post = Post.objects.get(id=post_id)
            data = JSONParser().parse(request)
            comment_serializer = CommentSerializer(data=data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                return JsonResponse(comment_serializer.data,
                                    status=status.HTTP_201_CREATED)
            return JsonResponse(comment_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            related_post = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post=related_post)
            for comment in comments:
                comment.delete()
            return JsonResponse({'message': 'Comments were deleted'},
                                status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def crud_comment(request, comment_id):
    if request.method == 'GET':
        try:
            related_comment = Comment.objects.get(id=comment_id)
            comment_serializer = CommentSerializer(related_comment)
            return JsonResponse(comment_serializer.data)
        except Comment.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested comment does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:
            related_comment = Comment.objects.get(id=comment_id)
            comment_data = JSONParser().parse(request)
            comment_serializer = CommentSerializer(related_comment,
                                                   data=comment_data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                return JsonResponse(comment_serializer.data)
            return JsonResponse(comment_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested comment does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        try:
            related_comment = Comment.objects.get(id=comment_id)
            related_comment.delete()
        except Comment.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested comment does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE'])
def manage_post_like(request, post_id):
    if request.method == 'GET':
        try:
            related_post = Post.objects.get(id=post_id)
            likes = Like.objects.filter(post=related_post)
            likes_serializer = LikeSerializer(likes, many=True)
            return JsonResponse(likes_serializer.data, safe=False)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:
            related_post = Post.objects.get(id=post_id)
            data = JSONParser().parse(request)
            like_serializer = LikeSerializer(data=data)
            if like_serializer.is_valid():
                like_serializer.save()
                return JsonResponse(like_serializer.data,
                                    status=status.HTTP_201_CREATED)
            return JsonResponse(like_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            related_post = Post.objects.get(id=post_id)
            likes = Comment.objects.filter(post=related_post)
            for like in likes:
                like.delete()
            return JsonResponse({'message': 'Likes were deleted'},
                                status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def crud_like(request, like_id):
    if request.method == 'GET':
        try:
            related_like = Like.objects.get(id=like_id)
            like_serializer = LikeSerializer(related_like)
            return JsonResponse(like_serializer.data)
        except Like.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested like does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:
            related_like = Like.objects.get(id=like_id)
            like_data = JSONParser().parse(request)
            like_serializer = LikeSerializer(related_like, data=like_data)
            if like_serializer.is_valid():
                like_serializer.save()
                return JsonResponse(like_serializer.data)
            return JsonResponse(like_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Like.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested like does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        try:
            related_like = Like.objects.get(id=like_id)
            related_like.delete()
        except Like.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested like does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def select_github_activity(request):
    #In this view, the webpage will allow user to observer all the recent activity on user profile.
    #The user will be allowed to select one activity and add it inot stream.
    the_user_profile = User_Profile.objects.get(user=request.user)
    github_username = the_user_profile.github

    #print(request.GET)
    if request.method == 'POST':
        user_profile = User_Profile.objects.get(user=request.user)
        github_data = json.loads(request.POST['select_event'])
        print(github_data)
        github_activity_post = Post(
            title=github_data['type'],
            text=' '.join([value for value in github_data.values()]),
            author=request.user)
        github_activity_post.save()
        return render(request, 'users/user_home_page.html')
    else:
        return render(request,
                      'posts/display_github_activities.html',
                      context={'insert_github_username': github_username})


class addPost(CreateView):
    model = Post
    template_name = 'posts/addPost.html'
    fields = '__all__'


class addComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/addComment.html'

    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('post')


class updatePost(UpdateView):
    model = Post
    template_name = 'posts/editPost.html'
    fields = ['title', 'text', 'image']


class deletePost(DeleteView):
    model = Post
    template_name = 'posts/deletePost.html'
    success_url = reverse_lazy('post')


class SharedPostView(UpdateView):
    model = Post
    template_name = 'posts/sharePost.html'
    fields = ['shared_on', 'shared_user']
