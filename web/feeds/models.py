from django.db import models
from tagging.fields import TagField
from tagging.models import Tag


class FeedCategories(models.Model):
  name = models.CharField(max_length=100)
  
  def __unicode__(self):
    return self.name
  

class Feeds(models.Model):
  url = models.URLField()
  title = models.CharField('Title', max_length=400)
  is_active = models.BooleanField('Active', default=True)  
  category = models.ForeignKey(FeedCategories)
  etag = models.CharField('etag', null=True, blank=True, max_length=400)
  last_modified = models.DateTimeField('last modified', null=True, blank=True)

  def __unicode__(self):
    return self.title
  
  def delete(self):
    FeedItems.objects.filter(feed=self).delete()
    super(Feeds, self).delete()
    
    
  

class FeedItems(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True)
    guid = models.CharField(blank=False, max_length=2000)
    feed = models.ForeignKey(Feeds)
    date = models.DateTimeField()
    url = models.URLField(max_length=2000)
    tags = TagField()
    author = models.TextField(blank=True, null=True)    
    
    def __unicode__(self):
      return self.title
      
    class Meta:
      get_latest_by = '-date'
      ordering = ( '-date', )
     
