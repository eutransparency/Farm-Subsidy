#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import commands
import re
import MySQLdb
import csv
import codecs

import fsconf


def mysql2csv():
  mysql_prefix = fsconf.mysql_prefix
  mysql_user = fsconf.mysql_user
  mysql_pass = fsconf.mysql_pass
  
  mysql_string = "mysql -u %s --password=%s " % (mysql_user,mysql_pass)
  databases = re.findall("((^|(?<=\n))%s[^\n]+)" % mysql_prefix,commands.getoutput("echo 'SHOW DATABASES' | %s" % (mysql_string)))
  
  for database in databases:
    database = database[0]
    mysql_string
    tables = commands.getoutput('echo "SHOW TABLES" | %s %s' % (mysql_string, database)).split("\n")
    for table in tables:
      
      if table[0:7] == 'payment':
        payment_table = table
      if table[0:9] == 'recipient':
        recipient_table = table

    if recipient_table and payment_table:
      print "working with %s" % database
      
      writer = csv.writer(codecs.open("%s/%s.csv" % (fsconf.csvdir, database),'w'))
      
      print "Opening Connection"
      
      connection = MySQLdb.connect (host = "localhost",
                                 user = mysql_user,
                                 passwd = mysql_pass,
                                 db = database)
        
      start = 0                         
      db_end = 0
      while db_end is 0:
        c = connection.cursor()
            
        query = """SELECT *
        FROM %s p, %s r 
        WHERE r.recipient_id=p.recipient_id 
        LIMIT %s,100000
        """ % (payment_table, recipient_table, start)
          

        print "Execute Query %s to %s" % (start,start+100000)

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
        while row:
          writer.writerow(row)
          row = c.fetchone()
        
        c.scroll(0,mode='absolute')
        # print "rows:%s" % len(c.fetchall())
        if len(c.fetchall()) <= 99999:
          print "yes"
          db_end = 1
  
      
        start +=100000  
        c.close()
      connection.close()
    
    







if __name__ == '__main__':
  mysql2csv()







