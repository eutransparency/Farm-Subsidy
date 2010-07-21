import os

import django
from django.conf import settings
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, backend, models


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country', '-c', dest='country',),
        make_option('--table', '-t', dest='table',),
        )

    def __init__(self):
        self.cursor = connection.cursor()
    
    def format_file_name(self, table):
        path = "%s/data/csv/%s/%s.csv" % (settings.ROOT_PATH, self.country, table)
        path = "/" + "/".join(path.split('/')[2:])
        if os.path.exists(path):
            return path
        else:
            raise IOError('Data file not found at %s' % path)
    
    def copy(self):
        print self.filename
        sql = """
            DELETE FROM data_%(table)s WHERE countrypayment = '%(country)s';
        """ % {
            'country' : self.country,
            'table' : self.table,
        }
        self.cursor.execute(sql)
        
        sql = """
            COPY data_%(table)s (%(columns)s)
            FROM '%(filename)s'
            DELIMITERS ';'
            CSV;
            COMMIT;
        """ % {
            'filename' : self.filename,
            'columns' : self.columns,
            'table' : self.table,
        }
        print sql
        self.cursor.execute(sql)
    
    def get_columns(self):
        columns = {
            'scheme' : ['globalschemeid', 'namenationallanguage', 'nameenglish', 'budgetlines8digit', 'countrypayment'],
            'recipient' : ['recipientid', 'recipientidx', 'globalrecipientid', 'globalrecipientidx', 'name', 'address1', 'address2', 'zipcode', 'town', 'countryrecipient', 'countrypayment', 'geo1', 'geo2', 'geo3', 'geo4', 'geo1nationallanguage', 'geo2nationallanguage', 'geo3nationallanguage', 'geo4nationallanguage', 'lat', 'lng'],
            'payment' : ['paymentid', 'globalpaymentid', 'globalrecipientid', 'globalrecipientidx', 'globalschemeid', 'amounteuro', 'amountnationalcurrency', 'year', 'countrypayment'],
        }
        print ",".join(columns[self.table])
        return ",".join(columns[self.table])
        
    def handle(self, **options):
        
        if not options.get('country'):
            raise Exception('Please specify a country.')
        else:
            self.country = options['country']
        
        if options.get('table', False):
            self.tables = [options['table']]
        else:
            self.tables = ['recipient', 'scheme', 'payment',]

        for table in self.tables:
            self.table = table
            self.filename = self.format_file_name(table)
            self.columns = self.get_columns()
            self.copy()