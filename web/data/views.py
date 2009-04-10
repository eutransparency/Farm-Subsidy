import sys
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from farmsubsidy.indexer import countryCodes
import forms

from farmsubsidy import fsconf
from farmsubsidy.queries import queries

def test(response, something):
  """docstring for test"""
  return render_to_response('base.html')
  

def search(request):
  """Does a xapian search and returns the results"""
  try:
    query = request.GET['q']
    request.session["query"] = query
    title = "Search results for %s" % query
  
    options = {
      'collapse_key' : fsconf.index_values['recipient_id_x'], 
      'sort_value' : fsconf.index_values['total_amount'],
      'offset' : 0,
      'len' : 50,
      'page' : int(request.GET.get('page',0))
    }
  
    results = queries.do_search(query, options)
    return render_to_response(
    'data/results.html', 
    {'results' : results, 'query' : query, 'title' : title},
    context_instance=RequestContext(request)
    )  
  
  except Exception, e:
    title = "Search %s" % e
    query = ''
    error = e
    raise e
    return render_to_response(
      'data/search.html', 
      {'form' : forms.SearchForm(), 'title' : title, 'error' : error}, 
      context_instance=RequestContext(request)
    )  

  
def recipient(request, recipient_id, country=None):
  options = {
    'sort_value' : fsconf.index_values['year'],
  }
  results = queries.do_search("xid:%s" % recipient_id)
  total = 0
  for key,result in results['documents'].items():
    total = total + float(result['amount'])
  return render_to_response('data/recipient.html', 
  {'results' : results, 'title' : results, 'total' : total},
  context_instance=RequestContext(request))  
  
  
  
  
def country(request, country):
  path = country
  return render_to_response('data/country.html', {'browsepath' : path}, context_instance=RequestContext(request))    



def countrybrowse(request, country, browsepath):
  return render_to_response('data/country.html', {'browsepath' : browsepath }, context_instance=RequestContext(request))    



def home(request):
  """temp home view"""
  # TODO replace with a real view!
  return render_to_response('base.html', context_instance=RequestContext(request))    
  


