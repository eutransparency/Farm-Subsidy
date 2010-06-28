from django.template import Library, Node
from web.comments.models import Comment
from web.misc.models import FarmOwners

register = Library()

def download_recipient(recipient_id):
  return {'recipient' : recipient_id}
register.inclusion_tag('blocks/recipient_download.html')(download_recipient)