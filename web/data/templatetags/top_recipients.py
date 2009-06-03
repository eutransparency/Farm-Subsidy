from django.template import Library, Node

from farmsubsidy.queries import queries
from farmsubsidy import fsconf
from farmsubsidy.indexer import countryCodes

register = Library()
def top_recipients(location="EU", number=5):
  
  country = "country:%s" % location
  if location == "EU":
    country = ""
    countryname = "Europe"
  else:
    countryname = countryCodes.code2name[location.strip()]  
    
  options = {
    'page' : 0,
    'len' : number,
    'collapse_key' : fsconf.index_values['global_id_x'],  
    'sort_value' : fsconf.index_values['amount'],
    'cache' : True,
  }
  
  results = queries.do_search("%s amount:1000..1000000000" % country, options)
  
  
  
  return locals()

register.inclusion_tag('blocks/top_recipients.html')(top_recipients)  