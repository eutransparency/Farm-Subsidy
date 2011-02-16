from django.test import TestCase
from django.test.client import Client

from models import Signee
from forms import SigneeForm

class SigneeTests(TestCase):

    def setUp(self):
        
        self.client = Client()
        
        s = Signee()
        s.name = "Test User"
        s.affiliation = "Test"
        s.email = "test.user@example.com"
        s.comments = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        s.save()

    def test_unicode(self):
        o = Signee.objects.get(name="Test User")
        self.assertEqual(unicode(o), u'Test User')

    def test_query(self):
        qs = Signee.objects.all()
        self.assertEqual(len(qs), 1)

    def test_form_page(self):
        response = self.client.get('/petition/sign')
        self.assertEqual(response.status_code, 200)

    def test_form_fields(self):
        form_dict = {
            'name' : 'Test User 2',
            'affiliation' : 'Test Affiliation',
            'email' : 'test@example.com',
            'comments' : 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        }
        form = SigneeForm(form_dict)
        self.assertTrue(form.is_valid())
    
    def test_form_fields_stupid(self):
        bad_form_data = [
            {
                'name' : '',
                'affiliation' : '',
                'email' : '',
                'comments' : '',
            },
            {
                'name' : 'Test',
                'affiliation' : '',
                'email' : 'fail@fail',
                'comments' : '',
            },
            {
                'name' : 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'affiliation' : '',
                'email' : 'test@example.com',
                'comments' : '',
            },
        ]
        
        for d in bad_form_data:
            form = SigneeForm(d)
            self.failIf(form.is_valid())
        
    
    def test_form_post(self):
        post_data = {
            'name' : 'Test User 3',
            'affiliation' : 'Test',
            'email' : 'testuser3@example.com',
            'comments' : 'None',
        }
        
        self.client.post('/petition/sign', post_data)
        qs = Signee.objects.filter(name='Test User 3')
        self.assertEqual(len(qs), 1)
        





