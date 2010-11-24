# encoding: utf-8
import re

from django.db import models
from django.db import connection, backend, models
from django.db.models import Sum, Max

from data import countryCodes
from django.conf import settings

DEFAULT_YEAR = settings.DEFAULT_YEAR

class RecipientYearManager(models.Manager):
    """
    Various reusable queries, like top_recipients
    """

    def recipents_for_location(self, location, year=DEFAULT_YEAR, country='EU'):
        """
        Given a location slug, retuen all recipients where the geo fields match.
        
        Location slugs are paths like a/b/c, where a=geo1, b-geo2 etc.
        
        """
        
        geos = []
        for l in location.get_ancestors():
            geos.append(l)
        geos.append(location)

        kwargs = {}
        for i, g in enumerate(geos):
            i = i + 1
            kwargs["recipient__geo%s" % i] = g.name
        
        if country != 'EU':
            kwargs['country'] = country
            kwargs['recipient__countrypayment'] = country

        
        kwargs['year'] = year
        qs =  self.filter(**kwargs)
        # qs = qs.only('name', 'total', 'country',)
        return qs






