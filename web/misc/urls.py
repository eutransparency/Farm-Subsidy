from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
   url(r'^login', views.login, name='login'),
 )