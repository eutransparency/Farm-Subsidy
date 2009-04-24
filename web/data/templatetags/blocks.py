import re 
from farmsubsidy.queries import queries
from farmsubsidy.indexer import countryCodes
from farmsubsidy import fsconf
from farmsubsidy.web.data import forms
from django.template import Library, Node
from django import forms
register = Library()


def countryBrowse(country, path):
  regions = queries.dumpRegions(country, path)
  # return {'regions' : regions}
  browsepaths = {}
  for region in regions:
    regionpath = "%s/%s" % (path.encode('utf8'),region)
    if regionpath[0] == "/":
      regionpath = regionpath[1:]
    
    browsepaths[region] = {
      'name' : re.sub('\+',' ', region),
      'path' : regionpath,
    }
  return {'regions' : browsepaths, 'country' : country}


register.inclusion_tag('blocks/regions.html')(countryBrowse)

def browsePathTitle(browsepath):
  stem = ""
  paths = browsepath.split('/')
  if len(paths) > 1:
    for path in paths:
      stem = " | ".join([path,stem])
    try:
      return countryCodes.code2name[re.sub('\+',' ',stem)]
    except:
      return re.sub('\+',' ',stem)
  return ''
register.simple_tag(browsePathTitle)

def browsePathHead(browsepath):
  try:
    return countryCodes.code2name["%s" % browsepath.split('/')[-1:][0]]
  except:
    return "%s" % re.sub('\+',' ',browsepath.split('/')[-1:][0])
register.simple_tag(browsePathHead)


def search_form(q=None):
  form = forms.SearchFormLite(initial={'q' : q})
  return {'form' : form, 'q' : q}
register.inclusion_tag('blocks/search_form.html')(search_form)  



def search(prefix, query, rlen=30, page=0, sort_value=fsconf.index_values['total_amount'],):
  options = {
  'sort_value' : sort_value,
  'collapse_key' : fsconf.index_values['recipient_id_x'],  
  'offset' : 0,
  'len' : rlen,
  'page' : page,
  # 'cache' : True,
  }
  results = queries.do_search(prefix+query, options)
  return {'results' : results}

register.inclusion_tag('blocks/results.html')(search)


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

register.inclusion_tag('blocks/country-menu.html')(countryMenu)



