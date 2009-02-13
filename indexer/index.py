#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf, loadScheme, csv, traceback, xapian
sys.path.append('lib')
import  progressbar

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
  stemmer = xapian.Stem("english")
  indexer.set_stemmer(stemmer)
  
  
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
        linecount = csv.reader(open(dataFilePath))
        
        pbar = progressbar.ProgressBar(maxval=len(list(linecount))).start()
        for key,line in enumerate(reader):
          recipient_id = None

          # Only loop 10 lines.  Just for testing!
          # if key > 10: 
          #   break

          if scheme['tabletype'] == 'payment':
            # We're looking at a payment record
            index_payments(scheme,line)


          if scheme['tabletype'] == 'recipient':
            # We're looking at a payment record
            index_recipient(scheme,line)
            
          pbar.update(key)
        pbar.finish()
    database.flush()

  
def index_payments(scheme,line):
  """indexes all payment records"""
  doc = xapian.Document()
  doc.set_data("|||".join(line))

  #Create a unique document ID
  unique_id = "%s-%s-%s" % (scheme['country'], scheme['table'].split('.')[0], line[scheme['recipient_id']])  
  doc.add_value(0,unique_id)
  docid = "XDOCID"+unique_id
  doc.add_term(docid)

  if 'recipient_id' in scheme:
    doc.add_term("XRID"+line[scheme['recipient_id']])
  
  if 'amount' in scheme:
    if line[scheme['amount']] is not "":
      doc.add_value(1,xapian.sortable_serialise(float(line[scheme['amount']])))
  if 'year' in scheme:
    try:
      year_float = float(line[scheme['year']])
      doc.add_value(2,xapian.sortable_serialise(float(line[scheme['year']])))
    except:
      f = open('/tmp/borkedyears/%s-%s.txt' % (scheme['country'],scheme['table']),'w')
      f.write(",".join(line))
      f.close()

  indexer.set_document(doc)

  database.replace_document(docid,doc)


def index_recipient(scheme,line):
  """indexes all recipient records"""
  doc = xapian.Document()
  doc.set_data("|||".join(line))

  #Create a unique document ID
  unique_id = "%s-%s-%s" % (scheme['country'], scheme['table'].split('.')[0], line[scheme['recipient_id']])  
  doc.add_value(0,unique_id)
  docid = "XDOCID"+unique_id
  doc.add_term(docid)

  doc.add_term("XCOUNTRY:"+scheme['country'])

  if 'recipient_id' in scheme:
    doc.add_term("XRID"+line[scheme['recipient_id']])
    
  # Will add this later:
  # if 'address1' in scheme:
  #   if scheme['address1'] not "":
  #     doc.add_term("XADDRESS1:"+line[scheme['address1']])

  indexer.set_document(doc)

  indexer.index_text(line[scheme['name']],10,"XNAME")
  
  database.replace_document(docid,doc)


if __name__ == '__main__':
  index()
