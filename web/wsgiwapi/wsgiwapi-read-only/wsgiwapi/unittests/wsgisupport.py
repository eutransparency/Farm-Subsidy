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
r"""Test wsgisupport.py.

"""
__docformat__ = "restructuredtext en"

from harness import *
from wsgiwapi import wsgisupport

class ResponseTest(TestCase):
    """Test Response class.

    """
    def test_status(self):
        """Test setting and getting the status.

        """
        # Check default status
        res = wsgisupport.Response()
        self.assertEqual(res.status, '200 OK')

        # Check setting status by numeric code
        res = wsgisupport.Response(status=404)
        self.assertEqual(res.status, '404 Not Found')

        # Check setting status by string containing code
        res = wsgisupport.Response(status='100')
        self.assertEqual(res.status, '100 Continue')

        # Check setting status by unicode string containing code
        res = wsgisupport.Response(status=u'101')
        self.assertEqual(res.status, '101 Switching Protocols')

        # Check setting status by string containing code and message
        res = wsgisupport.Response(status='404 Lost and lonely')
        self.assertEqual(res.status, '404 Lost and lonely')

        # Check setting status by unicode string containing code and message
        res = wsgisupport.Response(status=u'200 Feeling pretty good')
        self.assertEqual(res.status, '200 Feeling pretty good')

        # Check failures for badly formed status codes:
        # extraneous space:
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]200 ['\"]\) is not valid",
                                 wsgisupport.Response, status=u'200 ')
 
        # Too short
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]2['\"]\) is not valid",
                                 wsgisupport.Response, status=u'2')

        # Too long
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]2001['\"]\) is not valid",
                                 wsgisupport.Response, status=u'2001')
 
        # Not numeric
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]foo['\"]\) is not a valid status "
                                 "code",
                                 wsgisupport.Response, status=u'foo')

        # Not numeric, with reason phrase
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]foo bar['\"]\) is not valid",
                                 wsgisupport.Response, status=u'foo bar')

        # Not standard - as numeric
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(470\) is not known",
                                 wsgisupport.Response, status=470)

        # Not standard - as string
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]470['\"]\) is not known",
                                 wsgisupport.Response, status=u'470')

        # Not standard - with reason phrase works
        res = wsgisupport.Response(status=u'470 Novel problem')
        self.assertEqual(res.status, '470 Novel problem')

        # Out of range, with reason phrase
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(670\) is not in valid range",
                                 wsgisupport.Response, status=670)
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]670['\"]\) is not in valid range",
                                 wsgisupport.Response, status=u'670')
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]670 Novel problem['\"]\) is not valid",
                                 wsgisupport.Response,
                                 status=u'670 Novel problem')

        # Check non-US-ASCII characters.
        self.assertRaisesMessage(ValueError, "Supplied status "
                                 "\(u?['\"]6\\\\xa30['\"]\) is not a valid"
                                 " status code",
                                 wsgisupport.Response, status=u'6\u00a30')

        self.assertRaises(ValueError, wsgisupport.Response,
                          status=u'404 Invalid character\u00a3.')

if __name__ == '__main__': main()
# vim: set fileencoding=utf-8 :
