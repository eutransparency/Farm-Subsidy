#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf

def extractmdb2csv():
  """Uses mdbtools to extract tables from access
  databases and put them in to a given directory, 
  as set in fsconf.py"""

  datadir = fsconf.datadir
  mdbdir = fsconf.mdbdir
  csvdir = fsconf.csvdir

  #Find all files with a .mdb extention and loop though them
  dbs = commands.getstatusoutput('find %s -name "*.mdb"' % (mdbdir))[1].splitlines()
  for db in dbs:

    # Get the path the file is in
    filepath = '/'.join(db.split('/')[:-1])

    # Get the file name
    filename = db.split('/')[-1]

    # Get the country
    country = filename.split('-')[0]

    # Make the country folder for the CSV files
    commands.getstatusoutput('mkdir %s/%s' % (csvdir,country))
    tables = commands.getstatusoutput('mdb-tables %s' % (db))[1].split(" ")
      
    for table in tables:
      if table[0:7] == 'payment':
        tabletype = 'payment'
      if table[0:9] == 'recipient':
        tabletype = 'recipient'
      
      if tabletype:
        print "%s - %s" % (country, tabletype)
        
        #Dump the table to a csv file
        tablepath = "%s/%s/%s/" % (csvdir,country, tabletype)
        commands.getstatusoutput('mkdir -p %s' % (tablepath))
        commands.getstatusoutput('mdb-export %s %s > %s%s.csv'% (db,table,tablepath,table))
      
        # Create the scheme file
        schemepath = "%s%s/%s/" % (fsconf.schemedir, country, tabletype)
        commands.getstatusoutput('mkdir -p %s' % (schemepath))
        fields = commands.getstatusoutput('head -n 1 %s%s.csv' % (tablepath,table))[1]
        filename = schemepath+table
        file = open(filename, 'w')
        file.write(fields)
        file.close()
        file_all = open("%s/all-%s" % (fsconf.schemedir,tabletype),'a')
        file_all.write(fields+"\n")
        file_all.close()
        
        tabletype = None
  
  
if __name__ == '__main__':
  extractmdb2csv()
