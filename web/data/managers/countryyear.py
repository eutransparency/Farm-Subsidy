# encoding: utf-8
import re

from django.db import models
from django.db import connection, backend, models
from django.db.models import Sum, Max



class CountryYearManager(models.Manager):
    """
    Various reusable queries, like top_schemes
    """
    
    def year_max_min(self, country=None):
        """
        return a tuple of the highest and lowest year know about for a country
        """
        kwargs = {}
        if country and country != "EU":
            kwargs['country'] = country

        years = self.all()
        years = years.filter(**kwargs)
        years = years.order_by('-year')
        years = years.values('year')
        years = [y['year'] for y in years]
        if not years:
            # If no years, return a 'blank' list
            years = [0,0]
        
        return min(years), max(years)

