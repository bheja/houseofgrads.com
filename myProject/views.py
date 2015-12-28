import json
import re
from django.core.signing import Signer, TimestampSigner
from actstream import action
from userena.contrib.umessages.forms import ComposeForm
from userena.utils import get_user_model
from actstream.actions import follow,unfollow
from actstream import models as ActStream
from actstream.models import following, followers
from posts.models import CreatePost, ParentThread, PreviewUrl, PostImage
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from accounts.forms import LoginForm
from django.contrib.auth.decorators import login_required
from posts.forms import PostForm
from django.contrib.auth import login, authenticate, logout
from django.template import Context, RequestContext
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, Http404
from userena.forms import SignupFormOnlyEmail
from posts.forms import ParentThreadForm
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.utils.highlighting import Highlighter
from django.utils.html import strip_tags
from endless_pagination.decorators import page_template
from notifications import notify
from guardian.shortcuts import assign, assign_perm
from posts.tasks import send_notice_mail
from blogs.models import Blog
from operator import itemgetter
from accounts.forms import FeedBackForm
from accounts.models import MyProfile
from django.utils.encoding import smart_str

@page_template('base/latest_threads_paginate.html')
def ajax_login(request, template='base/base.html', extra_context=None):
    if request.method == 'POST':
        if request.is_ajax():
            data = request.POST.copy()
            check = data.get('username','')
            rex = re.compile(r'[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}',re.I|re.M)
            match = rex.findall(check)
            if match !=[]:
                try:
                    user = User.objects.get(email__iexact=match[0])
                except User.DoesNotExist:
                    user = None
                if user is not None:
                    data['username'] = user.username
            
            login_form = LoginForm(data)
            if login_form.is_valid():
                username=data.get('username')
                password=data.get('password')
                user = authenticate(username=username, password=password)                                                                       
                if user is not None:
                    if data.get('remember') == 'true':
                        request.session.set_expiry(1296000)
                    login(request, user)
                    data = {'success':True}
                else:
                    data = {'success': False, 'error': 'Wrong username and/or password'}
                    
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponseForbidden('wrong!!') 
                
    else:
        search_form = ModelSearchForm()
        login_form = LoginForm()
        signup_form = SignupFormOnlyEmail()
        blogs = Blog.objects.filter(editor_pick = True)[:5]
        threads = ParentThread.objects.exclude(name='myWall')
        thread_list = [t.no_followers() for t in threads]
        thread_list = sorted(thread_list,key=itemgetter(1),reverse=True)
        c = Context({
        'search_form': search_form,
        'login_form': login_form,
        'signup_form': signup_form,
        'threads':thread_list,
        'blogs':blogs,
        'request':request,                                                                                                                  
        })
        if extra_context is not None:
            c.update(extra_context)
        return render_to_response(template, c, context_instance=RequestContext(request))

def signup(request):
    if request.method == 'POST':
        if request.is_ajax:
            posted_data = request.POST.copy()
            flag = posted_data.get('flag','')
            email = posted_data.get('email','')
            password = posted_data.get('password1','')
            if flag != '':
                del posted_data['flag']
            signup_form = SignupFormOnlyEmail(posted_data)
            if signup_form.is_valid():
                p = signup_form.save()
                username = str(p.username)
                user_login = authenticate(username=username,password=password)
                if user_login is not None:
                    login(request,user_login)
                user =  get_object_or_404(User, username__iexact=username)
                follow(user,user)
                signedun = TimestampSigner().sign(username)
                assign('change_profile', p, p.get_profile())
                assign('delete_profile', p, p.get_profile())
                assign('change_user', p, p)
                assign('delete_user', p, p)
                data = {'success':True, 'signedun':signedun,'email':email,'flag':flag}
                return HttpResponse(json.dumps(data), content_type = 'application/json')
            else:
                for f in signup_form:
                    for e in f.errors:
                        errors = str(e)
                data = {'success':False, "error": errors }
                return HttpResponse(json.dumps(data), content_type = 'application/json')

    else:
        search_form = ModelSearchForm()
        signup_form = SignupFormOnlyEmail()
        login_form = LoginForm()
        c = Context({                                                                                                                                                                                                                        
        'signup_form': signup_form,
        'login_form': login_form,
        'request':request,})
        return render_to_response('base/base.html', c, context_instance=RequestContext(request))


