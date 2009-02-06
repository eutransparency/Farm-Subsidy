#!/usr/bin/env python2.5
# encoding: utf-8


import sys
import re
import os
import xapian
import fsconf

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

amount = xapian.NumberValueRangeProcessor(1,"amount")
qp.add_valuerangeprocessor(amount)

year = xapian.NumberValueRangeProcessor(2,"year")
qp.add_valuerangeprocessor(year)


# qp.set_stemmer(xapian.Stem("english"))
qp.set_database(database)
qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

qp.add_prefix("name", "XNAME")
qp.add_boolean_prefix("id", "XID")




query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS, "XNAME")
print "Parsed query is: %s" % query.get_description()


enquire.set_query(query)
matches = enquire.get_mset(0, 10)

# Display the results.
print "%i results found." % matches.get_matches_estimated()
print "Results 1-%i:" % matches.size()

for m in matches:
  title = re.search("<h1>[^<]+<",m.document.get_data())
  print m.document.get_data()
  print "%i: %i%% docid=%i" % (m.rank + 1, m.percent, m.docid)
