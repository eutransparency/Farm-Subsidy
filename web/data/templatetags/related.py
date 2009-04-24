from django.template import Library, Node

from farmsubsidy.queries import queries
from farmsubsidy import fsconf
from farmsubsidy.indexer import countryCodes

register = Library()
def get_related(docid):
    
  results = queries.get_rset(docid)
  
  return locals()

register.inclusion_tag('blocks/related.html')(get_related)