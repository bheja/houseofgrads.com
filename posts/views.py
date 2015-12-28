import os
import json
import re
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from posts.models import CreatePost, ParentThread, PreviewUrl
from actstream import action
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from notifications import notify
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from posts.forms import PostForm
from django.contrib.contenttypes.models import ContentType
from django.template import Context, RequestContext
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.easythumbnails import EasyThumbnailUploadBackend
from phileo.models import Like
from phileo.signals import object_liked, object_unliked
from phileo.utils import widget_context
from django.template.loader import render_to_string
from accounts.models import MyProfile
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required_or_403
from actstream.models import Action
from posts.forms import ParentThreadForm
from accounts.forms import LoginForm

post_image_upload = AjaxFileUploader(backend=EasyThumbnailUploadBackend, DIMENSIONS=(800,000), QUALITY=95, DETAIL = True, SHARPEN = False, UPLOAD_DIR='uploads', KEEP_ORIGINAL=False)
mugshot_uploader =  AjaxFileUploader(backend=EasyThumbnailUploadBackend, DIMENSIONS=(256,000), QUALITY=95, DETAIL = True, SHARPEN = False, UPLOAD_DIR='mugshots', KEEP_ORIGINAL=False)

class PostDetailView(DetailView):
    def get_object(self):
		object = get_object_or_404(CreatePost.objects.select_related(), pk=self.kwargs.get('pk',None))
		return object
    def get_context_data(self, **kwargs):
        thread_form = ParentThreadForm()
        login_form = LoginForm()
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['thread_form'] = thread_form
        context['login_form'] = login_form
        return context


@login_required
@require_POST
def like_handler(request, content_type_id, object_id):
        content_type = get_object_or_404(ContentType, pk=content_type_id)
        obj = content_type.get_object_for_this_type(pk=object_id)
        if not request.user.has_perm("phileo.can_like", obj):
                return HttpResponseForbidden()
        like, created = Like.objects.get_or_create(
                sender=request.user,
                receiver_content_type=content_type,
                receiver_object_id=object_id
                    )
        if created:
                object_liked.send(sender=Like, like=like, request=request)
                if hasattr(obj, 'author'):
                        if request.user != obj.author:
                                notify.send(request.user, recipient=obj.author, verb=u'liked your post', action_object=obj)
                elif hasattr(obj, 'user'):
                        if request.user != obj.user:
                                notify.send(request.user, recipient=obj.user, verb=u'liked your comment', action_object=obj)
        else:
                like.delete()
                object_unliked.send(
                    sender=Like,
                    object=obj,
                    request=request
                        )
    
        if request.is_ajax():
                html_ctx = widget_context(request.user, obj)
                template = "phileo/_widget.html"
                if request.GET.get("t") == "b":
                        template = "phileo/_widget_brief.html"
                data = {
                        "html": render_to_string(
                                template,
                                html_ctx,
                                context_instance=RequestContext(request)
                                    ),
                        "likes_count": html_ctx["like_count"],
                        "liked": html_ctx["liked"],
                        }
                return HttpResponse(json.dumps(data), content_type="application/json")
    
        return redirect(request.META["HTTP_REFERER"])

@login_required
def like_list(request, object_id):
        if request.method == "GET":
                if request.is_ajax:
                        post_id = int(object_id)
                        obj = get_object_or_404(CreatePost, pk=post_id)
                        c = Context({
                            'obj':obj,
                            'request':request,})
                        return render_to_response('phileo/like_list_main.html', c, context_instance=RequestContext(request))
                else:
                    return HttpResponseRedirect('home/')
        else:
               return Http404()


@login_required
def ajaxpostrefresh(request, pk):
        if request.method == "GET":
                if request.is_ajax:
                        commid = int(pk)
                        obj = get_object_or_404(Comment, pk=commid)
                        c = Context({
                            'object':obj,
                            'request':request,})
                        return render_to_response('posts/post_ajax_refresh.html', c, context_instance=RequestContext(request))
                else:
                    return HttpResponseRedirect('home/')
        else:
              return HttpResponseForbidden('no Post my friend')
