#!/usr/bin/env python
# encoding: utf-8


import xapian, sys, os
sys.path.append('/var/www/farmsubsidy/indexer/')
sys.path.append('/var/www/farmsubsidy/web/')

import web
from web import form
import fsconf

urls = (
  '/', 'index',
  '/results', 'results',
  )

application = web.application(urls, globals()).wsgifunc()
render = web.template.render('/var/www/farmsubsidy/web/templates/',base='layout')



search_form = form.Form(
  form.Textbox("query",descripton="Company name"),
  form.Button("submit", type="submit", description="search"),
)

  

class index:
    def GET(self):
      f = search_form()
      return render.index(f)

class results:
    def GET(self):
      i = web.input()
      results = xapian_search(i.query)
      return render.results(results)


def xapian_search(query):


  DEFAULT_SEARCH_FLAGS = (
          xapian.QueryParser.FLAG_BOOLEAN 
          )


  print >> sys.stderr, xapian.Database
  database = xapian.Database(fsconf.xapianDbPath)
  enquire = xapian.Enquire(database)
  query_string = query

  qp = xapian.QueryParser()
  qp.set_default_op(xapian.Query.OP_AND)

  amount = xapian.NumberValueRangeProcessor(1,"amount")
  qp.add_valuerangeprocessor(amount)

  year = xapian.NumberValueRangeProcessor(2,"year")
  qp.add_valuerangeprocessor(year)


  qp.set_database(database)
  qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

  qp.add_prefix("name", "XNAME")
  qp.add_boolean_prefix("id", "XID")
  qp.add_boolean_prefix("country", "XCOUNTRY")

  query = qp.parse_query(query_string, DEFAULT_SEARCH_FLAGS, "XNAME")
  
  results = {}
  results['decsription'] = "Parsed query is: %s" % query.get_description()

  enquire.set_query(query)
  matches = enquire.get_mset(0, 50)

  results['info'] = "%i results found.<br>" % matches.get_matches_estimated()
  results['documents'] = {}  
  for k,m in enumerate(matches):
    results['documents'][k] =  m.document.get_data()

  return results


#if __name__ == "__main__": app.run()



