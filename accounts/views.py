from userena.views import profile_detail
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from posts.models import CreatePost, ParentThread
from actstream import models as ActStream
from actstream.models import followers, following
from actstream.actions import follow, unfollow
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from conversation.views import ConversationCreateView, ConversationUpdateView
from accounts.forms import MugshotForm
from django.template import Context, RequestContext
from conversation.models import Conversation
from accounts.models import BlockList
from endless_pagination.decorators import page_template
from operator import itemgetter
from accounts.models import MyProfile
from conversation.models import Message
from notifications import notify
from posts.tasks import send_notice_mail
from guardian.shortcuts import assign_perm
from posts.forms import ParentThreadForm
from accounts.forms import LoginForm, MyMessageForm
from userena.utils import get_protocol
from django.template.loader import render_to_string
from userena import settings as userena_settings
from django.contrib.sites.models import Site
from userena.tasks import send_activate_mail
from django.conf import settings
from django.contrib.comments.models import Comment
from .models import ReportedContent
import sys
import json


@login_required
def profile(request, username):
    user = get_object_or_404(User, username__iexact=username)
    if request.is_ajax():
        action_list = ActStream.actor_stream(user).exclude(verb='started following').exclude(verb='commented on')
        c = Context({
                'request': request,
                'action_list': action_list, })
        return render_to_response('feed/feed_paginate.html', c, context_instance=RequestContext(request))
    else:
        extra_context = dict()
        extra_context['followers'] = len(followers(user))
        extra_context['followings'] = len(following(user, User))
        extra_context['pic_form'] = MugshotForm()
        extra_context['thread_form'] = ParentThreadForm()
        extra_context['action_list'] = ActStream.actor_stream(user).exclude(verb='started following')
        response = profile_detail(request, username, extra_context=extra_context)
        return response


