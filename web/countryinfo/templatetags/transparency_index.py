from django.template import Library, Node
from web.countryinfo.transparency import transparency_score, transparency_list

register = Library()

def transparency_index(country):
  if country != "EU":
    score = transparency_score(country)
    score['country'] = country
    return {'score' : score, 'country' : country}
  
register.inclusion_tag('blocks/transparency_index.html')(transparency_index)

def transparency_table():
  return {'table' : transparency_list()}

register.inclusion_tag('blocks/transparency_table.html')(transparency_table)