from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from . import forms


# Create your views here.
def homepage(request):
    return HttpResponse("Placeholder homepage")


def placeholder(request, User_id):
    #latest_user_list = User.objects.order_by('-id')[:5]
    #output = ','.join([str(q.username) for q in latest_user_list])
    user = User.objects.get(pk=User_id)
    output = 'User id is: {}, Username is: {}, passoword is: {}'.format(
        user.id, user.username, user.password)
    return HttpResponse(output)


def index(request):
    my_dict = {'insert_me': "This line is from users/index.html"}
    return render(request, 'users/index.html', context=my_dict)


def create_user(request):
    return render(request, 'users/index.html')


def create_user_form(request):
    form = forms.create_user()
    return render(request, 'users/create_user_form.html', {'form': form})
