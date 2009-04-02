from django.conf.urls.defaults import *
from web import settings
from farmsubsidy.indexer import countryCodes
from web.basic.blog import feeds as blogfeeds
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


feeds = {
    'latest': blogfeeds.BlogPostsFeed,
}



urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^blog/', include('web.basic.blog.urls')),    
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    )


countries = "|".join(countryCodes.countryCodes())

urlpatterns += patterns('web.data.views',
    (r'^$', 'home'),
    (r'^search', 'search'),
    (r'^(?P<country>%s)/browse/(?P<browsepath>[^$]+)' % countries, 'countrybrowse'),    
    (r'^(?P<country>%s)/recipient/(?P<recipient_id>[^/]+)' % countries, 'recipient'),
    (r'^(%s)' % countries, 'country'),
    )

urlpatterns += patterns('django.views',
     (r'^media/(?P<path>.*)$', 'static.serve',
     {'document_root': settings.MEDIA_ROOT}),

)