def signup_complete(request, slug, email):
    username = TimestampSigner().unsign(slug, max_age=1200000000000)
    if username:
        if email==request.user.email:
            return render(request,'userena/signup_complete.html',{'email':email,'username':username})
        else:
            return HttpResponseForbidden('Permission denied')
    else:
        return HttpResponseForbidden('expired')

def signup_complete_alternate(request, slug, email, flag):
    username = TimestampSigner().unsign(slug, max_age=1200000000000)
    if username:
        if email==request.user.email:
            return render(request,'userena/signup_complete.html',{'email':email,'username':username,'flag':flag})
        else:
            return HttpResponseForbidden('Permission denied')
    else:
        return HttpResponseForbidden('expired')

def profile_fill(request):
    if request.method == 'POST':
        if request.is_ajax(): 
            data = request.POST.copy()
            email = data.get('email','')
            username = data.get('username','')
            firstname = data.get('firstname','')
            lastname = data.get('lastname','')
            stream = data.get('gate_stream','')
            mugshot = data.get('mugshot','')
            try:
                inst = User.objects.get(email__iexact=email)
                profile = MyProfile.objects.get(user = request.user)
            except User.DoesNotExist:
                inst = None
            if inst is not None:
                inst.username = username
                inst.first_name = firstname
                inst.last_name = lastname
                profile.gate_stream = stream
                if mugshot !='':
                    profile.mugshot = mugshot
                inst.save()
                profile.save()
                signedun = TimestampSigner().sign(username)
                data = {'success':'true','slug':signedun}
                return HttpResponse(json.dumps(data), content_type = 'application/json')
            else:
                data = {'success':'false'}
                return HttpResponse(json.dumps(data), content_type = 'application/json')
        else:
            return HttpResponseForbidden('wrong mate')
    else:
        return HttpResponseForbidden('really mate! really')
        
  
@login_required
def logout_view_custom(request):
    logout(request)
    signup_form = SignupFormOnlyEmail()
    login_form = LoginForm()
    search_form = ModelSearchForm()
    blogs = Blog.objects.filter(editor_pick = True)[:5]
    threads = ParentThread.objects.exclude(name='myWall')
    thread_list = [t.no_followers() for t in threads]
    thread_list = sorted(thread_list,key=itemgetter(1),reverse=True)
    c = Context({
        'search_form':search_form,
        'signup_form': signup_form,
        'login_form': login_form,
        'blogs':blogs,
        'threads':thread_list,
        'page_template': 'base/latest_threads_paginate.html',
        'request':request,})
    return render_to_response('base/base.html', c, context_instance=RequestContext(request))


@login_required
@page_template('feed/feed_paginate.html')
def home(request,template='landing/landing2.html',extra_context = None):
    if request.method == 'POST':
        if request.is_ajax:
            data = request.POST.copy()
            tagged_users = ''
            preview = data.get('preview','')
            img_url = data.get('img_url','')
            if img_url != '':
                del data['img_url']
            del data['preview']
            thread_id = int(data.get('thread',''))
            data["thread"]=ParentThread.objects.get(id=thread_id).id
            TargetThread = ParentThread.objects.get(id=thread_id)
            content_post = data.get('content','')
            rex = re.compile(r'<a.*?>(.*?)</a>',re.I|re.M)
            match = rex.findall(content_post)
            form = PostForm(data)
            if form.is_valid():
                p = form.save()
                assign_perm('posts.delete_createpost',request.user)
                postid = str(p.id)
                if match:
                    for m in match:
                        try:
                            userobj = User.objects.get(username__iexact=m)
                        except User.DoesNotExist:
                            userobj = None
                        if userobj !=None:
                            if request.user != userobj:
                                notify.send(request.user, recipient=userobj, verb=u'tagged you in a post', action_object=p)
                                text = 'Hi'+str(userobj.username)+',/n'+str(request.user.username)+' has tagged you in a post. Please go to following link to see the post./n'+ str(p.get_absolute_url)+'/n/nThanks and best regards,/nHouseofGrads.com'
                                send_notice_mail.delay(contenttext=postid,text=text,template="notification/email/tagged.html",targetuser=str(userobj.id),fromuser=str(request.user.id),verb='tagged you in a post')
                if preview != '':
                    inst = PreviewUrl(preview=preview, post=p)
                    inst.save()
                if img_url !='':
                    imgarr = img_url.lstrip().split(' ')
                    for img in imgarr:
                        instance = PostImage(img_url = img, post=p)
                        instance.save()
                data2 = {'success':True }
                action.send(request.user, verb="posted on", action_object= p,target= TargetThread)
            else:
                data2 = {'success':False, 'errmsg':"Posting failed, sorry"}
        return HttpResponse(json.dumps(data2), content_type='application/json')
    else:
        action_list = ActStream.user_stream(request.user).exclude(verb='commented on').exclude(verb = 'started following')
        post_form = PostForm()
        thread_form = ParentThreadForm()
        message_form = ComposeForm()
        login_form = LoginForm()
        c = Context({                                                                                                                                                                                                                        
        'post_form': post_form,
        'thread_form':thread_form,
        'message_form':message_form,
        'login_form':login_form,
        'request':request,
        'action_list':action_list,
        })
        return render_to_response(template, c, context_instance=RequestContext(request))

