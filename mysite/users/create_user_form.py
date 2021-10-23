from django import forms
from django.forms.widgets import Textarea

class create_user(forms.Form):
    name = forms.CharField()
    github_user_url =  forms.URLField()
    bio = forms.CharField(widget=Textarea)
    profile_photot = forms.ImageField()