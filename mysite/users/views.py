from django.shortcuts import render, get_object_or_404
from . import views
from django.http import HttpResponse
from .models import User, Create_user, User_Profile
# Create your views here.
def homepage(request):
	return HttpResponse("Placeholder homepage")

def placeholder(request, User_id):
	#latest_user_list = User.objects.order_by('-id')[:5]
	#output = ','.join([str(q.username) for q in latest_user_list])
	user = User.objects.get(pk=User_id)
	output = 'User id is: {}, Username is: {}, passoword is: {}'.format(user.id, user.username, user.password)
	return HttpResponse(output)

def index(request):
    my_dict = {'insert_me': "This line is from users/index.html"}
    return render(request, 'users/index.html', context=my_dict)

def create_user_view(request):
	form = Create_user()
	if request.method == "POST":
		form = Create_user(request.POST)
		if form.is_valid():
			print("OK")
			#TODO: CHECK IF THE USER ALREADY EXISTS IN THE DATABASE
			new_user = User.objects.create_user(username=form.cleaned_data['username'],  password=form.cleaned_data['password'])
			user_prof = User_Profile(user=new_user)
			print(user_prof.user, user_prof.type)
			print(new_user.id)
			user_prof.save()
		else:
			print("not ok")
			
	return render(request, 'users/create_user.html', {'form':form})
	#return HttpResponse("etst")