from django.template import Library, Node
from django.core.urlresolvers import reverse
from urllib import urlencode

# from web.graphs.graphlib import make_fig

register = Library()


def graph(graph_type, data):
  
  if graph_type == "country_years":
    url = reverse('country_graph', kwargs={'country':data})
    print url
    return {'url' : "%s" % (url)}


  if graph_type == "recipient_graph":
    url = reverse('recipient_graph', kwargs={'recipient_id':data})
    print url
    return {'url' : "%s" % (url)}
    
    
register.inclusion_tag('recipient-graph.html')(graph)
