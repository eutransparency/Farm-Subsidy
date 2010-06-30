from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
   url(r'^$', views.feature_list, name="feature_list"),
   url(r'^(?P<slug>[-\w]+)/$', views.feature_detail, name="feature_detail"),
   )