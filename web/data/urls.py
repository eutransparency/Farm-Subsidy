from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from data import countryCodes
import views

def country_url(pattern, *args, **kwargs):
    """
    Wrap url() with a URL that always prepends a list of countries (upper and
    lower case)
    """
    countries = countryCodes.country_codes()
    countries = "|".join(countries)
    return url(r'^(?i)(?P<country>%s)/%s' % (countries, pattern), *args, **kwargs)

countries = ''

urlpatterns = patterns('data.views',
  url(r'^$', 'home', name='home'),
  url(r'countries/', 'countries', name='countries' ),    
  country_url(r'$', 'country', name='country'),
  country_url(r'(?P<year>\d+)/$', 'country', name='country_year'),
  country_url(r'recipient/(?P<recipient_id>[^/]+)/(?P<name>(.*))/', 'recipient', name='recipient_view' ),

  # Locations
  country_url(r'location/(?P<year>\d+)/(?P<slug>([^\d]+))/$', 'location', name='location_view' ),
  # country_url(r'location/(?P<slug>([^\d]+))/$', 'location', name='location_view' ),

  country_url(r'location/(?P<year>\d+)/$', 'all_locations', name='all_locations' ),
  # country_url(r'location/$', 'all_locations', name='all_locations' ),

  # Schemes
  country_url(r'scheme/$', 'all_schemes', name='all_schemes'),
  country_url(r'scheme/(?P<globalschemeid>[^/]+)/(?P<name>(.*))/', 'scheme', name='scheme_view'),


  country_url(r'browse/', 'browse', name='browse' ),
  country_url(r'browse/(?P<browse_type>(recipient|scheme|location))/(?P<year>\d+)/(?P<sort>(amount|name))', 'browse', name='browse' ),
  country_url(r'browse/(?P<browse_type>(recipient|scheme|location))', 'browse', name='browse_default' ),
  
  
  # downloads
  url(r'^getthedata/download$', 'download', name='download'),
  url(r'^getthedata/download/(?P<data_file>\d+)$', 'download', name='download_file'),
  url(r'^getthedata/data_agreement$', 'data_agreement_form', name='data_agreement_form'),    


  url(r'^heatmap$', 'heatmap', name='heatmap'),
  url(r'^tiles/(?P<color_scheme>\w+)/(?P<zoom>\d+)/(?P<x>\d+),(?P<y>\d+).png$','serve_tile', name='serve_tile',),
)
