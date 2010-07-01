from django.template import Library, Node
import urlparse
import urllib
register = Library()

@register.simple_tag
def parse_qs(qs, k=None,v=None):
    qs = qs.copy()
    if k:
        qs[k] = v
    # Normally, we don't want to keep the page element of the string
    if 'page' in qs:
        del qs['page']
    return "?%s" % urllib.urlencode(qs)

# @register.inclusion_tag('blocks/add_remove_item.html', takes_context=True)
# def list_item_edit(context, list_object):
#     ct = ContentType.objects.get_for_model(list_object)
#     in_list = list_object in [i.content_object 
#                             for i in context['request'].session.get('list_items', [])]
#     list_enabled = context['request'].session.get('list_enabled')
#     
#     return {
#     'ct' : ct,
#     'list_object' : list_object,
#     'in_list' : in_list,
#     }
