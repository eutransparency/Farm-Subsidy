import re 
from django.template import Library, Node
from farmsubsidy.queries import queries
from farmsubsidy.indexer import countryCodes
from farmsubsidy import fsconf
register = Library()


# class LatestLinksNode(Node):
#     def __init__(self, bits):
#       self.bits = bits
#   
#     def render(self, context):
#       context['recent_links'] = self.bits
#       return ''
# 
# 
# def get_latest_links(parser, token):
#     bits = token.contents.split()
#     return LatestLinksNode(bits)
# 
# get_latest_links = register.tag(get_latest_links)


def countryBrowse(country, path):
  regions = queries.dumpRegions(country, path)
  # return {'regions' : regions}
  browsepaths = {}
  for region in regions:
    regionpath = "%s/%s" % (path,region)
    if regionpath[0] == "/":
      regionpath = regionpath[1:]
    
    browsepaths[region] = {
      'name' : re.sub('\+',' ', region),
      'path' : regionpath,
    }
  return {'regions' : browsepaths, 'country' : country}


register.inclusion_tag('data/blocks/regions.html')(countryBrowse)



def search(prefix, query, rlen=30, page=0, sort_value=fsconf.index_values['total_amount'],):
  options = {
  'sort_value' : sort_value,
  'collapse_key' : fsconf.index_values['recipient_id_x'],  
  'offset' : 0,
  'len' : rlen,
  'page' : page
  }
  results = queries.do_search(prefix+query, options)
  return {'results' : results}

register.inclusion_tag('data/blocks/results.html')(search)


def countryMenu(country=None):
  """returns a list of countries"""
  countries = {}
  for code,name in countryCodes.code2name.items():
    countries[code] = {
      'name' : name,
    }
  if country:
    countries[country]['active'] = 'active'
  return {'countries' : countries}

register.inclusion_tag('data/blocks/country-menu.html')(countryMenu)



