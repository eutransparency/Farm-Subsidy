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
        
        print "Making recipient total colum"
        cursor = connection.cursor()
        cursor.execute("""
            BEGIN;
            UPDATE data_recipient
            SET total = s.total
            FROM (
                SELECT globalrecipientidx, SUM(amounteuro) as total
                FROM data_payment
                GROUP BY globalrecipientidx) s
            WHERE data_recipient.globalrecipientidx=s.globalrecipientidx;
            AND data_recipient.total IS NULL
            COMMIT;
        """)
        
        print "Making year totals for %s" % self.country
        cursor = connection.cursor()
        cursor.execute("""
            BEGIN;
            DELETE FROM data_totalyear WHERE country=%(country)s;
            INSERT INTO data_totalyear (recipient_id, year, total, country)
                (
                SELECT globalrecipientidx, year, SUM(amounteuro) as total, countrypayment
                FROM data_payment
                GROUP BY globalrecipientidx, year, countrypayment);
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
            BEGIN;
            UPDATE data_scheme
            SET total = s.total
            FROM (
                SELECT p.globalschemeid, SUM(p.amounteuro) as total
                FROM data_payment p
                GROUP BY globalschemeid) s
            WHERE data_scheme.globalschemeid=s.globalschemeid;
            COMMIT;
        """)


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
        
    
    def handle(self, **options):
        self.country = options.get('country')
        if not self.country:
            raise Exception('A valid country is required')
        
        
        # First do the recipients
        print "recipients"
        self.totals()
        print "schemes"
        self.schemes()
    