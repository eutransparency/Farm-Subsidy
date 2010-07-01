from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from models import Feature

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