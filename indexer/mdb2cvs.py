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
    country = filenameToCountryCode(filename)
    
    # Make the country folder for the CSV files
    commands.getstatusoutput('mkdir %s/%s' % (csvdir,country))
    tables = commands.getstatusoutput('mdb-tables %s' % (db))[1].split(" ")
      
    for table in tables:

      tabletype = None

      if table[0:7] == 'payment':
        tabletype = 'payment'
      if table[0:9] == 'recipient':
        tabletype = 'recipient'
      
      if tabletype:
        print "%s - %s" % (country, tabletype)
        
        #Dump the table to a csv file
        tablepath = "%s/%s/%s/" % (csvdir,country, tabletype)
        commands.getstatusoutput('mkdir -p %s' % (tablepath))
        commands.getstatusoutput('mdb-export -H %s %s > %s%s.csv'% (db,table,tablepath,table))
      
        # Create the scheme file
        schemepath = "%s%s/%s/" % (fsconf.schemedir, country, tabletype)
        commands.getstatusoutput('mkdir -p %s' % (schemepath))
        fields = commands.getstatusoutput('mdb-export %s %s | head -n 1' % (db,table))[1]
        filename = schemepath+table+".scheme"
        file = open(filename, 'w')
        file.write(fields)
        file.close()
        file_all = open("%s/all-%s" % (fsconf.schemedir,tabletype),'a')
        file_all.write(fields+"\n")
        file_all.close()
        
def filenameToCountryCode(filename):
  if filename[0:7] == 'austria':
    return 'AT'
  if filename[0:7] == 'belgium':
    return 'UK'
  if filename[0:8] == 'bulgaria':
    return 'AT'
  if filename[0:5] == 'czech':
    return 'UK'
  if filename[0:8] == 'estonia':
    return 'AT'
  if filename[0:7] == 'finland':
    return 'UK'
  if filename[0:6] == 'france':
    return 'AT'
  if filename[0:7] == 'germany':
    return 'UK'
  if filename[0:7] == 'hungary':
    return 'AT'
  if filename[0:7] == 'ireland':
    return 'UK'
  if filename[0:5] == 'italy':
    return 'AT'
  if filename[0:6] == 'latvia':
    return 'UK'
  if filename[0:9] == 'lithuania':
    return 'AT'
  if filename[0:6] == 'poland':
    return 'UK'
  if filename[0:8] == 'portugal':
    return 'AT'
  if filename[0:8] == 'slovakia':
    return 'UK'
  if filename[0:8] == 'slovenia':
    return 'UK'
  if filename[0:5] == 'spain':
    return 'UK'
  if filename[0:7] == 'toscana':
    return 'UK'
  if filename[0:13] == 'unitedkingdom':
    return 'UK'
  if filename[0:13] == '':
    return 'UK'
  else:
    raise Exception, "Could not work out country for %s!" % filename
  
  
  
  
  
  
  
  
if __name__ == '__main__':
  extractmdb2csv()
