from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class List(models.Model):
  
  def __unicode__(self):
    return self.name
  
  name = models.TextField(blank=False)
  user = models.ForeignKey(User, unique=False, blank=True)


class ListItem(models.Model):
  list_id = models.ForeignKey(List)
  content_type = models.ForeignKey(ContentType)
  item_pk = models.TextField(blank=True)