#!/usr/bin/env python
#
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
"""Setup script for WSGIWAPI.

"""

from distutils.core import setup

long_description="""

WSGIWAPI makes it easy to build web APIs, without dealing with the details of
HTTP. You simply define a hierarchical tree of URL components, with callables
as the leaves of the tree, and WSGIWAPI does the work of making this into a
WSGI application.

WSGIWAPI also provides some additional features, such as automatic
documentation support for your API and parameter validation, and includes
support for easily running your application as a standalone server.

"""

setup(name = "WSGIWAPI",
      version = "0.2",
      description = "Framework for building web APIs",
      long_description = long_description,
      author = "Richard Boulton",
      author_email = "richard@tartarus.org",
      maintainer = "Richard Boulton",
      maintainer_email = "richard@tartarus.org",
      url = "http://wsgiwapi.tartarus.org/",
      #test_suite = "wsgiwapi.testsupport.makesuite.make_suite",
      download_url = "http://wsgiwapi.googlecode.com/files/WSGIWAPI-0.2.tar.gz",

      classifiers = [
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
          'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
      ],
      keywords='web API,REST,WSGI',
      license = 'MIT',
      platforms = 'Any',

      packages = ['wsgiwapi'],
      package_dir = {'wsgiwapi': 'wsgiwapi'},
      package_data = {'docs': ['docs/*.html']}
)
