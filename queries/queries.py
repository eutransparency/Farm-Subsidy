#!/usr/bin/env python
# encoding: utf-8
"""
queries.py

Created by Sym on 2009-02-25.
"""

import sys
import os

import xapian
sys.path.append('../indexer')
import fsconf
import querylib

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


# def get_recipients(query):
#   DEFAULT_SEARCH_FLAGS = (
#           xapian.QueryParser.FLAG_BOOLEAN
#           )
#   
#   qp = xapian.QueryParser()
#   qp.set_default_op(xapian.Query.OP_AND)
#   
#   qp.add_boolean_prefix("rid", "XRID:")
#   qp.add_boolean_prefix("country", "XCOUNTRY:")
#   
# 
#   query = qp.parse_query(query, DEFAULT_SEARCH_FLAGS, "XNAME")
#   
#   return query
  


if __name__ == '__main__':
  
  
  query_string = querylib.parse_query(" ".join(sys.argv[1:]))
  print query_string
  
  (qp,valueranges) = querylib.load_queryparser()
  qp.set_default_op(xapian.Query.OP_AND)

  query = qp.parse_query(query_string, qp.FLAG_BOOLEAN, "XNAME")
  
  print "Parsed query is: %s" % query.get_description()
  v = []  
  db = querylib.load_database()
  # 
  enq = querylib.load_enquire(db)
  # 
  enq.set_query(query)
  enq.set_sort_by_value(fsconf.index_values['amount'],1)
  matches = enq.get_mset(0,10)
  # ids = []
  for m in matches:
    print xapian.sortable_unserialise(m.document.get_value(fsconf.index_values['amount']))
  # 
  # 
  # p_enq = querylib.load_enquire(db)
  # 
  # 
  # 
  # p_matches = p_enq.get_mset(0, 100)
  # for p in p_matches:
  #   print "%s" % p.document.get_value(0)      
  #   print "     %s" % xapian.sortable_unserialise(p.document.get_value(1))
  #   # print "     %s" % p.document.get_data()    
  # 
  #   # t = db.termlist(p.docid)
  #   # for term in t:
  #   #   print term.term
  #   
  