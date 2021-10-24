import sys

sys.path.append(".")
from django.shortcuts import render
from django.http import HttpResponse
from . import create_user_form

# Create your views here.


def index(request):
    my_dict = {'insert_me': "This line is from users/index.html"}
    return render(request, 'users/index.html', context=my_dict)


def create_user(request):
    return render(request, 'users/index.html')


def create_user_profile(request):
    form = create_user_form.create_user()
    if request.method == 'POST':
        print('check')
        form = create_user_form.create_user(request.POST)
        if form.is_valid():
            print("We got a post")
            print('print' + form.cleaned_data['username'])
            print('print' + form.cleaned_data['github_user_url'])
            print('print' + form.cleaned_data['bio'])
    return render(request, 'users/create_user_form.html', {'form': form})