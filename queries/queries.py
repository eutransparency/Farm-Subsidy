#!/usr/bin/env python
# encoding: utf-8
"""
queries.py

Created by Sym on 2009-02-25.
"""

import sys
import os
import re
import xapian
from farmsubsidy import fsconf as fsconf
import querylib
import cPickle

def load_doc(doc_id, db=querylib.load_database()):
  """ Returns a xapian.Document with the given doc_id.
  
  - `doc_id` (int) the Document ID
  
  """
  return db.get_document(int(doc_id))


def get_payments_by_rid(rid, db=querylib.load_database()):
  """Creates a query that searches on an RID for all payments
  
  - `rid` list of recipient IDs to be OR'd together.
  
  """
  
  DEFAULT_SEARCH_FLAGS = (
          xapian.QueryParser.FLAG_BOOLEAN
          )
  
  qp = xapian.QueryParser()
  qp.set_default_op(xapian.Query.OP_OR)
  
  qp.add_boolean_prefix("id", "XRID:")
  qp.add_boolean_prefix("type", "XTYPE:")
  
  rid_string = " OR ".join(['(id:%s)' % (v) for v in rid])
  query = qp.parse_query('(%s) AND type:payment' % (rid_string), DEFAULT_SEARCH_FLAGS,)
  
  return query
  

def do_search(query, options={'len' : 100, 'page' : 0, 'len' : 50,}):  
      
  
  query_string = querylib.parse_query(query)
  (qp,valueranges) = querylib.load_queryparser()
  db = querylib.load_database()
  qp.set_database(db)
 
  qp.set_default_op(xapian.Query.OP_AND)
  DEFAULT_SEARCH_FLAGS = (
         xapian.QueryParser.FLAG_BOOLEAN |
         xapian.QueryParser.FLAG_PHRASE |
         # xapian.QueryParser.FLAG_LOVEHATE |   
         # xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
         xapian.QueryParser.FLAG_WILDCARD |
         xapian.QueryParser.FLAG_SPELLING_CORRECTION
         # xapian.QueryParser.FLAG_PARTIAL 
         )


  query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS )
  
 # print "Parsed query is: %s" % query.get_description()
  enq = querylib.load_enquire(db)
  enq.set_query(query)

  if 'sort_value' in options:
    enq.set_sort_by_value(options['sort_value'],1)
  if 'collapse_key' in options:
    enq.set_collapse_key(options['collapse_key'])

  matches = enq.get_mset(calcPages(options['page'], options['len']),options['len'],)

  results = {}
  results['decsription'] = "Parsed query is: %s" % query.get_description()
  results['info'] = "%i results found." % (matches.get_matches_estimated())
  results['documents'] = {}
  results['spelling'] = qp.get_corrected_query_string()
  results['size'] = matches.get_matches_estimated()

  for k,m in enumerate(matches):
    results['documents'][k] = dict(cPickle.loads(m.document.get_data()))
    # results['documents'][k] = get_collapse_count()
    

  return results

def calcPages(page,resultlen):
  """docstring for calcPages"""
  return resultlen*(page)

def allterms(prefix=''):
  db = querylib.load_database()
  return db.allterms(prefix)


def dumpRegions(country, path=''):
  """dumps all regions in the 'geopath' term in to a file"""
    
  path = "XGEOPATH:%s" % (path)
  # return path
  regions = []
  for term in allterms(path):
    region = term.term[len(path)+1:].split('/')[0]
    if region != "":
      regions.append(region)
  return set(regions)




if __name__ == "__main__":
  results = do_search(" ".join(sys.argv[1:]))
  print results['decsription']  
  if results['spelling']:
    print results['spelling']
  print results['info']
  for key in results['documents']:
    meta = results['documents'][key]
    print meta['name']





