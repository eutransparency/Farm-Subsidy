#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf, loadScheme, csv, traceback, xapian
import math
from optparse import OptionParser
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


def index(country=None, tabletype=None, table=None):
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

        # Load the scheme information        
        schemeFilePath = os.path.join(dirpath, name)
        scheme = loadScheme.loadScheme(schemeFilePath)
      
      
        # Get some information about the data
        dataFilePath = loadScheme.mapSchemeToData(schemeFilePath)
        scheme['country'] = dataFilePath.split('/')[-3]
        scheme['tabletype'] = dataFilePath.split('/')[-2]
        scheme['table'] = dataFilePath.split('/')[-1]
        scheme['database'] = scheme['table'].split('--')[0]

        if country is not None and country != scheme['country']:
          continue

        if tabletype is not None and tabletype != scheme['tabletype']:
          continue
        
        if table is not None and table != scheme['table']:
          continue        
                
        # Open the data file for looping over
        reader = csv.reader(open(dataFilePath))
        linecount = csv.reader(open(dataFilePath))
        
        print scheme['country'],scheme['tabletype'],scheme['table']
        
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
    doc.add_term("XRID:%s-%s" % (scheme['database'],line[scheme['recipient_id']]))
  
  if 'amount' in scheme:
    if line[scheme['amount']] is not "":
      doc.add_value(1,xapian.sortable_serialise(float(line[scheme['amount']])))
  if 'year' in scheme:
    calced_year = calc_year(line[scheme['year']])
    if calced_year:
      doc.add_value(2,xapian.sortable_serialise(calced_year))


  indexer.set_document(doc)

  if not options.dryrun:
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
  
  if not options.dryrun:
    database.replace_document(docid,doc)



def calc_year(year):
  """Takes a string in the format of either '2000', '2000-2001' or '2000-2008'
  and does something sane with them"""
  years = str(year).split('-')
  for key,year in enumerate(years):
    years[key] = float(year)

  years_len = len(range(int(years[0]),int(years[-1])))
  if years_len > 2:
    if not options.fragile:
      return
    else:
      raise ValueError, "Year span too long"
  elif years_len < 1:
    year_int = int(math.ceil(sum(years)))
  else:
    year_int = int(math.ceil(sum(years) / 2))
  return year_int



if __name__ == '__main__':
  
  parser = OptionParser()
  
  parser.add_option("-c", "--country", dest="country",
                    help="ISO country code, as defined by countryCodes.py", metavar="COUNTRY")

  parser.add_option("-t", "--type", dest="type",
                    help="Table type: paymnt or recipient", metavar="TYPE")
  
  parser.add_option("-n", "--tablename", dest="table",
                    help="Table name, if indexing a single table only.  Should be used with country", metavar="NAME")

  parser.add_option("-i", "--index", action="store_true", dest="index",
                    help="Index, the default action", metavar="[Y|N]")

  parser.add_option("-d", "--debug", action="store_true", dest="debug",
                    help="debug: write stuff to files", metavar="[Y|N]")

  parser.add_option("-F", "--fragile", action="store_true", dest="fragile",
                    help="Fragile: fall over if there are problems (option debug mode)", metavar="[Y|N]")

  parser.add_option("-r", "--dry-run", action="store_true", dest="dryrun",
                    help="Do everything without adding a document to xapian", metavar="[Y|N]")

  global options  
  (options, args) = parser.parse_args()



  if options.index:
    index(options.country,options.type,options.table)






