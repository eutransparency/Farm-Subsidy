import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, backend, models


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--drop', '-d', dest='drop',
        action="store_true",
        help='[drop|create]'),

        make_option('--create', '-c', dest='create',
        action="store_true",
        help='Create Indexes'),

        make_option('--table', '-t', dest='table',
        help='Table to interact with.  Assumes all if none provided'),
    )
    help = 'Create or Drop indexes'
    
    
    def __init__(self):

        self.cursor = connection.cursor()
        
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
    
    def drop(self):
        for table in self.tables:
            for index in self.indexes[table]:
                print "dropping %s" % index[0]
                sql = "DROP INDEX %s CASCADE; COMMIT;" % index[0]
                try:
                    self.cursor.execute(sql)
                except Exception, e:
                    print e
                    pass

    def create(self):
        for table in self.tables:
            for index in self.indexes[table]:
                print "dropping %s" % index[0]
                sql = """
                         BEGIN;
                         CREATE INDEX %s
                         ON %s
                         USING btree
                         (%s);
                         COMMIT;
                """ % (index[0], table, index[1])
                                
                try:
                    self.cursor.execute(sql)
                except Exception, e:
                    print e
                    pass
        
        
    
    def handle(self, **options):
        
        if options.get('table', False):
            self.tables = [options['table']]
        else:
            self.tables = ['data_payment', 'data_recipient',]
        
        if options.get('drop'):
            self.drop()
        if options.get('create'):
            self.create()
        
        


