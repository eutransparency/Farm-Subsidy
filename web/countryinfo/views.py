from django.shortcuts import render_to_response
from django.template import RequestContext

import load_info

def compare(request):
  
  info = load_info.countries_by_category()
  
  return render_to_response(
    'compare.html', 
    {'info' : info},
    context_instance=RequestContext(request)
  )  
  