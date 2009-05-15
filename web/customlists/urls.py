from django.conf.urls.defaults import *
from web.customlists import views


urlpatterns = patterns('',
    url(r'^lists/$', view=views.main, name='main_list_view'),
    url(r'^lists/add_recipient', view=views.add_to_list),
    url(r'^lists/ajax/list$', view=views.list_view_ajax, name='ajax_list_view'),    
    url(r'^lists/ajax/(?P<action>add|del)/(?P<docid>.*)$', view=views.ajax_add_del, name='ajax_add_del'),
  )


