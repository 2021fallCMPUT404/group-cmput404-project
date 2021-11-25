from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Post, Comment, Share


class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
        }))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #How to set author into fields?
        fields = ('comment_body', )
        widgets = {
            'comment_body': forms.Textarea(attrs={'rows':4}),
        }


class addPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'privacy',)
        widgets={
            'title': forms.Textarea(attrs={'rows': 1}),
            'text': forms.Textarea(attrs={'rows': 7}),
        }
