"""
COPY's the data for the country specified.

"""

import connection

class Populate():
    
    def __init__(self, country, **kwargs):
        self.conn, self.c = connection.connect()
        self.country = country
        self.data_path = kwargs.get('data_path', '/var/www/stage.farmsubsidy.org/data')
        
    def populate_raw(self):
        """
        Reads in the CSV files and adds the data to the _raw table
        
        """
        
        for table in ('schemes','payments', 'recipients'):
        
            sql = "DELETE FROM data_%s_raw WHERE countrypayment='%s'" % (table, self.country)
            self.c.execute(sql)
            self.conn.commit()
            data_file = "%s/csv/%s/%s.csv" % (self.data_path, self.country, table)
            sql = """
                COPY data_%(table)s_raw 
                FROM '%(data_file)s'
                DELIMITERS ';' 
                CSV;
            """ % locals()

            print "COPYing %s" % table
            self.c.execute(sql)
            self.conn.commit()

p = Populate('AT')
p.populate_raw()