from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django import template
from posts.connection import *
import traceback
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, AnonymousUser
from . import views
from django.urls.base import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.utils import timezone
from .models import Post, Comment, Like, Share, CommentLike, Node
from .forms import ShareForm, CommentForm, addPostForm
from .models import Post
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, View, ListView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from .forms import addPostForm
from django.shortcuts import render
from users.models import User_Profile, UserFollows, Inbox
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
import ast
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, LikeCommentSerializer
from .authentication import UsernamePasswordAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication, BaseAuthentication, SessionAuthentication, BasicAuthentication
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
import requests
import re
import datetime
from rest_framework import authentication, permissions
import base64
from rest_framework.views import APIView
from rest_framework.decorators import action
from users.serializers import User_Profile, userPSerializer, UserSerializer

class ExemptGetPermission(permissions.BasePermission):        

    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == 'GET':
            return True

        # Otherwise, only allow authenticated requests
        # Post Django 1.10, 'is_authenticated' is a read-only attribute
        return request.user and request.user.is_authenticated


class AccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_type, _, credentials = auth_header.partition(' ')

        expected = base64.b64encode(b'socialdistribution_t05:c404t05').decode()
        if token_type == 'Basic' and credentials == expected:
            return True

        else:
            return False


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token_type, _, credentials = auth_header.partition(' ')

        expected = base64.b64encode(b'socialcircleauth:cmput404').decode()
        if token_type == 'Basic' and credentials == expected:
            return (True, None)

        else:
            return None

    def authenticate_header(self, request):
        return '{"username" : <username>, "password" : <password>}'


# Create your views here.
def handle_not_found(request, exception):
    return render(request, 'not_found.html')


def post(request, Post_id):

    current_user = User.objects.get(id=request.user.id)
    print(current_user)
    post = get_object_or_404(Post, pk=Post_id)
    user_profile = get_object_or_404(User_Profile, user=current_user)
    followers = UserFollows.objects.filter(object=user_profile)

    share_form = ShareForm()
    user = request.user
    username = user.username

    if post.privacy == 0:
        print("Public")
        return render(request, 'posts/post.html', {
            'post': post,
            'user_name': username,
            'followers': followers
        })

    elif post.privacy == 1:
        if post.author == current_user:
            print("private ")
            return render(request, 'posts/post.html', {
                'post': post,
                'user_name': username,
                'followers': followers
            })

    elif post.privacy == 2:
        if post.author == current_user:
            print("friend ")
            return render(request, 'posts/post.html', {
                'post': post,
                'user_name': username,
                'followers': followers
            })
        else:
            for f in followers:
                if f.actor.displayName == post.author.user_profile.displayName:
                    print("friend ")
                    return render(request, 'posts/post.html', {
                        'post': post,
                        'user_name': username,
                        'followers': followers
                    })
                else:
                    if post.shared_user != None:
                        friend = User.objects.get(id=post.shared_user.id)
                        friends_profile = get_object_or_404(User_Profile,
                                                            user=friend)
                        if f.actor.displayName == friends_profile.displayName:
                            print("friend share")
                            return render(request, 'posts/post.html', {
                                'post': post,
                                'user_name': username,
                                'followers': followers
                            })

    return render(request, 'not_found.html')

    #output = "Post text is: {}, Post date is: {}, Post id is: {}, Post author is: {}".format(post.text, post.pub_date,post.id, post.author)
    #return HttpResponse(output)


class post_comments_api(APIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self, request, author_id, post_id, format=None):
        try:
            author = get_object_or_404(User, pk=author_id)
            related_post = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post=related_post)
            comments_serializer = CommentSerializer(comments, many=True)
            return Response(comments_serializer.data)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


    def post(self, request, author_id, post_id, format=None):
        try:
            test = json.loads(request.body)
            post = get_object_or_404(Post, pk=post_id)
            author = userPSerializer(data=test['author'])
            print(author.is_valid())
            if not author.is_valid():
                return HttpResponseBadRequest("Author object cannot be serialized.")
            new_comment = Comment(author=author.data, comment_body=test['comment'], post=post)
            new_comment.save()
            return HttpResponse(new_comment)
        except Exception as e:
            return JsonResponse({'message':'Error: {}'.format(e)})

