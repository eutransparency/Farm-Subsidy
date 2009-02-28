#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, fsconf, scheme, csv, traceback, xapian
import math
from string import Template
from optparse import OptionParser
sys.path.append('lib')
import  progressbar
import countryCodes
import pprint

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
  
  
  # Find each scheme file
  for dirpath, dirnames, filenames in os.walk(csvdir):
    
    for name in filenames: 

      if name[-7:] == ".scheme":
        print name  
        # Get some information about the data
        meta = {}
        
        data_file_path = scheme.mapSchemeToData(name)
                
        meta['scheme'] = scheme.loadScheme("%s/%s" % (csvdir,name))

        meta['country'] = countryCodes.filenameToCountryCode(name[12:])


        # TODO Add more options here.  Like the filename to index
        if country is not None and country != meta['scheme']['country']:
          continue
      

        # Open the data file for looping over
        reader = csv.reader(open(data_file_path))

        # FIXME - Can I just count the lines from the first reader?
        linecount = csv.reader(open(data_file_path))

      
        # pbar = progressbar.ProgressBar(maxval=len(list(linecount))).start()
        for key,line in enumerate(reader):
          recipient_id = None

          # Only loop 10 lines.  Just for testing!
          if key > 10: 
            break
        
          meta['linenumber'] = key+1
          
          
          index_line(line, meta)

          
        #   pbar.update(key)
        # pbar.finish()
      database.flush()


def index_line(line,meta):
  """docstring for index_line"""
  doc = xapian.Document()
  
  #Create a unique document ID
  
  # TODO Come up with a really good, true, unique ID 
  #      (in a way that can make a nice hackable URL)
  
  uniques = (
    meta['country'], 
    line[meta['scheme']['year']], 
    line[meta['scheme']['recipient_id']],
  )
  
  unique_id = "-".join("%s" % v for v in uniques)
    
  doc.add_value(0,unique_id)
  docid = "XDOCID"+unique_id
  doc.add_term(docid)

  fields = scheme.fieldTypeMaps()

  # pp = pprint.PrettyPrinter(indent=4)
  # pp.pprint(dict(fields))
  # 
  # sys.exit()
  indexer.set_document(doc)
  
  for field in meta['scheme']:
    if fields[field]:
      if meta['scheme'][field] in range(len(line)):
        if 'formatter' in fields[field]:
          field_value = line[meta['scheme'][field]]
          field_value = eval(fields[field]['formatter'])
        else:
          field_value = line[meta['scheme'][field]]
      else:
        field_value = meta['scheme'][field]

      
      if 'prefix' in fields[field]:
        if 'index' in fields[field]:
          indexer.index_text(field_value,fields[field]['termweight'],fields[field]['prefix'])
          print "yes"
        else:
          doc.add_term(fields[field]['prefix']+field_value)
      
      if 'value' in fields[field]:
        print field_value
        # print fields[field]['value'],eval(fields[field]['value_formatter'])
        doc.add_value(fields[field]['value'],eval(fields[field]['value_formatter']))
      
      # if 'formatter' in fields[field]:
      #   print field,eval(fields[field]['formatter'])
      # else:
      #   print field,meta['scheme'][field]

        
  
  # print meta
  # sys.exit()

  # doc.add_term("XCOUNTRY:"+meta['country'])
  # 
  # if 'recipient_id' in meta['scheme']:
  #   rid = "%s" % (line[meta['scheme']['recipient_id']])
  #   doc.add_value(3,rid)
  #   doc.add_term("XRID:%s" % rid)

  doc.set_data(format_doc(meta,line))


  database.replace_document(docid,doc)

  
def index_payments(data,line):
  """indexes all payment records"""
  doc = xapian.Document()


  #Create a unique document ID
  unique_id = "%s-%s-%s" % (data['country'], data['table'].split('.')[0], line[data['scheme']['recipient_id']])  
  doc.add_value(0,unique_id)
  docid = "XDOCID"+unique_id
  doc.add_term(docid)

  doc.add_term('XTYPE:payment')

  if 'recipient_id' in data['scheme']:
    rid = "%s-%s" % (data['database'],line[data['scheme']['recipient_id']])
    doc.add_value(3,rid)
    doc.add_term("XRID:%s" % rid)

  if 'amount' in data['scheme']:
    if line[data['scheme']['amount']] is not "":
      doc.add_value(1,xapian.sortable_serialise(float(line[data['scheme']['amount']])))
  if 'year' in data['scheme']:
    data['calced_year'] = loadScheme.calc_year(line[data['scheme']['year']],options.fragile)
    if data['calced_year']:
      doc.add_value(2,xapian.sortable_serialise(data['calced_year']))

  doc.set_data(format_doc(data,line))

  indexer.set_document(doc)

  if not options.dryrun:
    database.replace_document(docid,doc)


def index_recipient(data,line):
  """indexes all recipient records"""
  doc = xapian.Document()

  #Create a unique document ID
  unique_id = "%s-%s-%s" % (data['country'], data['table'].split('.')[0], line[data['scheme']['recipient_id']])  
  doc.add_value(0,unique_id)
  docid = "XDOCID"+unique_id
  doc.add_term(docid)

  doc.add_term('XTYPE:recipient')

  doc.add_term("XCOUNTRY:"+data['country'])

  if 'recipient_id' in data['scheme']:
    rid = "%s-%s" % (data['database'],line[data['scheme']['recipient_id']])
    doc.add_value(3,rid)
    doc.add_term("XRID:%s" % rid)
    
  # Will add this later:
  # if 'address1' in scheme:
  #   if data['address1'] not "":
  #     doc.add_term("XADDRESS1:"+line[data['address1']])

  doc.set_data(format_doc(data,line))
  indexer.set_document(doc)

  indexer.index_text(line[data['scheme']['name']],10,"XNAME")

  if not options.dryrun:
    database.replace_document(docid,doc)





def format_doc(data,line):
  """Takes a scheme, with all the data and returns a formatted HTML string"""
  # line = '"%s"' % ('","'.join(line))
  doc = []
  for item in data:
    if item == "scheme":
      doc.append('<div class="scheme">')
      for schemeitem in data[item]:
        s = Template('  <div class="$key">$value</div>')
        doc.append(s.substitute(key=schemeitem, value=data[item][schemeitem]))
      doc.append('</div>')        
    else:
      s = Template('<div class="$key">$value</div>')
      doc.append(s.substitute(key=item, value=data[item]))
  s = Template('<div class="line">$value</div>')
  doc.append(s.substitute(value='"%s"' % ('","'.join(line))))
  
  doc.append('<div class="originaldata">')
  
  for item in data['scheme']:
    s = Template('  <div class="$key">$value</div>')
    doc.append(s.substitute(key=item, value=line[data['scheme'][item]]))
  doc.append('</div>')        

  # print "\n".join(doc)
  
  # print scheme,line
  return "\n".join(doc)


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






