from django.shortcuts import render, get_object_or_404
from . import views
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User, Create_user, User_Profile
from django.apps import apps
from . import create_user_form
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

Post_model = apps.get_model('posts', 'Post')


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
            if user.is_active:
                login(request, user)
                #return HttpResponseRedirect(reverse('advance_home_page'))
                return HttpResponseRedirect('user_home_page')

            else:
                print('This user account is not activated yet')
                HttpResponse('This user account is not activated yet')
        else:
            print('No such username or password in the database')
            #HttpResponse('No such username or password in the database')
            return render(request, 'users/login_failed.html')
    else:
        return render(request, 'users/login.html', {})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_home_page'))


@login_required
def confirm_logout_view(request):
    return HttpResponse("logout from the user account")


@login_required
def user_home_page_view(request):
    user = User.objects.get(id = request.user.id)
    user_profile_image = User_Profile.profileImage
    return render(request, 'users/user_home_page.html', context={'insert_username': request.user.username, 'user_profile_image':user_profile_image})

