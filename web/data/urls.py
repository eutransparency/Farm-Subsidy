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
)