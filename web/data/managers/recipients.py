# encoding: utf-8
import re

from django.db import models
from django.db import connection, backend, models
from django.db.models import Sum, Max

from data import countryCodes
from django.conf import settings

DEFAULT_YEAR = settings.DEFAULT_YEAR

class RecipientManager(models.Manager):
    """
    Various reusable queries, like top_recipients
    """
    
    def top_recipients(self, country=None, year=DEFAULT_YEAR):
        if int(year) == 0:
            recipients = self.all()
            recipients = recipients.exclude(total=None)
            if country:
                recipients = recipients.filter(countrypayment=country)
            recipients = recipients.order_by('-total')[:10]
            return recipients