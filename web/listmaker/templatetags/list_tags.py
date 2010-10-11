from django.contrib.contenttypes.models import ContentType
from django.template import Library, Node
from django.template import Context, Variable
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma

from listmaker.models import List
from listmaker import lists

register = Library()

def latest_lists(number=5):
  return {
    'lists' : List.objects.all().order_by('-pk')[:5],
  }
register.inclusion_tag('blocks/latest_lists.html')(latest_lists)


@register.inclusion_tag('blocks/add_remove_item.html', takes_context=True)
def list_item_edit(context, list_object):
    ct = in_list = None
    list_name = context['request'].session.get('list_name')
    if list_name:
        if type(list_object) == dict:
            ct = ContentType.objects.get(pk=list_object.get('content_type'))
            list_object['pk'] = list_object.get('content_object')
            item_key = "%s:%s" % (ct.pk, list_object['pk'])
            in_list = lists.item_in_list(list_name, item_key)
        else:            
            ct = ContentType.objects.get_for_model(list_object)
            item_key = lists.make_item_key(list_object, ct)
            in_list = lists.item_in_list(list_name, item_key)
            
    return {
        'ct' : ct,
        'list_name' : list_name,
        'list_object' : list_object,
        'in_list' : in_list,
    }

class ListItems(Node):
    def __init__(self, list_name, varname=None):
        self.varname = varname
        self.list_name = list_name

    def render(self, context):
        self.list_name = Variable(self.list_name).resolve(context)
        context[self.varname] = lists.list_items(self.list_name)
        return ''


@register.tag
def list_items(parser, token):
    bits = token.contents.split()    
    if len(bits) > 2:
        if bits[2] == "as":
            varname = bits[3]
    else:
        varname = None
    return ListItems(bits[1], varname)


@register.simple_tag
def list_total(list_name):
    total = lists.get_total(list_name)
    total = floatformat(total, 2)
    total = intcomma(total)
    return total



