from guardian.shortcuts import assign_perm
from actstream import action
from django.contrib.auth.models import User
from actstream.models import following, followers
from actstream.actions import follow, unfollow
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from posts.models import ParentThread, CreatePost
from posts.forms import PostForm
from django.views.generic import DetailView, ListView
from threads.models import StudyStream
from endless_pagination.decorators import page_template
from accounts.forms import LoginForm
from accounts.models import MyProfile
from posts.forms import ParentThreadForm
import json


@login_required
def create_thread(request):
    if request.method == 'POST':
        if request.is_ajax:
            data = request.POST.copy()
            stream = data.get("stream", "")
            stream_obj = StudyStream.objects.get(name=stream)
            data["stream"] = stream_obj.name
            data['author'] = request.user.id
            thread_form = ParentThreadForm(data)
            if thread_form.is_valid:
                t = thread_form.save()
                follow(request.user, t)
                action.send(request.user, verb="created a thread", action_object=t)
                datajson = {'success': 'true', 'tid': t.slug}
                return HttpResponse(json.dumps(datajson), content_type='application/json')
            else:
                err = str(thread_form.errors)
                datajson = {'success': 'false', 'error': err}
                return HttpResponse(json.dumps(datajson), content_type='application/json')
        else:
            return HttpResponseForbidden('no ajax')
    else:
        return HttpResponseForbidden('only posts my friend')

@page_template('posts/post_list.html')
def thread_detail(request,slug,template='posts/parentthread_detail.html',extra_context = None):
    if request.method == 'GET':
        object = get_object_or_404(ParentThread.objects.select_related(),slug=slug)
        follower = followers(object)
        no_followers = len(followers(object))
        post_form = PostForm()
        login_form = LoginForm()
        thread_form = ParentThreadForm()
        try:
            post_list = CreatePost.objects.filter(thread=object.pk).order_by('-date')
        except CreatePost.DoesNotExist:
            post_list = None
        c = Context({
                'request': request,
                'post_list': post_list,
                'object':object,
                'login_form':login_form,
                'post_form':post_form,
                'thread_form':thread_form,
                'followers':follower,
                'no_followers':no_followers,
                })
        return render_to_response(template, c, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('only gets my friend')


@page_template('threads/following_threads.html')
def following_threads(request, template='threads/following_threads_base.html', extra_context=None):
    if request.method == 'GET':
        user = request.user
        thread_list = following(user, ParentThread)
        no_threads = len(thread_list)
        flag = False
        if thread_list == []:
            flag = True
        c = Context({
            'request': request,
            'thread_list': thread_list, 'flag': flag,
            'thread_form': ParentThreadForm(),
            'login_form': LoginForm(),
            'no_threads': no_threads,
        })
        return render_to_response(template, c, context_instance=RequestContext(request))


@page_template('threads/discussion_list.html')
def thread_list(request, key, template='threads/discussions.html', extra_context=None):
    stream = key
    if stream == 'enggschools':
        stream = 'ENG'
    elif stream == 'gatenpsu':
        stream = 'PSU'
    elif stream == 'gatecs':
        stream = 'CS'
    elif stream == 'gateec':
        stream = 'EC'
    elif stream == 'gateee':
        stream = 'EE'
    elif stream == 'gatemech':
        stream = 'ME'
    elif stream == 'gatechem':
        stream = 'CH'
    elif stream == 'gatecivil':
        stream = 'CV'
    elif stream == 'jobsncareer':
        stream = 'JNC'
    elif stream == 'mystream':
        stream = request.user.my_profile.gate_stream
    object_list = ParentThread.objects.filter(stream=StudyStream.objects.get(name=stream))
    no_users = MyProfile.objects.filter(gate_stream__iexact=stream).count()
    no_posts = CreatePost.objects.filter(thread__stream=stream).count()
    c = Context({
        'request': request,
        'object_list': object_list,
        'name': stream,
        'no_users': no_users,
        'login_form': LoginForm(),
        'thread_form': ParentThreadForm(),
        'no_posts': no_posts,
    })
    return render_to_response(template, c, context_instance=RequestContext(request))
