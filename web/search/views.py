# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from haystack.query import SearchQuerySet
from haystack import backend

from data.models import Recipient, Location
from features.models import Feature
from listmaker.models import List

import forms

def search(request, q=None, search_map=False):
    form = forms.SearchForm()

    if request.POST:
        # initial redirect, to get linkable URLs
        if request.POST.get('q'):
            args = [request.POST.get('q')]
            if search_map:
                v = 'search_map'
                args.append('map')
            else:
                v = 'search'
            return HttpResponseRedirect(reverse(v, args=args))
        else:
            return HttpResponseRedirect(reverse('search'))
        
    if q:
        form = forms.SearchForm(initial={'q' : q})
        
        be = backend.SearchBackend()
        qu = be.parse_query("%s django_ct:data.recipient" % q)
        
        
        sqs = SearchQuerySet()
        sqs = sqs.raw_search(qu, end_offset=20).load_all()

        total = 0
        offset = 0
        if request.GET.get('page'):
            offset = 20*(int(request.GET.get('page'))-1)
        for t in sqs[offset:offset+20]:
            if t.object.total:
              total += t.object.total
        results = len(sqs)

        # Lists search:
        list_search = SearchQuerySet()
        list_search = list_search.models(List)
        list_search = list_search.auto_query(q).load_all().highlight()
        
        # Location search:
        location_search = SearchQuerySet()
        location_search = location_search.models(Location)
        location_search = location_search.auto_query(q)[:5]
        
        # Features search:
        feature_search = SearchQuerySet()
        feature_search = feature_search.models(Feature)
        feature_search = feature_search.auto_query(q).load_all().highlight()
        feature_search = feature_search.filter(published=True)[:3]
        
    if search_map:
        t = 'map.html'
    else:
        t = 'results.html'
    return render_to_response(
    t, 
    locals(),
    context_instance=RequestContext(request)
    )  
