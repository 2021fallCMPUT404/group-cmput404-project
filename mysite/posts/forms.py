from django import forms
from django.db.models import fields
from django.forms import widgets,Textarea
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['text'].required = True

    class Meta:
        model = Post

        exclude=['author','pub-date','like','shared_on']
        widgets={
            'title': Textarea(attrs={'rows':1, 'cols':60 , 'placeholder':'Title'}),
            'text': Textarea(attrs={'rows':8, 'cols':60,'placeholder':'Write your post here !'}),
            
        }
    
   

