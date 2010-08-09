# -*- coding: utf-8 -*-
"""
This script takes a file name and a table name along with other database
connection settings.

It then uses Postgresql's server side COPY command to import the CSV file.

Note, that the postgres user use to connect must be a superuser.

"""

import sys
import os
sys.path.append('..')

from optparse import OptionParser
import os.path
from django.db import connection, backend, models

import psycopg2

parser = OptionParser()
parser.add_option("-c", "--country", dest="country",
                  help="country to COPY",
                  metavar="COUNTRY")

parser.add_option("-t", "--data_type", dest="data_type",
                  help="Type of data to index, scheme, recpient, payment",
                  metavar="TABLE")

parser.add_option("-r", "--reindex", dest="reindex",
                  action="store_true",
                  help="Reindex all tables",
                  metavar="INDEX")

(options, args) = parser.parse_args()

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'

import django
from django.conf import settings


class Copier():
    def __init__(self, options):
        
        cursor = connection.cursor()
        
        self.country = options.country
        print self.country
        
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
    
    def file_paths(self):
        return ""
    
    def drop_indexes(self):
        if self.table in self.indexes:
                
            for index in self.indexes[self.table]:
                print "dropping %s" % index
                sql = "DROP INDEX %s CASCADE;" % index
                try:
                    self.cur.execute(sql)
                except:
                    self.connect()
                    pass

    def create_indexes(self):
        if self.table in self.indexes:
                
            for index in self.indexes[self.table]:
                print "CREATING %s" % index
                sql = "CREATE INDEX %s;" % index

                self.cur.execute(sql)

    def copy_file(self):
        
        sql = """
            COPY %(table)s
            FROM '%(filename)s'
            DELIMITERS ';'
            CSV;
            COMMIT;
        """ % {
            'filename' : self.filename,
            'table' : self.table,
        }
        print "COPYING"
        #self.cur.execute(sql)
        self.create_indexes()


c = Copier(options)
c.copy_file()
