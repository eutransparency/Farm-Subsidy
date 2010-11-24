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

    def top_recipients(self, country=None, year=0):
        recipients = self.all()
        recipients = recipients
        kwargs = {}
        if country and country != 'EU':
            kwargs['countrypayment'] = country
        if int(year) != 0:
            kwargs['payment__year__exact'] = year
            # recipients = recipients.distinct()
        recipients = recipients.filter(**kwargs)
        recipients = recipients.order_by('-total').distinct()
        return recipients
        
    def recipents_for_location(self, location, country='EU'):
        """
        Given a location slug, retuen all recipients where the geo fields match.
        
        Location slugs are paths like a/b/c, where a=geo1, b-geo2 etc.
        
        Because we have the RecipientYear model, every total returned here is 
        for all years
        """
        
        geos = []
        for l in location.get_ancestors():
            geos.append(l)
        geos.append(location)
        kwargs = {}
        for i, g in enumerate(geos):
            i = i + 1
            kwargs["geo%s" % i] = g.name
        
        qs =  self.filter(**kwargs)
        # qs = qs.only('name', 'total', 'countrypayment',)
        return qs






