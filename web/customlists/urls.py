from django.conf.urls.defaults import *
from web.customlists import views


urlpatterns = patterns('',
    url(r'^lists/$', view=views.main, name='main_list_view'),
    url(r'^lists/add_recipient', view=views.add_to_list),
  )

