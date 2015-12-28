"""
Django settings for myProject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from __future__ import absolute_import
BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_IMPORT = ['posts.tasks','userena.tasks']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=y^p!-ci^gjr^lybpo2%*u3y9b-2-$c)@%5s=4uxz@s_82ngbf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'haystack',
    'easy_thumbnails',
    'accounts',
    'userena',
    'guardian',
    'posts',
    'threads',
    'jsonfield',
    'tinymce',
    'actstream',
    'conversation',
    'notifications',
    'phileo',
    'endless_pagination',
    'ajaxuploader',
    'djcelery',
    'social.apps.django_app.default',
    'blogs',
    'django.contrib.sitemaps',
)
THUMBNAIL_NAMER = 'easy_thumbnails.namers.hashed'
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'myProject.urls'
TEMPLATE_DIRS = (
    '/Users/vishalsingh/django/myProject/templates',
    )
WSGI_APPLICATION = 'myProject.wsgi.application'
AUTH_PROFILE_MODULE = 'accounts.MyProfile'
AUTHENTICATION_BACKENDS = (
     'social.backends.facebook.FacebookOAuth2',
    'userena.backends.UserenaAuthenticationBackend',
     'phileo.auth_backends.CanLikeBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
   
)
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
 'django.template.loaders.app_directories.Loader')

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'houseofgradsdb',
        'USER': 'root',
        'PASSWORD': 'dream',
        'HOST': '',
        'PORT': '',
    }
}

ADMINS = (
    ('Vishal Singh', 'vish.iitd1@gmail.com'),
)

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
#TEST_EMAIL_BACKEND_RECIPIENTS = ADMINS
##EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FROM_EMAIL = 'admin@houseofgrads.com'
EMAIL_SUBJECT_PREFIX = '[HouseofGrads] '
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'admin@houseofgrads.com'
EMAIL_HOST_PASSWORD = 'dreamcometrue'
EMAIL_PORT = 465

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True

USE_L10N = True

USE_TZ = False
MEDIA_ROOT = '/Users/vishalsingh/django/myProject/media/'

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '/staticfiles/')

STATIC_URL = '/static/'
LOGOUT_URL = '/signout/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)
LOGIN_REDIRECT_URL='/home/'
ANONYMOUS_USER_ID = -1
TINYMCE_COMPRESSOR = True
ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'auth.group', 'posts.createpost','posts.parentthread'),
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}
USERENA_MUGSHOT_DEFAULT = 'wavatar'
USERENA_PROFILE_DETAIL_TEMPLATE = '/Users/vishalsingh/django/myProject/templates/userena/profile_detail.html'
USERENA_WITHOUT_USERNAMES = True
USERENA_HIDE_EMAIL = True
USERENA_MUGSHOT_SIZE = 150
USERENA_HTML_EMAIL = True
AUTH_PROFILE_MODULE = "accounts.MyProfile"
TEMPLATE_CONTEXT_PROCESSORS = ( 'social.apps.django_app.context_processors.backends',
                                'social.apps.django_app.context_processors.login_redirect',
                                "django.core.context_processors.request",
                                "django.contrib.auth.context_processors.auth",)
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/%s/" % o.username,}
ACTSTREAM_MANAGER = 'managers.MyActionManager'
PHILEO_LIKABLE_MODELS = {
    "posts.CreatePost":{},
    "comments.Comment":{},
    "posts.ParentThread":{},
    "blogs.Blog":{}
    }
CONVERSATION_MESSAGE_FORM = 'accounts.forms.MyMessageForm'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
HAYSTACK_CUSTOM_HIGHLIGHTER = 'myProject.views.MyHighlighter'
## social authentication settings

SOCIAL_AUTH_FACEBOOK_KEY = '671512716272640'
SOCIAL_AUTH_FACEBOOK_SECRET = 'ed17e3b432797773bff0859802c3385d'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/register/social/'
SOCIAL_AUTH_LOGIN_ERROR_URL = 'accounts/login/error/auth/'
SOCIAL_AUTH_USER_MODEL = 'auth.User'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'myProject.pipeline.save_profile_picture',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
FIELDS_STORED_IN_SESSION = ['flag',]