# -*- coding: utf-8 -*-
import django
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, backend, models
from django.conf import settings
from django.db.models import Sum

from data.models import Recipient, Payment

class Command(BaseCommand):
    
    def handle(self, **options):
        
        file_path = "%s/data/stats/payment_totals.txt" % settings.ROOT_PATH
        totals_file = open(file_path, 'w')

        total_recipients = Recipient.objects.count()
        sum_of_payments = int(Payment.objects.aggregate(total=Sum('amounteuro'))['total'])

        totals_file.write("%s,%s" % (total_recipients,sum_of_payments))


