from django.conf.urls.defaults import *
from feeds import FeaturesFeed
import views

urlpatterns = patterns('',
   url(r'^$', views.feature_list, name="feature_list"),
   url(r'^feed/$', FeaturesFeed(), name="feature_feed"),
   url(r'^(?P<slug>[-\w]+)/$', views.feature_detail, name="feature_detail"),
   )