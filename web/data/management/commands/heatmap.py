from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from data.models import GeoRecipient, Recipient
from django.db import connection, backend, models

from gheat.models import Point
from gheat import ROOT
import shutil


class Command(BaseCommand):
    def handle(self, **options):
        
        shutil.rmtree(ROOT)
        Point.objects.all().delete()
        
        for recipient in GeoRecipient.objects.all():
            Point(uid=recipient.pk,
                latitude=recipient.location.x,
                longitude=recipient.location.y,
                density=1,
                ).save()