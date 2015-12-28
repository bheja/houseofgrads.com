from django.contrib import admin
from .models import CreatePost, ParentThread

admin.site.register(CreatePost)
admin.site.register(ParentThread)