def handle_not_found(request, exception):
    return render(request, 'not_found.html')


def placeholder(request):
    latest_post_list = Post.objects.order_by('-pub_date')
    backup_list = Post.objects.order_by('-pub_date')[5:]
    template = loader.get_template('posts/placeholder.html')
    current_user = User.objects.get(id=request.user.id)
    user_profile = get_object_or_404(User_Profile, user=current_user)
    followers = UserFollows.objects.filter(object=user_profile)
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

            elif p.privacy == 2:  #friend: visible to creator and friends only
                if p.author == current_user:
                    authorized_posts.append(p)
                else:
                    for f in followers:
                        if f.actor.displayName == p.author.user_profile.displayName:
                            authorized_posts.append(p)
                        else:
                            if p.shared_user != None:
                                friend = User.objects.get(id=p.shared_user.id)
                                friends_profile = get_object_or_404(
                                    User_Profile, user=friend)
                                if f.actor.displayName == friends_profile.displayName:
                                    authorized_posts.append(p)

    if len(authorized_posts) < 5:  #fill up the list if necessary
        if len(backup_list) > 0:
            for p in backup_list:
                if p.unlisted:  #unlisted posts: always visible to creator
                    if p.author == current_user:
                        authorized_posts.append(p)
                else:  #listed posts
                    if p.privacy == 0:  #public: visible to all
                        authorized_posts.append(p)

                    elif p.privacy == 1:  #private: visible to creator
                        if p.author == current_user:
                            authorized_posts.append(p)

                    elif p.privacy == 2:  #friend: visible to creator and friends only
                        if p.author == current_user:
                            authorized_posts.append(p)
                        else:
                            for f in followers:
                                if f.actor.displayName == p.author.user_profile.displayName:
                                    authorized_posts.append(p)
                                else:
                                    if p.shared_user != None:
                                        friend = User.objects.get(
                                            id=p.shared_user.id)
                                        friends_profile = get_object_or_404(
                                            User_Profile, user=friend)
                                        if f.actor.displayName == friends_profile.displayName:
                                            authorized_posts.append(p)

                if len(authorized_posts) == 5:
                    break

    #NEED FRIEND POST

    #output = '\n'.join([q.text for q in latest_post_list])
    #print(latest_post_list)

    context = {
        'latest_post_list': authorized_posts,
        'current_user': current_user,
        'followers': followers
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
    like = Like(user=request.user, object='https://cmput404-socialdist-project.herokuapp.com/author/{}/post/{}'.format(post.author.id, post.id))
    
    like.save()
    post.like.add(like)
    
    return HttpResponseRedirect(reverse('post_placeholder', args=[str(pk)]))


class HandleAuthorPost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ExemptGetPermission]
    
    def get(self, request, AUTHOR_ID, POST_ID, format=None):
        try:
            print(request.user)
            user = User.objects.get(id=AUTHOR_ID)
            post = Post.objects.get(id=POST_ID)
            user_profile = User_Profile.objects.get(user=user)
            comments = Comment.objects.filter(post = post)
            count = len(comments)
            if post.author.username != user.username:
                return JsonResponse(
                    {
                        'message':
                        'The post author id does not match the provided user id'
                    },
                    status=status.HTTP_403_FORBIDDEN)
            if post.privacy != 0:
                return JsonResponse({'message': 'This is not a public post.'},
                                    status=status.HTTP_403_FORBIDDEN)
            post_serializer = PostSerializer(post, many=False)
            post_serializer_data = post_serializer.data
            post_serializer_data['origin'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post.id))
            post_serializer_data['source'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post.id))
            post_serializer_data['description'] = "This post discusses stuff -- brief"
            post_serializer_data['categories'] = []
            post_serializer_data['count'] = count
            post_serializer_data['comments'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post.id))
            if post_serializer_data['contentType'] == 1:
                post_serializer_data['contentType'] = "text/markdown"
            else:
                post_serializer_data['contentType'] = "text/plain"
            return Response(post_serializer_data)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, AUTHOR_ID, POST_ID, format=None):
        try:
            if Post.objects.filter(id = POST_ID).exists():
                return JsonResponse(
                {'message': 'The requested post has already existed'},
                status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(id=AUTHOR_ID)
            request_user = request.user
            data = JSONParser().parse(request)
            
            if data['contentType'] == "text/markdown":
                data['contentType'] = 1
            else:
                data['contentType'] = 0

            created_post = Post( id = POST_ID, title=data['title'], text=data['text'], image=data['image'], author=user,
                    shared_user = data['shared_user'],shared_on = data['shared_on'],
                    privacy=data['privacy'], contentType=data['contentType'],)
            
            created_post.save()
            post_serializer = PostSerializer(created_post)
            
            return JsonResponse(post_serializer.data)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request, AUTHOR_ID, POST_ID, format=None):
        try:
            #This part of code will check if the token from request matches the token of author.
            user = User.objects.get(id=AUTHOR_ID)
            request_user = request.user
            print(request_user.id)
            
            if request_user.id != AUTHOR_ID:
                return JsonResponse(
                    {
                        'message':
                        'The authorized user id does not match the provided user id in url.'
                    },
                    status=status.HTTP_403_FORBIDDEN)
            
            post = Post.objects.get(id=POST_ID)
            if post.author.id != user.id:
                return JsonResponse(
                    {
                        'message':
                        'The provided author id does not match the provided user id in url.'
                    },
                    status=status.HTTP_403_FORBIDDEN)
            data = JSONParser().parse(request)
            if data['contentType'] == "text/markdown":
                data['contentType'] = 1
            else:
                data['contentType'] = 0
            post_serializer = PostSerializer(post, data=data)
            if post_serializer.is_valid():
                post_serializer.save()
                return JsonResponse(post_serializer.data)
            return JsonResponse(post_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, AUTHOR_ID, POST_ID, format=None):
        try:

            #This part of code will check if the token from request matches the token of author.
            user = User.objects.get(id=AUTHOR_ID)
            #End of this part of code

            post = Post.objects.get(id=POST_ID)
            if post.author.id != user.id:
                return JsonResponse(
                    {
                        'message':
                        'The post author id does not match the provided user id'
                    },
                    status=status.HTTP_403_FORBIDDEN)

            post.delete()
            return JsonResponse({'message': 'Post was deleted'},
                                status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)

