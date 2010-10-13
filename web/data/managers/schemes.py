# encoding: utf-8
import re

from django.db import models
from django.db import connection, backend, models
from django.db.models import Sum, Max

from data import countryCodes

from django.conf import settings

DEFAULT_YEAR = settings.DEFAULT_YEAR

class SchemeManager(models.Manager):
    """
    Various reusable queries, like top_schemes
    """
    
    def top_schemes(self, country=None, year=DEFAULT_YEAR, limit=10):
        """
        Top schemes for a given country over all years.
        """
        kwargs = {}
        if country and country != "EU":
            kwargs['countrypayment'] = country

        schemes = self.all()
        schemes = schemes.filter(**kwargs)
        schemes = schemes.exclude(total=None)
        schemes = schemes.order_by('-total')
        return schemes[:limit]

class SchemeYearManager(models.Manager):
    """
    Various reusable queries, like top_schemes
    """
    
    def top_schemes(self, country=None, year=DEFAULT_YEAR):
        kwargs = {}
        if int(year) != 0:
            kwargs['year'] = year
        if country and country is not "EU":
            kwargs['countrypayment'] = country

        schemes = self.all()
        schemes = schemes.filter(**kwargs)
        schemes = schemes.annotate(scheme_total=Sum('total'))
        schemes = schemes.order_by('-scheme_total')
        return schemes
