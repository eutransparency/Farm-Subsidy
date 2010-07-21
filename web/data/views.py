from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Sum, Count
from django.conf import settings
from feeds.models import *
from tagging.models import TaggedItem
from misc.helpers import country_template
from web.countryinfo.transparency import transparency_score, transparency_list
from web.countryinfo.load_info import load_info
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
    'is_home' : True,
    'top_for_ip' : top_for_ip,
    },
    context_instance=RequestContext(request)
  )  

def countries(request):
    countries = []
    for country in countryCodes.country_codes():
        countries.append(countryCodes.country_codes(country)) 
        
    return render_to_response('countries.html', {'countries' : countries},context_instance=RequestContext(request))
        

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
    
    #get transparency score
    transparency = None
    if country != "EU":
      transparency = transparency_score(country)
    # print top_regions
    
    #get the most recent news story
    latest_news_item = False    
    news_items = TaggedItem.objects.get_by_model(FeedItems, Tag.objects.filter(name=country))
    news_items = news_items.order_by("-date")
    if news_items:
        latest_news_item = news_items[0]

    #get country stats
    stats_info = load_info(country)

    return render_to_response(
    country_template('country.html', country),
    {
        'top_recipients' : top_recipients,
        'top_schemes' : top_schemes,
        'top_locations' : top_locations,
        'transparency' : transparency,
        'latest_news_item': latest_news_item,
        'stats_year': settings.STATS_YEAR,
        'stats_info': stats_info,
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
  payment_schemes = list(set(payment.scheme.globalschemeid for payment in payments))
  
  
  return render_to_response(
    'recipient.html', 
    {
    'recipient' : recipient,
    'payments' : payments,
    'recipient_total' : recipient_total,
    'payment_years' : payment_years,
    'has_direct' : 'LU1' in payment_schemes,
    'has_indirect' : 'LU2' in payment_schemes,
    'has_rural' : 'LU3' in payment_schemes,
    'first_year' : payment_years[0],
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
        country_template('recipient.html', country),
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
        country_template('all_schemes.html', country),
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
        payment__scheme=globalschemeid)\
        .annotate(scheme_total=Sum('payment__amounteuro'))\
        .order_by('-scheme_total')\
        .distinct()

    return render_to_response(
        country_template('scheme.html', country), 
        {
            'scheme' : scheme,
            'top_recipients' : top_recipients,
        },
        context_instance=RequestContext(request)
    )  
  

def browse(request, country):
    """
    Browse recipients, sorted / filtered by various things using django-filter
    """

    recipients = models.Recipient.objects.filter(total__isnull=False)\
        .distinct()\
        .order_by('-total')

    if country != "EU":
        recipients = recipients.filter(countrypayment=country)
  
    return render_to_response(
        country_template('browse.html', country),
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
        country_template('all_locations.html', country),
        {
            'locations' : locations,
        },
        context_instance=RequestContext(request)
    )  

def location(request, country, slug=None):

    location = get_object_or_404(models.Location, country=country, slug=slug)
    kwargs = {}
    for p in location.get_ancestors():
        kwargs[p.geo_type] = p.name
    location_recipients = models.Recipient.objects.all()[:10]
    location_recipients = models.Recipient.objects.recipents_for_location(location)

    sub_locations = location.get_children()
    
    
    return render_to_response(
        country_template('location.html', country), 
        {
            'location' : location,
            'location_recipients' : location_recipients,
            'sub_locations' : sub_locations,
        },
        context_instance=RequestContext(request)
    )  
  

  
