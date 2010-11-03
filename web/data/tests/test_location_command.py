import cStringIO
import sys

from django.test import TestCase
from django.core.urlresolvers import reverse
from data import countryCodes
from django.core import management
from django.db import connection, backend, models

from data.models import *

class DataLocationCommandTest(TestCase):
    fixtures = ['data/fixtures/test_locations.json']
    
    def setUp(self):
        management.call_command('locations', country='XX')

    def test_length(self):
        all_locations = Location.objects.filter(country='XX')
        self.assertEqual(len(all_locations), 22)
    
    def test_root_length(self):
        cursor = connection.cursor()
        cursor.execute("""
        select year,slug from data_location where country='XX' and geo_type='geo4' and year=0;
        """ )

        # for x in cursor.fetchall():
        #     print x[1]

    # def test_dump(self):
    #     
    #     from django.core import serializers
    #     recipient_data = serializers.serialize("json", Recipient.objects.filter(countrypayment='XX'))
    #     payment_data = serializers.serialize("json", Payment.objects.filter(countrypayment='XX'))
    #     print payment_data
    # 
