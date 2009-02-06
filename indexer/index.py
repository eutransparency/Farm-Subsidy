#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf, loadScheme, csv, traceback, xapian

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
  """The Main indexing function.  This will:
  1. Load each scheme and check the data file exists for it
  2. Load the data file in to a csv reader object
  3. Loop though the data, line by line, trying to guess the field names.
  """
  global database,indexer 
  database = xapian.WritableDatabase(fsconf.xapianDbPath, xapian.DB_CREATE_OR_OPEN)
  indexer = xapian.TermGenerator()

  
  # Find each scheme file
  for dirpath, dirnames, filenames in os.walk(schemedir):
    for name in filenames: 
      if name[-7:] == ".scheme":
        schemeFilePath = os.path.join(dirpath, name)
        
        # Load the scheme information
        scheme = loadScheme.loadScheme(schemeFilePath)
        
        # Get some information about the data
        dataFilePath = loadScheme.mapSchemeToData(schemeFilePath)
        scheme['country'] = dataFilePath.split('/')[-3]
        scheme['tabletype'] = dataFilePath.split('/')[-2]
        scheme['table'] = dataFilePath.split('/')[-1]
        
        
        
        # Open the data file for looping over
        reader = csv.reader(open(dataFilePath))
        for key,line in enumerate(reader):
          recipient_id = None
          
          # Only loop 10 lines.  Just for testing!
          # if key > 10: 
          #             break
                    
          if scheme['tabletype'] == 'payment':
            # We're looking at a payment record
            index_payments(scheme,line)
                            
              
          if scheme['tabletype'] == 'recipient':
            # We're looking at a payment record
            index_recipient(scheme,line)
    database.flush()

  
def index_payments(scheme,line):
  """indexes all payment records"""
  pass

def index_recipient(scheme,line):
  """indexes all recipient records"""
  doc = xapian.Document()
  doc.set_data("|||".join(line))
  
  unique_id = "%s-%s-%s" % (scheme['country'], scheme['table'].split('.')[0], line[scheme['recipient_id']])  
  doc.add_value(0,unique_id)
  docid = "XDOCID"+unique_id
  doc.add_term(docid)

  indexer.set_document(doc)
  # print line[scheme['name']]
  indexer.index_text(line[scheme['name']],10,"XNAME")

  # for value in doc.values():
  #   print value.num,value.value
  
  # print doc
  
  database.replace_document(docid,doc)

  # payment_id = line[scheme['payment_id']]
                  
  # try:

  #   amount = line[scheme['amount']]
  #   try:
  #     payment_id = line[scheme['payment_id']]
  #   except:
  #     payment_id = 0
  #   recipient_id = line[scheme['recipient_id']]              
  # except Exception, e:
  #   print scheme
  #   print line
  #   print e
  #   traceback.print_exc()  
  #   sys.exit()

if __name__ == '__main__':
  index()
