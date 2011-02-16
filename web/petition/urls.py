from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
   url(r'', views.sign, name='sign'),
   url(r'^/thanks', views.sign_thanks, name='sign_thanks'),
 )