from django.db import models
from django.contrib.auth.models import User
from threads.models import StudyStream
from tinymce import models as tinymce_models
from datetime import datetime
from actstream.models import following, followers


class ParentThread(models.Model):
    name = models.CharField(max_length=500)
    brief = models.TextField(blank=True)
    stream = models.ForeignKey(StudyStream, to_field='name')
    author = models.ForeignKey(User,related_name='threads')
    slug = models.SlugField(max_length=500,blank=True,null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        fake_slug = '-'.join(self.name.split(','))
        fake_slug = '-'.join(fake_slug.split('.'))
        fake_slug = '-'.join(fake_slug.split('['))
        fake_slug = '-'.join(fake_slug.split(']'))
        fake_slug = '-'.join(fake_slug.split('('))
        fake_slug = '-'.join(fake_slug.split(':'))
        fake_slug = '-'.join(fake_slug.split(')'))
        fake_slug = '-'.join(fake_slug.split('_'))
        self.slug = '-'.join(fake_slug.split())
        return super(ParentThread, self).save(*args, **kwargs)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('threads.views.thread_detail', args=[self.slug])

    class Meta:
        ordering = ['name']

    def no_followers(self):
        return self, len(followers(self))

class CreatePost(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=None)
    thread = models.ForeignKey(ParentThread)
    content = models.TextField()
    share_num = models.PositiveIntegerField(default=0)
    like_num = models.PositiveIntegerField(default=0)
    view_num = models.PositiveIntegerField(default=0)

    def save(self,*args,**kwargs):
        self.date = datetime.now()
        return super(CreatePost, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.content

    @models.permalink
    def get_absolute_url(self):
        return ('post_details', [self.id])

    class Meta:
        ordering = ['-view_num', '-like_num']


class Comment(models.Model):
    post = models.ForeignKey(CreatePost)
    comment_content = models.TextField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User)
    like_num = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.comment_content, self.author

    class Meta:
        ordering = ['date']


class PreviewUrl(models.Model):
    preview = models.TextField()
    post = models.OneToOneField(CreatePost)

    def __unicode__(self):
        return self.preview


class PostImage(models.Model):
    img_url = models.CharField(max_length=500, blank=True)
    post = models.ForeignKey(CreatePost, related_name='image')
    def __unicode__(self):
        return self.img_url
