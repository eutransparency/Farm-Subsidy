#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf, loadScheme

# This modules should:
# 
# 1. loop though everthing in the data directory
# 2. Load the scheme for that file
# 3. Find out what type of file it is (payment or recepant)
# 4. index it in to xapian

datadir = fsconf.datadir
csvdir = fsconf.csvdir
schemedir = fsconf.schemedir


def index():
  for dirpath, dirnames, filenames in os.walk(schemedir):
    for name in filenames: 
      if name[-7:] == ".scheme":
        schemeFilePath = os.path.join(dirpath, name)
        scheme = loadScheme.loadScheme(schemeFilePath)
        
        dataFilePath = mapSchemeToData(schemeFilePath)
        
        country = dataFilePath.split('/')[-3]
        tabletype = dataFilePath.split('/')[-2]
        table = dataFilePath.split('/')[-1]
        
        reader = file(dataFilePath)
                
        for key,line in enumerate(reader):
          recipient_id = None
          if key > 10: # just for testing :)
            break
          values = line.split(',')
          if tabletype == 'payment':
            try:
              rec_type = 'payment'
              amount = values[scheme['amount']]
              payment_id = values[scheme['payment_id']]
              recipient_id = values[scheme['recipient_id']]              
            except:
              raise Exception, "There was an error, maybe with the scheme mappings for %s/%s/%s?" % (country, tabletype, table)
          if tabletype == 'recipient':
            try:
              rec_type = 'recipient'
              name = values[scheme['name']]
              recipient_id = values[scheme['recipient_id']]
            except:
              pass
          print country,rec_type,recipient_id

def mapSchemeToData(schemefile):
  """Maps a given scheme file to the relivent data file"""
  path = "%s/%s.csv" % (csvdir, "/".join(schemefile.split('/')[-3:]).split('.')[0])
  if os.path.exists(path):
    return path
  else:
    raise Exception, "The scheme file %s has no data file mapping at %s" % (schemefile, path)
  
if __name__ == '__main__':
  index()
  