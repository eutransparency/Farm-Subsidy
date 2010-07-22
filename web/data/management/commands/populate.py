"""
Load the data from CSV files in to the database

"""
import os
import csv

import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from data.models import Recipient, Payment, Scheme
from django.conf import settings

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country', '-c', dest='country',
        help='ISO country name'),
    )
    help = 'Populate the database with a countries data.'
    
    def format_csv_path(self, data_type):
        path = "%s/data/csv/%s/%s.csv" % (
            settings.ROOT_PATH,
            self.country,
            data_type)
        if os.path.exists(path):
            return path
    
    def open_csv(self, path, field_names=None):
        class SKV(csv.excel):
            # like excel, but uses semicolons
            delimiter = ";"
        csv.register_dialect("SKV", SKV)        
        f = csv.DictReader(open(path, 'U'), dialect='SKV', fieldnames=field_names)
        return f
    
    def recipients(self):
        print "Indexing Recipients"
        field_names = (
            'recipientid',
            'recipientidx',
            'globalrecipientid',
            'globalrecipientidx',
            'name',
            'address1',
            'address2',
            'zipcode',
            'town',
            'countryrecipient',
            'countrypayment',
            'geo1',
            'geo2',
            'geo3',
            'geo4',
            'geo1nationallanguage',
            'geo2nationallanguage',
            'geo3nationallanguage',
            'geo4nationallanguage',
            'lat',
            'lng',
            'total',
        )
        
        c = self.open_csv(self.format_csv_path('recipients'), field_names)
        for line in c:
            if c.line_num != 1:
                try:
                    if len(line['zipcode']) < 12:
                      r = Recipient()
                      line['total'] = line['lat'] = line['lng'] = 0
                      r.__dict__.update(line)
                      r.save()
                except Exception, e:
                  print e
                  print c.line_num

    def schemes(self):
        print "Indexing Schemes"
        field_names = (
            'globalschemeid',
            'namenationallanguage',
            'nameenglish',
            'budgetlines8digit',
            'countrypayment',
            'total',
        )
        
        c = self.open_csv(self.format_csv_path('schemes'), field_names)
        for line in c:
            if c.line_num != 1:
                s = Scheme()
                line['total'] = 0
                s.__dict__.update(line)
                s.save()
        
    def payments(self):
        print "Indexing Payments"
        field_names = (
            'paymentid',
            'globalpaymentid',
            'globalrecipientid',
            'recipient_id',
            'scheme_id',
            'amounteuro',
            'amountnationalcurrency',
            'year',
            'countrypayment',
        )
        
        c = self.open_csv(self.format_csv_path('payments'), field_names)
        for line in c:
            try:
              if c.line_num != 1:
                  p = Payment()
                  if not line['amountnationalcurrency']:
                      line['amountnationalcurrency'] = line['amounteuro']
                  p.__dict__.update(line)
                  p.save()
            except Exception, e:
              print e
    
    def handle(self, **options):
        self.country = options.get('country')
        
        self.recipients()
        self.schemes()
        self.payments()
        
