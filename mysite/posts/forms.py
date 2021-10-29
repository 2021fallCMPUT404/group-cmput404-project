from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Post, Comment

class ShareForm(forms.Form):
  body = forms.CharField(
  label='',
  widget=forms.Textarea(attrs={
    'rows': '3',
    'placeholder': 'Say Something...'
  }))



class CommentForm(forms.ModelForm):
  class Meta:
    model=Comment
    #How to set author into fields?
    fields=('comment_body',)
    widgets={
      #'author':forms.TextInput(),
      'comment_body':forms.Textarea(),

    }
