from django.test import TestCase
from django.core.urlresolvers import reverse
from data import countryCodes

class DataViewsTest(TestCase):
    fixtures = ['data/fixtures/test_data.json']
    
    def country_runner(self, f):
        for country in countryCodes.country_codes():
            print "Running %s with %s" % (f.func_name, country)
            f(country)
    
    def test_home_view(self):
        response = self.client.get(reverse('home',))
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get(reverse('home',))
        self.assertEqual(response.status_code, 200)

    def test_all_country_views(self):
        def country_page(country):
            response = self.client.get(reverse('country', kwargs={'country' : country}))
            self.assertEqual(response.status_code, 200)
        self.country_runner(country_page)
