#!/usr/bin/env python
# encoding: utf-8

import os, sys, string, commands, traceback, xapian
sys.path.append('..')
import fsconf
from optparse import OptionParser
from lib import progressbar
import countryCodes
import pprint
import cPickle
import collections
import re
import psycopg2
import psycopg2.extras


import connection


def index(country):
  conn, c = connection.connect()
  c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  database = xapian.WritableDatabase(fsconf.xapianDbPath, xapian.DB_CREATE_OR_OPEN)
  indexer = xapian.TermGenerator()
  stemmer = xapian.Stem("english")
  indexer.set_stemmer(stemmer)
  indexer.set_database(database)
  indexer.set_flags(indexer.FLAG_SPELLING)
  
  
  sql = """
    SELECT t.global_id, t.countrypayment, r.name, r.address1, r.address2, r.town, r.geo1, r.geo2, r.geo3, r.geo4, t.amount_euro
    FROM data_recipients r
    JOIN data_totals t
    ON t.global_id=r.globalrecipientidx
    WHERE t.year=0 AND r.name IS NOT NULL AND r.countryrecipient='%(country)s'
  """ % locals()
  
  
  c.execute(sql)
    
  pbar = progressbar.ProgressBar(maxval=c.rowcount).start()
  row = c.fetchone()
  while row:
    # print "\rAdding Document %s (%s)" % (i, row['global_id']),
    doc = xapian.Document()
    indexer.set_document(doc)
    
    
    doc.add_value(1, xapian.sortable_serialise(float(row['amount_euro'])) )
    
    geo_fields = ['address1','address2','town','geo1','geo2','geo3','geo4', 'countrypayment',]
    location_text = ""
    for field in geo_fields:
      if row[field]:
        location_text += " " + row[field]
    # Index terms with prefixes    
    indexer.index_text(location_text.lower(),1,'XLOC:')
    indexer.index_text(row['name'].lower(),1000,'XNAME:')
    doc.add_term("XCOUNTRY:%s" % row['countrypayment'].lower())
    
    # Index the same terms without prefixes
    indexer.index_text(location_text.lower(), 1)
    indexer.index_text(row['name'].lower(), 1000)
    
    
    docid = "XDOCID:%s" % row['global_id'].lower()
    doc.add_term(docid)
    doc.set_data(cPickle.dumps(dict(row)))
    database.replace_document(docid,doc)

        
    # for term in doc.termlist():
    #   print term.term
    # sys.exit()
    pbar.update(c.rownumber)
    row = c.fetchone()
  pbar.finish()

if __name__ == "__main__":
  index('GB')
  
  
  
  