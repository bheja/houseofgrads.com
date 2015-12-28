from django.forms import ModelForm
from posts.models import CreatePost, ParentThread
from django import forms
import datetime

class PostForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','required':'required','autofocus':'none','id':'text'}))
    date = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.datetime.now())
    class Meta:
		model = CreatePost
		fields = ('author', 'date', 'thread','content')
		widgets = {
			'author': forms.HiddenInput(),
                        'thread': forms.HiddenInput(),
                        }
class ParentThreadForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required','autofocus':'none','id':'threadTitle','placeholder':'Give a title to your thread...'}))
    class Meta:
		model = ParentThread
		fields = ('name', 'brief', 'stream','author')
		widgets = {
			'stream': forms.HiddenInput(),
            'author': forms.HiddenInput(),
                        }