@login_required
def share(request):
        if request.is_ajax():
                data = request.POST.copy()
                preview = data.get('preview','')
                del data['preview']
                data["thread"]=ParentThread.objects.get(id=1).id
                data["author"] = request.user.id
                TargetThread = ParentThread.objects.get(id=1)
                content_post = data.get('content','')
                rex = re.compile(r'<a.*?>(.*?)</a>',re.I|re.M)
                match = rex.findall(content_post)
                form = PostForm(data)
                if form.is_valid():
                        p = form.save()
                        assign_perm('posts.delete_createpost',request.user)
                        if match:
                            for m in match:
                                try:
                                    userobj = User.objects.get(username__iexact=m)
                                except User.DoesNotExist:
                                    userobj = None
                                if userobj !=None:
                                    if request.user != userobj:
                                        notify.send(request.user, recipient=userobj, verb=u'tagged you in a post', action_object=p)  
                        if preview != '':
                            inst = PreviewUrl(preview=preview, post=p)
                            inst.save()
                        data2 = {'success':True }
                        action.send(request.user, verb="shared a post", action_object= p,target= TargetThread)
                else:
                        data2 = {'success':False, 'errmsg':"Posting failed, sorry"}
                return HttpResponse(json.dumps(data2), content_type='application/json')
        else:
                return HttpResponseForbidden('no Post my friend')

@login_required
def delete_uploaded(request):
        if request.is_ajax():
                filename = request.POST.get('filename','')
                if filename != '':
                        os.unlink('/Users/vishalsingh/django/myProject/'+filename)
                        data = {'success':'true'}
                        return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                        data = {"success": "false","msg":"no file received"}
                        return HttpResponse(json.dumps(data), content_type="application/json")   

        else:
                return HttpResponseForbidden('no ajax! no result!')

@login_required
def delete_uploaded_mugshot(request):
        if request.is_ajax():
                filename = request.POST.get('filename','')
                if filename != '':
                        os.unlink('/Users/vishalsingh/django/myProject/'+filename)
                        data = {'success':'true'}
                        return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                        data = {"success": "false","msg":"no file received"}
                        return HttpResponse(json.dumps(data), content_type="application/json")   

        else:
                return HttpResponseForbidden('no ajax! no result!')

def mugshot_avatar(request):
        if request.is_ajax():
                url = request.POST.get('url','')
                if url != '':
                        try:
                                inst = MyProfile.objects.get(user=request.user)
                        except MyProfile.DoesNotExist:
                                inst = None
                        if inst is not None:
                                inst.mugshot = url
                                inst.save()
                                data = {'success':'true'}
                                return HttpResponse(json.dumps(data), content_type="application/json")
                        else:
                                data = {'success':'false'}
                                return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                        data = {'success':'false'}
                        return HttpResponse(json.dumps(data), content_type="application/json")
        else:
                return HttpResponseForbidden('No ajax!')

@login_required
@permission_required_or_403('posts.delete_createpost')
def delete_post(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        post = get_object_or_404(CreatePost, pk=int(pk))
        content_type = ContentType.objects.get_for_model(post)
        action = Action.objects.filter(action_object_content_type = content_type).filter(action_object_object_id = pk)
        if request.user == post.author:
            data = {'success':'true','post_pk':post.id}
            post.delete()
            action.delete()
            return HttpResponse(json.dumps(data),content_type='application/json')
        else:
            return HttpResponseForbidden('wrong man, very wrong!!')
    else:
        return HttpResponseForbidden('wrong man, very wrong!!')

@login_required
def delete_comment(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        comment = get_object_or_404(Comment, pk=int(pk))
        if request.user == comment.content_object.author or request.user == comment.user:
            data = {'success':'true','post_pk':comment.id}
            comment.delete()
            return HttpResponse(json.dumps(data),content_type='application/json')
        else:
            return HttpResponseForbidden('wrong man, very wrong!!')
    else:
         return HttpResponseForbidden('wrong man, very wrong!!')
