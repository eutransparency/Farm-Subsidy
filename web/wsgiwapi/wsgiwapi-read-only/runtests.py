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
r"""runtests.py: Run test wsgiwapi tests.

"""
__docformat__ = "restructuredtext en"

########################
# End of configuration #
########################

import sys
from wsgiwapi.testsupport.makesuite import run

if __name__ == '__main__':
    args = {
    }
    for arg in sys.argv[1:]:
        if arg in ('-c', '--coverage'):
            args['use_coverage'] = True
        elif arg in ('-p', '--profile'):
            args['use_profiling'] = True
        elif arg in ('-h', '--help'):
            print("./runtests.py [-c] [-p]")
            sys.exit(0)
        else:
            print("Unknown parameter '%s'" % arg)
            sys.exit(1)
    run(**args)
