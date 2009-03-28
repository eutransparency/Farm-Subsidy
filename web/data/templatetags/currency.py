from django import template
import locale
locale.setlocale(locale.LC_ALL, '')
register = template.Library()
 
 
@register.filter()
def currency(value):
  try:
    return locale.format('%.2f', float(value), True)
  except:
    return value