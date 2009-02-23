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
r"""Support for converting responses to JSON formats.

"""
__docformat__ = "restructuredtext en"

import simplejson
from wsgisupport import Response

def convert_to_json(request, response, props):
    """Convert a response to JSON.

    """
    return Response(simplejson.dumps(response),
                    content_type="text/javascript")

def convert_to_jsonp(request, response, props):
    """Convert a response to JSONP, according to the props.

    """
    response = Response(simplejson.dumps(response),
                        content_type="text/javascript")
    paramname = props['return_JSONP_paramname']
    jsonp = request.validated.get(paramname)
    if jsonp != '':
        response.body = jsonp + '(' + response.body + ')'
    return response

# vim: set fileencoding=utf-8 :
