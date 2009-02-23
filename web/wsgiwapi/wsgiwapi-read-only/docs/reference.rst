=========================
WSGIWAPI Reference Manual
=========================

.. Warning:: This manual is not in any way complete yet, but the information contained in it should be accurate.

Design Philosophy
=================

WSGIWAPI tries hard not to get in your way, and to let you do just those things
you want to do, without forcing you to do anything you'd rather not.  Further,
it aims to allow you to write clear and maintainable code, which is
comprehensible to other developers.

The main design principles used when designing WSGIWAPI have been:

 - Don't force use of non-essential components.  (eg, if you're not using JSON,
   you don't need to have a python JSON library installed.)
 - Don't make users repeat themselves.  For example, you don't need to provide
   a separate list of the parameters for a function for documentation purposes:
   the documentation functionality makes use of the same list as the validation
   functionality.
 - Avoid gratuitous magic (or explicit is better than implicit).  For example,
   there's no magic encoding of result types into particular character sets, or
   serialisation formats - instead you must explicitly specify that results
   should be marshalled into JSON, if that's what you want.

URI resolution
==============

FIXME - document

.. Note:: arbitrary trailing path information is not accepted by default.  If you want to accept trailing path information, you need to decorate your callable with the ``@pathinfo`` decorator.

Request objects
===============

Response objects
================

Your callable must return a `wsgiwapi.Response` object (either explicitly, or
by being decorated with a decorator like the `jsonreturning` decorator.

Redirection
-----------

WSGIWAPI currently has no explicit support for HTTP redirects.  For
now, you can implement it yourself by setting the appropriate headers
and returning the appropriate response code.

Setting headers
---------------

FIXME - general description

When adding a header, it is possible to add

Note about problem with '-'s not being allowed as keyword argument names; use {} syntax if you need to specify arguments.

Returning errors
----------------

The `wsgiwapi.Response` object allows the HTTP status code to be set
(and knows some standard reason messages for all the standard HTTP 1.1
status codes, so you can just set the numeric code if you're happy to
use the standard reason messages).  This allows you to return any HTTP
status code you like, to represent errors (or redirects, etc).

However, it is often convenient to be able to use exceptions to report
errors.  To enable this, WSGIWAPI provides `wsgiwapi.HTTPError`,
which is a subclass of `wsgiwapi.Response`, and also of the standard
`Exception` class.  This can be thrown, and provided with whatever
status code and message body you like.

For even greater convenience, there are also some subclasses for
specific error conditions:

 - `wsgiwapi.HTTPServerError`: thrown to report "500 Server Error"
 - `wsgiwapi.HTTPNotFound`: thrown to report a "404 Not Found"
   error.  
 - `wsgiwapi.HTTPMethodNotAllowed`: thrown to report a disallowed
   method.  Takes the method which was requested, and a list of the
   allowed methods for this URL.

If your callable raises any other exception, the WSGI application will
return a "500 Server Error".


Decorators
==========

WSGIWAPI provides a set of useful decorators, to make it easy to
produce certain types of API.  You don't need to use any of these, but
they will often make it easier to produce a clean API.

The WSGIWAPI decorators can be applied in any order: they all
operate by adding some extra properties to the API, and replacing the
API method with a special wrapper which interprets these properties.

If you are using other (non WSGIWAPI) decorators which replace the
callable by a decorated callable, you need to ensure that the
properties used by WSGIWAPI are copied onto the decorated callable.
If you do not do this, WSGIWAPI will raise an exception at runtime,
to ensure that inconsistent behaviour doesn't result.

Well-behaved decorators will copy the properties by default (by coping
the contents of __dict__ from the original callable to the decorated
callable), but it's best to use one of two approaches provided by
wsgiwapi to ensure that 

 - If you are writing the decorator yourself, include a call to
   ``wsgiwapi.copyprops`` at the end of the decorator: pass this the
   original callable, and the decorated callable, and it will copy all
   the appropriate properties across.

   FIXME - example.

 - If you are using an existing decorator, wrap it in the
   ``wsgiwapi.decorate`` decorator (ie, pass it as an argument to
   this decorator).  This decorator first applies the decorator it is
   given, and then applies ``wsgiwapi.copyprops`` to fix up the
   properties.

   FIXME - example.

Validation
==========

Restricting HTTP methods
------------------------

By default, WSGIWAPI will allow any HTTP method to be used to call
your API.  It is often desirable to restrict the set of methods which
are allowed at a particular path.  To do this, you can use the
`allow_method` decorator.  This decorator takes one or more parameters
listing allowable methods.  If the decorator is used multiple times,
any of the methods listed in any of its invocations will be allowed::

    FIXME - example

Some convenient shortcuts are available:

 - allow_GET: allow GET requests; equivalent to allow_method('GET')
 - allow_HEAD: allow HEAD requests; equivalent to allow_method('HEAD')
 - allow_GETHEAD: allow GET or HEAD requests; equivalent to
   allow_method('GET', 'HEAD')
 - allow_POST: allow POST requests; equivalent to allow_method('POST')

If any of these decorators have been used, and the method used is not
listed, the request will return an HTTP 405 or 501 error (depending on
whether the request method is one of the standard HTTP 1.1 methods),
as suggested by the HTTP 1.1 specification.  In this case, the
callable you specified for the URL will not be called.

Query parameters
----------------

FIXME - document more

By default, any query parameters can be supplied to a method - it is
up to the method to check that they are valid.

The parameters allowed at a particular path can be specified using the
"param" decorator.  This performs validation of the parameters, and
will raise a ValidationError if the parameters are not valid (the
default validation error handler will translate this into an HTTP 400
error, but you can override this behaviour with your own handler).

This allows parameters to be taken from the query string part of the
URL, or from POST request bodies (if both are specified, they are
merged, and the POST ones are returned first).

Pathinfo
--------

FIXME - document

.. Warning:: if you've decorated with the @pathinfo decorator, and also decorated with another (non-WSGIWAPI) decorator, you may find that the method still doesn't seem to accept trailing path information.  This is because ... to fix it call copyprops, or use the wsgiwapi.decorate decorator.

JSON output
===========

To use the JSON support, your python environment must contain the
``simplejson`` module.

Returning JSON
--------------

Often, you will want to return JSON output from an API.  This can be done very
simply by using the `jsonreturning` decorator.  The return type of a method
wrapped in this decorator should be an object which is capable of being
converted to JSON (typically, a string, integer, or a sequence or dictionary
containing strings, integers, sequences or dictionaries).  The returned value
will automatically be converted to JSON, and the content type will be set
appropriately.

Here's an example of this decorator (which you can see in a cherrypy wrapper at
`<examples/jsonsumapp_cp.py>`_)::

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

