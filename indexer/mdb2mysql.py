#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf, countryCodes
import re
import MySQLdb
import MySQLdb.converters
import csv
import codecs

 


def extractmdb2mysql(countryToProcess="all"):
  """Uses mdbtools to extract tables from access
  databases and load them in to a given database, 
  as set in fsconf.py"""

  mysql_prefix = fsconf.mysql_prefix
  mysql_user = fsconf.mysql_user
  mysql_pass = fsconf.mysql_pass
  mdbdir = fsconf.mdbdir
  
  connection = MySQLdb.connect (host = "localhost",
                             user = mysql_user,
                             passwd = mysql_pass,
                             charset = 'utf8',
                             )
  c = connection.cursor()
  
  
  #Find all files with a .mdb extention and loop though them
  dbs = commands.getstatusoutput('find %s -name "*.mdb"' % (mdbdir))[1].splitlines()
  for db in dbs:

    # Get the path the file is in
    filepath = '/'.join(db.split('/')[:-1])

    # Get the file name
    filename = db.split('/')[-1]
        
    # Database ID
    dbid =  filename.split('.')[0].replace('-','_')

    # Get the country
    country = countryCodes.filenameToCountryCode(filename)
    if countryToProcess != "all" and countryToProcess != country:
      continue
      
    print country

    mysql_database_name = mysql_prefix+dbid
    
    connection.query("drop database IF EXISTS %s;" % (mysql_database_name))
        
    connection.query("create database %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;" % (mysql_database_name))

    connection.query("use %s;" % (mysql_database_name))
    
    
    scheme = commands.getoutput("mdb-schema %s mysql" % (db))
    scheme = re.findall("(CREATE TABLE [^;]+;)", str(scheme))
    scheme_sql = []
    for match in scheme:
      scheme_sql.append(re.sub("-","_", "%s\n\n\n" % match))    
    scheme_sql = "\n\n".join(scheme_sql)

    scheme_sql = re.sub("CREATE TABLE ([^\n]+)","CREATE TABLE `\\1`",scheme_sql)

    tablenames = re.findall("CREATE TABLE ([^\n]+)",scheme_sql)
    for tablename in tablenames:
      scheme_sql = re.sub("CREATE TABLE %s" % tablename,"CREATE TABLE %s" % re.sub(" ","_",tablename), scheme_sql)

   
    scheme_sql = re.sub("\t([^\t]+)\t\t","\t`\\1`\t", scheme_sql)

    # Add Indexes
    indextable = re.findall("CREATE TABLE `([^`]+)`[^;]+(`recipient_id`)[^;]+;",scheme_sql, re.S)
    for table,field in indextable:
      scheme_sql = """
        %s

        ALTER TABLE `%s` ADD INDEX ( %s );  
      """ % (scheme_sql,table,field)

    # c.execute("FLUSH TABLES")
    # connection.query("FLUSH TABLES")
    # connection.commit()
    try:
      connection.query("%s;" % scheme_sql)    
    except Exception, e:
      print "Error loading scheme"
      print scheme_sql
      print e
    c.close()
    connection.close()
    
    
    connection = MySQLdb.connect (host = "localhost",
                               user = mysql_user,
                               passwd = mysql_pass,
                               db=mysql_database_name
                               )
    c = connection.cursor()

    
    tables = commands.getstatusoutput('mdb-tables %s' % (db))[1].split(" ")
      
    for table in tables:

      tabletype = None

      if table[0:7] == 'payment':
        tabletype = 'payment'
      if table[0:9] == 'recipient':
        tabletype = 'recipient'
      
      if tabletype:
        print "%s - %s" % (country, tabletype)
        
        print commands.getstatusoutput("mdb-export -H %s %s > /tmp/%s-%s.csv" % (db, table, country, table))
        
        reader = csv.reader(codecs.open("/tmp/%s-%s.csv" % (country, table),'r'))
        
        for line in reader:
          # Only loop 10 lines.  Just for testing!
          #if key > 10: 
          #  break
          #line = ",".join("\"%s\"" % field for field in line) 

          try:
            line = ",".join("'%s'" % re.escape(field) for field in line)

            sql = "INSERT INTO `%s` VALUES (%s);" % (table, line)
            #print sql
            c.execute(sql)
          except Exception,e:
            print line
            print sql
            print e


        
          
        # sys.exit()
        # rows = 

        # # cCreate the scheme file.  
        # # Scheme files are created sepirate so the data files can be split later, if need be.
        # schemepath = "%s%s/%s/" % (fsconf.schemedir, country, tabletype)
        # commands.getstatusoutput('mkdir -p %s' % (schemepath))
        # fields = commands.getstatusoutput('mdb-export %s %s | head -n 1' % (db,table))[1]
        # filename = "%s%s--%s.scheme" %(schemepath,dbid,table)
        # file = open(filename, 'w')
        # file.write(fields)
        # file.close()
        # file_all = open("%s/all-%s" % (fsconf.schemedir,tabletype),'a')
        # file_all.write(fields+"\n")
        # file_all.close()
        

  
  
  
  
  
  
  
if __name__ == '__main__':
  if len(sys.argv) > 1:
    if sys.argv[1] in countryCodes.countryCodes() or sys.argv[1] == "all":
      country = sys.argv[1]
      extractmdb2mysql(country)
    else:
      print "%s isn't a valid country code" % sys.argv[1]
  else:
    print "Usage: 'python mdb2csv.py [country|all]"