@login_required
@page_template('notification/notice.html')
def notification_fetch(request, template='notification/notice.html', extra_context=None):
    if request.method == 'GET':
        if request.is_ajax:
            notification_list = request.user.notifications.all()
            c = Context({                                                                                                                                                                                                                        
            'request':request,
            'notification_list': notification_list,})
            return render_to_response(template, c, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('home/')
    else:
        return HttpResponseForbidden('Access Not Allowed')

@login_required
def notification_read(request):
    if request.is_ajax:
        request.user.notifications.all().mark_all_as_read()
        data = {'success':'true'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponseForbidden('Access Not Allowed')

@login_required
@page_template('feed/feed_paginate.html')
def feed(request, template='feed/feed2.html', extra_context=None):
    if request.method == 'GET':
        if request.is_ajax:
            action_list = ActStream.user_stream(request.user).exclude(verb='commented on').exclude(verb = 'started following')
            following_list = following(request.user)
            c = Context({                                                                                                                                                                                                                        
            'request':request,
            'action_list':action_list,})
            return render_to_response(template, c, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('home/')
    else:
        return HttpResponseForbidden('Access Not Allowed')

@login_required
def latest_post(request):
    if request.is_ajax():
        latest = ActStream.user_stream(request.user).exclude(verb='commented on').exclude(verb = 'started following')[:1]
        c = Context({                                                                                                                                                                                                                        
            'request':request,
            'action':latest,})
        return render_to_response('posts/latest_post.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('Access Not Allowed')
        
@login_required
def latest_thread_post(request):
    if request.is_ajax():
        tid = request.GET.get('id','')
        tid = int(tid)
        latest = CreatePost.objects.filter(thread__id__iexact=tid).order_by('-date')[:1]

        c = Context({                                                                                                                                                                                                                        
            'request':request,
            'latest':latest,})
        return render_to_response('posts/latest_post_thread.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('Access Not Allowed')


@login_required
def taguser(request):
    if request.is_ajax():
        taglist = request.GET.get('tagexist','').split()
        sqs1 = SearchQuerySet().autocomplete(content_auto=request.GET.get('content', '')).models(User)
        result = sqs1
        if taglist != []:
            sqs2 = sqs1.exclude(content__in = taglist)[:10]
            result = sqs2
        c = Context({
            'request': request,
            'results': result,
            })
        return render_to_response('search/user_autocomplete.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('No mate, not right')

def autocomplete_search(request):
    if request.is_ajax():
        sqs1 = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', '')).models(User)[:10]
        sqs2 = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', '')).models(ParentThread)[:10]
        query = request.GET.get('q', '')
        c = Context({
            'request': request,
            'results_users': sqs1,
            'query':query,
            'results_threads': sqs2,
            })
        return render_to_response('search/autocomplete.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('No mate, not right')

def autocomplete_recipient(request):
    if request.is_ajax():
        sqs1 = SearchQuerySet().autocomplete(content_auto=request.GET.get('query', '')).models(User)[:10]
        list_user = [u.object.username for u in sqs1]
        data = json.dumps(list_user)
        return HttpResponse(data,content_type='application/json')
    else:
        return HttpResponseForbidden('No mate, not right')

@page_template('search/search_paginate.html')
def search_view(request, template='search/search.html', extra_context=None):
    if request.method == 'GET':
        sqs = SearchQuerySet().filter(content=request.GET.get('q', '')).exclude(thread="myWall")
        query = request.GET.get('q', '')
        thread_form = ParentThreadForm()
        c = Context({
            'request': request,
            'results': sqs,
            'query':query,
            'login_form':LoginForm(),
            'thread_form':thread_form,
            })
        return render_to_response(template, c, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('no post in search')

@login_required
def thread_search(request):
    if request.method == 'GET':
        if request.is_ajax:
            login_form = LoginForm()
            thread_form = ParentThreadForm()
            query = request.GET.get('q','')
            if query != '':
                sqs = SearchQuerySet().filter(content=query).models(ParentThread)[:6]
                if not sqs:
                    count = '0'
                else:
                    count = len(sqs)
                c = Context({
                    'request': request,
                    'results': sqs,
                    'query':query,
                    'count':count,
                    'login_form':login_form,
                    'thread_form':thread_form,
                        })
                return render_to_response('threads/resultSearchModal.html', c, context_instance=RequestContext(request))
            else:
                data = {'success':'false'}
                return HttpResponse(json.dumps(data),content_type='application/json')

    
class MyHighlighter(Highlighter):
    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        return self.render_html(highlight_locations, start_offset, end_offset)

    def find_window(self, highlight_locations):
        best_start = 0
        best_end = self.max_length

        # First, make sure we have words.
        if not len(highlight_locations):
            return (best_start, best_end)

        words_found = []

        # Next, make sure we found any words at all.
        for word, offset_list in highlight_locations.items():
            if len(offset_list):
                # Add all of the locations to the list.
                words_found.extend(offset_list)
                if words_found[0] > 10:
                    words_found[0] = words_found[0]-10 

        if not len(words_found):
            return (best_start, best_end)

        if len(words_found) == 1:
            return (words_found[0], words_found[0] + self.max_length)

        # Sort the list so it's in ascending order.
        words_found = sorted(words_found)

        # We now have a denormalized list of all positions were a word was
        # found. We'll iterate through and find the densest window we can by
        # counting the number of found offsets (-1 to fit in the window).
        highest_density = 0

        if words_found[:-1][0] > self.max_length:
            best_start = words_found[:-1][0]
            best_end = best_start + self.max_length

        for count, start in enumerate(words_found[:-1]):
            current_density = 1

            for end in words_found[count + 1:]:
                if end - start < self.max_length:
                    current_density += 1
                else:
                    current_density = 0

                # Only replace if we have a bigger (not equal density) so we
                # give deference to windows earlier in the document.
                if current_density > highest_density:
                    best_start = start
                    best_end = start + self.max_length
                    highest_density = current_density

        return (best_start, best_end)

def feedback(request, flag):
    if request.method == 'POST':
        if flag == 'feedback':
            form = FeedBackForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                c =({'request':request,'login_form':LoginForm(),'success':'true','flag':flag,})
                return render_to_response('base/contactus.html',c,context_instance=RequestContext(request))
            else:
                err = form.errors
                c =({'request':request,'login_form':LoginForm(),'error':err,'flag':flag,})
                return render_to_response('base/contactus.html',c,context_instance=RequestContext(request))
        else:
            return Http404()
    elif request.method == 'GET':
        c =({'request':request,'login_form':LoginForm(),'flag':flag})
        return render_to_response('base/contactus.html',c,context_instance=RequestContext(request))

@login_required()
def download_guides(request):
    if request.method == 'GET':
        stream = request.GET.get('stream')
        if stream == 'EC':
            response = HttpResponse(content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('hog_EC_helpbook.pdf')
            response['X-Sendfile'] = smart_str('/houseofgrads/lighttpd/hog/hogstatic/media/files/hog_EC_helpbook.pdf')
            return response
        else:
            return Http404()
    else:
        return Http404()

def authentication_page(request):
    if request.method == 'GET':
        signup_form = SignupFormOnlyEmail()
        c = ({'request':request,'signup_form':signup_form,})
        return render_to_response('registration/registration_page.html',c,context_instance=RequestContext(request))
