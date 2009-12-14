#!/usr/bin/env python
# encoding: utf-8
"""
queries.py

Created by Sym on 2009-02-25.
"""
import xapian
if __name__ == "__main__":
  import sys
  sys.path.append('../..')
import cPickle
import re
import fsconf as fsconf


def load_doc(doc_id, db=None):
  """ Returns a xapian.Document with the given doc_id.
  
  - `doc_id` (int) the Document ID
  
  """
  return db.get_document(int(doc_id))


def search(query_string, options={'len' : 100, 'page' : 0, 'len' : 50,}, db=fsconf.xapianDbPath):
  """
  
  Main search function. Takes a string and a dict of options and returns a dict
  containing the results along with some meta data.
  
  Input values:
  
  - `query_string` String to create search from.  This is passes to xapian.QueryParser
  - `options` A dict of options.  Use for paging, sorting etc. (Full list of options below)
  
  Output values:
  
  - `results` a dict containing:
    - `description` string explaining the parsed query
    - `info` string containing the number of (estimated) matches
    - `documents` dict with a key for each document id and a value containing 
                  each document (as a dict)
    - `spelling` Suggected spelling for the query (if any)
    - `pager` dict of paging info, including 'page', 'results' and 'len'
  
    
  """
  
  db = xapian.Database(db)  
  qp = xapian.QueryParser()
  qp.set_default_op(xapian.Query.OP_AND)  
  qp.add_prefix('name', 'XNAME:')
  qp.add_prefix('id', 'XDOCID:')
  qp.set_database(db)
 
  DEFAULT_SEARCH_FLAGS = (
         xapian.QueryParser.FLAG_BOOLEAN |
         xapian.QueryParser.FLAG_PHRASE |
         xapian.QueryParser.FLAG_LOVEHATE |   
         xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
         xapian.QueryParser.FLAG_WILDCARD |
         xapian.QueryParser.FLAG_SPELLING_CORRECTION
         # xapian.QueryParser.FLAG_PARTIAL 
         )

  query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS )
  
  enq = enquire = xapian.Enquire(db)
  enq.set_query(query)
  

  offset = calcPages(options['page'], options['len'])
  length = options['len']

  
  if 'sort_value' in options:
    enq.set_sort_by_value(options['sort_value'],1)
  if 'collapse_key' in options:
    enq.set_collapse_key(options['collapse_key'])
  
  matches = enq.get_mset(offset, length)

  results = {}
  results['description'] = "Parsed query is: %s" % query.get_description()
  results['info'] = matches.get_matches_estimated()
  results['documents'] = {}
  results['spelling'] = qp.get_corrected_query_string()
  results['pager'] = {
    'page' : options['page'],
    'results' : results['info'],
    'len' : options['len']
  }

  for k,m in enumerate(matches):
    results['documents'][k] = dict(cPickle.loads(m.document.get_data()))
    results['documents'][k]['doc_id'] = m.document.get_docid()
    
  return results  


def calcPages(page,resultlen):
  """docstring for calcPages"""
  return resultlen*(page)

def simmlar_name(name, db=fsconf.xapianDbPath):
    options={
        'len' : 5,
        'page' : 0,
        'offset' : 0
        }
    name = re.sub('&','', name)
    results = search("name:%s" % " OR ".join(re.sub('  ', ' ', name).split(" ")), options) or {'documents' : {0 : {'name' : ''}}}
    if results['documents'][0]['name'] == name:
        del results['documents'][0]
    return results 


def get_rset(rid='GB131541', db=fsconf.xapianDbPath):
  db = xapian.Database(db) 
  
  qp = xapian.QueryParser()
  qp.set_default_op(xapian.Query.OP_AND)  
  qp.add_prefix('id', 'XDOCID:')
  qp.set_database(db)
 
  DEFAULT_SEARCH_FLAGS = (
         xapian.QueryParser.FLAG_BOOLEAN |
         xapian.QueryParser.FLAG_PHRASE |
         xapian.QueryParser.FLAG_LOVEHATE |   
         xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
         xapian.QueryParser.FLAG_WILDCARD |
         xapian.QueryParser.FLAG_SPELLING_CORRECTION
         # xapian.QueryParser.FLAG_PARTIAL 
         )

  query = qp.parse_query("id:%s" % rid, DEFAULT_SEARCH_FLAGS )
  enq = xapian.Enquire(db)
  enq.set_query(query)
  
  matches = enq.get_mset(0, 2)
  
  
  rset = xapian.RSet()
  eset = xapian.Enquire(db)
  rset.add_document(matches.begin())
  
  eset = eset.get_eset(5, rset);  
  query = xapian.Query(xapian.Query.OP_ELITE_SET, [k for k,v in eset])
  enq.set_query(query)
  
  matches = enq.get_mset(1,6)

  results = {}
  results['description'] = "Parsed query is: %s" % query.get_description()
  results['documents'] = {}
  results['size'] = matches.get_matches_estimated()

  for k,m in enumerate(matches):
    results['documents'][k] = dict(cPickle.loads(m.document.get_data()))
    results['documents'][k]['doc_id'] = m.document.get_docid()
  
  return results

if __name__ == "__main__":
  results = get_rset(" ".join(sys.argv[1:]))
  # sys.exit()
  
  options = {
    'page' : 0,
    'len' : 10,  
  }
  
  # results = search(" ".join(sys.argv[1:]), options)
  print results['description']  
  # if results['spelling']:
  #   print results['spelling']
  # print results['info']
  for key in results['documents']:
    meta = results['documents'][key]
    print meta['name'], "(%s)" % " ".join(str(v) for r,v in meta.items())
    print meta['doc_id']
