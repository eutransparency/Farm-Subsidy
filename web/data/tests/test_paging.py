from django.test import TestCase
from django.core.urlresolvers import reverse
from data.models import Recipient

class PagingTest(TestCase):
    # fixtures = ['data/fixtures/test_data.json']
    
    def test_page(self):
        x = Recipient.objects.all().extra(where=["(total, globalrecipientidx) < (%s, %s)"], params=[0,'LV201239']).order_by('-total')
        print x
        print x.query
        