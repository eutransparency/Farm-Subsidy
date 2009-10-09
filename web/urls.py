from django.conf.urls.defaults import *
from web import settings
from indexer import countryCodes
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'', include('web.data.urls')),
    (r'search', include('web.search.urls')),
    (r'', include('web.feeds.urls')),
    # (r'', include('farmsubsidy.web.countryinfo.urls')),
    (r'', include('web.graphs.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # (r'', include('farmsubsidy.web.customlists.urls')),
    # (r'^api/', include('farmsubsidy.web.api.urls')),
    (r'^accounts/', include('registration.urls')),
    # (r'^profiles/', include('profiles.urls')),
    )

if settings.DEBUG:
  urlpatterns += patterns('django.views',
      (r'^media/(?P<path>.*)$', 'static.serve',
      {'document_root': settings.MEDIA_ROOT}),

  )
