import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from haystack import backend, site

from data.models import Recipient, Payment, Scheme



class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country', '-c', dest='country',
            help='ISO country name'),
    )
    help = 'Normalizeation scripts for the farm data'

    def handle(self, **options):
        back = backend.SearchBackend()
        index = site.get_index(Recipient)

        index_data = Recipient.objects.filter(countrypayment=options['country'])
        print "now indexing"
        back.update(index, index_data)
