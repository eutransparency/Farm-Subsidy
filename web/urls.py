from django.conf.urls.defaults import *
from web import settings
from data import countryCodes
# Uncomment the next two lines to enable the adminn:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'', include('data.urls')),
    (r'^news/', include('features.urls')),
    (r'', include('misc.urls')),
    (r'', include('search.urls')),
    (r'', include('countryinfo.urls')),
    (r'', include('graphs.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    
    (r'', include('web.customlists.urls')),
    (r'^accounts/', include('registration.urls')),

    # (r'^api/', include('farmsubsidy.web.api.urls')),
    )

if settings.DEBUG:
  urlpatterns += patterns('django.views',
      (r'^media/(?P<path>.*)$', 'static.serve',
      {'document_root': settings.MEDIA_ROOT}),

)
