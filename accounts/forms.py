from django import forms
from accounts.models import MyProfile
from django.contrib.auth.models import User
from django.db.models import Q
from userena.utils import get_user_model
from userena.contrib.umessages.fields import CommaSeparatedUserField
from conversation.models import Conversation, Message
from django.contrib.contenttypes.models import ContentType
from accounts.models import FeedBack

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','autofocus':'autofocus'}),label = 'Type in your nick or email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','autofocus':'autofocus'}))

class MugshotForm(forms.ModelForm):
	class Meta:
		model = MyProfile
		fields = ('mugshot', )

class FeedBackForm(forms.ModelForm):
    images = forms.ImageField()
    class Meta:
        model = FeedBack
        fields = ('description','category','images',)

class MyMessageForm(forms.ModelForm):
    """Form to post new messages to a new or existing conversation."""
    def __init__(self, user, conversation, initial_user, content_object, *args,
                 **kwargs):
        self.user = user
        self.conversation = conversation
        self.content_object = content_object
        super(MyMessageForm, self).__init__(*args, **kwargs)
        if not self.conversation:
            users = User.objects.exclude(pk=user.pk)
            self.fields['recipients'] = CommaSeparatedUserField(widget=forms.TextInput(attrs={'class':'form-control','required':'required','autofocus':'autofocus'}))

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
            if not self.conversation:
                # Check for existing conversations of these users
                recipient_list = self.cleaned_data['recipients']
                recipient_list_id = [r.id for r in recipient_list]
                recipients = User.objects.filter(
                    Q(pk__in=recipient_list_id)
                    | Q(pk=self.user.pk),
                )
                conversations = self.user.conversations.all()
                if self.content_object:
                    conversations = conversations.filter(
                        content_type=ContentType.objects.get_for_model(
                            self.content_object),
                        object_id=self.content_object.pk,
                    )
                for user in recipients:
                    conversations = conversations.filter(
                        pk__in=user.conversations.values_list('pk'))
                if conversations:
                    user_list = conversations[0].users.all()
                    if len(user_list) != len(recipient_list)+1:
                        self.conversation = Conversation.objects.create()
                        self.conversation.users.add(self.user)
                        for user in recipients:
                            self.conversation.users.add(user)
                    else:
                        self.conversation = conversations[0]
                else:
                    if self.content_object:
                        self.conversation = Conversation.objects.create(
                            content_object=self.content_object)
                    else:
                        self.conversation = Conversation.objects.create()
                    self.conversation.users.add(self.user)
                    for user in recipients:
                        self.conversation.users.add(user)
            self.instance.conversation = self.conversation

            # Reset archive marks
            self.instance.conversation.archived_by.clear()
            # Reset reading status
            self.instance.conversation.read_by.clear()
        return super(MyMessageForm, self).save(*args, **kwargs).conversation

    class Meta:
        model = Message
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class':'form-control','style':'border:1px solid #ddd;','required':'required','autofocus':'autofocus','rows':'1','id':'msgText','placeholder':'Write a reply...'}),}
