from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from myProject import settings
from myProject import views
from threads import views as thread_views
from accounts import views as account_views
from posts import ajax_comment_post
from posts import views as post_views
from userena import views as userena_views
from django.views.generic import TemplateView
from blogs import views as blog_views, ajax_comment_blog
from .sitemaps import BlogSiteMap, PostSiteMap, ThreadSiteMap

admin.autodiscover()

sitemaps = {
    'blog': BlogSiteMap(),
    'post':PostSiteMap(),
    'thread': ThreadSiteMap()
}

urlpatterns = patterns('',
                       url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                       url(r'^gogo/momo/jojo/', include(admin.site.urls)),
                       url(r'^$',views.ajax_login),
                       url(r"^messages/compose/", account_views.message_handler),
                       url(r'^home/$',views.home),
                       url(r'^home/new/$',TemplateView.as_view(template_name='landing/landing_new.html')),
                       url(r'^postonthread/$',views.home),
                       url(r'^register/social/$',account_views.get_stream_social),
                       url(r'^register/social/(?P<flag>\w+)/$',account_views.get_stream_social),
                       url(r'^fb/registration/feed/$', account_views.feed_build_social),
                       url(r'^share/$',post_views.share),
                       url(r'^feed/$',views.feed),
                       url(r'^threads/search/$',views.thread_search),
                       url(r'^comments/$', ajax_comment_post.post_comment),
                       url(r'^comments/blogs/$', ajax_comment_blog.post_comment),
                       url(r'^comments/list/(\d+)/$',ajax_comment_post.comment_list),
                       url(r'^tinymce/', include('tinymce.urls')),
                       url(r'^follow/followobj/$',account_views.follow_obj),
                       url(r'^notification/$',views.notification_fetch),
                       url(r'^notification/notification/read/$',views.notification_read),
                       url(r'^delete/post/$',post_views.delete_post),
                       url(r'^delete/comment/$',post_views.delete_comment),
                       url(r'^delete/blog/$',blog_views.delete_blog),
                       url(r'^follow/unfollowobj/$',account_views.unfollow_obj),
                       url(r'^signout/$',views.logout_view_custom),
                       url(r'^createthread/$',thread_views.create_thread),
                       url(r'^postdetail/(?P<pk>\d+)/$',post_views.PostDetailView.as_view(), name="post_details"),
                       url(r'^threads/(?P<slug>[\w-]+)/$',thread_views.thread_detail, name="thread_page"),
                       url(r'^following/threads/$',thread_views.following_threads),
                       url(r'^register/$',views.signup),
                       url(r'^activity/', include('actstream.urls')),
                       url(r'^(?P<username>(?!signout|signup|signin)[\.\w]+)/$',account_views.profile, name='userena_profile_detail'),
                       url(r'^myprofile/edit/$',account_views.profile_edit, name='userena_profile_edit'),
                       url(r'^registered/(?P<slug>.*)/signup_complete/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',views.signup_complete),
                       url(r'^registered/(?P<slug>.*)/signup_complete/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<flag>\w+)/$',views.signup_complete_alternate),
                       url(r"^likes/like/(?P<content_type_id>\d+):(?P<object_id>\d+)/$", post_views.like_handler, name="phileo_like_toggle"),
                       url(r"^like/likelist/(?P<object_id>\d+)/$", post_views.like_list),
                       url(r"^likes/", include("phileo.urls")),
                       url(r'^messages/view/all/',account_views.see_all_view),
                       url(r'^messages/list/$',account_views.message_list),
                       url(r'^messages/user_list/(?P<pk>\d+)/$',account_views.message_user_list),
                       url(r'^messages/(?P<pk>\d+)/$',account_views.conv_detail),
                       url(r'^messages/latest/new/$',account_views.get_latest_message),
                       url(r'^messages/', include('conversation.urls')),
                       url(r'^search/search/$', views.search_view,name='haystack_search'),
                       url(r'^search/autocomplete/$', views.autocomplete_search),
                       url(r'^search/autocomplete/recipients/$', views.autocomplete_recipient),
                       url(r'^search/autocomplete/tag/$', views.taguser),
                       url(r'^block/(?P<username>[\.\w]+)/$', account_views.blocking),
                       url(r'^unblock/(?P<username>[\.\w]+)/$', account_views.unblocking),
                       url(r'^ajaxpostrefresh/(?P<pk>\d+)/$', post_views.ajaxpostrefresh),
                       url(r'^upload/image/$', post_views.post_image_upload, name='post_upload'),
                       url(r'^upload/profile/mugshot/$', post_views.mugshot_uploader),
                       url(r'^upload/blog/cover/$', blog_views.blog_cover_upload),
                       url(r'^upload/delete/original/$', post_views.delete_uploaded),
                       url(r'^upload/delete/original/mugshot/$', post_views.delete_uploaded_mugshot),
                       url(r'^upload/delete/blog/$', blog_views.delete_uploaded_cover),
                       url(r'^post/latest/$', views.latest_post),
                       url(r'^post/thread/latest/$', views.latest_thread_post),
                       url(r'^check/user/$', account_views.check_user),
                       url(r'^profile/signup/complete/$', views.profile_fill),
                       url(r'^mugshot/select/$', post_views.mugshot_avatar),
                       url(r'^feed/build/(?P<slug>.*)/(?P<stream>\w+)/$', account_views.build_feed),
                       url(r'^accounts/activate/(?P<activation_key>\w+)/$',userena_views.activate,{'success_url':'/home/new/'},name='userena_activate'),
                       url(r'^discussions/(?P<key>\w+)/$',thread_views.thread_list),
                       url(r'^create/blog/(?P<flag>\w+)/$',blog_views.create_blog),
                       url(r'^blogs/all/(?P<flag>\w+)/$',blog_views.blogs_draft),
                       url(r'^blogs/(?P<pk>\d+)/(?P<slug>[\w-]+)/$',blog_views.blog_details, name='blog_page'),
                       url(r'^blogs/topics/(?P<pk>\d+)/$',blog_views.blogs_by_topics, name='blog_tag_list'),
                       url(r'^blogs/topics/(?P<flag>\w+)/$',blog_views.blog_topics),
                       url(r'^blogs/edit/(?P<pk>\d+)/(?P<flag>\w+)/$',blog_views.blogs_draft_edit),
                       url(r'^resend/activate/mail/(?P<username>[\.\w]+)/$',account_views.resend_activate_mail),
                       url(r'^houseofgrads/(?P<flag>\w+)/$',views.feedback),
                       url(r'^moderate/report/(?P<flag>\w+)/$',account_views.report),
                       url(r'^recent/pages/$', TemplateView.as_view(template_name = 'landing/recent_pages.html')),
                       url(r'^accounts/login/$', userena_views.signin, name='userena_signin'),
                       url(r'^register/download/$', views.download_guides),
                       url(r'^download/guides/$', views.authentication_page),
                       url(r'^accounts/', include('userena.urls')),
                       url('', include('social.apps.django_app.urls', namespace='social')),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
