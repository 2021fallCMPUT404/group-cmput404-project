from django import forms
from django.forms.widgets import Textarea


class create_user(forms.Form):
    username = forms.CharField(initial='doge')
    password = forms.CharField(initial='12345', widget=forms.PasswordInput())
    confirm_password = forms.CharField(initial='12345',
                                       widget=forms.PasswordInput())
    github_user_url = forms.URLField(
        initial=
        'https://github.com/2021fallCMPUT404/group-cmput404-project/tree/main')
    bio = forms.CharField(initial='I am a doge', widget=Textarea)
    profile_photot = forms.ImageField(initial='image/users/egg_dog.jpeg')