from django.template import Library, Node

register = Library()

def user_menu(user):
  return {'user' : user}


register.inclusion_tag('blocks/user_menu.html')(user_menu)