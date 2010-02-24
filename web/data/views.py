from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Sum, Count
import models
import fsconf
from indexer import countryCodes
from search import queries
import context_processors

DEFAULT_YEAR = fsconf.default_year

def home(request):
  
  ip_country = context_processors.ip_country(request)['ip_country']
  top_eu = models.data.objects.top_recipients(limit=10, year=DEFAULT_YEAR)
  top_for_ip = models.data.objects.top_recipients(ip_country['ip_country'], limit=10, year=DEFAULT_YEAR)
  
  return render_to_response(
    'home.html', 
    locals(),
    context_instance=RequestContext(request)
  )  
  


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
  top_regions = models.locations.objects.sub_locations(country=country, limit=10)
  
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



def recipient(request, country, recipient_id, name):
  """
  View for recipient page.
  
  - `country` ISO country, as defined in countryCodes
  - `recipient_id` is actually a globalrecipientidx in the date
  
  """
  country = country.upper()
  
  recipient = models.recipient.objects.filter(globalrecipientidx=recipient_id)[0]
  payments = models.data.objects.recipient_payments(globalrecipientidx=recipient_id)
  recipient_total = float(sum([i.amount_euro for i in payments]))
  payment_years = list(set(payment.year for payment in payments))
  related = queries.simmlar_name(recipient.name)
  
  return render_to_response(
    'recipient.html', 
    {
    'recipient' : recipient,
    'payments' : payments,
    'recipient_total' : recipient_total,
    'payment_years' : payment_years,
    'related' : related,
    },
    context_instance=RequestContext(request)
  )  

def scheme(request, country, globalschemeid):
  """
  Show a single scheme and a list of top recipients to get payments under it
  
  - `country` ISO country, as defined by countryCodes
  - ``globalschemeid` globalschemeid from the data_schemes table in the database
  """ 
  
  scheme = models.scheme.objects.get(globalschemeid=globalschemeid)
  totals = models.data.objects.amount_years(country=country, scheme=globalschemeid)
  top_recipients = models.data.objects.browse_recipients(country, year=0, scheme=globalschemeid)
  
  return render_to_response(
    'scheme.html', 
    {
    'scheme' : scheme,
    'totals' : totals,
    'top_recipients' : top_recipients,
    },
    context_instance=RequestContext(request)
  )  
  

def browse(request, country, browse_type, year=DEFAULT_YEAR, sort='amount'):
  
  if browse_type == "recipient":
    data = models.data.objects.browse_recipients(country, year, sort)
  if browse_type == "scheme":
    data = models.data.objects.browse_schemes(country, year, sort)
  if browse_type == "location":
    data = models.locations.objects.locations(country=country, parent=country, year=year, limit=None)
    
    
  years = models.data.objects.years(country=country)
  

  
  return render_to_response(
    'browse.html', 
    {
    'data' : data,
    'years' : years,
    'sort' : sort,
    'browse_type' : browse_type,
    'selected_year' : int(year),    
    },
    context_instance=RequestContext(request)
  )  


def location(request, country, geo1=None,geo2=None,geo3=None,geo4=None):

  sub_location_sort = request.GET.get('sublocation', 'amount')
  
  location = models.locations.objects.location(country=country, geo1=geo1, geo2=geo2, geo3=geo3, geo4=geo4)
  sub_location = models.locations.objects.sub_locations(country=country, geo1=geo1,geo2=geo2,geo3=geo3,geo4=geo4, limit=None, sort=sub_location_sort)
  location_recipients = models.locations.objects.recipients_by_location(country=country, geo1=geo1,geo2=geo2,geo3=geo3,geo4=geo4, limit=10)
  
   
  return render_to_response(
    'location.html', 
    {
    'location' : location,
    'location_recipients' : location_recipients,
    'sub_location' : sub_location,
    # 'sub_location_sort' : sub_location_sort,
    # 'selected_year' : int(year),        
    },
    context_instance=RequestContext(request)
  )  
  

  