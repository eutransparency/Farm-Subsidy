from django.db import models
from django.contrib.auth.models import User
import datetime
from registration.signals import user_registered

# Create your models here.

class FarmOwners(models.Model):
  user = models.ForeignKey(User, unique=False)
  farm = models.IntegerField(blank=False, unique=False)


class Profile(models.Model):
    """(profile description)"""

    user = models.ForeignKey(User)
    name = models.CharField(blank=True, max_length=255)
    data_agreement = models.BooleanField(default=False)
    data_description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.user

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

# Signal Registrations
# when a user gets registered, we want to generate a profile for them
from registration.signals import user_registered

def create_user_profile(sender, **kwargs):
    user = kwargs['user']
    name = kwargs['request'].POST.get('name')
    profile = Profile(user=user, name=name)
    profile.save()
user_registered.connect(create_user_profile)
