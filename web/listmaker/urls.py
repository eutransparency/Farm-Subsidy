from django.conf.urls.defaults import *
import django.contrib.auth.views as auth_views

import views as list_views
import forms

urlpatterns = patterns('',
   url(r'^lists/$',list_views.lists_home, name='lists_home'),
   url(r'^lists/edit/(?P<list_id>\d+)/$',list_views.manage_lists, name='edit_list'),
   url(r'^lists/activate/$',list_views.activate, name='activate_list'),
   url(r'^lists/deactivate/$',list_views.deactivate, name='deactivate_list'),
   url(r'^lists/save/$',list_views.manage_lists, name='save_list'),
   url(r'^lists/mylists$',list_views.my_lists,),
   url(r'^lists/(?P<list_id>\d+)/$',list_views.list_view, name="list_detail"),
   url(r'^lists/edit_items/(?P<list_id>\d+)/$',list_views.edit_list_items, name="edit_list_items"),
   
   # Ajax calls

   # List Management stuff
   url(r'^lists/item/add/$',list_views.add_remove_item, name='list_item_add'),
  
   )