#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf, countryCodes

def extractmdb2csv(countryToProcess="all"):
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
    
    # Database ID
    dbid =  filename.split('.')[0]

    # Get the country
    country = countryCodes.filenameToCountryCode(filename)
    if countryToProcess != "all" and countryToProcess != country:
      continue
    
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
        commands.getstatusoutput('mdb-export -H %s %s > %s%s--%s.csv'% (db,table,tablepath,dbid,table))
      
        # Create the scheme file.  
        # Scheme files are created sepirate so the data files can be split later, if need be.
        schemepath = "%s%s/%s/" % (fsconf.schemedir, country, tabletype)
        commands.getstatusoutput('mkdir -p %s' % (schemepath))
        fields = commands.getstatusoutput('mdb-export %s %s | head -n 1' % (db,table))[1]
        filename = "%s%s--%s.scheme" %(schemepath,dbid,table)
        file = open(filename, 'w')
        file.write(fields)
        file.close()
        file_all = open("%s/all-%s" % (fsconf.schemedir,tabletype),'a')
        file_all.write(fields+"\n")
        file_all.close()
        
  
if __name__ == '__main__':
  if len(sys.argv) > 1:
    if sys.argv[1] in countryCodes.countryCodes() or sys.argv[1] == "all":
      country = sys.argv[1]
      extractmdb2csv(country)
    else:
      print "%s isn't a valid country code" % sys.argv[1]
  else:
    print "Usage: 'python mdb2csv.py [country|all]"