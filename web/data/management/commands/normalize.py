# -*- coding: utf-8 -*-
"""
Various bits to clean upthe data

"""
import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from data.models import Recipient
from django.db import connection, backend, models


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country', '-c', dest='country',
        help='ISO country name'),
    )
    help = 'Normalizeation scripts for the farm data'
    
    def totals(self):
        """
        Updates the 'total' column on every recipient and creates the values in
        'recipient totals'
        """
        
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM recipient_totals WHERE country=%(country)s;
            INSERT INTO recipient_totals  
            SELECT globalrecipientidx, SUM(amounteuro) as total, %(country)s
            FROM data_payment 
            WHERE countrypayment=%(country)s
            GROUP BY globalrecipientidx;
            COMMIT;
        """, {'country' : self.country})

        cursor = connection.cursor()
        cursor.execute("""
            UPDATE data_recipient 
            SET total = t.total 
            FROM (
                SELECT * 
                FROM recipient_totals 
                WHERE country=%(country)s
                ) as t 
            WHERE t.recipient_id = globalrecipientidx;        
            COMMIT;
            """, {'country' : self.country})

        print "Making year totals for %s" % self.country
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM data_totalyear WHERE country=%(country)s;
            INSERT INTO data_totalyear (recipient_id, year, total, country)
                (
                SELECT globalrecipientidx, year, SUM(amounteuro) as total, countrypayment
                FROM data_payment
                WHERE countrypayment=%(country)s
                GROUP BY globalrecipientidx, year, countrypayment);
        """, {'country' : self.country})

    def recipient_year(self):
        print "Making recipient year totals for %s" % self.country
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM data_recipientyear WHERE country=%(country)s;
            INSERT INTO data_recipientyear (recipient_id, name, year, country, total)
            SELECT pay.globalrecipientidx, r.name, pay.year, pay.countrypayment, pay.total FROM 
                (SELECT globalrecipientidx, year, countrypayment, sum(amounteuro) as total 
                FROM data_payment
                AND countrypayment=%(country)s
                GROUP BY countrypayment, globalrecipientidx, year) as pay
            JOIN data_recipient r
            ON r.globalrecipientidx=pay.globalrecipientidx;
            COMMIT;
        """, {'country' : self.country})
        
    def country_years(self):
        print "Making country year totals for %s" % self.country
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM data_countryyear WHERE country=%(country)s;
            INSERT INTO data_countryyear (year, country, total)
            SELECT year, countrypayment, sum(amounteuro) 
            FROM data_payment 
            WHERE year !='0' 
            AND countrypayment=%(country)s
            GROUP BY countrypayment, year;
            COMMIT;
        """, {'country' : self.country})


    def schemes(self):
        """
        Makes a row in scheme_years for each scheme in each year.
        
        These rows contain the scheme ID, total amout they received on that
        year, and other stats, like number of recipients etc
        """
        
        print "Making scheme totals"
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE data_scheme
            SET total = s.total
            FROM (
                SELECT p.globalschemeid, SUM(p.amounteuro) as total
                FROM data_payment p
                WHERE countrypayment=%(country)s
                GROUP BY globalschemeid) s
            WHERE data_scheme.globalschemeid=s.globalschemeid;
        """, {'country' : self.country})


        print "Making scheme year totals"
        cursor = connection.cursor()
        cursor.execute("""
            BEGIN;
            DELETE FROM data_schemeyear WHERE countrypayment=%(country)s;
            COMMIT;
            BEGIN;
            INSERT INTO data_schemeyear (globalschemeid, nameenglish, countrypayment, year, total)
            SELECT s.globalschemeid, s.nameenglish, s.countrypayment, p.year, SUM(p.amounteuro)
            FROM data_scheme s
            JOIN data_payment p
            ON s.globalschemeid=p.globalschemeid
            WHERE s.countrypayment=%(country)s
            GROUP BY s.globalschemeid, p.year, s.nameenglish, s.countrypayment;
            COMMIT;
        """, {'country' : self.country})
        
        print "Making recipient scheme year totals"
        cursor = connection.cursor()
        cursor.execute("""
            BEGIN;
            DELETE FROM data_recipientschemeyear WHERE country=%(country)s;
            COMMIT;
            BEGIN;
            INSERT INTO data_recipientschemeyear (recipient_id, scheme_id, country, year, total)
            SELECT globalrecipientidx, globalschemeid, '%(country)s', '0', SUM(amounteuro) 
            FROM data_payment
            GROUP BY globalschemeid, globalrecipientidx
            COMMIT;
        """, {'country' : self.country})
        
    
    
    
    def handle(self, **options):
        self.country = options.get('country')
        if not self.country:
            raise Exception('A valid country is required')
        
        
        # First do the recipients

        print "recipients"
        #self.totals()
        # 
        print "schemes"
        self.schemes()

        print "country years"
        self.country_years()
    
# INSERT INTO data_georecipient  SELECT r.globalrecipientidx, geometryfromtext('POINT(' || lng || ' ' || lat || ')', 4326) from data_recipient r WHERE lng !=0