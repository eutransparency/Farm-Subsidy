from django.template import Library, Node
from web.countryinfo.load_info import load_info
from django.conf import settings

register = Library()

def country_stats(country, year):
  info = load_info(country)
  if int(year) == settings.STATS_YEAR:
    return {'info' : info}
  
register.inclusion_tag('blocks/country_stats.html')(country_stats)