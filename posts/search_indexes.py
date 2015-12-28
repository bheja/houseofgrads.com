import datetime
from haystack import indexes
from posts.models import ParentThread, CreatePost
from django.contrib.auth.models import User


class ParentThreadIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    stream = indexes.CharField(model_attr='stream')
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return ParentThread

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.exclude(name='myWall')

class CreatePostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    thread = indexes.CharField(model_attr='thread')
    author = indexes.CharField(model_attr='author')

    def get_model(self):
        return CreatePost

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date__lte = datetime.datetime.now())

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='username')
    content_auto = indexes.EdgeNgramField(model_attr='username')

    def get_model(self):
        return User
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.exclude(username='AnonymousUser')
