"""
Population script for the "TransparencyIndex" model.
"""
import csv
import urllib2

import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from countryinfo.models import TransparencyScore


class Command(BaseCommand):    
    def handle(self, **options):
        
        docs_file = urllib2.urlopen('https://spreadsheets.google.com/pub?key=0Aok7vm4kY2IvdDRIcTkyY2VUTWE4ZGNjSWVqNDBsQXc&authkey=CKvJ_PcC&single=true&gid=0&output=csv')
        # docs_file = open('../data/stats/transparency/index.csv', 'U')
        f = csv.DictReader(docs_file)
        TransparencyScore.objects.all().delete()
        for line in f:
            try:
                t = TransparencyScore.objects.get(country=line['country'])
            except TransparencyScore.DoesNotExist:
                t = TransparencyScore(country=line['country'])
            t.score = line['score']
            t.rank = line['rank']
            t.save()
