from requests import request, HTTPError
from accounts.models import MyProfile
from django.core.files.base import ContentFile
from actstream.actions import follow
from django.contrib.auth.models import User
from myProject import settings

def save_profile_picture(strategy, user, response, details,
                         is_new=False,*args,**kwargs):

    if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            try:
                profile = MyProfile.objects.get(user = user)
            except MyProfile.DoesNotExist:
                profile = MyProfile.objects.create(user = user)
            follow(user,user)
            profile.mugshot.save('{0}_social.jpg'.format(user.username),
                                   ContentFile(response.content))
            p = str(profile.mugshot.url)
            profile.mugshot =  p
            profile.save()