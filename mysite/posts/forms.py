from django import forms
from .models import Post, Comment

class ShareForm(forms.Form):
  body = forms.CharField(
  label='',
  widget=forms.Textarea(attrs={
    'rows': '3',
    'placeholder': 'Say Something...'
  }))
