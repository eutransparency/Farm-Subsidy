from django.conf.urls.defaults import *
from farmsubsidy.indexer import countryCodes
import views


countries = []
for country in countryCodes.country_codes():
  countries.append(country)
  countries.append(country.lower())

countries = "|".join(countries)


urlpatterns = patterns('data.views',
  url(r'^(?P<country>%s)/$' % countries, 'country', name='country'),
  url(r'^(?P<country>%s)/(?P<year>\d+)/$' % countries, 'country', name='country_year'),
  url(r'^(?P<country>%s)/recipient/(?P<recipient_id>[^/]+)' % countries, 'recipient', name='recipient_view' ),
  url(r'^(?P<country>%s)/scheme/(?P<globalschemeid>[^/]+)' % countries, 'scheme', name='scheme_view' ),
  url(r'^(?P<country>%s)/browse/(?P<browse_type>(recipient|scheme))' % countries, 'browse', name='browse_default' ),
  url(r'^(?P<country>%s)/browse/(?P<browse_type>(recipient|scheme))/(?P<year>\d+)/(?P<sort>(amount|name))' % countries, 'browse', name='browse' ),
  
)