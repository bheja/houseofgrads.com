from django.forms import ModelForm
from blogs.models import Blog
from django import forms

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ('title','author','blog_content','tag','published')
        widgets = {'author': forms.HiddenInput(),}