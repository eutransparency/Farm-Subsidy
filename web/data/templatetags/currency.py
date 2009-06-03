from django import template
import locale
locale.setlocale(locale.LC_ALL, '')
register = template.Library()
from django.contrib.humanize.templatetags import humanize
 
@register.filter()
def currency(value):
  try:
    # decimal = value.split('.')[1]
    return locale.format('%.2f', float(value), True)
  except:
    return value