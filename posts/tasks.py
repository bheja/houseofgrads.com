from django.contrib.auth.models import User
from datetime import timedelta
from actstream.actions import follow, unfollow
from celery import shared_task
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import get_object_or_404
from posts.models import CreatePost
from django.contrib.auth.models import User
from conversation.models import Conversation

@shared_task
def send_notice_mail(contenttext,text,template='',targetuser='',fromuser='',verb='',msg='False'):
        if msg == 'False':
                contenttext2 = CreatePost.objects.get(id=int(contenttext))
        else:
                contenttext2 = Conversation.objects.get(pk=int(msg))
                msg = contenttext
        try:
                targetuser = User.objects.get(pk=int(targetuser))
        except User.DoesNotExist:
                targetuser=None
        try:
                fromuser = User.objects.get(pk = int(fromuser))
        except User.DoesNotExist:
                fromuser = None
        if contenttext2 is not None and targetuser is not None and fromuser is not None:
                temp = get_template(template)
                from_email = 'HouseofGrads Notifications <admin@houseofgrads.com>'
                subject = '[HouseofGrads.com] '+str(fromuser.username) + ' '+str(verb)
                context = Context({'user': targetuser, 'fromuser':fromuser,'verb':verb,'content_text':contenttext2,'msg':msg})
                content = temp.render(context)
                if not targetuser.email:
                        raise BadHeaderError('No email address given for {0}'.format(targetuser))
                msg = EmailMultiAlternatives(subject, text, from_email,[targetuser.email])
                msg.attach_alternative(content, "text/html")
                msg.content_subtype = "html"
                msg.send()
                return ''
        else:
                return ''  ## find the correct return
