from __future__ import absolute_import
from django import http
from notifications import notify
from django.contrib.comments.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.tasks import send_notice_mail
import json
from .models import Blog
from guardian.shortcuts import assign_perm
import re

@login_required
def post_comment(request):
    if request.method== 'POST':
        if request.is_ajax:
            data = request.POST.copy()
            tagged_users = ''
            if not data.get('name', ''):
                data["name"] = request.user.username
            if not data.get('email', ''):
                data["email"] = request.user.email
            content_comment = data.get('comment','')
            rex = re.compile(r'<a.*?>(.*?)</a>',re.I|re.M)
            match = rex.findall(content_comment)
            ctype = data.get("content_type")
            object_pk = int(data.get("object_pk"))
            target = Blog.objects.get(id=object_pk)
            form = CommentForm(target, data=data)
            comment = form.get_comment_object()
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            if request.user.is_authenticated():
                comment.user = request.user
                c = comment.save()
                cid = str(comment.id)
                if target.author != comment.user:
                    notify.send(comment.user, recipient=target.author, verb=u'commented on your blog', action_object=target, target=c)
                    text = 'Hi'+str(target.author)+',/n'+str(request.user.username)+' has commented on your blog. Please go to following link to see the post./n'+ str(target.get_absolute_url)+'/n/nThanks and best regards,/nHouseofGrads.com'
                    send_notice_mail.delay(contenttext=target.id,text=text,template="notification/email/commented.html",targetuser=str(target.author.id),fromuser=str(request.user.id),verb='commented on your blog.')
                if match:
                    for m in match:
                        try:
                            userobj = User.objects.get(username__iexact=m)
                        except User.DoesNotExist:
                            userobj = None
                        if userobj != None:
                            if request.user != userobj:
                                notify.send(request.user, recipient=userobj, verb=u'tagged you in a comment', action_object=c)
                                text = 'Hi'+str(userobj.username)+',/n'+str(request.user.username)+' has tagged you in a comment. Please go to following link to see the post./n'+ str(target.get_absolute_url)+'/n/nThanks and best regards,/nHouseofGrads.com'
                                send_notice_mail.delay(contenttext=target.id,text=text,template="notification/email/tagged_comment.html",targetuser=str(userobj.id),fromuser=str(request.user.id),verb='tagged you in a comment')

                data1 = {"success": True,'commentid':cid }
            else:
                data1 = {"success": False}
            return http.HttpResponse(json.dumps(data1), content_type='application/json')
        else:
            http.Http404('no ajax call')
    else:
        http.HttpResponseForbidden('only posts')
