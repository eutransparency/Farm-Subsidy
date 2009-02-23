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
r"""Test OverlayDict class.

"""
__docformat__ = "restructuredtext en"

from harness import *
import wsgiwapi.overlaydict

class OverlayDictTest(TestCase):
    """Test OverlayDict support.

    """
    def test_overlaydict(self):
        """Test of the OverlayDict.

        """
        d1 = {}
        d2 = {}
        d = wsgiwapi.overlaydict.OverlayDict(d1, d2)
        def fn(): d[1] = 1
        self.assertRaises(AttributeError, fn)
        self.assertEqual(d.get(1), None)
        self.assertEqual(len(d), 0)
        def fn(): d[1]
        self.assertRaises(KeyError, fn)
        self.assertEqual(list(d), [])
        self.assertEqual(len(d), 0)

        d2[1] = ['a']
        self.assertEqual(len(d), 1)
        self.assertEqual(list(d), [1])
        self.assertEqual(d.items(), [(1, ['a'])])
        d1[1] = ['A']
        self.assertEqual(len(d), 1)
        self.assertEqual(list(d), [1])
        self.assertEqual(d.items(), [(1, ['A', 'a'])])

        correct_keys = [1, None]
        correct_keys.sort()

        d1[None] = ['B']
        self.assertEqual(len(d), 2)
        self.assertEqual(list(d), correct_keys)
        d2[None] = ['b']
        self.assertEqual(len(d), 2)
        self.assertEqual(list(d), correct_keys)

        del d1[None]
        self.assertEqual(len(d), 2)
        self.assertEqual(list(d), correct_keys)
        del d2[None]
        self.assertEqual(len(d), 1)
        self.assertEqual(list(d), [1])
        self.assertEqual(d.items(), [(1, ['A', 'a'])])

        del d1[1]
        self.assertEqual(len(d), 1)
        self.assertEqual(list(d), [1])
        self.assertEqual(d.items(), [(1, ['a'])])
        del d2[1]
        self.assertEqual(len(d), 0)
        self.assertEqual(list(d), [])
        self.assertEqual(d.items(), [])

 
if __name__ == '__main__': main()
# vim: set fileencoding=utf-8 :
