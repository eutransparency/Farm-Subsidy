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
r"""Overlay one dict on top of another.

"""
__docformat__ = "restructuredtext en"

import UserDict

class _Unused(object):
    """Sentinel class used for initial value of lastkey.

    """
    pass

class OverlayDict(UserDict.DictMixin):
    """A dictionary which behaves as if one dict is layered on top of another.

    """
    def __init__(self, dict1, dict2):
        self.dict1 = dict1
        self.dict2 = dict2

    def __contains__(self, key):
        if key in self.dict1:
            return True
        return key in self.dict2

    def __getitem__(self, key):
        try:
            items = self.dict1[key]
            try:
                items2 = self.dict2[key]
                return items + items2
            except KeyError:
                return items
        except KeyError:
            return self.dict2[key]

    def __iter__(self):
        keys = self.dict1.keys()
        keys.extend(self.dict2.keys())
        keys.sort()
        lastkey = _Unused
        for key in keys:
            if key != lastkey:
                yield key
                lastkey = key

    def keys(self):
        return list(iter(self))

# vim: set fileencoding=utf-8 :
