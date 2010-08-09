import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, backend, models


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--drop', '-d', dest='drop',
        help='Drop Indexes'),
    )
    option_list = BaseCommand.option_list + (
        make_option('--create', '-c', dest='create',
        help='Create Indexes'),
    )
    help = 'Create or Drop indexes'
    
    
    def __init__(self):
        self.indexes = {
            'data_payment' : [
                    ('data_payment_amounteuro', 'amounteuro'),
                    ('data_payment_countrypayment', 'countrypayment'),
                    ('data_payment_globalrecipientidx', 'globalrecipientidx'),
                    ('data_payment_globalschemeid', 'globalschemeid'),
                    ('data_payment_year', 'year'),
                ],
            'data_recipient' : [
                    ('data_recipient_countrypayment', 'countrypayment'),
                    ('data_recipient_countryrecipient', 'countryrecipient'),
                    ('data_recipient_total', 'total'),
                ]
        }
    
    def handle(self, **options):
        print options
        