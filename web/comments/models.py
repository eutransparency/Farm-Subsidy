from django.db import models
from django.contrib.auth.models import User
from web.misc.models import FarmOwners
from django.contrib.comments.models import Comment


class CommentWithOwner(Comment):
  owner = models.BooleanField(default=False)
