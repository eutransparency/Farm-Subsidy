from django.template import Library, Node
from web.countryinfo.transparency import transparency_score, transparency_list
from indexer import countryCodes

register = Library()

def transparency_index(country):
  if country['code'] != "EU":
    score = transparency_score(country['code'])
    score['country'] = country['code']
    return {'score' : score, 'country' : country}
  
register.inclusion_tag('blocks/transparency_index.html')(transparency_index)

def transparency_table():
  return {'table' : transparency_list()}

register.inclusion_tag('blocks/transparency_table.html')(transparency_table)
