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
r"""Test handling of extra path components.

"""
__docformat__ = "restructuredtext en"

from harness import *
import apps
import wsgiwapi

class PathComponentTest(TestCase):
    """Test handling of extra path components.

    """
    def check_path_components(self, app):
        """Check the behaviour of path components in an application.

        """
        # FIXME - test the body contents.
        r = simulate_get(app, '/')
        self.assertEqual(r.status, u'404 Not Found')

        r = simulate_get(app, '/foo')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/foo/')
        self.assertEqual(r.status, u'404 Not Found')
        r = simulate_get(app, '/foo/bar')
        self.assertEqual(r.status, u'404 Not Found')

        r = simulate_get(app, '/bar')
        self.assertEqual(r.status, u'404 Not Found')
        r = simulate_get(app, '/bar/')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/bar/foo')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/bar/foo/')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/bar/foo/baz')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/bar/foo/baz/')
        self.assertEqual(r.status, u'404 Not Found')
        r = simulate_get(app, '/bar/foo/baz/oink')
        self.assertEqual(r.status, u'404 Not Found')

        r = simulate_get(app, '/baz')
        self.assertEqual(r.status, u'404 Not Found')
        r = simulate_get(app, '/baz/')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/baz/foo')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/baz/foo/')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/baz/foo/baz')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/baz/foo/baz/')
        self.assertEqual(r.status, u'200 OK')
        r = simulate_get(app, '/baz/foo/baz/oink')
        self.assertEqual(r.status, u'200 OK')

        r = simulate_get(app, '/invalid')
        self.assertEqual(r.status, u'500 Internal Server Error')

    def test_functions(self):
        """Test extra path components with functions.

        """
        def foo(request):
            return "foo()"

        @wsgiwapi.pathinfo(
                           ('arg1',),            # No default specified - required.
                           ('arg2', None, None), # Default specified (None)
                          )
        def bar(request):
            return "bar(%s,%s)" % (request.pathinfo.get('arg1'),
                                   request.pathinfo.get('arg2'))

        @wsgiwapi.pathinfo(
                           ('arg1',),            # No default specified - required.
                           ('arg2', None, None), # Default specified (None)
                           tail=(None, None, None, None, "Trailing args"),
                          )
        def baz(request):
            return "baz(%s)" % (u','.join(request.pathinfo))

        def invalid(request):
            # This is mainly for a regression test.
            return foo(request, "invalid_extra_arg")

        app = wsgiwapi.make_application({
                                        'foo': foo,
                                        'bar': bar,
                                        'baz': baz,
                                        'invalid': invalid,
                                        },
                                        logger = wsgiwapi.SilentLogger)
        self.check_path_components(app)

    def test_members(self):
        """Test extra path components with member functions.

        """
        class zab(object):
            def foo(self, request):
                return "foo"

            @wsgiwapi.pathinfo(
                               ('arg1',),            # No default specified - required.
                               ('arg2', None, None), # Default specified (None)
                              )
            def bar(self, request):
                return "bar(%s,%s)" % (request.pathinfo.get('arg1'),
                                       request.pathinfo.get('arg2'))

            @wsgiwapi.pathinfo(
                               ('arg1',),            # No default specified - required.
                               ('arg2', None, None), # Default specified (None)
                               tail=(None, None, None, None, "Trailing args"),
                              )
            def baz(self, request):
                return "baz(%s)" % (u','.join(request.pathinfo))

            def invalid(self, request):
                return self.foo(request, "invalid_extra_arg")

        zabobj = zab()
        app = wsgiwapi.make_application({
                                        'foo': zabobj.foo,
                                        'bar': zabobj.bar,
                                        'baz': zabobj.baz,
                                        'invalid': zabobj.invalid,
                                        },
                                        logger = wsgiwapi.SilentLogger)
        self.check_path_components(app)

    def test_oldclass_members(self):
        """Test extra path components with members of an old-style class.

        """
        class zab():
            def foo(self, request):
                return "foo"

            @wsgiwapi.pathinfo(
                               ('arg1',),            # No default specified - required.
                               ('arg2', None, None), # Default specified (None)
                              )
            def bar(self, request):
                return "bar(%s,%s)" % (request.pathinfo.get('arg1'),
                                       request.pathinfo.get('arg2'))

            @wsgiwapi.pathinfo(
                               ('arg1',),            # No default specified - required.
                               ('arg2', None, None), # Default specified (None)
                               tail=(None, None, None, None, "Trailing args"),
                              )
            def baz(self, request):
                return "baz(%s)" % (u','.join(request.pathinfo))

            def invalid(self, request):
                return self.foo(request, "invalid_extra_arg")

        zabobj = zab()
        app = wsgiwapi.make_application({
                                        'foo': zabobj.foo,
                                        'bar': zabobj.bar,
                                        'baz': zabobj.baz,
                                        'invalid': zabobj.invalid,
                                        },
                                        logger = wsgiwapi.SilentLogger)
        self.check_path_components(app)

    def test_decorated_functions(self):
        """Test extra path components with decorated functions.

        """

        def baddeco(fn):
            def res(*args):
                return fn(*args)
            return res

        def deco(fn):
            def res(*args):
                return fn(*args)
            wsgiwapi.copyprops(fn, res)
            return res

        @deco
        def foo(request):
            return "foo()"

        @deco
        @wsgiwapi.pathinfo(
                           ('arg1',),            # No default specified - required.
                           ('arg2', None, None), # Default specified (None)
                          )
        def bar(request):
            return "bar(%s,%s)" % (request.pathinfo.get('arg1'),
                                   request.pathinfo.get('arg2'))

        @baddeco
        @wsgiwapi.pathinfo(
                           ('arg1',),            # No default specified - required.
                           ('arg2', None, None), # Default specified (None)
                          )
        def bar2(request):
            return "bar2(%s,%s)" % (request.pathinfo.get('arg1'),
                                    request.pathinfo.get('arg2'))

        @wsgiwapi.decorate(baddeco)
        @wsgiwapi.pathinfo(
                           ('arg1',),            # No default specified - required.
                           ('arg2', None, None), # Default specified (None)
                           tail=(None, None, None, None, "Trailing args"),
                          )
        def baz(request):
            return "baz(%s)" % (u','.join(request.pathinfo))

        @deco
        def invalid(request):
            # This is mainly for a regression test.
            return foo(request, "invalid_extra_arg")

        app = wsgiwapi.make_application({
                                        'foo': foo,
                                        'bar': bar,
                                        'bar2': bar2,
                                        'baz': baz,
                                        'invalid': invalid,
                                        },
                                        logger = wsgiwapi.SilentLogger)
        self.check_path_components(app)

        r = simulate_get(app, '/bar2')
        self.assertEqual(r.status, u'500 Internal Server Error')
        self.assertEqual(r.body, u'500 Internal Server Error\n'
                         'Handler properties do not match decorated '
                         'properties.  Probably missing call to '
                         'wsgiwapi.copyprops.')

if __name__ == '__main__': main()
# vim: set fileencoding=utf-8 :
