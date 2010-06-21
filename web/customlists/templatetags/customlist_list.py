from django.template import Library, Node
# from search import queries

register = Library() 

def list_items(custom_list):
  return {'items' : custom_list['list_items']}
register.inclusion_tag('blocks/custom_list_view.html')(list_items)
# 
# def list_total(items):
#   total = 0
#   for key,item in items.items():
#     total += float(item['amount'])
#   return {'total' : total}
# register.inclusion_tag('blocks/custom_list_total.html')(list_total)
# 

@register.filter
def in_list(value,arg):
    return value in arg
