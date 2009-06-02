import sys
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from farmsubsidy.indexer import countryCodes
from web.comments import forms as comment_forms
from web.data.country_years import years
import forms

from models import SearchModelWrapper

from farmsubsidy import fsconf
from farmsubsidy.queries import queries
  

def search(request):
  """Does a xapian search and returns the results"""
  try:
    query = request.GET['q']
    if query == '':
      raise ValueError({'error' : "Please Enter a search term"})
      
    if request.GET.get('country'):
      if request.GET['country'] in countryCodes.countryCodes():
        query = "%s country:%s" % (query, request.GET['country'])
      else:
        raise ValueError({'error' : "Please Enter valid country"})
        
    request.session["query"] = query
    title = "Search results for %s" % query
  
    options = {
      'collapse_key' : fsconf.index_values['global_id_x'], 
      'sort_value' : fsconf.index_values['amount'],
      'offset' : 0,
      'len' : 50,
      'page' : int(request.GET.get('page',0))
    }
  
    results = queries.do_search(query, options)
    
    results['url'] = reverse("web.data.views.search")
    results['GET'] = request.GET
    
    
    return render_to_response(
    'results.html', 
    {'results' : results, 'query' : query, 'title' : title},
    context_instance=RequestContext(request)
    )  
  
  except Exception, e:
    title = "Search"
    query = ''
    if 'error' in e[0]:
      errors = [e[0]['error']]
    else:
      errors = []

    return render_to_response(
      'search.html', 
      {'form' : forms.SearchForm(), 'title' : title, 'errors' : errors, 'e' : e}, 
      context_instance=RequestContext(request)
    )  

  
def recipient(request, recipient_id, country=None):
  
  if request.method == 'POST' and request.user.is_authenticated():
    form = comment_forms.CommentForm(request.POST)
    if form.is_valid():
      from web.comments.models import Comment
      c = Comment(
        user=request.user, 
        comment=form.cleaned_data['comment'], 
        owner=form.cleaned_data['owner'], 
        recipient_id=recipient_id
        )
      c.save()
      if form.cleaned_data['owner']:
        from web.misc.models import FarmOwners
        f = FarmOwners(user=request.user, farm=recipient_id)
        f.save()
      return HttpResponseRedirect(
        reverse("recipient_view", kwargs={'recipient_id' : recipient_id, 'country' : country})
        )
  else:
    form = comment_forms.CommentForm()
    
  options = {
    'page' : 0,
    'len' : 100,
    'sort_value' : fsconf.index_values['year'],
    'allyears' : True,
  }
  results = queries.do_search("xid:%s" % recipient_id, options)
  total = 0
  result = None
  for key,result in results['documents'].items():
    total = total + float(result['amount'])
  
  if result and 'year' in result:
    return render_to_response('recipient.html', 
    {'results' : results, 'title' : results, 'total' : total, 'form' : form},
    context_instance=RequestContext(request))  
  else:
    return render_to_response('recipient-indexing.html', 
    context_instance=RequestContext(request))
    
  
  
  
def country(request, country):
  data_years = years()['UK']
  latest_year = max(data_years)
  getyear = request.GET.get('year', latest_year)
  if getyear in data_years:
    year = getyear
  else:
    year = latest_year
    
  options = {
    'len' : 20,
    'page' : 0,
    #'year' : year,
    'allyears' : True,
    'collapse_key' : fsconf.index_values['global_id_x'], 
    'sort_value' : fsconf.index_values['amount'],
    'cache' : True,
    'offset' : 0,
  }  
  
  path = country  
  results = queries.do_search("geopath:%s" % path, options)
  

  query = "year:%s geopath:" % year
  return render_to_response('country.html', {'browsepath' : path, 'query' : query, 'year' : year, 'results' : results}, context_instance=RequestContext(request))    



def regionbrowse(request, country, browsepath):
  return render_to_response('country.html', {'browsepath' : browsepath }, context_instance=RequestContext(request))    



def home(request):
  """temp home view"""
  # TODO replace with a real view!
  return render_to_response('home.html', context_instance=RequestContext(request))    


def countrybrowse(request, country):
  options = {
    'collapse_key' : fsconf.index_values['recipient_id_x'], 
    'sort_value' : fsconf.index_values['amount'],
    'cache' : True,
    'offset' : 0,
    'len' : 50,
    'page' : int(request.GET.get('page',0)),
    'check_at_least_term' : 'XCOUNTRY:%s' % country
  }
  
  results = queries.do_search('country:%s' % country, options)
  results['GET'] = request.GET    
  return render_to_response(
  'browse.html', 
  {'results' : results},
  context_instance=RequestContext(request)
  )  
  


















