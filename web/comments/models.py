from django.db import models
from django.contrib.auth.models import User
from farmsubsidy.web.misc.models import FarmOwners

class Comment(models.Model):
  user = models.ForeignKey(User, unique=False)
  owner = models.BooleanField(default=False)
  recipient_id = models.TextField(blank=False, null=False)
  comment = models.TextField(blank=False)
  date = models.DateTimeField(auto_now_add=True)  
  
