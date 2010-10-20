import django
from optparse import make_option
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
        back = backend.SearchBackend()
        
        if options['index_type'] == 'feature':
                    feature_index = site.get_index(Feature)
                    features = Feature.objects.filter(published=True)
                    back.update(feature_index, features)
        else:
            recipient_index = site.get_index(Recipient)
            location_index = site.get_index(Location)

            index_data = Recipient.objects.filter(countrypayment=options['country'])
            locations = Location.objects.filter(country=options['country'])

            print "now indexing Recipients"
            back.update(recipient_index, index_data)

            print "now indexing Location"
            back.update(location_index, locations)

