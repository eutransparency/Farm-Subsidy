from django.conf.urls.defaults import *
import views


urlpatterns = patterns('',
    url(r'^stats/comapre',views.compare),
)