import json
import os
from django.shortcuts import render_to_response, get_object_or_404, redirect
from .models import Blog, BlogImage, BlogTags
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, Http404
from .forms import BlogForm
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.easythumbnails import EasyThumbnailUploadBackend
from django.views.generic import DetailView
import datetime
from guardian.decorators import permission_required
from guardian.shortcuts import assign_perm
from endless_pagination.decorators import page_template
from guardian.shortcuts import assign_perm
from posts.forms import ParentThreadForm
from accounts.forms import LoginForm

blog_cover_upload = AjaxFileUploader(backend=EasyThumbnailUploadBackend, DIMENSIONS=(800,000), QUALITY=75, DETAIL = True, SHARPEN = False, UPLOAD_DIR='blogs', KEEP_ORIGINAL=False)

@login_required
def create_blog(request, flag=''):
    if request.method == 'POST':
        data = request.POST.copy()
        user = data.get('author')
        user = get_object_or_404(User,username__iexact=user)
        data['author'] = user.id
        tag = data['tag']
        tag = get_object_or_404(BlogTags,tag__iexact=tag)
        data['tag'] = tag.id
        if data.get('img_url') != '':
            images = data.get('img_url')
            del data['img_url']
        else:
            images = ''
            del data['img_url']
        if flag == 'draft':
            data['published'] = False
        elif flag == 'publish':
            data['published'] = True
        else:
            data['published'] = False
        blog_form = BlogForm(data)
        if blog_form.is_valid():
            b = blog_form.save()
            assign_perm('blogs.change_blog',request.user)
            assign_perm('blogs.delete_blog',request.user)
            if images != '':
                p = BlogImage(url=images,blog=b)
                p.save()
            data = {'success':'true','id':b.id,'slug':b.slug}
        else:
            data = {'success':'false','error':str(blog_form.errors)}
        return HttpResponse(json.dumps(data),content_type='application/json')
    else:
        blog_form = BlogForm()
        thread_form = ParentThreadForm()
        c = Context({'request':request,'blog_form':blog_form,'thread_form':thread_form,})
        return render_to_response('blogs/createblog.html',c,context_instance=RequestContext(request))

@login_required
def delete_uploaded_cover(request):
    if request.method == 'POST':
        if request.is_ajax():
                filename = request.POST.get('filename','')
                if filename != '':
                    try:
                        obj = BlogImage.objects.get(url__iexact=filename)
                        obj.delete()
                    except BlogImage.DoesNotExist:
                        pass
                    os.unlink('/Users/vishalsingh/django/myProject'+filename)
                    data = {'success':'true'}
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data = {"success": "false","msg":"no file received"}
                    return HttpResponse(json.dumps(data), content_type="application/json")

        else:
                return HttpResponseForbidden('no ajax! no result!')

@login_required
def blogs_draft(request,flag):
    if request.method == 'GET':
        author = int(request.user.id)
        blogs = Blog.objects.filter(author_id = author).order_by('-date')
        c = Context({'request':request,'blogs':blogs,'flag':str(flag),'thread_form':ParentThreadForm(),})
        return render_to_response('blogs/draft_all.html',c,context_instance=RequestContext(request))
    else:
        return redirect('/create/blog/draft/')

def blog_details(request,pk,slug):
    if request.method == 'GET':
        object = Blog.objects.get(pk = int(pk))
        if str(object.slug) != slug:
            raise Http404()
        if not object.published:
            raise Http404()
        thread_form = ParentThreadForm()
        login_form = LoginForm()
        c = Context({'request':request,'object':object,'thread_form':thread_form,'login_form':login_form,})
        return render_to_response('blogs/blog_detail.html',c,context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden()


@login_required
@permission_required('blogs.change_blog',login_url='/')
def blogs_draft_edit(request, pk, flag=''):
    if request.method == 'GET':
        if pk !='':
            obj = Blog.objects.get(pk = int(pk))
            if obj.published:
                return redirect(obj.get_absolute_url())
            else:
                thread_form  = ParentThreadForm()
                c = Context({'request':request,'object':obj,'thread_form':thread_form,})
                return render_to_response('blogs/draft_edit.html',c,context_instance=RequestContext(request))
        else:
            return HttpResponseForbidden('not allowed!')
    else:
        obj = Blog.objects.get(pk=int(pk))
        data = request.POST.copy()
        user = data.get('author')
        user = get_object_or_404(User,username__iexact=user)
        data['author'] = user.id
        tag = data['tag']
        tag = get_object_or_404(BlogTags,tag__iexact=tag)
        data['tag'] = tag.id
        print flag
        if data.get('img_url') != '':
            images = data.get('img_url')
            del data['img_url']
        else:
            images = ''
            del data['img_url']
        if flag == 'draft':
            data['published'] = False
        elif flag == 'publish':
            data['published'] = True
        else:
            data['published'] = False
        if images != '':
                BlogImage.objects.filter(blog=obj).delete()
                p = BlogImage(url=images,blog=obj)
                p.save()
        obj.title = data['title']
        obj.published = data['published']
        obj.blog_content = data['blog_content']
        obj.tag = tag
        obj.date = datetime.datetime.now()
        obj.save()
        data = {'success':'true','id':obj.id,'slug':obj.slug}
        return HttpResponse(json.dumps(data),content_type='application/json')

@page_template(template='blogs/blog_editor_paginate.html')
@page_template(template='blogs/blog_latest_paginate.html',key='blog_latest_paginate')
def blog_topics(request,flag, template = 'blogs/topic_list.html', extra_context = None):
    if request.method == 'GET':
        topics = BlogTags.objects.all()
        thread_form = ParentThreadForm()
        blogs_picks = Blog.objects.filter(published=True).order_by('-date') #add editor picking logic here
        blogs_latest = Blog.objects.filter(published=True).order_by('-date')
        c = Context({'blogs_picks':blogs_picks,'blogs_latest':blogs_latest,'request':request,'flag':flag,'topics':topics,'thread_form':thread_form,})
        return render_to_response(template,c,context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('wrong calls fetch nothin!!')

@page_template(template='blogs/by_topics_paginate.html')
def blogs_by_topics(request, pk, template='blogs/by_topics.html',extra_context=None):
    if request.method == 'GET':
        tag = BlogTags.objects.get(pk=int(pk))
        blog_list = Blog.objects.filter(tag=tag).filter(published=True)
        thread_form = ParentThreadForm()
        c = Context({'blogs':blog_list,'request':request,'topic':tag,'thread_form':thread_form,})

        return render_to_response(template,c,context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('wrong calls fetch nothin!!')

@login_required
@permission_required('blogs.change_blog')
def delete_blog(request):
    if request.method == 'POST':
        pk = request.POST.get('id','')
        if pk != '':
            blog = get_object_or_404(Blog,pk=int(pk))
            blog.delete()
            data = {'success':'true'}
            return HttpResponse(json.dumps(data),content_type='application/json')
        else:
            return HttpResponseForbidden('no man, cant do!')
    else:
        return HttpResponseForbidden('no man, cant do!')