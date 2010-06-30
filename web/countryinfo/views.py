from django.shortcuts import render_to_response
from django.template import RequestContext

import transparency
import load_info

def compare(request):
  
  info = load_info.countries_by_category()
  
  return render_to_response(
    'compare.html', 
    {'info' : info},
    context_instance=RequestContext(request)
  )  
  

def transparency_list(request):
    transparency_list = transparency.transparency_list()
    
    return render_to_response(
        'transparency_list.html', 
        {'list' : transparency_list, },
        context_instance=RequestContext(request)
    )