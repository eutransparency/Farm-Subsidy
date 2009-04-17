from django.template import Library, Node
from django.core.urlresolvers import reverse
from urllib import urlencode

# from web.graphs.graphlib import make_fig

register = Library()


def graph(graph_type, data):
  
  if graph_type == "recipient":
    # We want a graph with amount/year values for this recipient
    values = {}
    for i,document in data['documents'].items():
      if not document['year'] in values:
        values[document['year']] = 0
      values[document['year']] += float(document['amount'])
    get_data = urlencode(values)
    url = reverse('graph', kwargs={'type':graph_type})
    
  return {'url' : "%s?%s" % (url,get_data)}

register.inclusion_tag('recipient-graph.html')(graph)