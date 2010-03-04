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

def clean_files(file_path):
    """
    When the files arrive they are in Latin-1 format with a header row.
    
    This function does the following:
    
    1) Renames (backs up) the csv file
    2) Removes the header row
    3) uses the iconv unix command to convert the file to UTF-8
    
    """

    try:
        if not os.path.exists(file_path):
            raise IOError("%s does not exist!" % file_path)
        filename = file_path.split('/')[-1]
        
        
        print "Cleaning up %s" % filename
        
        if not os.path.exists("%s.orig" % file_path):
            print "\t - Renaming %(filename)s to %(filename)s.orig" % {'filename':filename}
            os.rename(file_path, "%s.orig" % file_path)
        
            print "\t - Removeing first line"
            # subprocess.call("sed '1d' %(filename)s.orig > %(filename)s-latin" % {'filename':file_path}, shell=True)
            subprocess.call("cat %(filename)s.orig > %(filename)s-latin" % {'filename':file_path}, shell=True)
        
            print "\t - Converting %s to UTF8" % filename
            subprocess.call('iconv -f latin1 -t utf-8 %(filename)s-latin > %(filename)s' % {'filename':file_path}, shell=True)
        
            print "\t - Cleaning up"
            os.remove("%s-latin" % file_path)
        
        
        
    except Exception, e:
        print e
    

def indexes(opp, tables=None):
    
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
    
    conn,c = connection.connect()

    if tables is None:
        tables = [table for table in indexes]
    
    if opp == "delete":
        for table in indexes:
            if table in tables:
                print "Indexes for %s" % table
                for index in indexes[table]:
                    try:
                        print "\t - Deleting index %s on %s" % (index[0], table)
                        c.execute("DROP INDEX %s; COMMIT" % (index[0]))
                        conn.commit()
                    except Exception, e:
                        # We need to commit anyway, else the next DROP will fail
                        conn.commit()
    
    if opp == "create":
        for table in indexes:
            if table in tables:            
                print table
                print "Indexes for %s" % table
                for index in indexes[table]:
                    print "\t - Creating index %s on %s" % (index[0], table)
                    c.execute("CREATE INDEX %s ON %s USING %s (%s)" % (index[0], table, index[2], index[1]))
                    conn.commit()    
        # sys.exit()


def totals(country):
    """
    First deletes, then creates the total of each payment for each globalidx.
    This is done because we often want to show the total sum of payments per
    year rather than a particular payment so in summing them all now we save
    some time later.
    
    
    - `country` ISO country code.
    
    """
    conn,c = connection.connect()
    
    print "Making totals for %s" % country
        
    # Delete all totals from this country first:
    print "\t - Deleting old totals for %s" % country
    sql = "DELETE FROM data_totals WHERE countrypayment='%s'" % country
    c.execute(sql)
    conn.commit()    
    
    
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
    c.execute(sql)
    conn.commit()    

    sql = """
    BEGIN;
    INSERT INTO data_totals 
    SELECT global_id, SUM(amount_euro), '0', countrypayment, MAX(nameenglish)
    FROM data_totals
    WHERE countrypayment ='%(country)s'
    GROUP BY global_id, countrypayment;
    COMMIT;              
            """ % locals()
    c.execute(sql)
    conn.commit()    
    
    print "\t - Deleting old location totals for %s" % country
    sql = "DELETE FROM data_locations WHERE country='%s'" % country
    c.execute(sql)
    conn.commit()    
    
    print "\t - Deleting old recipient locations for %s" % country
    sql = "DELETE FROM data_recipient_locations WHERE country='%s'" % country
    c.execute(sql)
    conn.commit()    
    
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
        c.execute(sql)
        conn.commit()    


    print "\t - Deleting old years for %s" % country
    sql = "DELETE FROM data_years WHERE country='%s'" % country
    c.execute(sql)
    conn.commit()    


    print "\t - Creating years for %s" % country
    sql = """INSERT INTO data_years SELECT '%(country)s',year, count(*), SUM(amounteuro) 
                     FROM data_payments 
                     WHERE countrypayment='%(country)s' 
                     GROUP BY year""" % locals()
    c.execute(sql)
    conn.commit()    



    # Delete all totals from this country first:
    print "\t - Deleting old totals for %s" % country
    sql = "DELETE FROM data_scheme_totals WHERE country='%s'" % country
    c.execute(sql)
    conn.commit()    

    print "\t - Creating scheme totals for %s" % country
    sql = """
    BEGIN;
    INSERT INTO data_scheme_totals 
                     SELECT MIN(p.countrypayment), p.year, COALESCE(MAX(s.nameenglish), MAX(s.namenationallanguage)) as name, SUM(p.amounteuro) as E, p.globalschemeid
                     FROM data_payments p
                     JOIN data_schemes s
                     ON (p.globalschemeid = s.globalschemeid)
                     WHERE s.nameenglish IS NOT NULL AND p.countrypayment = '%(country)s'
                     GROUP BY p.year, name;
     COMMIT;
                        """ % locals()
    c.execute(sql)
    conn.commit()    



