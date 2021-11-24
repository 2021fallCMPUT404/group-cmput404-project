from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django import template
import traceback
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, AnonymousUser
from . import views
from django.urls.base import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from .models import Post, Comment, Like, Share
from .forms import ShareForm, CommentForm, addPostForm
from .models import Post
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, View, ListView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from .forms import addPostForm
from django.shortcuts import render
from users.models import User_Profile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
import ast
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .authentication import UsernamePasswordAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
# Create your views here.
def handle_not_found(request, exception):
    return render(request, 'not_found.html')


def post(request, Post_id):

    current_user = User.objects.get(id=request.user.id)
    print(current_user)
    post = get_object_or_404(Post, pk=Post_id)

    share_form = ShareForm()
    user = request.user
    username = user.username

    if post.privacy == 0:
        print("Public")
        return render(request, 'posts/post.html', {
            'post': post,
            'user_name': username
        })

    elif post.privacy == 1:
        if post.author == current_user:
            print("private ")
            return render(request, 'posts/post.html', {
                'post': post,
                'user_name': username
            })

    return render(request, 'not_found.html')

    #output = "Post text is: {}, Post date is: {}, Post id is: {}, Post author is: {}".format(post.text, post.pub_date,post.id, post.author)
    #return HttpResponse(output)


def placeholder(request):
    latest_post_list = Post.objects.order_by('-pub_date')[:5]
    template = loader.get_template('posts/placeholder.html')
    current_user = User.objects.get(id=request.user.id)
    authorized_posts = []
    print(current_user)
    for p in latest_post_list:
        if p.unlisted:  #unlisted posts: always visible to creator
            if p.author == current_user:
                authorized_posts.append(p)
        else:  #listed posts
            if p.privacy == 0:  #public: visible to all
                authorized_posts.append(p)

            elif p.privacy == 1:  #private: visible to creator
                if p.author == current_user:
                    authorized_posts.append(p)

    #NEED FRIEND POST

    #output = '\n'.join([q.text for q in latest_post_list])
    #print(latest_post_list)

    context = {
        'latest_post_list': authorized_posts,
        'current_user': current_user
    }

    return HttpResponse(template.render(context, request))


def delete_post(request, Post_id):
    post = Post.objects.get(pk=Post_id)
    print(request.user)
    if request.user == post.author:
        Post.objects.get(pk=Post_id).delete()
    return redirect('post')


def likePost(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.like.add(request.user)
    return HttpResponseRedirect(reverse('post_placeholder', args=[str(pk)]))


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def request_post_list(request):
    posts = Post.objects.all()
    posts_serializer = PostSerializer(posts, many=True)
    return Response(posts_serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def request_post(request, id):
    post = Post.objects.get(id=id)
    post_serializer = PostSerializer(post)
    return Response(post_serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

        ast.literal_eval(request.POST['select_event'])

        github_data = json.loads(request.POST['select_event'])
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


def likeComment(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.like.add(request.user)
    return HttpResponseRedirect(reverse('post_placeholder', args=[str(pk)]))


class addPost(CreateView):
    model = Post
    form_class = addPostForm
    template_name = 'posts/addPost.html'
    success_url = reverse_lazy('feed')


class addComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/addComment.html'
    success_url = reverse_lazy('post_placeholder')

    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class updatePost(UpdateView):
    model = Post
    template_name = 'posts/editPost.html'
    fields = ['title', 'text', 'image']
    success_url = reverse_lazy('feed')


class deletePost(DeleteView):
    model = Post
    template_name = 'posts/deletePost.html'
    success_url = reverse_lazy('feed')


class SharedPostView(View):

    model = Post
    template_name = 'posts/sharePost.html'
    fields = ['shared_on', 'shared_user']

    def get(self, request, pk):
        post_object = get_object_or_404(Post, pk=pk)
        current_user = request.user
        if current_user == AnonymousUser:
            return HttpResponseRedirect(
                reverse('post_placeholder',
                        args=(str(current_user), post_object.ID)))

        sharedPost = Post.objects.create(
            title=post_object.title,
            text=post_object.text,
            image=post_object.image,
            pub_date=post_object.pub_date,
            author=post_object.author,
            shared_user=current_user,
            contentType=post_object.contentType).save()

def send_token(request, username, password):
    '''
    new_token = Token.objects.get(user=request.user).key
    token_data = {'token': new_token}
    json_data = json.dumps(token_data)
    response = requests.post('http://127.0.0.1:8000/', json = token_data)
    print(response)
    return HttpResponseRedirect('user_home_page')
    '''
    
    user = User.objects.get(username=username)
    token = Token.objects.get(user=user)
    user_password = user.password
    if user_password == password:
        #return Response(token.key, safe=False)
    
    
        print(token)
    return {'message': 'The user or password does not exist'}
