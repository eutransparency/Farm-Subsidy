"""
Various bits to clean upthe data

"""
from optparse import make_option

import django
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, backend, models
import treebeard

from data.models import Recipient


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country', '-c', dest='country',
        help='ISO country name'),
    )
    help = 'Normalizeation scripts for the farm data'
    
    def handle(self, **options):
        self.country = options.get('country')
        if not self.country:
            raise Exception('A valid country is required')
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT geo1, geo2, geo3, geo4
            FROM data_recipient
        """)
        print cursor.fetchall()