def counts(country):
    """
    Populate the counts table.
    
    This table allows arbertry counts to be stored in the following format:
    
    [country], [year], [type], [value], [count]
    
    Type can be any string, however the following standards are kept:
    
    * location
    * country
    * scheme
    
    All values are strings.  locations are paths sepirated by 
    forwardslashs (/) so as to avoide counting the wrong location, for
    example:
    
    "england/east of england/norfolk/south norfolk"
    
    """
    conn,c = connection.connect()
    
    # Location counts.
    # This is the most complex, as we have to loop every location 
    # and sub-location
    
    print "Making counts for %s" % country
    geos = range(1,5)
    while geos:        
        concats = "||'/'||".join("r.geo%s" % i for i in geos)
        groups = ",".join("r.geo%s" % i for i in geos)
        geo = "geo%s" % geos.pop()
        print "\t Making %s counts" % geo
        sql = """
        INSERT INTO data_counts
        SELECT r.countrypayment, p.year, 'location',
        LOWER(%(concats)s) as d, count(*)
        FROM data_recipients r
        JOIN data_payments p
        ON r.globalrecipientidx=p.globalrecipientidx
        WHERE r.%(geo)s IS NOT NULL
        GROUP BY %(groups)s, r.countrypayment, p.year
        ORDER BY %(geo)s

        """ % locals()

        c.execute(sql)
        conn.commit()

    
    
    
def vacuum(tables):
    """
    Performs a vacuum analize on a given table
    
    - `tables` a tuple of tables to vacuum
    """ 
    conn,c = connection.connect()
    # Maigc...
    import psycopg2.extensions as e
    conn.set_isolation_level(e.ISOLATION_LEVEL_AUTOCOMMIT)
    for table in tables:
        print "VACUUMing %s" % table
        conn.commit()
        sql = "VACUUM ANALYZE %s;" % table
        c.execute(sql)
        conn.commit()

def process_country(country):
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
    tables = [
        'data_recipients', 
        'data_payments', 
        'data_schemes'
        ]
    
    conn,c = connection.connect()
    
    for table in tables:
        data_path = "%s/%s/%s.csv" % (fsconf.csvdir, country, table.split('_')[1])
        
        clean_files(data_path)
        
        print "Dumping %s data from %s" % (country, table)
        sql = "DELETE FROM %s WHERE countrypayment='%s'" % (table, country)
        c.execute(sql)
        conn.commit()        
        
        sql = """
            COPY %(table)s 
            FROM '%(data_path)s' 
            DELIMITERS ';' 
            CSV;
        """ % locals()
    
        print "COPYing %s" % table
        c.execute(sql)    
        conn.commit()        
        


if __name__ == "__main__":
        
    countries = sys.argv[1:]
    if len(countries) == 0:
        countries = countryCodes.country_codes()
        del countries['EU']
        print "No country specified, working on all countries in countrycodes()"
    # try:            
    indexes('delete')
    for country in countries:
        process_country(country.upper())
    indexes('create', ['data_schemes', 'data_payments', 'data_recipients'])

    for country in countries:
            totals(country)
            # counts(country)
    
    indexes('create', ['data_totals', 'data_years', 'data_locations', 'data_scheme_totals'])
    
    
    vacuum(('data_totals', 'data_payments', 'data_recipients', 'data_schemes')) 
