from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.conf import settings
from feeds.models import *
from tagging.models import TaggedItem
from misc.helpers import country_template, CachedCountQuerySetWrapper
from web.countryinfo.transparency import transparency_score
from web.countryinfo.load_info import load_info
from data import countryCodes
import context_processors
import models

from frontend.models import Profile
from frontend.forms import DataAgreementForm

DEFAULT_YEAR = settings.DEFAULT_YEAR

@cache_page(60 * 60 * 24)
def home(request):

  # ip_country = request.session.get('ip_country', 'GB')
  # top_for_ip = models.Recipient.objects.top_recipients(country=ip_country)

  top_eu = models.Recipient.objects.top_recipients()[:10]
  
  latest_annotations = Comment.objects.all().order_by('-submit_date')[:5]
  
  return render_to_response(
    'home.html', 
    {
    'top_eu' : top_eu,
    'is_home' : True,
    # 'top_for_ip' : top_for_ip,
    'latest_annotations' : latest_annotations,
    },
    context_instance=RequestContext(request)
  )  

def countries(request):
    countries = []
    for country in countryCodes.country_codes():
        countries.append(countryCodes.country_codes(country)) 
        
    return render_to_response('countries.html', 
    {'countries' : countries},
    context_instance=RequestContext(request))
        
@cache_page(60 * 60 * 4)
def country(request, country, year=DEFAULT_YEAR):
    """
    Provides all the variables for the country pages at, for example "/AT/"

    Querysets:

    - `top_recipients` Gets n recipients, sorted by total amount for a given year
    - `years` The years that we have data for a given country

    """
    country = country.upper()

    years_max_min = models.CountryYear.objects.year_max_min(country)

    years = models.CountryYear.objects.filter(country=country)
    
    top_recipients = models.Recipient.objects.top_recipients(country=country, year=year)[:5]
    top_schemes = models.SchemeYear.objects.top_schemes(country, year=year)[:5]
    top_locations = models.Location.get_root_nodes().filter(country=country, year=year).order_by('-total')[:5]
    
    #get transparency score
    transparency = None
    if country != "EU":
      transparency = transparency_score(country)
    
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
        'years' : years,
        'selected_year' : int(year),
        'years_max_min' : years_max_min,
    },
    context_instance=RequestContext(request)
    )


def recipient(request, country, recipient_id, name):
  """
  View for recipient page.
  
  - `country` ISO country, as defined in countryCodes
  - `recipient_id` is actually a globalrecipientidx in the date
  
  """
  # settings.DISABLE_QUERYSET_CACHE_QUERYSET_CACHE = True
  # # settings.DISABLE_QUERYSET_CACHE = False
  # 
  # from johnny.middleware import QueryCacheMiddleware
  # QueryCacheMiddleware().unpatch()
  
  
  country = country.upper()

  recipient = models.Recipient.objects.get(globalrecipientidx=recipient_id)
  
  payments = models.Payment.objects.select_related().filter(recipient=recipient_id).order_by('year', 'amounteuro')
  expanded = request.GET.get('expand', False)
  if not expanded:
      # Hack to stop *all* payments getting displayed, when there are sometimes
      # many 'trasactions' per year in the same scheme.
      all_payments = payments.values('year','scheme',).annotate(amounteuro=Sum('amounteuro')).order_by('year', 'amounteuro')
      payments = []
      for payment in all_payments:
          p = models.Payment()
          p.year = payment['year']
          p.amounteuro = payment['amounteuro']
          s = models.Scheme.objects.get(pk=payment['scheme'])
          p.scheme = s
          payments.append(p)

  recipient_total = recipient.total
  payment_years = list(set(payment.year for payment in payments))

  
  payment_schemes = []
  for payment in payments:
      for scheme in payment.scheme.schemetype_set.all():
          payment_schemes.append(scheme.scheme_type)
  
  try:
      georecipient = models.GeoRecipient.objects.get(pk=recipient.pk)
      closest = models.GeoRecipient.objects.distance(georecipient.location).order_by('distance')[:5]
  except:
      closest = None

  years_max_min = models.CountryYear.objects.year_max_min(country)
  # print years_max_min
  return render_to_response(
    'recipient.html', 
    {
        'recipient' : recipient,
        'payments' : payments,
        'recipient_total' : recipient_total,
        'payment_years' : payment_years,
        'has_direct' : 1 in payment_schemes,
        'has_indirect' : 2 in payment_schemes,
        'has_rural' : 3 in payment_schemes,
        'first_year' : 0,
        'years_max_min' : years_max_min,
        'expanded' : expanded,
        'closest' : closest,
    },
    context_instance=RequestContext(request)
  )  

@cache_page(60 * 60 * 4)
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
        .order_by('-scheme_total')
    
    # top_recipients.count = 1
    # top_recipients.__len__ = 1
    top_recipients = CachedCountQuerySetWrapper(top_recipients)
    
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

@cache_page(60 * 60 * 4)
def all_locations(request, country, year=0):
    locations = models.Location.objects.all()
    kwargs = {
        'geo_type' : 'geo1',
        'year' : year,
        }
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

# @cache_page(60 * 60 * 4)
def location(request, country, slug=None, year=0):
    """
    Single location object. This is a node in the tree, and could have
    children.
    
    If children are found, we call them 'sub locations' and display a list of
    them.
    """
    print year
    
    location = get_object_or_404(models.Location, country=country, slug=slug, year=year)

    # kwargs = {}
    # for p in location.get_ancestors():
    #     kwargs[p.geo_type] = p.name
    location_recipients = models.Recipient.objects.recipents_for_location(location, year=year).order_by('-total')[:10]

    sub_locations = location.get_children()
    
    years_max_min = models.CountryYear.objects.year_max_min(country)

    return render_to_response(
        country_template('location.html', country), 
        {
            'location' : location,
            'location_recipients' : location_recipients,
            'sub_locations' : sub_locations,
            'years_max_min' : years_max_min,
        },
        context_instance=RequestContext(request)
    )  


@login_required
def download(request, data_file=None):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()


    if profile.data_agreement == False:
        request.notifications.add("Please agree to the following licence before downloading the data")
        return HttpResponseRedirect(reverse('data_agreement_form'))

    if data_file:
        download_file = get_object_or_404(DataDownload, pk=data_file)
        f = open(download_file.file_path)
        file_mimetype = mimetypes.guess_type(download_file.file_path)
        response = HttpResponse(FileWrapper(f), content_type=file_mimetype[0])
        response['Content-Disposition'] = 'attachment; filename="%s"' % \
                        download_file.file_path.split('/')[-1]
        return response

    files = models.DataDownload.objects.filter(public=True)
    return render_to_response(
      'downloads.html', 
      {
      'files' : files,
      },
      context_instance=RequestContext(request)
    )


@login_required
def data_agreement_form(request):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.data_agreement:
            return HttpResponseRedirect(reverse('download'))
    except Profile.DoesNotExist:
        p = Profile(user=request.user)
        p.save()

    if request.POST:
        form = DataAgreementForm(request.POST, instance=profile)
        if form.is_valid():
            form.save() 
    else:
        form = DataAgreementForm(instance=profile)

    return render_to_response(
      'data_agreement_form.html', 
      {
      'form' : form,
      }, 
      context_instance=RequestContext(request)
    )
