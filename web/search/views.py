from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from haystack.query import SearchQuerySet
from haystack import backend

from data.models import Recipient
from features.models import Feature

import forms

def search(request, q=None, search_map=False):
    form = forms.SearchForm()

    if request.POST:
        # initial redirect, to get linkable URLs
        args=[request.POST.get('q')]
        if search_map:
            v = 'search_map'
            args.append('map')
        else:
            v = 'search'
        return HttpResponseRedirect(reverse(v, args=args))

    if q:
        form = forms.SearchForm(initial={'q' : q})
        sqs = SearchQuerySet()
        sqs = sqs.auto_query(q).load_all().models(Recipient)
        sqs = sqs.exclude(name__startswith="unknown")
        
        if 'country' in request.GET:
            sqs = sqs.filter(country=request.GET['country'])
        if 'scheme' in request.GET:
            sqs = sqs.filter(scheme=request.GET['scheme'])
        
        sqs = sqs.facet('country')

        total = 0
        for t in sqs:
            if t.object.total:
              total += t.object.total
        
        results = len(sqs)
        
        # Features search:
        feature_search = SearchQuerySet()
        feature_search = feature_search.models(Feature)
        feature_search = feature_search.auto_query(q).load_all().highlight()
        
    if search_map:
        t = 'map.html'
    else:
        t = 'results.html'
    return render_to_response(
    t, 
    locals(),
    context_instance=RequestContext(request)
    )  
