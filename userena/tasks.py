from django.contrib.auth.models import User
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import get_object_or_404
import re

@shared_task
def send_activate_mail(subject,message_plain,userid,protocol,activation_days,activation_key,site,email_from,email_to):
    user = get_object_or_404(User, id=int(userid))
    context = Context({'user': user,
                  'protocol': protocol,
                  'activation_days': activation_days,
                  'activation_key': activation_key,
                  'site': site})
    temp = get_template('userena/emails/activation_email_message.html')
    message_html = temp.render(context)
    msg = EmailMultiAlternatives(subject,'',email_from,email_to)
    msg.attach_alternative(message_html, "text/html")
    msg.content_subtype = "html"
    msg.send()

@shared_task
def send_confirm_mail(subject,message_plain,template,new_email,userid,protocol,confirmation_key,site,email_from,email_to):
    user = get_object_or_404(User, id=int(userid))
    context = Context({'user': user,
                  'protocol': protocol,
                  'confirmation_key': confirmation_key,
                       'new_email':new_email,
                  'site': site})
    temp = get_template(template)
    message_html = temp.render(context)
    msg = EmailMultiAlternatives(subject,'',email_from,email_to)
    msg.attach_alternative(message_html, "text/html")
    msg.content_subtype = "html"
    msg.send()

@shared_task
def send_reset_mail(subject, email, email_from, email_to):
    msg = EmailMultiAlternatives(subject,email,email_from,email_to)
    msg.attach_alternative(email, "text/html")
    msg.content_subtype = "html"
    msg.send()

