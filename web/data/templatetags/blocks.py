import re 
from farmsubsidy.queries import queries
from farmsubsidy.indexer import countryCodes
from farmsubsidy import fsconf
from farmsubsidy.web.data import forms
from django.template import Library, Node
from django import forms
register = Library()


def regionBrowse(country, path):
  regions = queries.dumpRegions(country, path)

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


register.inclusion_tag('blocks/regions.html')(regionBrowse)

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
  'cache' : True,
  }
  
  if len(query.split("/")) < 2:
    query = "%s amount:100000..100000000"  % query
  results = queries.do_search(prefix+query, options)
  return {'results' : results}

register.inclusion_tag('blocks/results.html')(search)


def countryMenu(country='UK'):
  """returns a list of countries"""
  countries = []
  for code,name in countryCodes.code2name.items():
    if country == code:
      countries.append({
        'name' : name,
        'code' : code,
        'active' : 'acitve'
      })
    else:
      countries.append({
        'name' : name,
        'code' : code,
      })
  return {'countries' : countries}

register.inclusion_tag('blocks/country-menu.html')(countryMenu)


def code_to_name(code):
  if code == "UK":
    code = "GB"
  return countryCodes.code2name[code]
register.simple_tag(code_to_name)
