#!/usr/bin/env python
# encoding: utf-8
from __future__ import with_statement
import os, sys, string, commands, fsconf, scheme, csv, traceback, xapian
import math
from string import Template
from optparse import OptionParser
sys.path.append('lib')
import  progressbar
import countryCodes
import pprint
import mappings
import cPickle
import collections

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
  1. Load each data file to a csv reader object
  2. Loop though the data, line by line (doc by doc), trying to guess the field names.
  """

  global database, indexer
  database = xapian.WritableDatabase(fsconf.xapianDbPath, xapian.DB_CREATE_OR_OPEN)
  indexer = xapian.TermGenerator()
  stemmer = xapian.Stem("english")
  indexer.set_stemmer(stemmer)
  indexer.set_database(database)
  indexer.set_flags(indexer.FLAG_SPELLING)
  
  
  # Find each scheme file
  for dirpath, dirnames, filenames in os.walk(csvdir):
    
    for name in filenames: 

      if name[-7:] == ".scheme":
        # Get some information about the data
        meta = {}
        
        data_file_path = scheme.mapSchemeToData(name)
                
        meta['scheme'] = scheme.loadScheme("%s/%s" % (csvdir,name))
        meta['data'] = {}
        meta['country'] = countryCodes.filenameToCountryCode(name[12:])

        print meta['country']
        # TODO Add more options here.  Like the filename to index
        if country is not None and country != meta['country']:
          continue
      
        print "\n %s" % name  
      

        with open(data_file_path) as csvfile:
          counter = csv.reader(csvfile)
          linecount = 0
          for countline in counter:
            linecount = counter.line_num
            
          if linecount is 0:
            print "No content in %s" % csvfile
            continue
          
          pbar = progressbar.ProgressBar(maxval=linecount).start()

          reader = csv.reader(csvfile)                    
          csvfile.seek(0)
          for line in reader:


            for k,v in meta['scheme'].items():
              meta['data'][k] = line[v]
              
            meta['data']['country'] = meta['country'] #Because it's not always there
            
            recipient_id = None
            meta['linenumber'] = reader.line_num
            
            if options.test:
              # Only loop 10 lines.  Just for testing!
              if meta['linenumber'] > 10: 
                break
        
            index_line(line, meta)
          
            pbar.update(meta['linenumber'])
        # pbar.finish()
      database.flush()


def index_line(line,meta):
  """The workhorse of the indexing.
  Here we are given a line of a CSV file and a dictionary "meta" that contains 
  all sorts of information about that line.
  
  A line contains the joined payment and recipient information as created by
  mysql2csv.py.
  
  meta contains:
    * The information on what data is contained in a particulay column (as 
      defined in scheme.py)
  """
  doc = xapian.Document()
  
  #Create a unique document ID
  
  # TODO Come up with a really good, true, unique ID 
  #      (in a way that can make a nice hackable URL)
  
  # HACK because the year isn't always there.  Sigh.
  if 'year' not in meta['data']:
    meta['data']['year'] = "0"
   
  uniques = (
    meta['data']['country'],
    meta['data']['recipient_id'],
    meta['data']['payment_id'],
    scheme.calc_year(meta['data']['year']),
  )
  
  unique_id = "".join("%s" % v for v in uniques)

  doc.add_value(0,unique_id)
  docid = "XDOCID"+unique_id
  doc.add_term(docid)

  unique_id_x = (
  meta['data']['recipient_id_x']
  )
  
  unique_id_x = "".join("%s" % v for v in unique_id_x).lower()
  meta['data']['recipient_id_x'] = unique_id_x
  
  #print "\rindexing %s" % unique_id_x,

  fields = mappings.fieldTypeMaps()
  
  indexer.set_document(doc)
  
  index_text = []
  for field in meta['data']:
    if fields[field]:
      if 'formatter' in fields[field]:
        field_value = meta['data'][field]
        field_value = eval(fields[field]['formatter'])
      else:
        field_value = meta['data'][field]

      
      if 'prefix' in fields[field]:
        if 'index' in fields[field]:
          indexer.index_text(field_value,fields[field]['termweight'],fields[field]['prefix'])
        else:
          doc.add_term(fields[field]['prefix']+field_value)
      
      if 'value' in fields[field]:
        doc.add_value(fields[field]['value'],eval(fields[field]['value_formatter']))
      

      if 'index' in fields[field]:
        index_text.append(field_value)
      
  indexer.index_text(" ".join(index_text))

  doc.set_data(format_doc(meta,line))

  database.replace_document(docid,doc)



def format_doc(meta,line):
  """Takes a scheme, with all the data and returns a formatted HTML string"""

  doc = collections.defaultdict(dict)
  for item in meta['scheme']:
    doc[item] = line[meta['scheme'][item]]
  return cPickle.dumps(doc)
  


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

  parser.add_option("-e", "--test", action="store_true", dest="test",
                    help="Only process the first 10 lines of each file", metavar="[Y|N]")


  global options  
  (options, args) = parser.parse_args()



  if options.index:
    index(options.country,options.type,options.table)






