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
r"""Example application returning JSON data.

"""
__docformat__ = "restructuredtext en"

# First, ensure that wsgiwapi is on the path
import sys
import os.path as osp
sys.path.insert(0, osp.dirname(osp.dirname(osp.dirname(osp.abspath(__file__)))))

# Make an application with wsgiwapi.
import wsgiwapi
@wsgiwapi.jsonreturning
@wsgiwapi.param("num", 1, None, "^[0-9]+$", None, "A number to be added")
@wsgiwapi.allow_GETHEAD
def calc_sum(request):
    """Return the sum of the values supplied in the `num` parameter.

    """
    res = sum(int(val) for val in request.params.get('num', []))
    return res
app = wsgiwapi.make_application({
    'sum': calc_sum
}, autodoc='doc')

# Use the built-in cherrypy WSGI server to run the application.
server = wsgiwapi.make_server(app(), ('0.0.0.0', 8080))

# Start the server.
if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

# vim: set fileencoding=utf-8 :