class MangePostUnderUser(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ExemptGetPermission]
    def get(self, request, AUTHOR_ID, format=None):
        try:
            user = User.objects.get(id=AUTHOR_ID)
            posts = Post.objects.filter(author=user)
            user_profile = User_Profile.objects.get(user=user)
            post_serializer = PostSerializer(posts, many=True)
            for post_serializer_data in post_serializer.data:
                comments = Comment.objects.filter(post = post_serializer_data['id'])
                count = len(comments)
                post_serializer_data['origin'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post_serializer_data['id']))
                post_serializer_data['source'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post_serializer_data['id']))
                post_serializer_data['description'] = "This post discusses stuff -- brief"
                post_serializer_data['categories'] = []
                post_serializer_data['count'] = count
                post_serializer_data['comments'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post_serializer_data['id']))
                if post_serializer_data['contentType'] == 1:
                    post_serializer_data['contentType'] = "text/markdown"
                else:
                    post_serializer_data['contentType'] = "text/plain"
            return JsonResponse(post_serializer.data, safe=False)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request, AUTHOR_ID, format=None):

        try:
            user = User.objects.get(id=AUTHOR_ID)
            request_user = request.user
            data = JSONParser().parse(request)
            if data['contentType'] == "text/markdown":
                data['contentType'] = 1
            else:
                data['contentType'] = 0
            created_post = Post(title=data['title'], text=data['text'], image=data['image'], author=user,
                    shared_user = data['shared_user'],shared_on = data['shared_on'],
                    privacy=data['privacy'], contentType=data['contentType'],)
            
            created_post.save()
            post_serializer = PostSerializer(created_post)
            
            return JsonResponse(post_serializer.data)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)

