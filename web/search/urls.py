from django.conf.urls.defaults import *
from data import countryCodes
from haystack.views import SearchView
import views
import forms

urlpatterns = patterns('search.views',
  url(r'^search/$', 'search', name='search'),
  url(r'^search/(.*)$', 'search', name='search'),
)