from django.conf.urls.defaults import *
from graphs import graphlib


urlpatterns = patterns('',
    # url(r'^graph',graphlib.make_fig),
    url(r'^graph/(?P<type>.*)$',graphlib.make_fig,  name="graph"),
)