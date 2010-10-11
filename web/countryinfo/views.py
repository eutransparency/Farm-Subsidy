from django.shortcuts import render_to_response
from django.template import RequestContext

import transparency
from models import TransparencyScore
import load_info

def compare(request):
  
  info = load_info.countries_by_category()
  
  return render_to_response(
    'compare.html', 
    {'info' : info},
    context_instance=RequestContext(request)
  )  
  

def transparency_list(request):
    transparency_list = TransparencyScore.objects.all().order_by('rank')
    
    green = "2A8330"
    yellow = "FF6600"
    red = "FE0000"
    
    map_colours = []
    map_countries = []
    for country in transparency_list:
        map_countries.append(country.country)
        if country.score > 50:
            map_colours.append(green)
        elif country.score > 30:
            map_colours.append(yellow)
        else:
            map_colours.append(red)

    
    return render_to_response(
        'transparency_list.html', 
        {
            'list' : transparency_list, 
            'map_colours' : map_colours, 
            'map_countries' : map_countries, 
        },
        context_instance=RequestContext(request)
    )