from django.template import Library, Node
from web.countryinfo.load_info import load_info
from farmsubsidy import fsconf

register = Library()

def country_stats(country, year):
  info = load_info(country)
  if int(year) == fsconf.default_year:
    return {'info' : info}
  
register.inclusion_tag('blocks/country_stats.html')(country_stats)