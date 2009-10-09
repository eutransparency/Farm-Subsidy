from django.conf.urls.defaults import *
from indexer import countryCodes
import views


urlpatterns = patterns('search.views',
  url(r'', 'results', name='results'),
)