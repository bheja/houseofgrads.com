"""Models for the conversation app."""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
class Conversation(models.Model):
    """
    Model to contain different messages between one or more users.

    :users: Users participating in this conversation.
    :archived_by: List of participants, who archived this conversation.
    :read_by: List of participants, who read this conversation.
    :content_object: Optional related object the users are talking about.

    """
    users = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Users'),
        related_name='conversations',
    )

    archived_by = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Archived by'),
        related_name='archived_conversations',
    )

    read_by = models.ManyToManyField(
        'auth.User',
        verbose_name=_('Read by'),
        related_name='read_conversations',
    )

    # Generic FK to the object this conversation is about
    content_type = models.ForeignKey(
        ContentType,
        related_name='conversation_content_objects',
        null=True, blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    latest_message_date = models.DateTimeField(auto_now_add=True)
    def latest_message(self):
        messages = self.messages.all()
        latest_message = messages.order_by('-id')[0] ##add a new column when migrating to MySQL
        return latest_message

    def save(self, *args, **kwargs):
        self.latest_message_date = datetime.datetime.now()
        return super(Conversation, self).save(*args, **kwargs)

class Message(models.Model):
    """
    Model, which holds information about a post within one conversation.

    :user: User, who posted the message.
    :conversation: Conversation, which contains this message.
    :date: Date the message was posted.
    :text: Message text.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='messages',
    )

    conversation = models.ForeignKey(
        Conversation,
        verbose_name=_('Conversation'),
        related_name='messages',
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date'),
    )

    text = models.TextField(
        max_length=2048,
        verbose_name=_('Text'),
    )
    
    def __unicode__(self):
        return "%s" %(self.text)

    def save(self,*args,**kwargs):
        conv = self.conversation
        conv.latest_message_date = self.date
        conv.save()
        return super(Message, self).save(*args, **kwargs)
