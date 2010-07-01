from django.template import Library, Node
from data.countryCodes import country_codes
from django.conf import settings

register = Library()

def code_to_name(code):
    """
    Given a valid country code, return the name of the country.
    """
    
    try:
        return country_codes(code)['name']
    except:
        pass
    
register.simple_tag(code_to_name)

