from django.db import models

from django.shortcuts import render_to_response
from simplejson import dumps
from django.utils.html import escape
from django.core import serializers 
import pyfo
import cPickle

from farmsubsidy.queries import queries
import farmsubsidy.fsconf as fsconf


def format_data(data, format):
  if format == "xml":    
    # Replace doc numbers with 'document' because xml can't have numbers as keys
    documents = []
    for doc in data['documents'].items():
      documents.append(('recipient', doc[1],))
    data['documents'] = documents
    
    data = pyfo.pyfo(('root',data), pretty=True)
    return data, "text/xml"
    
  if format == "json":
    return dumps(data), "application/json"
    
  if format == "pickle":
    return cPickle.dumps(data), "text"
  
  if format == "csv":
    csv = []
    for i,line in data['documents'].items():
      # assert False
      csv.append(
        ",".join('"%s"' % str(v) for k,v in line.items())
      )
      
    # assert False
    return ";\n".join(csv), "text"

def test(request):
  format = request.GET.get('format', 'xml')
  test = queries.do_search("roe")
  # data = serializers.serialize("json", test)
  data, mimetype = format_data(test, format)
    
  return render_to_response("data.html", {'data' : data}, mimetype=mimetype)
  
  
def get_recipient(request, rid):
  format = request.GET.get('format', 'xml')
  
  options = {
    'collapse_key' : fsconf.index_values['year'], 
    'page' : 0,
    'len' : 50
  }
  
  results = queries.do_search("xid:%s" % rid, options)

  data, mimetype = format_data(results, format)
    
  return render_to_response("data.html", {'data' : data}, mimetype=mimetype)






