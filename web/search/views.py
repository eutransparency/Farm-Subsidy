from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from haystack.query import SearchQuerySet
from haystack import backend


import forms

def search(request, q=None):
    form = forms.SearchForm()

    if request.POST:
        # initial redirect, to get linkable URLs
        return HttpResponseRedirect(reverse('search', args=[request.POST.get('q')]))

    if q:
        form = forms.SearchForm(initial={'q' : q})
        sqs = SearchQuerySet()
        sqs = sqs.auto_query(q).load_all()
        sqs = sqs.exclude(name__startswith="unknown")
        
        if 'country' in request.GET:
            sqs = sqs.filter(country=request.GET['country'])
        if 'scheme' in request.GET:
            sqs = sqs.filter(scheme=request.GET['scheme'])
        
        sqs = sqs.facet('scheme').facet('country')

        total = 0
        for t in sqs:
            total += t.object.total
        
        results = len(sqs)
    
    return render_to_response(
    'results.html', 
    locals(),
    context_instance=RequestContext(request)
    )  
