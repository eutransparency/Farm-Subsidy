from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
   url(r'^login', views.login, name='login'),
   url(r'^logout', views.logout, name='logout'),
   url(r'^myaccount/$', views.dashboard, name='dashboard'),
   url(r'^myaccount/annotations/$', views.annotations, name='annotations'),
   url(r'^myaccount/lists/$', views.lists, name='lists'),
   url(r'^myaccount/account/$', views.account, name='account'),
 )