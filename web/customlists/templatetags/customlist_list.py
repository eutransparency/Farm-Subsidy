from django.template import Library, Node
from farmsubsidy.queries import queries

register = Library() 

def list_items(items):
  total = 0
  for key,item in items.items():
    total += float(item['amount'])
  return {'items' : items, 'total' : total,}
register.inclusion_tag('blocks/custom_list_view.html')(list_items)