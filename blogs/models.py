from django.db import models
from django.contrib.auth.models import User
import datetime

class BlogTags(models.Model):
    tag = models.CharField(max_length=100)
    @models.permalink
    def get_absolute_url(self):
        return ('blog_tag_list',[str(self.id)])
    def no_blogs(self):
        count = Blog.objects.filter(tag = self.id).filter(published=True).count()
        return count

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User,related_name='blogs')
    date = models.DateTimeField(default=None)
    blog_content = models.TextField(max_length=1200)
    tag = models.ForeignKey(BlogTags,related_name='listed_blogs')
    published = models.BooleanField(default=False)
    editor_pick = models.BooleanField(default=False)
    slug = models.SlugField(blank=True,null=True, max_length=200)

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.now()
        fake_slug = '-'.join(self.title.split(','))
        fake_slug = '-'.join(fake_slug.split('_'))
        fake_slug = '-'.join(fake_slug.split('['))
        fake_slug = '-'.join(fake_slug.split(']'))
        fake_slug = '-'.join(fake_slug.split('('))
        fake_slug = '-'.join(fake_slug.split(':'))
        fake_slug = '-'.join(fake_slug.split(')'))
        fake_slug = '-'.join(fake_slug.split('.'))
        self.slug = '-'.join(fake_slug.split())
        return super(Blog, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('blogs.views.blog_details', args=(str(self.id),self.slug))


class BlogImage(models.Model):
    url = models.CharField(max_length=300)
    blog = models.OneToOneField(Blog,related_name='cover_image')

    def __unicode__(self):
        return self.url

class TagImage(models.Model):
    url = models.CharField(max_length=300)
    tag = models.ForeignKey(BlogTags,related_name='tag_image')
