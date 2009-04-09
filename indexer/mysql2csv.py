#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import commands
import re
import MySQLdb
import csv
import codecs

import farmsubsidy.fsconf as fsconf
import countryCodes


def mysql2csv(countryToProcess="all"):
  mysql_prefix = fsconf.mysql_prefix
  mysql_user = fsconf.mysql_user
  mysql_pass = fsconf.mysql_pass
  
  mysql_string = "mysql -u %s --password=%s " % (mysql_user,mysql_pass)
  databases = re.findall("((^|(?<=\n))%s[^\n]+)" % mysql_prefix,commands.getoutput("echo 'SHOW DATABASES' | %s" % (mysql_string)))
  
  for database in databases:

    database = database[0]
    
    country = countryCodes.filenameToCountryCode(database[len('farmsubsidy_'):])
    if countryToProcess != "all" and countryToProcess != country:
      continue
    
    

    mysql_string
    tables = commands.getoutput('echo "SHOW TABLES" | %s %s' % (mysql_string, database)).split("\n")
    for table in tables:
      
      if table[0:7] == 'payment':
        payment_table = table
      if table[0:9] == 'recipient':
        recipient_table = table
      if table[0:7] == 'scheme1':
        scheme_table = table

    if recipient_table and payment_table and scheme_table:
      print "working with %s" % database
      print recipient_table, payment_table, scheme_table
      writer = csv.writer(codecs.open("%s/%s.csv" % (fsconf.csvdir, database),'w'))
      
      print "Opening Connection"
      
      connection = MySQLdb.connect (host = "localhost",
                                 user = mysql_user,
                                 passwd = mysql_pass,
                                 db = database)
        
      c = connection.cursor()


      ## Make the total_amount field for each payment
      totals_query = """CREATE TEMPORARY TABLE totals
      SELECT sum(%(payment)s.amount)
      as total_amount, %(recipient)s.recipient_id_x
      FROM %(payment)s, %(recipient)s  
      WHERE %(payment)s.recipient_id=%(recipient)s.recipient_id
      GROUP BY %(recipient)s.recipient_id_x;
      """ % {'payment' : payment_table, 'recipient' : recipient_table}

      print "Making totals"
      c.execute(totals_query)

      index_query = """ALTER TABLE `totals` ADD INDEX ( `recipient_id_x` )"""
      c.execute(index_query)

      ## Make the scheme field for each payment
      scheme_query = """CREATE TEMPORARY TABLE scheme_total
      SELECT p.payment_id, s.name_english as scheme_name FROM payment p
      INNER JOIN %(scheme_table)s s
      ON p.scheme1_id=s.scheme1_id
      """ % {'scheme_table' : scheme_table}
      print "Making schemes"
      c.execute(scheme_query)

      scheme_index_query = """ALTER TABLE `scheme_total` ADD INDEX ( `payment_id` )"""
      c.execute(scheme_index_query)


      start = 0
      rlen = 100000
      db_end = 0
      while db_end is 0:
        query = """
        SELECT * from
          (%(recipient)s R 
          LEFT JOIN 
            (%(payment)s P LEFT JOIN scheme_total s ON p.payment_id=s.payment_id)
          ON R.recipient_id = P.recipient_id) 
          INNER JOIN totals T ON R.recipient_id_x=T.recipient_id_x
          LIMIT %(start)s,%(rlen)s;
        """ % {'payment' : payment_table, 'recipient' : recipient_table, 'rlen' : rlen, 'start' : start}
        

        print "Execute Query %s to %s" % (start,start+rlen)

        c.execute(query)



        if start == 0:
          print "Load Scheme"
          scheme = []
          for f in c.description:
            scheme.append(f[0])
          
  
          file = csv.writer(codecs.open("%s/%s.scheme" % (fsconf.csvdir, database),'w'))
          file.writerow(scheme)
  
        print "Writing rows"
        row = c.fetchone()
        row_count = 0
        while row:
          writer.writerow(row)
          row = c.fetchone()
          row_count += 1

        if row_count < rlen:
          print "Database End"
          db_end = 1

        start = start + rlen
              
      c.close()
      connection.close()
    

if __name__ == '__main__':
  if len(sys.argv) > 1:
    if sys.argv[1] in countryCodes.countryCodes() or sys.argv[1] == "all":
      country = sys.argv[1]
      mysql2csv(country)
    else:
      print "%s isn't a valid country code" % sys.argv[1]
  else:
    print "Usage: 'python mdb2csv.py [country|all]"







