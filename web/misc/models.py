from django.db import models
from django.contrib.auth.models import User
import datetime
from registration.signals import user_registered

# Create your models here.

class FarmOwners(models.Model):
  user = models.ForeignKey(User, unique=False)
  farm = models.IntegerField(blank=False, unique=False)


class Profile(models.Model):
  user = models.ForeignKey(User, unique=True)
  
  joined = models.DateTimeField(blank=False, default=datetime.datetime.now)
  
  def __unicode__(self):
    return self.user.username
  
  def get_absolute_url(self):
    return ('profiles_profile_detail', (), { 'username': self.user.username })
  get_absolute_url = models.permalink(get_absolute_url)




def add_deafult_profile(user, **kwargs):
  p = Profile(user_id=user.id)
  p.save()
user_registered.connect(add_deafult_profile)



