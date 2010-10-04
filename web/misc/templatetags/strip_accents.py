from django.template import Library, Node
register = Library()


import unicodedata

@register.filter(name='strip_accents')
def strip_accents(value):
   return ''.join((c for c in unicodedata.normalize('NFD', value) if unicodedata.category(c) != 'Mn'))

