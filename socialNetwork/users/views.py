from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    my_dict = {'insert_me': "This line is from users/index.html"}
    return render(request, 'users/index.html', context=my_dict)
