from django.template import Library, Node
from web.countryinfo.load_info import load_info

register = Library()

def country_stats(country):
  info = load_info(country)
  return {'info' : info}
  
register.inclusion_tag('blocks/country_stats.html')(country_stats)