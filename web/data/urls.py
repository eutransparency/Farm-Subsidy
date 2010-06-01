from django.conf.urls.defaults import *
from indexer import countryCodes
import views


countries = []
for country in countryCodes.country_codes():
  countries.append(country)
  countries.append(country.lower())

countries = "|".join(countries)


urlpatterns = patterns('data.views',
  url(r'^$', 'home', name='home'),
  url(r'^(?P<country>%s)/$' % countries, 'country', name='country'),
  url(r'^(?P<country>%s)/(?P<year>\d+)/$' % countries, 'country', name='country_year'),
  url(r'^(?P<country>%s)/recipient/(?P<recipient_id>[^/]+)/(?P<name>(.*))/' % countries, 'recipient', name='recipient_view' ),
  
  url(r'^(?P<country>%s)/location/(?P<geo1>[^/]+)/(?P<geo2>[^/]+)/(?P<geo3>[^/]+)/(?P<geo4>[^/]+)' % countries, 'location', name='location_view' ),
  url(r'^(?P<country>%s)/location/(?P<geo1>[^/]+)/(?P<geo2>[^/]+)/(?P<geo3>[^/]+)' % countries, 'location', name='location_view' ),
  url(r'^(?P<country>%s)/location/(?P<geo1>[^/]+)/(?P<geo2>[^/]+)' % countries, 'location', name='location_view' ),
  url(r'^(?P<country>%s)/location/(?P<geo1>[^/]+)' % countries, 'location', name='location_view' ),
  url(r'^(?P<country>%s)/location' % countries, 'location', name='location_view' ),
  
  url(r'^(?P<country>%s)/scheme/(?P<globalschemeid>[^/]+)' % countries, 'scheme', name='scheme_view' ),
  url(r'^(?P<country>%s)/browse/(?P<browse_type>(recipient|scheme|location))/(?P<year>\d+)/(?P<sort>(amount|name))' % countries, 'browse', name='browse' ),
  url(r'^(?P<country>%s)/browse/(?P<browse_type>(recipient|scheme|location))' % countries, 'browse', name='browse_default' ),
  
)


  # url(r'^(?P<country>%s)/$' % countries, 'country', name='country'),