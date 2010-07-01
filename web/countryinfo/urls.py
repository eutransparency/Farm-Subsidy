from django.conf.urls.defaults import *
import views


urlpatterns = patterns('',
    url(r'^stats/comapre',views.compare),
    url(r'^transparency/',views.transparency_list),
)