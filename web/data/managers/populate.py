"""
Below are managers for all types of model we have.

There are some standard normalization opperations, for example, there is no
canonical row for a recipient, rather there are a few different rows all with
the same global_recipientidx.

The correct thing would be to have a single row for each recipient (containing
the latest data), and then join everything with that row, rather than grouping
by the ID.

"""
from django.db import connection, backend, models
from django.template.defaultfilters import slugify

class Normalize(models.Manager):
    
    def hacks(self, data_type):
        """
        A load of hacks for each type.
        
        Mainly relating to MySQL being shit and not understanding NULL properly
        """
    
        if data_type == "recipients":
            return """
            (recipientid, recipientidx, globalrecipientid, globalrecipientidx, name, address1, address2, zipcode, town, countryrecipient, countrypayment, geo1, geo2, geo3, geo4, geo1nationallanguage, geo2nationallanguage, geo3nationallanguage, geo4nationallanguage, @lat, @lng)
            SET lat=nullif(lat, '0'),
                lng=nullif(lng, '0')
            """
        elif data_type == "payments":
            return """
            (
            paymentid,
            globalpaymentid,
            globalrecipientid,
            globalrecipientidx,
            globalschemeid,
            @amounteuro,
            @amountnationalcurrency,
            @year,
            countrypayment
            )
            SET amounteuro=nullif(@amounteuro, ''),
                amountnationalcurrency=nullif(@amountnationalcurrency, ''),
                year=CONVERT(@year,SIGNED)
            """
        else:
            return ""
    
    def populate_raw(self, data_type, from_table, country):
        """
        Does the inital loading.
        
        Assumes files are *always* called, schemes.csv, payments.csv or
        recipients.csv and *always live in ../data/csv/[country]/        
        """
        if data_type == "locations":
            return
        
        print data_type
        file_name = "%s.csv" % data_type
        file_path = "../data/csv"
        full_path = "%s/%s/%s" % (file_path, country, file_name,)
        
        table_hacks = self.hacks(data_type)
        print table_hacks
        
        sql = """
            ALTER TABLE %(from_table)s DISABLE KEYS;
            
            LOAD DATA LOCAL INFILE '%(full_path)s'
            REPLACE INTO TABLE %(from_table)s
            FIELDS TERMINATED BY ';'
            ENCLOSED BY '"'
            LINES TERMINATED BY '\r\n'
            %(table_hacks)s
            ;
            
            ALTER TABLE %(from_table)s ENABLE KEYS;
        """ % locals()
        print repr(sql)
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        print "done"



    def populate(self, data_type, from_table, dest_table, country):
        if data_type == "recipients":
            sql = """
            BEGIN;
            DELETE FROM %(dest_table)s WHERE countrypayment='%(country)s';
            COMMIT;
                        
            BEGIN;
            INSERT INTO %(dest_table)s
            SELECT 
                r.recipientid, 
                r.recipientidx, 
                r.globalrecipientid, 
                r.globalrecipientidx, 
                r.name, r.address1, r.address2, r.zipcode, r.town, 
                r.countryrecipient, r.countrypayment, 
                r.geo1, r.geo2, r.geo3, r.geo4, 
                r.geo1nationallanguage, r.geo2nationallanguage, 
                r.geo3nationallanguage, r.geo4nationallanguage, 
                r.lat, 
                r.lng, 
                SUM(p.amounteuro) as total
            FROM %(from_table)s r
            JOIN data_payments_raw p
            ON r.globalrecipientidx=p.globalrecipientidx
            WHERE r.countrypayment='%(country)s'
            GROUP BY r.globalrecipientidx;
            COMMIT;
            
            """ % {
                'from_table' : from_table,
                'dest_table' : dest_table,
                'country' : country,
                }
            cursor = connection.cursor()
            cursor.execute(sql)
                
            sql = """
            BEGIN;
            DELETE FROM data_year_total WHERE country='%(country)s';
            COMMIT;
            """ % {
                'from_table' : from_table,
                'dest_table' : dest_table,
                'country' : country,
                }
            cursor = connection.cursor()
            cursor.execute(sql)
                
            sql = """
            INSERT INTO data_year_total (recipient_id, year, total, country)
            SELECT globalrecipientidx, year, SUM(amounteuro), countrypayment 
            FROM data_payments_raw 
            WHERE countrypayment='%(country)s'
            GROUP BY globalrecipientidx, year;
            """ % {
                'from_table' : from_table,
                'dest_table' : dest_table,
                'country' : country,
                }
            
            cursor = connection.cursor()
            cursor.execute(sql)


        elif data_type == "payments":
            print "payments"
            sql = """
            DELETE FROM %(dest_table)s WHERE countrypayment='%(country)s';
            INSERT INTO %(dest_table)s
            SELECT *
            FROM data_payments_raw
            WHERE countrypayment='%(country)s';
            """ % {
                'from_table' : from_table,
                'dest_table' : dest_table,
                'country' : country,
                }
            
            cursor = connection.cursor()
            cursor.execute(sql)

        elif data_type == "schemes":
            print "schemes"
            sql = """
            DELETE FROM %(dest_table)s WHERE countrypayment='%(country)s';
            INSERT INTO %(dest_table)s
            SELECT *
            FROM %(from_table)s
            WHERE countrypayment='%(country)s';
            """ % {
                'from_table' : from_table,
                'dest_table' : dest_table,
                'country' : country,
                }
            
            cursor = connection.cursor()
            cursor.execute(sql)

            sql = """
            INSERT INTO data_schemeyear (scheme_id, year, total, country)
            SELECT globalschemeid, year, SUM(amounteuro), countrypayment
            FROM data_payments
            WHERE countrypayment='%(country)s'
            GROUP BY globalschemeid, year, countrypayment
            ;
            """ % {
                'from_table' : from_table,
                'dest_table' : dest_table,
                'country' : country,
                }
            
            cursor = connection.cursor()
            cursor.execute(sql)
        
        elif data_type == "locations":
            """
            This gets complex.
            
            TODO: document fully
            """
            
            from data.models import Location
                        
            def location_query(geo_type, country, cols={}):
                """
                Returns a list of rows, grouped by 'geo_type', where the parent
                is in the cols dict.
                """

                col_sql = "AND".join(["%s='%s'" % (k,v) for k,v in cols.items()])
                if col_sql:
                    col_sql = "AND %s" % col_sql
                
                sql = """
                SELECT %(geo_type)s as geoname, '%(country)s' as country, 
                       COUNT(r.globalrecipientidx) as recipients, 
                       SUM(r.total) as total, SUM(r.total)/COUNT(*) as average
                FROM data_recipients r
                WHERE countrypayment='%(country)s'
                %(col_sql)s
                GROUP BY geoname
            
                """ % {
                        'country' : country,
                        'geo_type' : geo_type,
                        'col_sql' : col_sql,
                    }
                print sql
                cursor = connection.cursor()
                cursor.execute(sql)
                desc = cursor.description
                rows = []
                for row in cursor.fetchall():
                    row_dict = dict(zip([col[0] for col in desc], row))
                    row_dict['name'] = row_dict.pop('geoname')
                    rows.append(row_dict)
                return rows

            def save_location(l, parent=Location, geo_type='geo1'):
                l['slug'] = slugify(l['name'])
                l['geo_type'] = geo_type

                try:
                    "See if this already exists"
                    new_location = parent.objects.get(name=l['name'],
                                             country=country)
                except Exception, e:
                    try:
                        ""
                        new_location = parent.add_child(**l)
                    except Exception, e:
                        new_location = parent.add_root(**l)

                return new_location


            geo_types = ['geo1', 'geo2', 'geo3', 'geo4']
            geo_cols = {}            
            
            # geo1
            geo1_results = location_query('geo1', country)
            for geo1_result in geo1_results:
                
                L1 = save_location(geo1_result)
                
                geo2_results = location_query('geo2', country, geo_cols)
                
                for geo2_result in geo2_results:
                    print "\t\t"+geo2_result['name']
                    save_location(geo2_result, parent=L1, geo_type='geo2')
            

