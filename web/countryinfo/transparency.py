import csv
import sys

from data import countryCodes
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import ordinal
from models import TransparencyScore
  
def transparency_score(country):
    ts = TransparencyScore.objects.get(country=country)
    return {'rank' : "%s" % (ordinal(ts.rank)),'percent' : ts.score}

def transparency_list():
    pass 