Returning JSONP
---------------

FIXME - document, and add notes on why JSONP might be a bad idea in some cases.


Unicode issues
==============

Python supports two types of strings:

 - byte string objects (ie, "str" objects in Python 2.x, "bytes"
   objects in Python 3.0 onwards)
 - unicode string objects (ie, "unicode" objects in Python 2.x, "str"
   objects in Python 3.0 onwards)

In general, if you're handling text data it is best to use unicode
objects; text isn't generally meaningful unless you know what
character set it is in, and things can get very messy if you work with
text objects which don't know what character set they are in.

If you're handling non-textual, binary data, you'll probably need to
work with byte string objects.

Getting strings from WSGIWAPI
-----------------------------

FIXME - Does WSGIWAPI always supply unicode strings in request
objects?  What should it do if parameters aren't encodable as unicode?

Supplying strings to WSGIWAPI
-----------------------------

In most situations, you should supply WSGIWAPI with unicode strings.
If you do this, you don't generally need to worry about character
encoding issues.  WSGIWAPI will also accept plain byte strings, but if
you supply it with these, it is up to you to ensure that any necessary
character set information is set.

There are four main places where WSGIWAPI is supplied with strings by
your code.

 - URL components, as supplied to ``wsgiwapi.make_application``.
 - The status code and reason message.
 - The HTTP response headers.
 - The HTTP response body.

There are various limitations on the data supplied in these locations:

 - The URL components must (currently) only contain US-ASCII
   characters.

   If you supply byte strings, they will be assumed to be US-ASCII
   strings - any non-US-ASCII characters in the strings supplied
   (whether byte strings or unicode strings) will cause an exception
   to be raised.

   Later releases of WSGIWAPI could add support for IRIs,
   which allow other characters to be encoded, but this is not yet
   implemented.  In the meantime, you could encode the URL components
   according to RFC 3987 yourself.

 - Status codes and the associated reason messages must only use
   US-ASCII characters.

   If you supply byte strings, they will be assumed to be US-ASCII
   strings - any non-US-ASCII characters in the strings supplied
   (whether byte strings or unicode strings) will cause an exception
   to be raised.

 - For headers, the header name and value must be composed of US-ASCII
   characters - though header values may take additional parameters whose
   values may contain arbitrary unicode characters.

   If you supply byte strings, they will be assumed to be US-ASCII strings -
   any non-US-ASCII characters in the strings supplied (whether byte strings or
   unicode strings) will cause an exception to be raised.

   If header values are supplied with additional parameters whose values are
   unicode objects which cannot be encoded in US-ASCII, the parameter values
   will be encoded according to the method described in RFC 2231.  Note that
   HTTP clients may not understand this correctly in all cases - anecdotal
   evidence at the time of writing suggests that many browsers only support
   this in the Conent-Disposition header's filename parameter, presently.
   Therefore, use such unicode values with caution.  If you're writing your own
   clients, you're probably safe.

 - There is no restriction on the byte values which are supplied for
   the HTTP response body - if you supply a byte string, it will be
   transmitted exactly as-is.

   By default, if a unicode object is supplied for the response body,
   it will be converted to UTF-8 for transmission.  The character set
   to use can be altered with the ``response_charset`` decorator.  In
   addition, if the ``Content-Type`` HTTP header is set to any
   ``text/*`` mime type, an appropriate "charset" attribute will be
   added to the resulting decorator (unless one has already been set
   explicitly).

Extra utilities
===============

Built-in server
---------------

Testing framework
-----------------

