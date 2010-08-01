"""
Main controler for the API. This is, annoyingly, split in to two areas: 

1) The django-piston controled stuff, making an API out of the models and 
2) Normal django views, for things like KML and CSV output that piston can't 
   support.

Note, making a piston emmiter for these might work, but it's easier to do it
this way at the moment
"""

from django.conf.urls.defaults import *
from piston.resource import Resource
from web.api.handlers import *
from web.data import countryCodes

import views

def v1_country_url(pattern, *args, **kwargs):
    """
    Wrap url() with a URL that always prepends a list of countries (upper and
    lower case)
    """
    countries = countryCodes.country_codes()
    countries = "|".join(countries)
    return url(r'^v1/(?i)(?P<country>%s)/%s' % (countries, pattern), *args, **kwargs)


recipient_handler = Resource(RecipientHandler)
search_handler = Resource(SearchHandler)
countryoverview_handler = Resource(CountryOverviewHandler)


# API v1 URLS
urlpatterns = patterns('',
   url(r'^v1/recipient/(?P<globalrecipientidx>[^/]+)/', recipient_handler),
   url(r'^v1/search/(?P<term>[^/]+)/', search_handler),
   v1_country_url('info/', countryoverview_handler),
   
   # Geo API
   url(r'v1/geo/(?P<lng>[^/]+),(?P<lat>[^/]+)\.(?P<format>[^/]+)', views.geo),
   
)