class HandleAuthorPostComment(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ExemptGetPermission]

    def get(self, request, AUTHOR_ID, POST_ID, format=None):
        
        try:
            post = Post.objects.get(id=POST_ID)
            if AUTHOR_ID != post.author.id:
                return JsonResponse({
                    'message':
                    'The provided author in url does have the request post'
                })
            comments = Comment.objects.filter(post=post)
            
            comments_serializer = CommentSerializer(comments, many=True)
            return JsonResponse(comments_serializer.data, safe=False)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request, AUTHOR_ID, POST_ID, format=None):
        print("Is this running/")
        try:
            data = JSONParser().parse(request)
            user = User.objects.get(id=data['author']['id'])
            post = Post.objects.get(id=POST_ID)

            created_comment = Comment(post = post, author=user,
                    comment_body = data['comment_body'], comment_created = data['comment_created'])
            
            created_comment.save()

            

            comment_serializer = CommentSerializer(created_comment)

            
            return JsonResponse(comment_serializer.data,
                                status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)

class HandleInboxLike(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ExemptGetPermission]

    def post(self, request, AUTHOR_ID, format=None):
        try:
            inbox = Inbox.objects.get(author=AUTHOR_ID)
            data = JSONParser().parse(request)
            try:
                user = User.objects.get(id=data['user']['id'])
            except:
                user = User.objects.get(id=AUTHOR_ID)
            
            created_like = Like(user=user, object = data['object'])
            like_serializer = LikeSerializer(created_like)
            inbox.like.add(created_like.id)
            return JsonResponse(like_serializer.data,
                                status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        except Inbox.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested inbox does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class HandlePostLikeList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ExemptGetPermission]
    def get(self, request, AUTHOR_ID, POST_ID, format=None):

        try:
            related_post = Post.objects.get(id=POST_ID)
            likes = Like.objects.filter(user=related_post.author)
            likes_serializer = LikeSerializer(likes, many=True)
            
            for like_data in likes_serializer.data:
                like_data['object'] = "https://cmput404-socialdist-project.herokuapp.com/author/{}/post/{}".format(str(AUTHOR_ID), str(POST_ID))
                like_data['@context'] = 'https://cmput404-socialdist-project.herokuapp.com/post/feed'
                user_profile = User_Profile.objects.get(user=like_data['user']['id'])
                like_data['summary'] = "{} Likes your post".format(user_profile.displayName)
            return JsonResponse(likes_serializer.data, safe=False)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class HandleCommentLike(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ExemptGetPermission]
    def get(self, request, AUTHOR_ID, POST_ID, COMMENT_ID, format=None):
        try:
            user_comment = Comment.objects.get(author = AUTHOR_ID)
            print(user_comment.id)
            comment = Comment.objects.get(id=COMMENT_ID)
            post = Post.objects.get(id=POST_ID)

            if comment.post.id != post.id:
                return JsonResponse(
                    {
                        'message':
                        'The requested post does not have the requested comment'
                    },
                    status=status.HTTP_404_NOT_FOUND)
            if post.author != AUTHOR_ID:
                return JsonResponse(
                    {
                        'message':
                        'The requested author does not have the requested post'
                    },
                    status=status.HTTP_404_NOT_FOUND)
            commentlikes = CommentLike.objects.filter(comment=comment)
            like_serializer = LikeCommentSerializer(likes, many=True)
            for like_data in like_serializer.data:
                like_data['object'] = "https://cmput404-socialdist-project.herokuapp.com/author/{}/post/{}".format(str(AUTHOR_ID), str(POST_ID))
                like_data['@context'] = 'https://cmput404-socialdist-project.herokuapp.com/post/feed'
                user_profile = User_Profile.objects.get(user=like_data['user']['id'])
                like_data['summary'] = "{} Likes your post".format(user_profile.displayName)
            return JsonResponse(like_serializer.data, safe=False)
        except Comment.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested comment does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class HandleAuthorLike(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ExemptGetPermission]
    def get(self, request, AUTHOR_ID, format=None):
        try:
            author = User.objects.get(id=AUTHOR_ID)
            likes = Like.objects.filter(user=author)
            comment_likes = CommentLike.objects.filter(user = author)
            likes_serializer = LikeSerializer(likes, many=True)
            comment_likes_serializer = LikeCommentSerializer(comment_likes, many = True)
            for like_data in likes_serializer.data:
                like_data['object'] = "https://cmput404-socialdist-project.herokuapp.com/author/{}".format(str(AUTHOR_ID))
                like_data['@context'] = 'https://cmput404-socialdist-project.herokuapp.com/post/feed'
                user_profile = User_Profile.objects.get(user=like_data['user']['id'])
                like_data['summary'] = "{} Likes your post".format(user_profile.displayName)
            for like_data in comment_likes_serializer.data:
                like_data['object'] = "https://cmput404-socialdist-project.herokuapp.com/author/{}".format(str(AUTHOR_ID))
                like_data['@context'] = 'https://cmput404-socialdist-project.herokuapp.com/post/feed'
                user_profile = User_Profile.objects.get(user=like_data['user']['id'])
                like_data['summary'] = "{} Likes your post".format(user_profile.displayName)
            
            return JsonResponse(likes_serializer.data + comment_likes_serializer.data, safe=False)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)

