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
r"""Test validation support.

"""
__docformat__ = "restructuredtext en"

from harness import *
import apps
import wsgiwapi

class ValidationTest(TestCase):
    """Test validation support.

    """
    def test_simple(self):
        """Test basic use of the simple API.

        """
        app = wsgiwapi.make_application(apps.simple(),
                                        logger = wsgiwapi.SilentLogger)
        r = simulate_get(app, '/6')
        self.assertEqual(r.status, u'200 OK')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'Static6')

        r = simulate_post(app, '/6', {})
        self.assertEqual(r.status, u'200 OK')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'Static6')

        r = simulate_get(app, '/6?foo=1')
        self.assertEqual(r.status, u'400 Bad Request')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'Validation Error: This resource does '
                         'not accept parameters')

        r = simulate_post(app, '/6', {'foo': '1'})
        self.assertEqual(r.status, u'400 Bad Request')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'Validation Error: This resource does '
                         'not accept parameters')

    def test_defaulting(self):
        """Test behaviour of default parameters.

        """
        app = wsgiwapi.make_application(apps.simple(),
                                        logger = wsgiwapi.SilentLogger)
        r = simulate_get(app, '/8')
        self.assertEqual(r.status, u'200 OK')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'bar')

        r = simulate_get(app, '/8?foo=baz')
        self.assertEqual(r.status, u'400 Bad Request')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'Validation Error: Too few instances of '
                         '\'foo\' supplied (needed 2, got 1)')

        r = simulate_get(app, '/8?foo=baz&foo=bong')
        self.assertEqual(r.status, u'200 OK')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'baz,bong')

        r = simulate_get(app, '/8?foo=bong&foo=baz')
        self.assertEqual(r.status, u'200 OK')
        self.assertEqual(dict(r.headers)[u'Content-Type'], u'text/plain')
        self.assertEqual(r.body, u'bong,baz')

    def test_inconsistent_decorators(self):
        """Test for inconsistent decorators.

        """
        def fn():
            @wsgiwapi.noparams
            @wsgiwapi.param('foo', 1, 2, None, None)
            def tmp(request):
                return wsgiwapi.Response('static')
        self.assertRaisesMessage(RuntimeError,
            "Can't decorate with param and noparams", fn)

        def fn():
            @wsgiwapi.param('foo', 2, 2, None, None)
            @wsgiwapi.param('foo', 1, 2, None, None)
            def tmp(request):
                return wsgiwapi.Response('static')
        self.assertRaises(RuntimeError, fn)

if __name__ == '__main__': main()
# vim: set fileencoding=utf-8 :
