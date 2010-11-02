from django.conf.urls.defaults import *
from feeds import FeaturesFeed
import views

urlpatterns = patterns('',
   url(r'^$', views.news_home, name="news_home"),
   url(r'^features/$', views.feature_list, name="feature_list"),
   url(r'^media/$', views.media_list, name="media_list"),
   url(r'^feed/$', FeaturesFeed(), name="feature_feed"),
   url(r'^features/(?P<slug>[-\w]+)/$', views.feature_detail, name="feature_detail"),
   )