import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.timezone import utc
from .utils import id2slug

from notifications.signals import notify

from model_utils import managers, Choices

now = datetime.datetime.now
if getattr(settings, 'USE_TZ'):
    try:
        from django.utils import timezone
        now = timezone.now
    except ImportError:
        pass


class NotificationQuerySet(models.query.QuerySet):
    
    def unread(self):
        "Return only unread items in the current queryset"
        return self.filter(unread=True)
    
    def read(self):
        "Return only read items in the current queryset"
        return self.filter(unread=False)
    
    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.
        
        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store 
        # the time they were marked as read.
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        
        qs.update(unread=False)
    
    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.
        
        Optionally, filter these by recipient first.
        """
        qs = self.read()
        
        if recipient:
            qs = qs.filter(recipient=recipient)
            
        qs.update(unread=True)

    def mark_as_unread(self):
        self.update(unread=True)

class Notification(models.Model):
    """
    Action model describing the actor acting out a verb (on an optional
    target).
    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/

    Generalized Format::

        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <action_object> <target> <time>

    Examples::

        <justquick> <reached level 60> <1 minute ago>
        <brosner> <commented on> <pinax/pinax> <2 hours ago>
        <washingtontimes> <started follow> <justquick> <8 minutes ago>
        <mitsuhiko> <closed> <issue 70> on <mitsuhiko/flask> <about 2 hours ago>

    Unicode Representation::

        justquick reached level 60 1 minute ago
        mitsuhiko closed issue 70 on mitsuhiko/flask 3 hours ago

    HTML Representation::

        <a href="http://oebfare.com/">brosner</a> commented on <a href="http://github.com/pinax/pinax">pinax/pinax</a> 2 hours ago

    """
    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(choices=LEVELS, default='info', max_length=20)
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='notifications')
    unread = models.BooleanField(default=True, blank=False)

    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor')
    actor_object_id = models.CharField(max_length=255)
    actor = generic.GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(ContentType, related_name='notify_target',
        blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = generic.GenericForeignKey('target_content_type',
        'target_object_id')

    action_object_content_type = models.ForeignKey(ContentType,
        related_name='notify_action_object', blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True,
        null=True)
    action_object = generic.GenericForeignKey('action_object_content_type',
        'action_object_object_id')

    timestamp = models.DateTimeField(default=now)

    public = models.BooleanField(default=True)
    
    objects = managers.PassThroughManager.for_queryset_class(NotificationQuerySet)()

    class Meta:
        ordering = ('-timestamp', )

    def __unicode__(self):
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'target': self.target,
            'timestamp': self.timestamp,
	    'description': self.description,
            'unread':self.unread
        }
        if self.target:
            if self.action_object:
                return u'%(actor)s and %(description)s others %(verb)s %(action_object)s on %(target)s %(timestamp)s ago %(unread)s' % ctx
            return u'%(actor)s %(verb)s %(target)s %(timestamp)s ago %(unread)s' % ctx
        if self.action_object:
            return u'%(actor)s and %(description)s others %(verb)s %(action_object)s %(timestamp)s ago %(unread)s' % ctx
        return u'%(actor)s and %(description)s others %(verb)s %(timestamp)s ago %(unread)s' % ctx

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)

    @property
    def slug(self):
        return id2slug(self.id)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

EXTRA_DATA = False
if getattr(settings, 'NOTIFY_USE_JSONFIELD', False):
    try:
        from jsonfield.fields import JSONField
    except ImportError:
        raise ImproperlyConfigured("You must have a suitable JSONField installed")
    
    JSONField(blank=True, null=True).contribute_to_class(Notification, 'data')
    EXTRA_DATA = True


def notify_handler(verb, **kwargs):
    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    actor = kwargs.pop('sender')
    action_obj = kwargs.pop('action_object',None)
    if action_obj is not None:
        is_similar_notice = Notification.objects.filter(action_object_object_id = action_obj.pk, action_object_content_type=ContentType.objects.get_for_model(action_obj),verb=unicode(verb)).exists()
        if is_similar_notice:
            is_similar_user_pair = Notification.objects.filter(recipient=recipient, actor_object_id=actor.pk,actor_content_type=ContentType.objects.get_for_model(actor),action_object_object_id = action_obj.pk, action_object_content_type=ContentType.objects.get_for_model(action_obj),verb=unicode(verb)).exists()
            if is_similar_user_pair:
                similar_notice = Notification.objects.filter(action_object_object_id = action_obj.pk, action_object_content_type=ContentType.objects.get_for_model(action_obj),verb=unicode(verb))
                desc = similar_notice.values('description')
                newnotify = similar_notice.update(
                            actor_content_type=ContentType.objects.get_for_model(actor),
                            actor_object_id=actor.pk,
                            timestamp=kwargs.pop('timestamp', now()))
                similar_notice.mark_as_unread()
            else:
                similar_notice = Notification.objects.filter(action_object_object_id = action_obj.pk, action_object_content_type=ContentType.objects.get_for_model(action_obj),verb=unicode(verb))
                desc = similar_notice.values('description')
                count = int(desc[0].get('description'))
                count = count + 1
                newnotify = similar_notice.update(
			actor_content_type=ContentType.objects.get_for_model(actor),
			actor_object_id=actor.pk,
			timestamp=kwargs.pop('timestamp', now()),
                        description = str(count)
                        )
                similar_notice.mark_as_unread()
        else:
            newnotify = Notification(
			recipient = recipient,
			actor_content_type=ContentType.objects.get_for_model(actor),
			actor_object_id=actor.pk,
			verb=unicode(verb),
			public=bool(kwargs.pop('public', True)),
			timestamp=kwargs.pop('timestamp', now()),
                        description = kwargs.pop('description','0')
			)
            setattr(newnotify, 'action_object_object_id', action_obj.pk)
            setattr(newnotify, 'action_object_content_type', ContentType.objects.get_for_model(action_obj))
            if kwargs.pop('target',None) != None:
                setattr(newnotify, 'target_content_type', ContentType.objects.get_for_model(kwargs.pop('target')))
                setattr(newnotify, 'target_object_id', kwargs.pop('target').pk)
            newnotify.save()
            newnotify.mark_as_unread()
    else:
        newnotify = Notification(
			recipient = recipient,
			actor_content_type=ContentType.objects.get_for_model(actor),
			actor_object_id=actor.pk,
			verb=unicode(verb),
			public=bool(kwargs.pop('public', True)),
			timestamp=kwargs.pop('timestamp', now()),
                        description = kwargs.pop('description','')
			)
        newnotify.save()
        if kwargs.pop('target',None) != None:
                setattr(newnotify, 'target_content_type', ContentType.objects.get_for_model(kwargs.pop('target')))
                setattr(newnotify, 'target_object_id', kwargs.pop('target').pk)
        newnotify.mark_as_unread()

# connect the signal
notify.connect(notify_handler, dispatch_uid='notifications.models.notification')
