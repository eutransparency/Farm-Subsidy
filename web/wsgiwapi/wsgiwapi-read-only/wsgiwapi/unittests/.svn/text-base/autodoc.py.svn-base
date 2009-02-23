#!/usr/bin/env python

# Copyright (c) 2009 Richard Boulton
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
r"""Test a simple API built with wsgiwapi.

"""
__docformat__ = "restructuredtext en"

from harness import *
import apps
import wsgiwapi

class SimpleApiTest(TestCase):
    """Test a simple API build with wsgiwapi.

    """
    def test_simple(self):
        """Test basic use of the simple API.

        """
        app = wsgiwapi.make_application(apps.simple(),
                                          autodoc = 'doc',
                                          logger = wsgiwapi.SilentLogger)
        r = simulate_get(app, '/')
        self.assertEqual(r.status, u'200 OK')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'Static')

        r = simulate_post(app, '/doc', {})
        self.assertEqual(r.status, u'405 Method Not Allowed')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(dict(r.headers)[u'Allow'], u'GET')
        self.assertEqual(r.body, u'405 Method Not Allowed')

        r = simulate_get(app, '/doc')
        self.assertEqual(r.status, u'200 OK')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/html')
        self.assertNotEqual(r.body.find(u'Display documentation about the API'), -1)

if __name__ == '__main__': main()
# vim: set fileencoding=utf-8 :
