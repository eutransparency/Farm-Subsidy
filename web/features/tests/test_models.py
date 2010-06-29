import unittest

from django.test import TransactionTestCase

from features import models

class Test__unicode__(TransactionTestCase):
    '''
    Simple test to verify the __unicode__ method
    of the various models works
    '''
    
    def test_feature(self):
        self.assertEqual(
            'Example Title',
            unicode(models.Feature(title='Example Title'))
        )
    
    
