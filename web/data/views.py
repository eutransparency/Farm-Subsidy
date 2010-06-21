from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Sum, Count
from django.conf import settings

from data import countryCodes
import context_processors
import models

DEFAULT_YEAR = settings.DEFAULT_YEAR

def home(request):
  
  ip_country = request.session.get('ip_country', 'GB')
  top_eu = models.Recipient.objects.top_recipients()
  top_for_ip = models.Recipient.objects.top_recipients(country=ip_country)
  
  return render_to_response(
    'home.html', 
    {
    'top_eu' : top_eu,
    'top_for_ip' : top_for_ip,
    },
    context_instance=RequestContext(request)
  )  
  


def country(request, country, year=DEFAULT_YEAR):
  """
  Provides all the variables for the country pages at, for example "/AT/"
  
  Querysets:
  
  - `top_recipients` Gets n recipients, sorted by total amount for a given year
  - `years` The years that we have data for a given country
  
  
  """
  country = country.upper()
  
  # years = models.data.objects.years(country=country)
  
  top_recipients = models.Recipient.objects.top_recipients(country=country, year=year)
  top_schemes = models.Scheme.objects.top_schemes(country)
  top_locations = models.Location.get_root_nodes().order_by('-total')
  # print top_regions
  
  return render_to_response(
    'country.html', 
    {
    'top_recipients' : top_recipients,
    'top_schemes' : top_schemes,
    'top_locations' : top_locations,
    # 'years' : years,
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
  
  recipient = models.Recipient.objects.get(globalrecipientidx=recipient_id)
  payments = models.Payment.objects.select_related().filter(recipient=recipient_id).order_by('year')
  recipient_total = recipient.total
  payment_years = list(set(payment.year for payment in payments))
  
  return render_to_response(
    'recipient.html', 
    {
    'recipient' : recipient,
    'payments' : payments,
    'recipient_total' : recipient_total,
    'payment_years' : payment_years,
    },
    context_instance=RequestContext(request)
  )  


def all_schemes(request, country='EU'):
    """
    Scheme browser (replaces generic 'browse' function for schemes)
    """

    schemes = models.Scheme.objects.all().order_by('-total')
    
    if country != 'EU':
        schemes = schemes.filter(countrypayment=country)

    return render_to_response(
        'all_schemes.html', 
        {
            'schemes' : schemes,
        },
        context_instance=RequestContext(request)
    )  
    

def scheme(request, country, globalschemeid, name):
  """
  Show a single scheme and a list of top recipients to get payments under it
  
  - `country` ISO country, as defined by countryCodes
  - ``globalschemeid` globalschemeid from the data_schemes table in the database
  """ 
  
  scheme = models.Scheme.objects.get(globalschemeid=globalschemeid)
  
  # To add one day
  # scheme_years = models.SchemeYear.objects.filter(globalschemeid=globalschemeid)

  top_recipients = models.Recipient.objects.filter(
                        payment__scheme=globalschemeid
                    ).annotate(scheme_total=Sum('payment__amounteuro')).order_by('-scheme_total').distinct()
  
  return render_to_response(
    'scheme.html', 
    {
    'scheme' : scheme,
    # 'totals' : totals,
    'top_recipients' : top_recipients,
    },
    context_instance=RequestContext(request)
  )  
  

def browse(request, country):
    """
    Browse recipients, sorted / filtered by various things using django-filter
    """

    recipients = models.Recipient.objects.filter(total__isnull=False).distinct().order_by('-total')
    if country != "EU":
        recipients = recipients.filter(countrypayment=country)
  
    return render_to_response(
        'browse.html', 
        {
            'recipients' : recipients,
        },
        context_instance=RequestContext(request)
    )  

def all_locations(request, country):
    locations = models.Location.objects.all()
    kwargs = {'geo_type' : 'geo1'}
    if country != "EU":
        kwargs['country'] = country
    locations = locations.filter(**kwargs)

    return render_to_response(
        'all_locations.html', 
        {
            'locations' : locations,
        },
        context_instance=RequestContext(request)
    )  

def location(request, country, slug=None):

    location = get_object_or_404(models.Location, country=country, slug=slug)
    # sub_location = models.locations.objects.sub_locations(country=country, geo1=geo1,geo2=geo2,geo3=geo3,geo4=geo4, limit=None, sort=sub_location_sort)
    kwargs = {}
    for p in location.get_ancestors():
        kwargs[p.geo_type] = p.name
    location_recipients = models.Recipient.objects.all()[:10]
    # location_recipients = location_recipients.filter(**kwargs)


    sub_locations = location.get_children()
    
    
    return render_to_response(
    'location.html', 
    {
    'location' : location,
    'location_recipients' : location_recipients,
    'sub_locations' : sub_locations,
    # 'sub_location_sort' : sub_location_sort,
    # 'selected_year' : int(year),        
    },
    context_instance=RequestContext(request)
    )  
  

  
