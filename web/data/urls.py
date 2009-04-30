from django.conf.urls.defaults import *
from web import settings
from farmsubsidy.indexer import countryCodes

countries = "|".join(countryCodes.countryCodes())


urlpatterns = patterns('web.data.views',
    url(r'^$', 'home'),
    url(r'^search', 'search'),
    url(r'^(?P<country>%s)/region/(?P<browsepath>[^$]+)' % countries, 'regionbrowse'),    
    url(r'^(?P<country>%s)/browse' % countries, 'countrybrowse', name='countrybrowse'),
    url(r'^(?P<country>%s)/recipient/(?P<recipient_id>[^/]+)' % countries, 'recipient', name='recipient_view' ),
    url(r'^(%s)' % countries, 'country'),
    )
