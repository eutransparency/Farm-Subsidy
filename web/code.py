#!/usr/bin/env python
# encoding: utf-8


import xapian, sys, os
sys.path.append('/var/www/farmsubsidy/indexer/')
sys.path.append('/var/www/farmsubsidy/web/')
sys.path.append('/var/www/farmsubsidy/queries')

import web
from web import form
import fsconf
import queries

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
      results = queries.do_search(i.query)
      return render.results(results)
