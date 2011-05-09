# -*- coding: utf-8 -*-
import django
from django.conf import settings
from optparse import make_option
from django.db import connection
from django.core.management.base import BaseCommand, CommandError

from haystack import backend, site

from data.models import Recipient, Payment, Scheme, Location
from features.models import Feature



class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country', '-c', dest='country',
            help='ISO country name'),
        make_option('--type', '-t', dest='index_type',
            help='Type of data to index'),
    )
    help = 'Normalizeation scripts for the farm data'

    def handle(self, **options):

        
        if options['index_type'] == 'feature':
                    feature_index = site.get_index(Feature)
                    features = Feature.objects.filter(published=True)
                    back.update(feature_index, features)
        else:
            recipient_index = site.get_index(Recipient)
            location_index = site.get_index(Location)
            
            if options['country']:
                index_data = Recipient.objects.select_related().filter(countrypayment=options['country'], total__gt=1000).only('name', 'geo1', 'geo2', 'geo3', 'geo4', 'zipcode', 'countrypayment')
                locations = Location.objects.filter(country=options['country'])
            else:
                raise ValueError('Country is required')
            
            settings.HAYSTACK_XAPIAN_PATH = "%s-%s" % (settings.HAYSTACK_XAPIAN_PATH, options['country'])
            back = backend.SearchBackend()
            print "now indexing Recipients"
            back.update(recipient_index, index_data)

            print "now indexing Location"
            back.update(location_index, locations)
        connection.close()
