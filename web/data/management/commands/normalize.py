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

        UPDATE_PAGE_SIZE = 10000
        sql_count = """
          SELECT COUNT(*) from data_recipient WHERE countrypayment='%(country)s' AND total IS NULL;
          """ % {'country' : self.country}
        cursor.execute(sql_count)
        to_process = cursor.fetchone()[0]
        more_to_process = int(to_process) > 0
        print to_process
        offset = 0

        print int(to_process/UPDATE_PAGE_SIZE)
        print "Making recipient total colum, %s at a time" % UPDATE_PAGE_SIZE
        for i in range(int(to_process/UPDATE_PAGE_SIZE)):
          print UPDATE_PAGE_SIZE, offset, to_process
          cursor.execute("""
            UPDATE data_recipient                                                              
            SET total = s.newtotal
            FROM (
                  SELECT r.globalrecipientidx, SUM(p.amounteuro) AS newtotal FROM 
                    (
                        SELECT globalrecipientidx
                        FROM data_recipient
                        WHERE total IS NULL
                        AND countrypayment = %(country)s
                        LIMIT %(update_page_size)s OFFSET %(offset)s
                    ) as r
                    JOIN data_payment p
                    ON r.globalrecipientidx=p.globalrecipientidx
                    GROUP BY r.globalrecipientidx

                   ) s
            WHERE data_recipient.globalrecipientidx=s.globalrecipientidx;

          """, {'country' : self.country, 'update_page_size' : UPDATE_PAGE_SIZE, 'offset' : offset})

          cursor.execute(sql_count, {'country' : self.country})
          to_process = cursor.fetchone()[0]
          more_to_process = int(to_process) > 0
          print to_process
          offset = offset+ UPDATE_PAGE_SIZE
       

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
        
    
    def handle(self, **options):
        self.country = options.get('country')
        if not self.country:
            raise Exception('A valid country is required')
        
        
        # First do the recipients
        print "recipients"
        #self.totals()
        print "schemes"
        self.schemes()
    
