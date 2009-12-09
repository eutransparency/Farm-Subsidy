from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import queries
import forms

def results(request):
  
  
  
  query = request.GET.get('q','')
  results = queries.search(query)
  total = float()
  for i,doc in results['documents'].items():
    total += float(doc['amount_euro'])
  
  
  form = forms.searchForm(request.GET)
  
  return render_to_response(
    'results.html', 
    locals(),
    context_instance=RequestContext(request)
  )  