@login_required
def profile_edit(request):
    if request.method == 'GET':
        c = Context({
            'request': request,
        })
        return render_to_response('userena/profile_form.html', c, context_instance=RequestContext(request))
    else:
        if request.is_ajax():
            user = request.user
            profile = MyProfile.objects.get(user=request.user)
            data = request.POST.copy()
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            location = data.get('location', '')
            age = int(data.get('age'))
            about_me = data.get('about_me', '')
            privacy = data.get('privacy', '')
            mugshot = data.get('mugshot', '')
            if first_name != '':
                user.first_name = first_name
            if last_name != '':
                user.last_name = last_name
            if location != '':
                profile.location = location
            if age != 0:
                profile.age = age
            if about_me != '':
                profile.about_me = about_me
            if privacy != '':
                user.privacy = privacy
            if mugshot != '':
                profile.mugshot = mugshot
            user.save()
            profile.save()
            data = {'success': 'true'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponseForbidden('Access Not Allowed')

@login_required
def myfeed(request):
    if request.method == 'GET':
        if request.is_ajax:
            data = request.GET.copy()
            username = data['username']
            user1 = get_object_or_404(User, username__iexact=username)
            action_list = ActStream.actor_stream(user1).exclude(verb='started following')
            c = Context({
                'request': request,
                'action_list': action_list, })
            return render_to_response('feed/feed2.html', c, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('home/')
    else:
        return HttpResponseForbidden('Access Not Allowed')


@login_required
def follow_obj(request):
    if request.is_ajax:
        postdata = request.POST.copy()
        objname = postdata.get('objname', '')
        if postdata.get('thread') == 'True':
            obj = get_object_or_404(ParentThread, id=int(objname))
        else:
            obj = get_object_or_404(User, id=int(objname))

        follow(request.user, obj)
        if postdata.get('thread') == 'False':
            notify.send(recipient=obj, sender=request.user, verb='has started following you')
        data = {'success': True}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseForbidden('Access Not Allowed')


@login_required
def unfollow_obj(request):
    if request.is_ajax:
        postdata = request.POST.copy()
        objname = postdata.get('objname', '')
        if postdata.get('thread') == 'True':
            obj = get_object_or_404(ParentThread, id=int(objname))
        else:
            obj = get_object_or_404(User, id=int(objname))
        unfollow(request.user, obj)
        data = {'success': True}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseForbidden('Access Not Allowed')


@login_required
def message_handler(request):
    response = ConversationCreateView.as_view()(request)
    url = str(response.url)
    conv_id = url.split('/')
    conv_id = conv_id[2]
    users = request.POST.get('recipients', '')
    message = request.POST.get('text', '')
    user_list = [get_object_or_404(User, username__iexact=u) for u in users.split(',')]
    for user in user_list:
        text = 'Hi' + str(user.username) + ',/n' + str(
            request.user.username) + ' has messaged you. Please go to following link to see the message./n http://www.houseofgrads.com/' + str(
            user.username) + '/nThanks and best regards,/nHouseofGrads.com'
        send_notice_mail.delay(contenttext=message, msg=conv_id, text=text,
                               template="notification/email/messaged.html", targetuser=str(user.id),
                               fromuser=str(request.user.id), verb='messaged you.')
    if response.status_code == 200:
        assign_perm('conversation.delete_message', request.user)
        data = {'success': 'true'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        data = {'success': 'false'}
        return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
@page_template('conversation/conversation_list.html')
def message_list(request, template='conversation/conversation_list.html', extra_context=None):
    if request.is_ajax():
        conversation_list = request.user.conversations.exclude(archived_by__username__exact=request.user.username).order_by('-latest_message_date')
        total_conversations = request.user.conversations.all().count()
        read_conversation = request.user.read_conversations.all().count()
        unread_conversation = total_conversations - read_conversation
        c = Context({
            'request': request,
            'unread_count': unread_conversation,
            'conversation_list': conversation_list,
            'thread_form': ParentThreadForm(), })
        return render_to_response(template, c, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('ajax only')


@login_required
def message_user_list(request, pk):
    obj = get_object_or_404(Conversation, pk=pk)
    user_list = obj.users.all()
    c = Context({
        'request': request,
        'user_list': user_list, })
    return render_to_response('conversation/user_list.html', c, context_instance=RequestContext(request))


@login_required
def blocking(request, username):
    if request.is_ajax():
        block_user = get_object_or_404(User, username__iexact=username)
        try:
            b = BlockList.objects.get(user=request.user)
            b.blockedlist.add(block_user)
            unfollow(request.user, block_user)

        except BlockList.DoesNotExist:
            b = BlockList(user=request.user)
            b.save()
            b.blockedlist.add(block_user)
            unfollow(request.user, block_user)
        data = {'success': "true"}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseForbidden('wrong mate!! very wrong')


@login_required
def unblocking(request, username):
    if request.is_ajax():
        unblock_user = get_object_or_404(User, username__iexact=username)
        try:
            b = BlockList.objects.get(user=request.user)
            b.blockedlist.remove(unblock_user)
            data = {'success': "true"}

        except BlockList.DoesNotExist:
            data = {'messsage': 'technically not possible'}

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseForbidden('wrong mate!! very wrong')


def check_user(request):
    if request.is_ajax():
        username = request.POST.get('username', '')
        if username != '':
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                user = None
            if user is not None:
                data = {'exist': 'true'}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data = {'exist': 'false'}
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'exist': 'false'}
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseForbidden('wrong mate!! very wrong')


def build_feed(request, slug, stream):
    if request.method == 'GET':
        u = User.objects.get(username= 'AnonymousUser')
        top_users = MyProfile.objects.exclude(user=request.user).filter(gate_stream__iexact=stream)
        thread_list = ParentThread.objects.exclude(name='myWall').filter(stream__name__iexact=stream)
        top_list = [t.no_followers() for t in top_users]
        top_threads = [t.no_followers() for t in thread_list]
        a = sorted(top_list, key=itemgetter(1), reverse=True)[:10]
        b = sorted(top_threads, key=itemgetter(1), reverse=True)[:5]
        c = Context({
            'request': request,
            'top_users': a,
            'top_threads': b,
            'slug':slug,
        })
        return render_to_response('feed/feed_build.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('wrong mate!! very wrong')


@login_required
@page_template('conversation/conversation_all_list.html')
def see_all_view(request, template='conversation/conversation_all.html', extra_context=None):
    if request.method == 'GET':
        conversation_list = request.user.conversations.exclude(
            archived_by__username__exact=request.user.username).order_by('latest_message_date')
        c = Context({
            'request': request,
            'conversation_list': conversation_list,
            'thread_form': ParentThreadForm(),
        })
        return render_to_response(template, c, context_instance=RequestContext(request))
    else:
        return Http404('redirect maadi!!')


@login_required
@page_template('conversation/latest_message_main.html')
def conv_detail(request, pk, template='conversation/conversation_form.html', extra_context=None):
    if request.method == 'GET':
        object = get_object_or_404(Conversation, pk=int(pk))
        messages = Message.objects.filter(conversation=object).order_by('-date')
        object.read_by.add(request.user)
        form = MyMessageForm(user=request.user, conversation=object, initial_user=None, content_object=None)
        c = Context({
            'request': request,
            'object': object,
            'messages': messages,
            'form': form,
            'thread_form': ParentThreadForm(),
        })
        return render_to_response(template, c, context_instance=RequestContext(request))
    else:
        data = request.POST.copy()
        print data.get('text')
        object = get_object_or_404(Conversation, pk=int(pk))
        target = Message.objects.create(text=data.get('text'), user=request.user, conversation=object)
        object.archived_by.clear()
        object.read_by.clear()
        object.read_by.add(request.user)
        data = {'success': 'true', 'id': str(target.id)}
        return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def get_latest_message(request):
    if request.is_ajax():
        id = request.POST.get('pk', '')
        if id != '':
            lat_msg = Message.objects.get(pk=int(id))
            conv = lat_msg.conversation
            length = conv.messages.filter(user=request.user).count()
            messageq = conv.messages.filter(user=request.user)[length - 2:length]
            last_message_date = messageq[0].date
            new_messages = conv.messages.filter(date__gt=last_message_date)
            c = Context({
                'request': request,
                'messages': new_messages,
            })
            return render_to_response('conversation/latest_message.html', c, context_instance=RequestContext(request))
        else:
            raise Http404()
    else:
        return HttpResponseForbidden('no ajax call!!')

@login_required
def resend_activate_mail(request,username):
    if request.is_ajax:
        user = get_object_or_404(User,username__iexact=username)
        context ={'user': user,
                  'protocol': get_protocol(),
                  'activation_days': userena_settings.USERENA_ACTIVATION_DAYS,
                  'activation_key': user.userena_signup.activation_key,
                  'site': Site.objects.get_current()}

        subject = render_to_string('userena/emails/activation_email_subject.txt',
                                   context)
        subject = ''.join(subject.splitlines())
        message_html = None
        if (not userena_settings.USERENA_HTML_EMAIL or not message_html or
            userena_settings.USERENA_USE_PLAIN_TEMPLATE):
            message = render_to_string('userena/emails/activation_email_message.txt',
                                   context)
        else:
            message = None

        userid = user.id
        protocol = get_protocol()
        activation_days = userena_settings.USERENA_ACTIVATION_DAYS
        activation_key = user.userena_signup.activation_key
        site = 'houseofgrads.com'
        send_activate_mail.delay(subject,
                  message,
                  userid,protocol,activation_days,activation_key,site,
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email,])
        data= {'success':'true'}
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        return HttpResponseForbidden('no ajax my friend!!')

@login_required
def report(request,flag):
    if request.is_ajax:
        id = request.POST.get('id','')
        category = request.POST.get('category','')
        try:
            sanity_check = ReportedContent.objects.filter(primarykey__exact=int(id),contenttype__iexact=flag, reported_by=request.user).exists()
        except ReportedContent.DoesNotExist:
            sanity_check = False
        if sanity_check:
                data = {'success':'duplicate'}
                return HttpResponse(json.dumps(data),content_type='application/json')
        if flag == 'comment':
            content = get_object_or_404(Comment,id=int(id))
        elif flag == 'post':
            content = get_object_or_404(CreatePost,id=int(id))
        else:
            data = {'success':'false'}
            return HttpResponse(json.dumps(data),content_type='application/json')
        try:
            check = ReportedContent.objects.get(primarykey__exact=int(id),contenttype__iexact=flag)
        except ReportedContent.DoesNotExist:
            check = None
        if check is not None:
            check.reported_by.add(request.user)
            cat = check.category
            cat = category + cat
            check.category = cat
        else:
            c = ReportedContent(contenttype=flag,content=content,primarykey=int(id), category=category)
            c.save()
            c.reported_by.add(request.user)
        data= {'success':'true'}
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        return HttpResponseForbidden('no ajax no result!!')

@login_required
def get_stream_social(request, flag=''):
    if request.method == 'GET':
        c = Context({
            'request': request,
            'flag': flag,
                })
        return render_to_response('registration/social_registration.html',c,context_instance=RequestContext(request))
    else:
        if request.is_ajax:
            profile = MyProfile.objects.get(user = request.user)
            data = request.POST.copy()
            profile.gate_stream = data.get('stream')
            profile.save()
            data = {'success':'true'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponseForbidden('no ajax no result')

@login_required
def feed_build_social(request):
    if request.is_ajax:
        stream = request.GET.get('stream')
        u = User.objects.get(username= 'AnonymousUser')
        top_users = MyProfile.objects.exclude(user=request.user).filter(gate_stream__iexact=stream)
        thread_list = ParentThread.objects.exclude(name='myWall').filter(stream__name__iexact=stream)
        top_list = [t.no_followers() for t in top_users]
        top_threads = [t.no_followers() for t in thread_list]
        a = sorted(top_list, key=itemgetter(1), reverse=True)[:10]
        b = sorted(top_threads, key=itemgetter(1), reverse=True)[:5]
        c = Context({
            'request': request,
            'top_users': a,
            'top_threads': b,
        })
        return render_to_response('registration/feed_build_social.html',c,context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('not allowed')