class HandleInboxPost(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [ExemptGetPermission]
    def get(self, request, AUTHOR_ID, format=None):
        try:
            author = User.objects.get(id=AUTHOR_ID)
            user_profile = User_Profile.objects.get(user = author)
            user_follows = UserFollows.objects.filter(actor= user_profile)

            new_data = [] 
            for user_follow in user_follows:
                posts = Post.objects.filter(author=user_follow.object.user)
                post_serializer = PostSerializer(posts, many=True)
                for post_serializer_data in post_serializer.data:
                    comments = Comment.objects.filter(post = post_serializer_data['id'])
                    count = len(comments)
                    post_serializer_data['origin'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post_serializer_data['id']))
                    post_serializer_data['source'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post_serializer_data['id']))
                    post_serializer_data['description'] = "This post discusses stuff -- brief"
                    post_serializer_data['categories'] = []
                    post_serializer_data['count'] = count
                    post_serializer_data['comments'] = "https://cmput404-socialdist-project.herokuapp.com/posts/{}".format(str(post_serializer_data['id']))
                    if post_serializer_data['contentType'] == 1:
                        post_serializer_data['contentType'] = "text/markdown"
                    else:
                        post_serializer_data['contentType'] = "text/plain"
                print(type(post_serializer.data))
                new_data.extend(post_serializer.data)
            
            return JsonResponse(new_data, safe=False)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)
    def post(self, request, AUTHOR_ID, format=None):
        try:
            author = User.objects.get(id=AUTHOR_ID)
            user_profile = User_Profile.objects.get(user = author)
            user_follows = UserFollows.objects.filter(actor= user_profile)
            data = JSONParser().parse(request)
            print('check1')
            if data['type'] == 'post':
                try:
                    try: 
                        
                        user = User.objects.get(id=data['user'])
                    
                    except KeyError:
                        
                        user = User.objects.get(id=data['author']['id'])

                    except TypeError:
                        
                        user = User.objects.get(id=data['user']['id'])
                                 
                    except:
                        
                        user = User.objects.get(id=data['author'])
                        
                    
                    
                    
                    if data['contentType'] == "text/markdown":
                        data['contentType'] = 1
                    else:
                        data['contentType'] = 0
                    created_post = Post(title=data['title'], text=data['text'], image=data['image'], author=user,
                            shared_user = data['shared_user'],shared_on = data['shared_on'],
                            privacy=data['privacy'], contentType=data['contentType'],)
                    
                    created_post.save()
                    post_serializer = PostSerializer(created_post)
                    inbox = Inbox.objects.get(author=AUTHOR_ID)
                    inbox.post.add(created_post.id)
                    
                    return JsonResponse(post_serializer.data)
                except User.DoesNotExist:
                    return JsonResponse(
                        {'message': 'The requested user does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
            print('check2')
            if data['type'] == 'follow':
                try:
                    try: 
                        
                        user = User.objects.get(id=data['user'])
                    
                    except KeyError:
                        
                        user = User.objects.get(id=data['author']['id'])

                    except TypeError:
                        
                        user = User.objects.get(id=data['user']['id'])
                                 
                    except:
                        
                        user = User.objects.get(id=data['author'])
                    
                    request_user = User.objects.get(id=AUTHOR_ID)
                    
                    actor = data['actor']
                    actor_user = User.objects.get(actor['id'])
                    actor_profile = User_Profile.objects.get(user=actor_user)
                    friend_request = FriendRequest.create_friend_request(foreign_user_profile, user_profile)
                    friend_request.save()
                    inbox = Inbox.objects.get(author=AUTHOR_ID)
                    inbox.follow.add(friend_request.id)
                    
                except User.DoesNotExist:
                    return JsonResponse(
                        {'message': 'The requested user does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
            print('check3')
            if data['type'] == 'like':
                try:
                    inbox = Inbox.objects.get(author=AUTHOR_ID)
                    
                    
                    try: 
                        
                        user = User.objects.get(id=data['user'])
                    
                    except KeyError:
                        
                        user = User.objects.get(id=data['author']['id'])

                    except TypeError:
                        
                        user = User.objects.get(id=data['user']['id'])
                                 
                    except:
                        
                        user = User.objects.get(id=data['author'])
                    
                    created_like = Like(user=user, object = data['object'])
                    created_like.save()
                    like_serializer = LikeSerializer(created_like)
                    inbox.like.add(created_like.id)

                    search_comment = re.findall("(?:(comments\/))(.+)", data['object'])
                    if search_comment:
                        if len(search_comment) != 0:
                            comment_id = search_comment[0]
                            comment = Comment.objects.get(id = comment_id[1])
                            comment.like.add(created_like)
                    else:
                        search_post = re.findall("(?:(post\/))(.+)", data['object'])
                        if len(search_post) != 0:
                            post_id = search_post[0]
                            print(post_id)
                            post = Post.objects.get(id = int(post_id[1]))
                            post.like.add(created_like)


                    return JsonResponse(like_serializer.data,
                                        status=status.HTTP_201_CREATED)
                except User.DoesNotExist:
                    return JsonResponse(
                        {'message': 'The requested user does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
                except Inbox.DoesNotExist:
                    return JsonResponse(
                        {'message': 'The requested inbox does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def request_post_list(request):
    posts = Post.objects.all()
    posts_serializer = PostSerializer(posts, many=True)
    return Response(posts_serializer.data)


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


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_posts_from_user(request, username):
    if request.method == 'GET':
        try:
            related_user = User.objects.get(username=username)
            posts = Post.objects.filter(author=related_user)
            posts_serializer = PostSerializer(posts, many=True)
            return JsonResponse(posts_serializer.data, safe=False)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def manage_user_post(request, username):
    if request.method == 'POST':
        try:
            related_user = User.objects.get(username=username)

            #This part of code will check if the token from request matches the token of author.
            user_token = Token.objects.get(user=related_user)
            entered_token = re.findall('(?:Token\s)(\w*)',
                                       request.META['HTTP_AUTHORIZATION'])[0]
            if str(user_token) != entered_token:
                return JsonResponse(
                    {'message': 'The token user does not match the post user'},
                    status=status.HTTP_403_FORBIDDEN)
            #End of this part of code.

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
            related_user = User.objects.get(username=username)

            #This part of code will check if the token from request matches the token of author.
            user_token = Token.objects.get(user=related_user)
            entered_token = re.findall('(?:Token\s)(\w*)',
                                       request.META['HTTP_AUTHORIZATION'])[0]
            if str(user_token) != entered_token:
                return JsonResponse(
                    {'message': 'The token user does not match the post user'},
                    status=status.HTTP_403_FORBIDDEN)
            #End of this part of code.

            posts = Post.objects.filter(author=related_user)
            for post in posts:
                post.delete()
            return JsonResponse({'message': 'Posts were deleted'},
                                status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested user does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def request_post(request, id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(id=id)
            post_serializer = PostSerializer(post)
            return Response(post_serializer.data)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE'])
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

            #This part of code will check if the token from request matches the token of author.
            user_token = Token.objects.get(user=related_post.author)
            entered_token = re.findall('(?:Token\s)(\w*)',
                                       request.META['HTTP_AUTHORIZATION'])[0]
            if str(user_token) != entered_token:
                return JsonResponse(
                    {'message': 'The token user does not match the post user'},
                    status=status.HTTP_403_FORBIDDEN)
            #End of this part of code.

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
            related_post = Post.objects.get(id=id)

            #This part of code will check if the token from request matches the token of author.
            user_token = Token.objects.get(user=related_post.author)
            entered_token = re.findall('(?:Token\s)(\w*)',
                                       request.META['HTTP_AUTHORIZATION'])[0]
            if str(user_token) != entered_token:
                return JsonResponse(
                    {'message': 'The token user does not match the post user'},
                    status=status.HTTP_403_FORBIDDEN)
            #End of this part of code

            related_post.delete()
            return JsonResponse({'message': 'Post was deleted'},
                                status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_comments_from_post(request, post_id):
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


@api_view(['POST', 'DELETE'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def manage_post_comment(request, post_id):

    if request.method == 'POST':
        try:
            related_post = Post.objects.get(id=post_id)
            '''
            #This part of code will check if the token from request matches the token of author.
            user_token = Token.objects.get(user=related_post.author)
            entered_token = re.findall('(?:Token\s)(\w*)',
                                       request.META['HTTP_AUTHORIZATION'])[0]
            if str(user_token) != entered_token:
                return JsonResponse(
                    {'message': 'The token user does not match the post user'},
                    status=status.HTTP_403_FORBIDDEN)
            #End of this part of code.
            '''
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

            #This part of code will check if the token from request matches the token of author.
            user_token = Token.objects.get(user=related_post.author)
            entered_token = re.findall('(?:Token\s)(\w*)',
                                       request.META['HTTP_AUTHORIZATION'])[0]
            if str(user_token) != entered_token:
                return JsonResponse(
                    {'message': 'The token user does not match the post user'},
                    status=status.HTTP_403_FORBIDDEN)
            #End of this part of code.

            comments = Comment.objects.filter(post=related_post)
            for comment in comments:
                comment.delete()
            return JsonResponse({'message': 'Comments were deleted'},
                                status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def request_comment(request, comment_id):
    if request.method == 'GET':
        try:
            related_comment = Comment.objects.get(id=comment_id)
            comment_serializer = CommentSerializer(related_comment)
            return JsonResponse(comment_serializer.data)
        except Comment.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested comment does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def crud_comment(request, comment_id):
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


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def get_likes_from_post(request, post_id):
    if request.method == 'GET':
        try:
            related_post = Post.objects.get(id=post_id)
            likes = Like.objects.filter(post=related_post)
            likes_serializer = LikeSerializer(likes, many=True)
            print(likes_serializer.data)
            return JsonResponse(likes_serializer.data, safe=False)
        except Post.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested post does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def manage_post_like(request, post_id):

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


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def request_like(request, like_id):
    if request.method == 'GET':
        try:
            related_like = Like.objects.get(id=like_id)
            like_serializer = LikeSerializer(related_like)
            return JsonResponse(like_serializer.data)
        except Like.DoesNotExist:
            return JsonResponse(
                {'message': 'The requested like does not exist'},
                status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def crud_like(request, like_id):

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
        event = request.POST.get('select_event', False)
        if event == False:
            return render(request, 'users/user_home_page.html')
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
    like = Like(user=request.user, object = 'https://cmput404-socialdist-project.herokuapp.com/author/{}/post/{}/comments/{}'.format(comment.post.author.id, comment.post.id, comment.id))
    like.save()
    comment.like.add(like)
    
    return HttpResponseRedirect(reverse('post_placeholder', args=[str(pk)]))


class addPost(CreateView):
    model = Post
    form_class = addPostForm
    template_name = 'posts/addPost.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pub_date = datetime.datetime.now()
        return super().form_valid(form)


class addComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/addComment.html'
    success_url = reverse_lazy('feed')
    
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)


class updatePost(UpdateView):
    model = Post
    template_name = 'posts/editPost.html'
    fields = ['title', 'text', 'image', 'image_link']
    success_url = reverse_lazy('feed')


class deletePost(DeleteView):
    model = Post
    template_name = 'posts/deletePost.html'
    success_url = reverse_lazy('feed')


class SharedPostView(View):
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
            image_link=post_object.image_link,
            pub_date=post_object.pub_date,
            author=post_object.author,
            shared_user=current_user,
            privacy=post_object.privacy,
            contentType=post_object.contentType).save()
        post_object.share.add(current_user)
        return HttpResponseRedirect(reverse('feed'))


def send_token(request, username, password):

    data = {'username': username, 'password': password}

    response = requests.post(
        'https://cmput404-socialdist-project.herokuapp.com/api-token-auth/',
        json=data)
    dict_data = ast.literal_eval(response.text)
    print(ast.literal_eval(response.text))
    return JsonResponse(dict_data, safe=False)


def get_t15_posts(url):

    ext_request = requests.get(url,
                               auth=('connectionsuperuser', '404connection'),
                               headers={'Referer': "http://127.0.0.1:8000/"})

    ext_request = ext_request.json()
    return ext_request


def view_t15_posts(request):
    url = "https://unhindled.herokuapp.com/service/allposts/"
    posts = get_t15_posts(url)
    return render(request, 'posts/team15posts.html', {'posts': posts})

def testing(request, user_id):
    is_foreign_id(user_id)
    return HttpResponse("test")

def view_foriegn_posts(request):
    if node_working(request):
        node = get_nodes()
        url = request.get_full_path()
        if url in node:
            n = list(filter(lambda node: node['url'] == url, node))
            print('list :'+ str(n))
            ext_request = requests.get(url, auth=(n.username,n.password), headers={'Referer': "http://localhost:8000/"})
            ext_request = ext_request.json()
            return render(request, 'posts/team15posts.html', {'posts': ext_request})
        else:
            return HttpResponse(node)
    else:
        return HttpResponse()

def node_working(request):
    url = request.build_absolute_uri()
    host  = ['http://127.0.0.1:8000/', 'http://localhost:8000/', 'https://social-dis.herokuapp.com/',]
    
    for node in get_nodes():
        print('node ' + str(node['url']))
        print('url ' + url)
        if url in node['url']:
            return True
        else:
            return False

def get_nodes():
    nodes = Node.objects.all()
    serializer = NodeSerializer(nodes, many=True)
    connected = []
    for node in serializer.data:
        connected.append(node)
    return connected     


#curl -X POST -d "username=1&password=12345" http://127.0.0.1:8000/api-token-auth/
#curl -X POST -d '{"title":"This is a new post","text":"a new post is here","image":null,"pub_date":"2021-11-09T21:51:55.850726Z","author":2,"shared_user":null,"shared_on":null,"privacy":0,"contentType":"text/plain"}' http://127.0.0.1:8000/post/create_new_post -H 'Authorization: Token 8a91340fa2849cdc7e0e7aa07f4b2c0e91f09a3a'
#curl -X GET http://127.0.0.1:8000/post/manage_user_post/1 -H 'Authorization: Token 8a91340fa2849cdc7e0e7aa07f4b2c0e91f09a3a'
#curl -X POST -d '{"title":"This is a new post","text":"a new post is here","image":null,"pub_date":"2021-11-09T21:51:55.850726Z","author":2,"shared_user":null,"shared_on":null,"privacy":0,"contentType":"text/plain"}' http://127.0.0.1:8000/post/manage_user_post/9 -H 'Authorization: Token 8a91340fa2849cdc7e0e7aa07f4b2c0e91f09a3a'
#curl -X PUT -d '{"title":"This is a new post","text":"a new post is here","image":null,"pub_date":"2021-11-09T21:51:55.850726Z","author":2,"shared_user":null,"shared_on":null,"privacy":0,"contentType":"text/plain"}' http://127.0.0.1:8000/post/crud_post/42 -H 'Authorization: Token 8a91340fa2849cdc7e0e7aa07f4b2c0e91f09a3a'
#curl -X DELETE http://127.0.0.1:8000/post/crud_post/33 -H 'Authorization: Token 8a91340fa2849cdc7e0e7aa07f4b2c0e91f09a3a'
