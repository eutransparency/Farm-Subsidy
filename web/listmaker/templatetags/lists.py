from django.contrib.contenttypes.models import ContentType
from django.template import Library, Node
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
    list_name = context['request'].session.get('list_name')
    ct = ContentType.objects.get_for_model(list_object)

    if list_name:
        in_list = lists.item_in_list(list_name, "%s:%s" % (ct, list_object.pk))

    return {
        'ct' : ct,
        'list_name' : list_name,
        'list_object' : list_object,
        'in_list' : in_list,
    }
