from django.template import Library, Node

from farmsubsidy.queries import queries

register = Library()
def top_recipients(location="EU", number=5):
  
  country = "country:%s" % location
  if location == "EU":
    country = ""
  
  options = {
    'page' : 0,
    'len' : number,
  }
  
  results = queries.do_search("%s amount:1000..1000000000" % country, options)
  
  return locals()

register.inclusion_tag('blocks/top_recipients.html')(top_recipients)  