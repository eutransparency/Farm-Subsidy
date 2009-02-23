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
r"""Logging support for WSGIWAPI.

"""
__docformat__ = "restructuredtext en"

import time
import traceback

class StdoutLogger(object):
    """Logger which writes messages to stdout.

    """
    def request_start(self, environ):
        return time.time()

    def request_end(self, environ, start_value, request, response):
        elapsed = time.time() - start_value
        print("%f(%f):%s %r %s" % (start_value, elapsed,
                                   request.method, request.path,
                                   response.response.status)
             )

    def request_failed(self, environ, start_value, exc_info):
        elapsed = time.time() - start_value
        traceback.print_exception(*exc_info)
        print("%f(%f):ERROR %r %s" % (start_value, elapsed,
                                      environ.get('PATH_INFO', ''),
                                      str(exc_info[1]))
             )

class SilentLogger(object):
    """Logger which produces no output.

    """
    def request_start(self, environ):
        pass
    def request_end(self, environ, start_value, request, response):
        pass
    def request_failed(self, environ, start_value, exc_info):
        pass

class VerboseLogger(object):
    """Logger which writes verbose messages to stdout.

    """
    def request_start(self, environ):
        print ("%f:START:%s %s" % (time.time(),
                                   environ.get('REQUEST_METHOD'),
                                   environ.get('PATH_INFO'))
              )
        return time.time()

    def request_end(self, environ, start_value, request, response):
        now = time.time()
        elapsed = now - start_value
        print ("%f(%f):DONE:%s %r %s" % (now, elapsed,
                                         request.method, request.path,
                                         response.response.status)
              )

    def request_failed(self, environ, start_value, exc_info):
        now = time.time()
        elapsed = now - start_value
        traceback.print_exception(*exc_info)
        print ("%f(%f):ERROR %r %s" % (now, elapsed,
                                       environ.get('PATH_INFO', ''),
                                       str(exc_info[1]))
              )

# vim: set fileencoding=utf-8 :
