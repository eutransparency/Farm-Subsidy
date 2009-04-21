from django.conf.urls.defaults import *

import views




urlpatterns = patterns('',
   url(r'^xml/test/', views.test),
   url(r'^get_recipient/(\d+)/$', views.get_recipient),
 )