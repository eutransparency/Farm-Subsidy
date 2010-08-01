from django.http import HttpResponse
from django.template import RequestContext
from django.template import Context, Template
from django.template.loader import render_to_string, select_template
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.shortcuts import render_to_kml

from vectorformats.Formats import Django, GeoJSON

from data.models import Recipient, GeoRecipient, Payment

def geo(request, lng, lat, format='kml'):
    lng, lat = map(float, (lng, lat,))
    limit = request.GET.get('limit', 10)
    offset = request.GET.get('offset', 0)
    

    base_qs = GeoRecipient.objects.distance(Point((lng, lat))).order_by('-distance')
    
    if format == 'kml':
        qs = base_qs.kml()
    if format == 'json':
        qs = base_qs.json()
        print "json"
    
    qs = qs[offset:limit]
    
    djf = Django.Django(geodjango="geometry", properties=['city', 'state'])
    geoj = GeoJSON.GeoJSON()
    string = geoj.encode(djf.decode(qs))
    print string
    
    # return render_to_kml('kml.html', {'qs' : qs}) 

