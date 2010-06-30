"""
List making is a simple set of models for storing 'lists' of other models.

The objects in the list are refered to by a unique forign key, using the
generic relations system.

Lists are stored against a user.
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class List(models.Model):
    """Stores list definitions against a user"""
    
    name = models.CharField(blank=False, max_length=100)
    description = models.TextField(blank=False, help_text="""Text will be formatted using <a href="">Markdown</a>""")
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return u"%s" % self.name


class ListItem(models.Model):
    """Stores ids of other objects against a list"""
    
    list_id = models.ForeignKey(List)
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(blank=False, null=False, max_length=100)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u"%s-%s" % (self.content_type, self.object_id)


