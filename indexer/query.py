#!/usr/bin/env python2.5
# encoding: utf-8


import sys
import re
import os
import xapian
import fsconf


def main_search():
  DEFAULT_SEARCH_FLAGS = (
          xapian.QueryParser.FLAG_BOOLEAN |
          xapian.QueryParser.FLAG_PHRASE |
          # xapian.QueryParser.FLAG_LOVEHATE |   
          # xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
          xapian.QueryParser.FLAG_WILDCARD | 
          xapian.QueryParser.FLAG_SPELLING_CORRECTION
          # xapian.QueryParser.FLAG_PARTIAL 
          )

  # Open the database for searching.
  database = xapian.Database(fsconf.xapianDbPath)

  # Start an enquire session.
  enquire = xapian.Enquire(database)

  query_string = " ".join(sys.argv[1:])

  # print sys.argv[1:]

  qp = xapian.QueryParser()
  qp.set_default_op(xapian.Query.OP_AND)

  amount = xapian.NumberValueRangeProcessor(fsconf.index_values['amount'],"amount:")
  qp.add_valuerangeprocessor(amount)
  print fsconf.index_values['amount']
  year = xapian.NumberValueRangeProcessor(fsconf.index_values['year'],"year:")
  qp.add_valuerangeprocessor(year)


  # qp.set_stemmer(xapian.Stem("english"))
  qp.set_database(database)
  qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

  qp.add_prefix("name", "XNAME")
  qp.add_boolean_prefix("country", "XCOUNTRY:")
  qp.add_boolean_prefix("id", "XRID:")
  qp.add_boolean_prefix("type", "XTYPE:")


  stopper = xapian.SimpleStopper()
  stopper.add('and')
  stopper.add('my')  
  qp.set_stopper(stopper)

  print "Ignored:"
  for word in qp.stoplist():
    print word


  query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS)
  print "Parsed query is: %s" % query.get_description()
  
  print "Did you mean:%s" % qp.get_corrected_query_string()
  
  enquire.set_query(query)
  #enquire.set_collapse_key(fsconf.index_values['recipient_id_x'])
  matches = enquire.get_mset(0, 10)

  # Display the results.
  print "%i results found." % matches.get_matches_estimated()
  print "Results 1-%i:" % matches.size()

  for m in matches:
    # print m.document.get_data()
    print "%i: %i%% docid=%i" % (m.rank + 1, m.percent, m.docid)
    t = database.termlist(m.docid)
    name = []
    RID = []
    for term in t:
      if term.term[0:5] == "XNAME":
        name.append(term.term[5:])
      if term.term[0:5] == "XRID:":
        RID.append(term.term[5:])
    print " ".join(name)
    print "RID:",RID
    # print get_doc_by_rid(RID)

    v = m.document.values()
    #     name = []
    info = []
    for value in v:
      print value.num,value.value

    print "\n\n"
    
    
  
def allterms():
  database = xapian.Database(fsconf.xapianDbPath)  
  for term in database.allterms("XPATH:/a"):
    print term.term
  
if __name__ == '__main__':
  main_search()
  # allterms()







