from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile
from django.dispatch import receiver
from actstream.models import following, followers

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=('user'),
                                related_name='my_profile')
    about_me = models.TextField(null = True, blank=True)
    location = models.CharField(max_length = 50, null = True, blank=True)
    age = models.PositiveSmallIntegerField(null = True, blank=True)
    gate_stream = models.CharField(max_length = 3)
    genius_score=models.PositiveIntegerField(default = 1)
    no_of_followers = models.PositiveIntegerField(default=1)
    birth_date = models.DateField(null=True)
    college = models.CharField(max_length=400,blank=True,null=True)
    
    @models.permalink
    def get_absolute_url(self):
	return ('userena_profile_detail', [self.username])
    def no_followers(self):
        return self.user, len(followers(self.user))
        
class BlockList(models.Model):
    user = models.ForeignKey(User, related_name="block_list")
    blockedlist = models.ManyToManyField(User,related_name="blocked_by")

class FeedBack(models.Model):
    description = models.TextField()
    category = models.CharField(max_length=200)
    images = models.ImageField(upload_to='/houseofgrads/lighttpd/hog/hogstatic/media/feedback')

class ReportedContent(models.Model):
    contenttype = models.CharField(max_length=300)
    reported_by = models.ManyToManyField(User,related_name='reported_content')
    primarykey = models.IntegerField(max_length=50)
    content= models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
   ##/home/houseofg/lighttpd/hog/hogstatic/media/feedback/