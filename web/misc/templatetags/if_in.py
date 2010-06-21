from django import template 
register = template.Library() 

@register.filter
def in_list(value,arg):
  for a in arg:

    if str(a) == str(value):
      return True

