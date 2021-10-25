from django import forms
from django.forms.widgets import Textarea
from django.core import validators
from users.models import User_Profile
'''
class create_user(forms.Form):
    username = forms.CharField(initial='doge')
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='confirm_password',
                                       widget=forms.PasswordInput())
    github_user_url = forms.URLField(
        initial=
        'https://github.com/2021fallCMPUT404/group-cmput404-project/tree/main')
    bio = forms.CharField(initial='I am a doge', widget=Textarea)
    profile_photot = forms.ImageField(initial='image/users/egg_dog.jpeg')
    check_bot = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super(create_user, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        checking_bot = cleaned_data.get("check_bot")
        print(password, confirm_password)
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match.")
        if len(checking_bot) > 0:
            raise forms.ValidationError("This is a bot.")

'''


class create_new_user(forms.ModelForm):

    password = forms.CharField(label='password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='confirm_password',
                                       widget=forms.PasswordInput())
    check_bot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta():
        model = User_Profile
        #fields = ['profileImage', 'bio', 'github', 'created_date']
        fields = ['profileImage', 'bio', 'github']

    def clean(self):
        cleaned_data = super(create_new_user, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        checking_bot = cleaned_data.get("check_bot")
        print(password, confirm_password)
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match.")
        if len(checking_bot) > 0:
            raise forms.ValidationError("This is a bot.")