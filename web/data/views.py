from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Sum
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
  
  top_recipients = models.data.objects.top_recipients(country, limit=10, year=year)
  top_schemes = models.data.objects.top_schemes(country, limit=10, year=year)
  top_regions = models.data.objects.top_regions(country, limit=10, year=year)
  
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



def recipient(request, country, recipient_id):
  """
  View for recipient page.
  
  - `country` ISO country, as defined in countryCodes
  - `recipient_id` is actually a globalrecipientidx in the date
  
  """
  country = country.upper()
  
  recipient = models.recipient.objects.filter(globalrecipientidx=recipient_id)[0]
  payments = models.payment.objects.filter(globalrecipientidx=recipient_id).select_related().order_by('year')
  
  return render_to_response(
    'recipient.html', 
    {
    'recipient' : recipient,
    'payments' : payments,
    },
    context_instance=RequestContext(request)
  )  
  

def browse(request, country, browse_type, year, sort='amount'):
  if browse_type == "recipient":
    data = models.total.objects.aggregate(Sum('year'))
    # .filter(countrypayment=country).order_by('-amount_euro')
  
  print data
  # if int(year) != 0:
  #   data.filter(year=year)

  return render_to_response(
    'browse.html', 
    {
    'data' : data,
    },
    context_instance=RequestContext(request)
  )  



  
  
  