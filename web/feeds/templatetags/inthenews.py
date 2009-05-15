from django.template import Library, Node

from feeds.models import *
from tagging.utils import get_tag
from tagging.models import TaggedItem
from tagging.models import Tag



register = Library()

def latestnews(country=None, num=5, category='News', oneline=False):
  cat = FeedCategories.objects.filter(name=category)
  q = FeedItems.objects.all()
  feeds = Feeds.objects.filter(category__in=cat)
  q = q.filter(feed__in=feeds)
  
  if country:
    query_tag = Tag.objects.filter(name=country)
    q = TaggedItem.objects.get_by_model(FeedItems, query_tag)


  q = q.order_by("-date")
  return {'newsitems' : q[:num], 'oneline' : oneline}

register.inclusion_tag('blocks/latest-news.html')(latestnews)
