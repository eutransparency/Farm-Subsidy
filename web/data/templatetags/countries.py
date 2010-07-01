from django.template import Library, Node
from data import countryCodes
register = Library()

def country_menu():
  countries = []
  for country in countryCodes.country_codes():
    countries.append(countryCodes.country_codes(country))
  return {'countries' : countries}
  
register.inclusion_tag('blocks/country_menu.html')(country_menu)

def country_map(country_code):
    return {"country_code" : country_code}

register.inclusion_tag('blocks/country_map.html')(country_map)    