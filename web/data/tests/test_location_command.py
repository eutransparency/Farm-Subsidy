import cStringIO
import sys

from django.test import TestCase, TransactionTestCase
# from unittest import TestCase
from django.core.urlresolvers import reverse
from data import countryCodes
from django.core import management
from StringIO import StringIO

from django.db import connection, backend, models, transaction

from data.models import *

class DataLocationCommandTest(TestCase):
        
    def setUp(self):
        stdout=StringIO()
        management.call_command('locations', country='GB', stdout=stdout)
        
    def test_all_locations_length(self):
        all_locations = Location.objects.filter(country='GB', year='0')
        self.assertEqual(len(all_locations), 29)
    
    def test_geo1_length(self):
        all_locations = Location.objects.filter(country='GB', year=0, slug='england')
        self.assertEqual(len(all_locations), 1)
    
    def test_geo1_recipient_length(self):
        recipients = Recipient.objects.filter(geo1__iexact='england')
        location = Location.objects.get(country='GB', year=0, slug='england')
        self.assertEqual(location.recipients, len(recipients))
    
    def test_geo2_recipient_length(self):
        recipients = Recipient.objects.filter(geo1__iexact='northern ireland', geo2__iexact='tyrone')
        location = Location.objects.get(country='GB', year=0, slug='northern-ireland/tyrone')
        self.assertEqual(location.recipients, len(recipients))
    
    # def test_geo3_recipient_length(self):
    #     recipients = Recipient.objects.filter(geo1__iexact='diekirch', geo2__iexact='redange', geo3__iexact='beckerich')
    #     location = Location.objects.get(country='LU', year=0, slug='diekirch/redange/beckerich')
    #     self.assertEqual(location.recipients, len(recipients))

    def test_recipient_counts(self):
        """
        """








