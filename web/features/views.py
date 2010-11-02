from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from web.feeds.models import FeedItems, FeedCategories
from models import Feature

def news_home(request):
    features = Feature.objects.filter(published=True)[:5]
    feed_items = FeedItems.objects.all()[:5]
    
    return render_to_response(
        'news_home.html', 
        {
        'features' : features,
        'feed_items' : feed_items,
        }, 
        context_instance = RequestContext(request)
        )

def media_list(request, cat='News'):
    category = FeedCategories.objects.get(name=cat)
    feed_items = FeedItems.objects.filter(feed__category=category)

    return render_to_response(
        'media_list.html', 
        {
        'feed_items' : feed_items,
        }, 
        context_instance = RequestContext(request)
    )


    
    
def feature_list(request):
    features = Feature.objects.filter(published=True)
    return render_to_response(
        'feature_list.html', 
        {
        'features' : features
        }, 
        context_instance = RequestContext(request)
    )

def feature_detail(request, slug):
    feature = get_object_or_404(Feature, published=True, slug=slug)
    recent_features = Feature.objects.filter(published=True).exclude(slug=slug).order_by('-id')[:5]    
    return render_to_response(
        'feature_detail.html', 
        {
        'feature' : feature,
        'recent_features' : recent_features,
        }, 
        context_instance = RequestContext(request)
    )    