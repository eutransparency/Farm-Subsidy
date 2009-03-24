from django.db import models

# Create your models here.

class blog(models.Model):
  title = models.CharField(max_length=300)
  body = models.TextField(max_length=3000)
  published = models.BooleanField(default=True)
  
  def __unicode__(self):
    return self.title
    