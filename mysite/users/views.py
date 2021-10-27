from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from . import views
from django.http import HttpResponse

from .models import User, Create_user, User_Profile, FriendRequest, UserFollows
from django.apps import apps
from . import create_user_form
#from django

Post_model = apps.get_model('posts', 'Post')


# Create your views here.
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
    my_dict = {'insert_me': "This line is from users/index.html"}
    return render(request, 'users/index.html', context=my_dict)


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


def login_view(request):
    if request.method == "POST":
        displayName = request.POST.get('displayName')
        password = request.POST.get('password')
    else:
        print('login failed')


def send_friend_request(request, User_id):
    user = get_object_or_404(User,pk=User_id)
    print(user)
    request_profile = User_Profile.objects.get(user=request.user)
    object_profile = User_Profile.objects.get(user_id=User_id)
    f_request, created = FriendRequest.objects.get_or_create(actor=request_profile, object=object_profile)
    print("Friend request created")
    print(f_request.summary())
    return HttpResponseRedirect('/authors/{}'.format(User_id))

def accept_friend_request(request, User_id):
    #User id is from the actor, the person who sent the friend request
    actor_user_profile = get_object_or_404(User_Profile, user_id=User_id)
    object_user_profile = get_object_or_404(User_Profile,user=request.user)
    f_request = FriendRequest.objects.filter(actor=actor_user_profile, object=object_user_profile)

    actor_user = get_object_or_404(User,pk=User_id)
    UserFollows.objects.get_or_create(actor_id=actor_user, object_id=request.user)
    UserFollows.objects.get_or_create(actor_id=request.user, object_id=actor_user)
    #TODO: DO SOME ERROR CHECKING AND CHECK IF THE F_REQUEST INSTANCE EXISTS
    f_request.delete()
    print("{} accepted {}s' friend request")
    return HttpResponseRedirect('/authors/{}'.format(User_id))

def reject_friend_request(request, User_id):
    return
