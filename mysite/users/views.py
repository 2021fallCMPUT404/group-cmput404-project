from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from . import views
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Create_user, User_Profile, FriendRequest, UserFollows
from posts.views import *  #Will change this later on
from posts.serializers import * #Also will change this too
from django.apps import apps
from . import create_user_form
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.db.models import Q
from .serializers import UserSerializer, userFollowSerializer, userPSerializer, friend_request_serializer
from users.connect import get_authors
#rest framework imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication, get_authorization_header
import requests

Post_model = apps.get_model('posts', 'Post')


@api_view(['GET'])
def apiOverview(request):
    return Response("API BASE POINT", safe=False)

#TODO: ADD PAGINATION WHERE NEEDED
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def UserList(request):
    user_profiles = User_Profile.objects.all()
    serializer = userPSerializer(user_profiles, many=True)
    return Response({'type': 'authors', 'items': serializer.data})


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def userGet(request, User_id):
    user = get_object_or_404(User, pk=User_id)
    print(user)
    print(user.id, User_id)
    user_profile = get_object_or_404(User_Profile, user=user)
    if request.method == "GET":
        serializer = userPSerializer(user_profile, many=False)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = userPSerializer(instance=user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def follow_list(request, User_id):
    user = get_object_or_404(User, pk=User_id)
    user_profile = get_object_or_404(User_Profile, user=user)
    followers_list = UserFollows.objects.filter(object=user_profile)
    actor_list = []
    for follow in followers_list:
        actor_list.append(follow.actor)
    serializer = userPSerializer(actor_list, many=True)
    return Response({'type': 'follow', 'items': serializer.data})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def following_list(request, User_id):
    user = get_object_or_404(User, pk=User_id)
    user_profile = get_object_or_404(User_Profile, user=user)
    followers_list = UserFollows.objects.filter(actor=user_profile)
    object_list = []
    for followed in followers_list:
        object_list.append(followed.object)
    serializer = userPSerializer(object_list, many=True)
    return Response({'type': 'following', 'items': serializer.data})


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def follow_crud(request, User_id, Foreign_id):
    user = get_object_or_404(User, pk=User_id)
    foreign_user = get_object_or_404(User, pk=Foreign_id)
    user_profile = get_object_or_404(User_Profile, user=user)
    foreign_user_profile = get_object_or_404(User_Profile, user=foreign_user)
    if request.method == 'GET':
        thing = UserFollows.objects.filter(actor=foreign_user_profile,
                                           object=user_profile).first()
        serializer = userFollowSerializer(thing, many=False)
        print('PRINTING DATA:', serializer)
        return Response(serializer.data)
    elif request.method == 'PUT':
        #TODO: PUT METHOD NEEDS TO BE AUTHENTICATED
        #f_request, created = FriendRequest.objects.get_or_create(actor=foreign_user_profile, object=user_profile)
        FriendRequest.create_friend_request(foreign_user_profile, user_profile)
        UserFollows.create_user_follow(foreign_user_profile, user_profile)
        return Response('PUT')
    elif request.method == 'DELETE':
        print('{} is unfollowing {}'.format(foreign_user_profile.displayName,
                                            user_profile.displayName))
        UserFollows.delete_user_follow(foreign_user_profile, user_profile)
        return Response('DELETE')
    else:
        return HttpResponseBadRequest('Bad')
    return Response()


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def get_post_comments(request, User_id, post_id):
    user = get_object_or_404(User, pk=User_id)
    post = get_object_or_404(Post_model, pk=post_id, author=user)

    if request.method == "GET":
        comments = Comment.objects.filter(post=post_id)
        serializers = CommentSerializer(comments, many=True)
        return Response(serializers.data)
    elif request.method == "POST":
        return
    else:
        return HttpResponseBadRequest("Method {} is not allowed".format(request.method))

    return Response()

    return Response('')
def homepage(request):
    return HttpResponse("Placeholder homepage")


def placeholder(request, User_id):
    #latest_user_list = User.objects.order_by('-id')[:5]
    #output = ','.join([str(q.username) for q in latest_user_list])

    user = get_object_or_404(User, pk=User_id)

    output = 'User id is: {}, Username is: {}, passoword is: {}'.format(
        user.id, user.username, user.password)
    return HttpResponse(output)


def user_post_view(request, User_id):
    user = get_object_or_404(User, pk=User_id)
    latest_post_list = Post_model.objects.all().filter(author__id=user.id)
    print(latest_post_list)
    return render(request, 'posts/placeholder.html',
                  {'latest_post_list': latest_post_list})


def index(request):
    #my_dict = {'insert_me': "This line is from users/index.html"}
    return render(request, 'users/user_home_page.html')


def create_user_view(request):
    #form = Create_user()
    form = create_user_form.create_new_user(request.POST)
    if request.method == "POST":
        #form = Create_user(request.POST)
        form = create_user_form.create_new_user(request.POST)
        if form.is_valid():
            print("OK")
            #TODO: CHECK IF THE USER ALREADY EXISTS IN THE DATABASE
            new_user = User.objects.create_user(
                username=form.cleaned_data['displayName'],
                password=form.cleaned_data['password'])
            user_prof = User_Profile(user=new_user)
            print(user_prof.user, user_prof.type)
            print(new_user.id)
            user_prof.save()
            form.clean()
        else:
            print("not ok")

    return render(request, 'users/create_user.html', {'form': form})


def register(request):
    registered_user = False

    if request.method == "POST":
        user_form = create_user_form.create_new_user(request.POST)
        user_profile_form = create_user_form.create_new_user_profile(
            request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = user_profile_form.save(commit=False)
            profile.user = user

            if 'profileImage' in request.FILES:
                profile.profileImage = request.FILES['profileImage']

            profile.save()

            registered = True

        else:
            print('register failed')
            print('user form error:' + str(user_form.errors))
            print('user profile form error:' + str(user_profile_form.errors))
    else:
        user_form = create_user_form.create_new_user()
        user_profile_form = create_user_form.create_new_user_profile()

    return render(
        request, 'users/register.html', {
            'user_registered': registered_user,
            'user_form': user_form,
            'profile_form': user_profile_form
        })


def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            try:

                token = Token.objects.get(user_id=user.id)

            except Token.DoesNotExist:

                token = Token.objects.create(user=user)

        if user:
            if user.is_active:
                login(request, user)
                #return HttpResponseRedirect(reverse('advance_home_page'))
                return HttpResponseRedirect('user_home_page')

            else:
                print('This user account is not activated yet')
                return HttpResponse('This user account is not activated yet')
        else:
            print('No such username or password in the database')
            #HttpResponse('No such username or password in the database')
            return render(request, 'users/login_failed.html')
    else:
        return render(request, 'users/login.html', {})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'users/login.html')


@login_required
def confirm_logout_view(request):
    return HttpResponse("logout from the user account")


@login_required
def user_home_page_view(request):
    user = User.objects.get(id=request.user.id)
    user_profile_image = User_Profile.profileImage

    the_user_profile = User_Profile.objects.get(user=request.user)
    user_display_name = the_user_profile.displayName
    return render(request,
                  'users/user_home_page.html',
                  context={
                      'insert_display_name': user_display_name,
                      'user_profile_image': user_profile_image
                  })


@login_required
def edit_user_profile_view(request):
    if request.method == "POST":

        user_profile_form = create_user_form.create_new_user_profile(
            request.POST)
        original_user_profile = User_Profile.objects.get(user=request.user)
        if user_profile_form.is_valid():
            #profile = user_profile_form.save(commit=False)
            #request.user.profile = profile
            original_user_profile.displayName = request.POST['displayName']
            original_user_profile.bio = request.POST['bio']
            original_user_profile.github = request.POST['github']
            if 'profileImage' in request.FILES:
                original_user_profile.profileImage = request.FILES[
                    'profileImage']

            original_user_profile.save()

        else:
            print('edit user profile failed')
            print('user profile form error:' + str(user_profile_form.errors))

    else:

        user_profile_form = create_user_form.create_new_user_profile()

    return render(request, 'users/edit_user_profile.html',
                  {'profile_form': user_profile_form})


def advance_home_page_view(request):
    return render(request, 'users/advance_home_page.html')


def send_friend_request(request, User_id):
    if request.user.is_anonymous:
        return HttpResponseForbidden("Please sign in")
    user = get_object_or_404(User, pk=User_id)
    print(user)
    request_profile = User_Profile.objects.get(user=request.user)
    #Checks if the object_profile is valid
    object_profile = get_object_or_404(User_Profile, user_id=User_id)
    #TODO: CHECK IF THE ACTOR IS ALREADY FOLLOWING THE OBJECT
    f_request = FriendRequest.create_friend_request(request_profile, object_profile)
    serializer = friend_request_serializer(f_request, many=False)
    print(serializer)
    print(serializer.data)
    #return HttpResponseRedirect(reverse('users:request_page'))
    return JsonResponse(serializer.data)


def accept_friend_request(request, User_id):
    #User id is from the actor, the person who sent the friend request
    #Error checking
    if request.user.is_anonymous:
        return HttpResponseForbidden("Please sign in")
    actor_user_profile = get_object_or_404(User_Profile, user_id=User_id)
    object_user_profile = get_object_or_404(User_Profile, user=request.user)
    f_request = FriendRequest.objects.filter(actor=actor_user_profile,
                                             object=object_user_profile)
    if not f_request.exists():
        return HttpResponseBadRequest("Friend request does not exist")
    #TODO: ADD THE ACTOR IN USER FOLLOWS

    actor_user = get_object_or_404(User, pk=User_id)
    UserFollows.objects.get_or_create(actor=actor_user_profile,
                                      object=object_user_profile)
    UserFollows.objects.get_or_create(actor=object_user_profile,
                                      object=actor_user_profile)
    #TODO: DO SOME ERROR CHECKING AND CHECK IF THE F_REQUEST INSTANCE EXISTS
    f_request.delete()
    print("{} accepted {}s' friend request".format(
        object_user_profile.displayName, actor_user_profile.displayName))
    return HttpResponseRedirect('/authors/requests/view-request/{}/'.format(
        request.user.id))


def reject_friend_request(request, User_id):
    if request.user.is_anonymous:
        return HttpResponseForbidden("Please sign in")
    actor_user_profile = get_object_or_404(User_Profile, user_id=User_id)
    object_user_profile = get_object_or_404(User_Profile, user=request.user)
    f_request = FriendRequest.objects.filter(actor=actor_user_profile,
                                             object=object_user_profile)
    if not f_request.exists():  #Checks if the friend request exists
        return HttpResponseBadRequest("Friend request does not exist")
    f_request.delete()
    print("{} deleted {}s' friend request".format(
        object_user_profile.displayName, actor_user_profile.displayName))
    return HttpResponseRedirect('/authors/requests/view-request/{}/'.format(
        request.user.id))


def view_friend_requests(request, User_id):
    #Makes sure that only the author can see the requests
    if request.user.id != User_id:
        return HttpResponseForbidden("You are forbidden")
    user_profile = get_object_or_404(User_Profile, user_id=User_id)
    recieved_requests = FriendRequest.objects.filter(object=user_profile)
    sent_requests = FriendRequest.objects.filter(actor=user_profile)
    print(recieved_requests, sent_requests)
    return render(request, 'users/view_requests.html', {
        'recieved_requests': recieved_requests,
        'sent_requests': sent_requests
    })


def get_t15_authors(url):

    ext_request = requests.get(url, auth=('connectionsuperuser','404connection'), headers={'Referer': "http://127.0.0.1:8000/"})

    ext_request = ext_request.json()
    return ext_request


def view_t15_users(request):
    url = "https://unhindled.herokuapp.com/service/authors"
    authors = get_t15_authors(url)
    list_of_authors = []
    for i in authors['items']:
        list_of_authors.append(i)
    return render(request, 'users/server-2.html', {'authors': list_of_authors})

def view_followers(request, User_id):
    user = get_object_or_404(User, pk=User_id)
    user_profile = get_object_or_404(User_Profile, user=user)
    followers_list = UserFollows.objects.filter(object=user_profile)
    follows_list = UserFollows.objects.filter(actor=user_profile)
    #friends_list = UserFollows.objects.filter(object_id=user_profile)
    for x in followers_list:
        print(x.actor.displayName)
    return render(
        request, 'users/view_followers.html', {
            'followers_list': followers_list,
            'user': user_profile,
            'request': request,
            'follows_list': follows_list
        })


def send_request_page(request):
    user_profile = get_object_or_404(User_Profile, user_id=request.user.id)
    users_list = User_Profile.objects.filter(~Q(user=request.user))
    print(users_list)
    return render(request, 'users/send_requests.html',
                  {'users_list': users_list})


@login_required
def generate_token(request):
    user = request.user
    new_token = Token.objects.get(user=user)
    user.token = new_token
    user.save()
    return HttpResponseRedirect('user_home_page')


#curl -X GET http://127.0.0.1:8000/post/request_post_list -H 'Authorization: Token 8a91340fa2849cdc7e0e7aa07f4b2c0e91f09a3a'