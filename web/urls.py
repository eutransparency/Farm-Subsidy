from django.conf.urls.defaults import *
from web import settings
from farmsubsidy.indexer import countryCodes
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'', include('farmsubsidy.web.data.urls')),
    (r'', include('farmsubsidy.web.feeds.urls')),
    (r'', include('farmsubsidy.web.graphs.urls')),
    (r'', include('farmsubsidy.web.customlists.urls')),
    (r'^api/', include('farmsubsidy.web.api.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    )

urlpatterns += patterns('django.views',
     (r'^media/(?P<path>.*)$', 'static.serve',
     {'document_root': settings.MEDIA_ROOT}),

)