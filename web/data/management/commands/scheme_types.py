"""
Population script for the "schemeType" model.

Takes data from the google doc and adds or replaces rows in the SchemeType table.
"""
import csv
import urllib2

import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from data.models import SchemeType
from django.db import connection, backend, models


class Command(BaseCommand):    
    def handle(self, **options):
        
        docs_file = urllib2.urlopen('https://spreadsheets.google.com/pub?key=0Aok7vm4kY2IvdFFGQ2hwekhHRk5MZGM1dTF6SHBQY1E&authkey=CP-WxbwN&hl=en&single=true&gid=0&output=csv')
        f = csv.DictReader(docs_file)
        
        for line in f:
            try:
                s = SchemeType.objects.get(pk=line['pk'])
            except SchemeType.DoesNotExist:
                s = SchemeType(**line)
            if s.scheme_type:
                s.save()