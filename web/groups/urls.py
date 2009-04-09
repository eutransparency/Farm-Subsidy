from django.conf.urls.defaults import *
from web.groups import views as groups


urlpatterns = patterns('',
  url(r'^cart/test$',
    view=groups.test),
    )

