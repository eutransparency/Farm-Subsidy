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
r"""Support for WSGI applications providing web APIs.

"""
__docformat__ = "restructuredtext en"

from application import (
                         make_application,
                         make_server,
                        )
from decorators import (
                        jsonreturning,
                        jsonpreturning,
                        allow_method,
                        allow_GET,
                        allow_HEAD,
                        allow_GETHEAD,
                        allow_POST,
                        param,
                        noparams,
                        pathinfo,
                        copyprops,
                        decorate,
                       )
from wsgisupport import (
                         Response,
                         HTTPError,
                         HTTPNotFound,
                         HTTPServerError,
                        )
from logging import (
                     StdoutLogger,
                     SilentLogger,
                     VerboseLogger,
                    )

# vim: set fileencoding=utf-8 :
