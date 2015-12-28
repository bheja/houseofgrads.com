__author__ = 'vishalsingh'

from django.contrib.sitemaps import Sitemap
from posts.models import CreatePost, ParentThread
from blogs.models import Blog

class PostSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 0.8
    wallid = ParentThread.objects.get(name='myWall')
    def items(self, wallid=wallid):
        return CreatePost.objects.exclude(thread = wallid)

class ThreadSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ParentThread.objects.exclude(stream = 'WAL')

class BlogSiteMap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Blog.objects.exclude(published = False)
