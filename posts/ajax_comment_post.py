from __future__ import absolute_import
from django import http
from notifications import notify
from django.contrib.comments.forms import CommentForm
from posts.models import CreatePost
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from actstream import action
from django.contrib.auth.models import User
from posts.tasks import send_notice_mail
import json
import re
from endless_pagination.decorators import page_template
from django.contrib.comments.models import Comment
from guardian.shortcuts import assign_perm

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
            target = CreatePost.objects.get(id=object_pk)
            brief = str(target.content)
            form = CommentForm(target, data=data)
            if not form.is_valid:
                print form.errors
            comment = form.get_comment_object()
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            if request.user.is_authenticated():
                comment.user = request.user
                c = comment.save()
                cid = str(comment.id)
                if target.author != comment.user:
                    notify.send(comment.user, recipient=target.author, verb=u'commented on your post', action_object=target, target=c)
                    text = 'Hi'+str(target.author)+',/n'+str(request.user.username)+' has commented on your post. Please go to following link to see the post./n'+ str(target.get_absolute_url)+'/n/nThanks and best regards,/nHouseofGrads.com'
                    send_notice_mail.delay(contenttext=target.id,text=text,template="notification/email/commented.html",targetuser=str(target.author.id),fromuser=str(request.user.id),verb='commented on your post.')
                if match:
                    for m in match:
                        try:
                            userobj = User.objects.get(username__iexact=m)
                        except User.DoesNotExist:
                            userobj = None
                        if userobj !=None:
                            if request.user != userobj:
                                notify.send(request.user, recipient=userobj, verb=u'tagged you in a comment', action_object=target)
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

@login_required
@page_template('feed/comment_paginate.html')
def comment_list(request, post_id, template='feed/comment_paginate.html',extra_context=None):
    if request.method == "GET":
        if request.is_ajax:
            post_id = int(post_id)
            c_list = Comment.objects.filter(object_pk = post_id).order_by('-submit_date')
            count = c_list.count()
            c = Context({
            'comments':c_list,
            'count':count,
            'request':request,})
            return render_to_response(template, c, context_instance=RequestContext(request))
        else:
            return http.HttpResponseRedirect('home/')
    else:
        http.Http404()
