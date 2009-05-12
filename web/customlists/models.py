from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class List(models.Model):
  """(list description)"""
  
  name = models.TextField(blank=False)
  country = models.TextField(blank=True)
  user = models.ForeignKey(User)
  
  class Admin:
    list_display = ('name', 'country',)
    
  def __unicode__(self):
    return self.name
    

    
class List_Item(models.Model):
  """(list_item description)"""
  lid = models.ManyToManyField(List)
  rid = models.TextField(blank=False)
  
  def __unicode__(self):
    return u"list_item. RID: %s" % self.rid




# List.objects.filter(list_item__rid__exact="815")
