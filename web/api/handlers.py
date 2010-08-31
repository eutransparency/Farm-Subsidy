from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from piston.handler import BaseHandler
from piston.utils import throttle
from haystack.query import SearchQuerySet
from haystack import backend

from data.models import Recipient, GeoRecipient, Payment
from countryinfo.load_info import load_info

import emitters

def required_args(request, args):
    for arg in args:
        try:
            request.GET[arg]
        except:
            raise ValueError('%s is required' % arg)

def add_kml_to_recipient(recipient):
    # Try to get KML for this recipient
    geos = recipient.georecipient_set.all()
    if len(geos) > 0:
        recipient.kml = geos.kml()[0].location.kml
    return recipient


class RecipientHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Recipient
    exclude = ('recipientidx','recipientid',)

    @throttle(30, 60)
    def read(self, request):
        required_args(request, ['id'])

        recipient = Recipient.objects.select_related().get(globalrecipientidx=request.GET['id'])
        payments = recipient.payment_set.all()
    
        if request.GET.get('format') == 'kml':
            recipient = add_kml_to_recipient(recipient)

        res =  recipient.__dict__
        res['payments'] = payments
        return res

class SearchHandler(BaseHandler):
    allowed_methods = ('GET',)

    @throttle(30, 60)
    def read(self, request):
        required_args(request, ['term',])

        sqs = SearchQuerySet()
        sqs = sqs.auto_query(request.GET['term']).load_all()
        sqs = sqs.exclude(name__startswith="unknown")
        
        results = {}
        for i,result in enumerate(sqs):
            if request.GET.get('format') == 'kml':
                r = add_kml_to_recipient(result.object).__dict__
            else:
                r = result.object
            results[i] = r

        return results


class CountryOverviewHandler(BaseHandler):
    allowed_methods = ('GET',)

    @throttle(30, 60)
    def read(self, request):
        required_args(request, ['country',])
        try:
            results = load_info(request.GET['country'])
            results['year'] = settings.STATS_YEAR
        except:
            results = {}
        
        return results
