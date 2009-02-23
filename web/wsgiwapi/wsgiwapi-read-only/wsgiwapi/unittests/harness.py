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
r"""Framework for wsgiwapi unittests.

Unittests should just start with "from harness import *", which will provide
a convenient environment for writing tests of wsgiwapi features.

"""
__docformat__ = "restructuredtext en"

import os
import re
import StringIO
import sys
import unittest 
from unittest import main
import urllib
import wsgiref.util
import wsgiref.validate

# Ensure that wsgiwapi is on the path, when run uninstalled.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import wsgiwapi

class SimulationResult(object):
    """The result of a simulated call to the API.

    """
    def __init__(self):
        self.status = None
        self.headers = []
        self.body = None

    def start_response(self, status, headers):
        self.status = status
        self.headers = headers

    def __str__(self):
        return '<SimulationResult(status=%r, headers=%r, body=%r)>' % (self.status, self.headers, self.body)

def perform_simulation(environ, app):
    """Perform a simulation, given a WSGI environment and application.

    """
    inst = wsgiref.validate.validator(app)
    result = SimulationResult()
    response = inst(environ, result.start_response)
    body = []
    response_iter = iter(response)
    for part in response_iter:
        body.append(part)
    result.body = u''.join(body)
    if hasattr(response_iter, 'close'):
        response_iter.close()
    return result

def simulate_get(app, urlpath):
    """Simulate a GET request.

     - `urlpath` is the path part of the URL (including any querystring
       parameters).

    """
    if '?' in urlpath:
        urlpath, queryargs = urlpath.split('?', 1)
    else:
        queryargs = ''
    environ = {
        'PATH_INFO': urlpath,
        'SCRIPT_NAME': '',
        'QUERY_STRING': queryargs,
    }
    wsgiref.util.setup_testing_defaults(environ)
    return perform_simulation(environ, app())

def simulate_post(app, url, data, encoding='url'):
    """Simulate a GET request.

     - `url` is the URL path.
     - `data` is the post data.
     - `encoding` is the encoding to use for the post data.

    """
    if encoding == 'url':
        data = urllib.urlencode(data)
    else:
        raise ValueError("Unknown value %r for encoding" % encoding)

    environ = {
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': url,
        'SCRIPT_NAME': '',
        'QUERY_STRING': '',
        'wsgi.input': StringIO.StringIO(data),
        'CONTENT_LENGTH': str(len(data)),
    }
    wsgiref.util.setup_testing_defaults(environ)

    return perform_simulation(environ, app())

class TestCase(unittest.TestCase):
    def assertRaisesMessage(self, excClass, excMessageRe, callableObj,
                            *args, **kwargs):
        try:
            callableObj(*args, **kwargs)
            self.assertFalse('')
        except excClass,  e:
            emsg = unicode(e)
            pat = re.compile(excMessageRe)
            self.failUnless(pat.match(emsg), "Exception message %r does not "
                            "match pattern %r" % (emsg, excMessageRe))
        else:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            raise self.failureException, "%s not raised" % excName

# vim: set fileencoding=utf-8 :
