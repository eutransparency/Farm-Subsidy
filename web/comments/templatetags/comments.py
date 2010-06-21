from django.template import Library, Node
from web.comments.models import Comment
from web.misc.models import FarmOwners

register = Library()

def recipient_comments(rid):
  comments = Comment.objects.filter(recipient_id=rid)
  return {'comments' : comments}


register.inclusion_tag('recipient_comments.html')(recipient_comments)