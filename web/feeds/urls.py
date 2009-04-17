from django.conf.urls.defaults import *
from feeds import views as feeds_views


urlpatterns = patterns('',
    url(r'^blog/(?P<tag>.*)',feeds_views.feed_list,{'category' : 'Blog'},),
    url(r'^news/(?P<tag>.*)',feeds_views.feed_list,{'category' : 'News'},)
)