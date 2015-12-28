from django.template import Library, Node, TemplateSyntaxError
from conversation.models import Conversation
from django.template import Node

register = Library()

@register.assignment_tag(takes_context=True)
def unread_messages_count(context):
    user = context['user']
    total_conversations = user.conversations.all().count()
    read_conversation = user.read_conversations.all().count()
    unread_conversation = total_conversations - read_conversation
    return unread_conversation

