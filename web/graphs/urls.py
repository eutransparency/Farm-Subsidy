from django.conf.urls.defaults import *
from graphs import graphlib


urlpatterns = patterns('',
    # url(r'^graph',graphlib.make_fig),
    # url(r'^graph/(?P<type>.*)$',graphlib.make_fig,  name="graph"),
    url(r'^graph/country_years/(?P<country>.*)$',graphlib.country_years,  name="country_graph"),
    url(r'^graph/recipient/(?P<recipient_id>.*)$',graphlib.recipient,  name="recipient_graph"),
    url(r'^graph/scheme/(?P<globalschemeid>.*)$',graphlib.scheme_years,  name="scheme_graph"),
)