from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import models
from farmsubsidy import fsconf
DEFAULT_YEAR = fsconf.default_year


def country(request, country, year=DEFAULT_YEAR):
  """
  Provides all the variables for the country pages at, for example "/AT"
  
  Querysets:
  
  - `top_recipients` Gets n recipients, sorted by total amount for a given year
  - `years` The years that we have data for a given country
  
  
  """
  country = country.upper()
  
  years = models.data.objects.years(country=country)
  
  top_recipients = models.data.objects.top_recipients(country, limit=30, year=year)
  top_schemes = models.data.objects.top_schemes(country, limit=30, year=year)
  top_regions = models.data.objects.top_regions(country, limit=30, year=year)
  
  return render_to_response(
    'country.html', 
    {
    'top_recipients' : top_recipients,
    'top_schemes' : top_schemes,
    'top_regions' : top_regions,
    'years' : years,
    'selected_year' : int(year),
    },
    context_instance=RequestContext(request)
  )  

