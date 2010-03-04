#!/usr/bin/env python
# encoding: utf-8

"""
populate.py

Created by Sym on 2009-08-02.

COPYs 

This script assumes the fields are correct and in place.    
It does nothing to account for bad data, and this should 
be fixed *before* running it (or not broken in the first place?!)

1) Loop though each country
2) Loop though each table (payment, recipient, scheme)
3) Adds each row in the table to the database

"""
import sys
import os
import csv
import codecs
import subprocess

sys.path.append('..')
import fsconf
import countryCodes
import connection


class Populate(object):
    def __init__(self):
        self.conn, self.c = connection.connect()

    def indexes(self, opp, tables=None):
    
        indexes = {
            'data_payments' : [
                ('year', 'year', 'btree'),
                ('globalrecipientidx', 'globalrecipientidx', 'btree'),
                ('amounteuro', 'amounteuro', 'btree'),
                ('payments_globalschemeid', 'globalschemeid', 'btree'),
                ],
            'data_recipients' : [
                ('G1', 'geo1', 'btree'),
                ('G2', 'geo2', 'btree'),
                ('G3', 'geo3', 'btree'),
                ('recipient_globalrecipientidx', 'globalrecipientidx', 'btree'),
                ('globalrecipientid', 'globalrecipientid', 'btree'),
                ],
            'data_schemes' : [
            ('scheme_globalschemeid', 'globalschemeid', 'btree'),
            ('budgetlines8digit', 'budgetlines8digit', 'btree'),
            ],
            'data_totals' : [
            ('totals_year', 'year', 'btree'),
            ('gid', 'global_id', 'btree'),
            ('country', 'countrypayment', 'btree'),
            ('amount', 'amount_euro', 'btree'),
            ],
            'data_years' : [
            ('years_c', 'country', 'btree'),
            ('years_y', 'year', 'btree'),
            ],
            'data_locations' : [
            ('locations_type', 'location_type', 'btree'),
            ('locations_geo1', 'geo1', 'btree'),
            ('locations_geo2', 'geo2', 'btree'),
            ('locations_geo3', 'geo3', 'btree'),
            ('locations_geo4', 'geo4', 'btree'),
            ],
            'data_scheme_totals' : [
            ('scheme_totals_y', 'year', 'btree'),
            ('scheme_totals_sid', 'globalschemeid', 'btree'),
            ],
        }

        if tables is None:
            tables = [table for table in indexes]
    
        if opp == "delete":
            for table in indexes:
                if table in tables:
                    print "Indexes for %s" % table
                    for index in indexes[table]:
                        try:
                            print "\t - Deleting index %s on %s" % (index[0], table)
                            self.c.execute("DROP INDEX %s; COMMIT" % (index[0]))
                            self.conn.commit()
                        except Exception, e:
                            # We need to commit anyway, else the next DROP will fail
                            self.conn.commit()
    
        if opp == "create":
            for table in indexes:
                if table in tables:            
                    print table
                    print "Indexes for %s" % table
                    for index in indexes[table]:
                        print "\t - Creating index %s on %s" % (index[0], table)
                        self.c.execute("CREATE INDEX %s ON %s USING %s (%s)" % (index[0], table, index[2], index[1]))
                        self.conn.commit()    
            # sys.exit()
    
    def denormalize(self, country):
        """
        Util function that calls each funstion in the 'funcs' list
        """
        self.country = country
        
        funcs = [self.totals, self.locations, self.years]
        for f in funcs:
            f(self.country)
        
        
    def totals(self, country):
        """
        First deletes, then creates the total of each payment for each globalidx.
        This is done because we often want to show the total sum of payments per
        year rather than a particular payment so in summing them all now we save
        some time later.
    
    
        - `country` ISO country code.
    
        """
        
        print "Making totals for %s" % country
        
        # Delete all totals from this country first:
        print "\t - Deleting old totals for %s" % country
        sql = "DELETE FROM data_totals WHERE countrypayment='%s'" % country
        self.c.execute(sql)
        self.conn.commit()    
    
    
        # SUM all payments for the country and group by globalrecipientidx then year
        print "\t - Making new totals for %s" % country
        sql = """
        BEGIN;
        INSERT INTO data_totals 
        SELECT pay.globalrecipientidx, pay.totalamount, pay.year, pay.countrypayment, r.name FROM 
        	(SELECT globalrecipientidx, SUM(amounteuro) as totalamount, year, countrypayment 
        	FROM data_payments 
        	WHERE countrypayment='%s'
        	GROUP BY globalrecipientidx, year, countrypayment) as pay
        JOIN data_recipients r
        ON r.globalrecipientidx=pay.globalrecipientidx;
        COMMIT;
        """ % country
        self.c.execute(sql)
        self.conn.commit()    

        sql = """
        BEGIN;
        INSERT INTO data_totals 
        SELECT global_id, SUM(amount_euro), '0', countrypayment, MAX(nameenglish)
        FROM data_totals
        WHERE countrypayment ='%(country)s'
        GROUP BY global_id, countrypayment;
        COMMIT;              
                """ % locals()
        self.c.execute(sql)
        self.conn.commit()    
    
    def locations(self, country):
        print "\t - Deleting old location totals for %s" % country
        sql = "DELETE FROM data_locations WHERE country='%s'" % country
        self.c.execute(sql)
        self.conn.commit()    
    
        print "\t - Deleting old recipient locations for %s" % country
        sql = "DELETE FROM data_recipient_locations WHERE country='%s'" % country
        self.c.execute(sql)
        self.conn.commit()    
    
        geo_columns = ['geo1', 'geo2', 'geo3', 'geo4']
        while geo_columns:
            columns = []
            for i in range(0,4):
                try:
                    columns.append(geo_columns[i])
                except:
                    columns.append('NULL')
            columns_str = ", ".join("LOWER(%s)" % i for i in columns)
            group_by_str = ", ".join(geo_columns)
            column_type = geo_columns.pop()    

            sql = """
            BEGIN;
            INSERT INTO data_locations
            SELECT '%(column_type)s','%(country)s',%(columns_str)s, count(*) , SUM(t.amount_euro)
            FROM data_recipients r
            JOIN data_totals t
            ON r.globalrecipientidx=t.global_id
            WHERE %(column_type)s IS NOT NULL
            AND t.year = '0'
            and countryrecipient='%(country)s'
            GROUP BY %(group_by_str)s;
            COMMIT;
            """ % locals()
        
            print "\t - Making location totals for %s" % column_type
            self.c.execute(sql)
            self.conn.commit()    

    def years(self, country):
        print "\t - Deleting old years for %s" % country
        sql = "DELETE FROM data_years WHERE country='%s'" % country
        self.c.execute(sql)
        self.conn.commit()    


        print "\t - Creating years for %s" % country
        sql = """INSERT INTO data_years SELECT '%(country)s',year, count(*), SUM(amounteuro) 
                         FROM data_payments 
                         WHERE countrypayment='%(country)s' 
                         GROUP BY year""" % locals()
        self.c.execute(sql)
        self.conn.commit()    


    def data_scheme_totals(self, country):
        # Delete all totals from this country first:
        print "\t - Deleting old totals for %s" % country
        sql = "DELETE FROM data_scheme_totals WHERE country='%s'" % country
        self.c.execute(sql)
        self.conn.commit()    

        print "\t - Creating scheme totals for %s" % country
        sql = """
        BEGIN;
        INSERT INTO data_scheme_totals 
                         SELECT MIN(p.countrypayment), p.year, 
                         COALESCE(NULLIF(MAX(s.nameenglish), ''), NULLIF(MAX(s.namenationallanguage), '')) as name, SUM(p.amounteuro) as E, MAX(p.globalschemeid)
                          FROM data_payments p
                          JOIN data_schemes s
                          ON (p.globalschemeid = s.globalschemeid)
                          WHERE p.countrypayment = '%(country)s'
                          GROUP BY p.year, s.nameenglish, s.namenationallanguage;
         COMMIT;
                            """ % locals()
        self.c.execute(sql)
        self.conn.commit()    

    def vacuum(self, tables):
        """
        Performs a vacuum analize on a given table
    
        - `tables` a tuple of tables to vacuum
        """ 
        
        # Maigc...
        import psycopg2.extensions as e
        self.conn.set_isolation_level(e.ISOLATION_LEVEL_AUTOCOMMIT)
        for table in tables:
            print "VACUUMing %s" % table
            self.conn.commit()
            sql = "VACUUM ANALYZE %s;" % table
            self.c.execute(sql)
            self.conn.commit()

    def process_country(self, country):
        """"
    
        Works on one country at a time, and expects 3 files to be in a folder 
        called by the countries ISO country code.
    
        These 3 files should be:
        payments.csv
        recipients.csv
        schemes.csv
    
        and should contain semicolon-sepirated data with field values matching
        the data scheme laid out in scheme.sql in this directory.
    
        The files are cleaned (with clean_files()) and then COPY'd to the database
    
        For speed, all indexed are deleted before a COPY, and recreated after the copy.
    
        - `country`: String of the ISO country code
        """
        if country and country not in countryCodes.country_codes():
            print "%s is not a country!" % country
            return
        else:
            self.country = country
            
        tables = [
            'data_recipients', 
            'data_payments', 
            'data_schemes'
            ]
    
        for table in tables:
            data_path = "%s/%s/%s.csv" % (fsconf.csvdir, self.country, table.split('_')[1])
        
        
            print "Dumping %s data from %s" % (country, table)
            sql = "DELETE FROM %s WHERE countrypayment='%s'" % (table, self.country)
            self.c.execute(sql)
            self.conn.commit()        
        
            sql = """
                COPY %(table)s 
                FROM '%(data_path)s' 
                DELIMITERS ';' 
                CSV;
            """ % locals()
    
            print "COPYing %s" % table
            self.c.execute(sql)    
            self.conn.commit()        
        


if __name__ == "__main__":
        
    countries = sys.argv[1:]
    if len(countries) == 0:
        countries = countryCodes.country_codes()
        del countries['EU']
        print "No country specified, working on all countries in countrycodes()"
    populate = Populate()
    
    populate.indexes('delete')
    for country in countries:
        populate.process_country(country.upper())
    populate.indexes('create', ['data_schemes', 'data_payments', 'data_recipients'])

    for country in countries:
            populate.denormalize(country)
    
    populate.indexes('create', ['data_totals', 'data_years', 'data_locations', 'data_scheme_totals'])
    populate.vacuum(('data_totals', 'data_payments', 'data_recipients', 'data_schemes')) 
