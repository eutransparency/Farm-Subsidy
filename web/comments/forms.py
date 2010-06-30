from django import forms
from django.contrib.comments.forms import CommentForm
from web.comments.models import CommentWithOwner

from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
import time
import datetime
from django.conf import settings

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

class CommentFormWithOwners(CommentForm):  

  owner = forms.BooleanField(required=False, label="Are you the recipient?")
  comment = forms.CharField(label='What did you find out?', widget=forms.Textarea,
                                  max_length=COMMENT_MAX_LENGTH)

  def get_comment_model(self):
    # Use our custom comment model instead of the built-in one.
    return CommentWithOwner

  def get_comment_create_data(self):

    return dict(
        content_type = ContentType.objects.get_for_model(self.target_object),
        object_pk    = force_unicode(self.target_object._get_pk_val()),
        comment      = self.cleaned_data["comment"],
        submit_date  = datetime.datetime.now(),
        site_id      = settings.SITE_ID,
        is_public    = True,
        is_removed   = False,
        owner        = self.cleaned_data['owner']
    )


CommentFormWithOwners.base_fields.pop('url')
CommentFormWithOwners.base_fields.pop('name')
CommentFormWithOwners.base_fields.pop('email')