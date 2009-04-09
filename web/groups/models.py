from django.db import models
from django.utils.translation import ugettext_lazy as _
class Recipient(models.Model):

    recipient_id = '815'
    
    class Meta:
        verbose_name = _('Test')
        verbose_name_plural = _('Tests')

    def __unicode__(self):
        return unicode('test')
