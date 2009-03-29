from django.conf.urls.defaults import *
from web import settings
from farmsubsidy.indexer import countryCodes
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),

    )


countries = "|".join(countryCodes.countryCodes())

urlpatterns += patterns('web.data.views',
    (r'^data/(?P<country>)/', 'test'),
    (r'^$', 'home'),
    (r'^search', 'search'),
    (r'^(?P<country>%s)/browse/(?P<browsepath>[^$]+)' % countries, 'countrybrowse'),    
    (r'^(%s)' % countries, 'country'),
    (r'^data/recipient/(?P<recipient_id>[^/]+)', 'recipient'),
    )

urlpatterns += patterns('django.views',
     (r'^media/(?P<path>.*)$', 'static.serve',
     {'document_root': settings.MEDIA_ROOT}),

)