from models import *
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render_to_response
from tagging.utils import get_tag
from tagging.models import TaggedItem



def feed_list(request, category='', tag=None):
  cat = FeedCategories.objects.filter(name=category)
  q = FeedItems.objects.all()
  feeds = Feeds.objects.filter(category__in=cat)
  q = q.filter(feed__in=feeds)
  q = q.order_by("-date")
  
  
  if tag:
    query_tag = Tag.objects.get(name=tag)
    q = TaggedItem.objects.get_by_model(FeedItems, query_tag)
    # assert False

  
  return render_to_response('page.html', {'items' : q, 'title' : category}, context_instance=RequestContext(request))    