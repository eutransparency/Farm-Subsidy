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
    title = "Search results for %s" % query
  
    options = {
      'collapse_key' : fsconf.index_values['recipient_id_x'], 
      'sort_value' : fsconf.index_values['total_amount'],
      'offset' : 0,
      'len' : 50,
      'page' : int(request.GET.get('page',0))
    }
  
    results = queries.do_search(query, options)
    return render_to_response('data/results.html', {'results' : results, 'query' : query, 'title' : title})  
  
  except Exception, e:
    title = "Search"
    query = ''

    return render_to_response('data/search.html', {'form' : forms.SearchForm(), 'title' : title}, context_instance=RequestContext(request))  

  
def recipient(request, recipient_id):
  results = queries.do_search("xid:%s" % recipient_id)
  # assert False
  return render_to_response('data/recipient.html', {'results' : results})  
  
def country(request, country):
  countryinfo = {
    'code' : country,
    'name' : countryCodes.code2name[country]
  }
  path = ''
  return render_to_response('data/country.html', {'country' : countryinfo, 'browsepath' : path}, context_instance=RequestContext(request))    



def countrybrowse(request, country, browsepath):
  countryinfo = {
    'code' : country,
    'name' : countryCodes.code2name[country]
  }
  return render_to_response('data/country.html', {'country' : countryinfo, 'browsepath' : browsepath }, context_instance=RequestContext(request))    



