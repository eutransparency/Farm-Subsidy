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
        args=[request.POST.get('q')]
        if search_map:
            v = 'search_map'
            args.append('map')
        else:
            v = 'search'
        return HttpResponseRedirect(reverse(v, args=args))

    if q:
        form = forms.SearchForm(initial={'q' : q})
        
        be = backend.SearchBackend()
        qu = be.parse_query("%s django_ct:data.recipient" % q)
        qu = be.parse_query("%s django_ct:data.recipient" % q)
        
        
        sqs = SearchQuerySet().models(Recipient)
        sqs = sqs.raw_search(qu).load_all().models(Recipient)

        # total = 0
        # offset = 0
        # if request.GET.get('page'):
        #     offset = 30*request.GET.get('page')
        # for t in sqs[offset:30]:
        #     if t.object.total:
        #       total += t.object.total
        # results = len(sqs)

        # Lists search:
        list_search = SearchQuerySet()
        list_search = list_search.models(List)
        list_search = list_search.auto_query(q).load_all().highlight()
        
        # Location search:
        location_search = SearchQuerySet()
        location_search = location_search.models(Location)
        location_search = location_search.auto_query(q).load_all().highlight()
        
        # Features search:
        feature_search = SearchQuerySet()
        feature_search = feature_search.models(Feature)
        feature_search = feature_search.auto_query(q).load_all().highlight()
        feature_search = feature_search.filter(published=True)
        
        all_spellings =  " ".join([sqs.spelling_suggestion(), 
                  feature_search.spelling_suggestion(), 
                  location_search.spelling_suggestion()]).split(' ') 
        spellings = set()
        for s in all_spellings:
            if s:
                spellings.add(s)
        
    if search_map:
        t = 'map.html'
    else:
        t = 'results.html'
    return render_to_response(
    t, 
    locals(),
    context_instance=RequestContext(request)
    )  
