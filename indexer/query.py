#!/usr/bin/env python2.5
# encoding: utf-8


import sys
import re
import os
import xapian
import fsconf


def get_doc_by_rid(RIDS):
  """Queries the database for a RID"""
  DEFAULT_SEARCH_FLAGS = (
          xapian.QueryParser.FLAG_BOOLEAN          
          )

  # Open the database for searching.
  database = xapian.Database(fsconf.xapianDbPath)

  # Start an enquire session.
  enquire = xapian.Enquire(database)

  query_string = " OR ".join(RIDS)


  qp = xapian.QueryParser()
  qp.set_default_op(xapian.Query.OP_OR)


  # qp.set_stemmer(xapian.Stem("english"))
  qp.set_database(database)
  qp.set_stemming_strategy(xapian.QueryParser.STEM_NONE)

  qp.add_boolean_prefix("id", "XRID")




  query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS, "XRID")
  # print "Parsed query is: %s" % query.get_description()


  enquire.set_query(query)
  matches = enquire.get_mset(0, 10)

  # Display the results.
  # print "%i results found." % matches.get_matches_estimated()
  # print "Results 1-%i:" % matches.size()

  for m in matches:
    # print m.document.get_data()
    # print "%i: %i%% docid=%i" % (m.rank + 1, m.percent, m.docid)


    t = database.termlist(m.docid)
    for term in t:
      if term.term[0:5] == "XYEAR":
        year = term.term[5:]
        print "year:",year



    v = m.document.values()
    #     name = []
    info = []
    for value in v:
      if value.num == 2:
        info.append(str(int(xapian.sortable_unserialise(value.value))))
      if value.num == 1:
        info.append(str(xapian.sortable_unserialise(value.value)))  
    print " - ".join(info)


def main_search():
  DEFAULT_SEARCH_FLAGS = (
          xapian.QueryParser.FLAG_BOOLEAN |
          xapian.QueryParser.FLAG_PHRASE |
          # xapian.QueryParser.FLAG_LOVEHATE |   
          # xapian.QueryParser.FLAG_BOOLEAN_ANY_CASE |
          xapian.QueryParser.FLAG_WILDCARD 
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

  amount = xapian.NumberValueRangeProcessor(2,"amount")
  qp.add_valuerangeprocessor(amount)

  year = xapian.NumberValueRangeProcessor(1,"year")
  qp.add_valuerangeprocessor(year)


  # qp.set_stemmer(xapian.Stem("english"))
  qp.set_database(database)
  qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

  qp.add_prefix("name", "XNAME")
  qp.add_boolean_prefix("country", "XCOUNTRY:")
  qp.add_boolean_prefix("id", "XID")
  qp.add_boolean_prefix("type", "XTYPE:")



  query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS, "XNAME")
  print "Parsed query is: %s" % query.get_description()


  enquire.set_query(query)
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
      print term.term
      if term.term[0:5] == "XNAME":
        name.append(term.term[5:])
      if term.term[0:4] == "XRID":
        RID.append(term.term[4:])
    print " ".join(name)
    # print RID
    # print get_doc_by_rid(RID)
    print "\n"
  
  
  
  
if __name__ == '__main__':
  main_search()