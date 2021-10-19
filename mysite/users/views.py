from django.shortcuts import render
from django.http import HttpResponse
from .models import User
# Create your views here.
def homepage(request):
	return HttpResponse("Placeholder homepage")

def placeholder(request, User_id):
	#latest_user_list = User.objects.order_by('-id')[:5]
	#output = ','.join([str(q.username) for q in latest_user_list])
	user = User.objects.get(pk=User_id)
	output = 'User id is: {}, Username is: {}, passoword is: {}'.format(user.id, user.username, user.password)
	return HttpResponse(output)