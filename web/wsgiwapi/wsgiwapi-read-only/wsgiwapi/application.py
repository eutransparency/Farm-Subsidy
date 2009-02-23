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
r"""Create a WSGI application providing a web API.

"""
__docformat__ = "restructuredtext en"

import sys

from decorators import jsonreturning, _get_props
import decorators
from logging import StdoutLogger
from validation import ValidationError
from wsgisupport import Request, \
         HTTPError, \
         HTTPNotFound, \
         HTTPServerError, \
         WSGIResponse, \
         Response

def apply_request_checks_and_transforms(request, props):
    """Apply all the checks and transforms listed in props to a request.

    This is typically called from a decorator, and the props are read from the
    decorated function.

    """
    if props is None:
        return request
    request_filters = props.get('request_filters', [])
    for request_filter in request_filters:
        request = request_filter(request, props)
    return request

def apply_response_checks_and_transforms(request, response, props):
    """Apply all the checks and transforms listed in props to a response.

    This is typically called from a decorator, and the props are read from the
    decorated function.

    """
    if props is None:
        return response
    response_filters = props.get('response_filters', [])
    for response_filter in response_filters:
        response = response_filter(request, response, props)
    return response

def handle_validation_error(err):
    """
    """
    response = Response(u"Validation Error: " + err.message)
    response.status = 400
    return response

def make_application(urls,
                     autodoc=None,
                     validation_error_handler=handle_validation_error,
                     logger=None,
                     ):
    """Make a web application for a given set of URLs.

    - `urls` is a dict of urls to support: keys are url components, values are
      either sub dictionaries, or callables.

    - `logger` is a callable which returns a Logger.  When the application
      object returned is instantiated, it will call this callable, and use the
      returned object for logging.

    FIXME - document the other parameters to this function.

    """
    if logger is None:
        logger = StdoutLogger

    class Application(object):
        """WSGI application wrapping the search server.

        """
        def __init__(self):
            self.logger = logger()

        def __call__(self, environ, start_response):
            logstart = self.logger.request_start(environ)
            try:
                logged, request, response = \
                    self._do_call(environ, start_response, logstart)
            except Exception, e:
                # We get here only if there's an error building the Request
                # object from the environ.
                self.logger.request_failed(environ, logstart, sys.exc_info())
                return HTTPServerError(str(e))
            else:
                if not logged:
                    self.logger.request_end(environ, logstart,
                                            request, response)
                return response

        def _do_call(self, environ, start_response, logstart):
            request = Request(environ)
            try:
                handlers = urls
                handler = None
                for i in xrange(0, len(request.path_components)):
                    handler = handlers.get(request.path_components[i], None)
                    if handler is None:
                        break
                    if hasattr(handler, '__call__'):
                        break
                    handlers = handler
                if handler is None:
                    raise HTTPNotFound(request.path)
                if not hasattr(handler, '__call__'):
                    raise HTTPNotFound(request.path)

                # Read the properties from the handler
                handler_props = _get_props(handler)
                request._set_handler_props(handler_props)

                # Check that there are no tail components if the handler is not
                # marked as accepting pathinfo.
                tail_components = request.path_components[i + 1:]
                if len(tail_components) != 0:
                    # Raise a NotFound error unless the handler is marked as
                    # accepting pathinfo.
                    if handler_props is None or \
                       handler_props.get('pathinfo_allow', None) is None:
                        raise HTTPNotFound(request.path)

                # Set the path info
                request._set_pathinfo(tail_components)

                # Apply the pre-checks to the request.
                request = apply_request_checks_and_transforms(request, handler_props)

                # Call the handler.
                response = handler(request)

                # Apply the post-checks to the response
                response = apply_response_checks_and_transforms(request, response, handler_props)

                # Allow handlers to return strings - just wrap them in a
                # default response object.
                if isinstance(response, basestring):
                    response = Response(body=response)
                assert isinstance(response, Response)

                return False, request, WSGIResponse(start_response, response)
            except ValidationError, e:
                response = validation_error_handler(e)
                return False, request, WSGIResponse(start_response, response)
            except HTTPError, e:
                return False, request, WSGIResponse(start_response, e)
            except Exception, e:
                # Handle uncaught exceptions by returning a 500 error.
                self.logger.request_failed(environ, logstart, sys.exc_info())
                return True, request, WSGIResponse(start_response, HTTPServerError(str(e)))

    if autodoc:
        components = autodoc.split('/')
        suburls = urls
        for component in components[:-1]:
            suburls = suburls.setdefault(component, {})
        from autodoc import make_doc
        suburls[components[-1]] = make_doc(urls, autodoc)

    return Application

def make_server(app, bind_addr, *args, **kwargs):
    """Make a server for an application.

    This uses CherryPy's standalone WSGI server.  The first argument is the
    WSGI application to run; all subsequent arguments are passed directly to
    the server.  The CherryPyWSGIServer is accessible as
    wsgiwapi.cpwsgiserver: see the documentation in that module for calling
    details.

    Note that you will always need to set the bind_addr parameter; this is a
    (host, port) tuple for TCP sockets, or a filename for UNIX sockets.  The
    host part may be set to '0.0.0.0' to listen on all active IPv4 interfaces
    (or similarly, '::' to listen on all active IPv6 interfaces).

    """
    # Lazy import, so we don't pull cherrypy in unless we're using it.
    import cpwsgiserver
    server = cpwsgiserver.CherryPyWSGIServer(bind_addr, app, *args, **kwargs)
    return server

# vim: set fileencoding=utf-8 :
