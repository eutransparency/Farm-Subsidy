from django.conf.urls.defaults import *
from web import settings
from data import countryCodes
# Uncomment the next two lines to enable the adminn:
# from django.contrib import admin
from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'', include('data.urls')),
    (r'^news/', include('features.urls')),
    (r'', include('frontend.urls', namespace="my_account")),
    (r'', include('search.urls')),
    (r'', include('countryinfo.urls')),
    (r'', include('graphs.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    
    (r'lists/', include('listmaker.urls')),
    (r'^accounts/', include('registration.urls')),

    (r'^api/', include('web.api.urls')),
    )

if settings.DEBUG:
  urlpatterns += patterns('django.views',
      (r'^media/(?P<path>.*)$', 'static.serve',
      {'document_root': settings.MEDIA_ROOT}),

)
