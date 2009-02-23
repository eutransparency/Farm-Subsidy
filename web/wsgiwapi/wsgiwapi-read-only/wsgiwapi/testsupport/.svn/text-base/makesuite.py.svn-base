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
r"""makesuite.py: Build a test suite for the wsgiwapi tests.

"""
__docformat__ = "restructuredtext en"

########################
# End of configuration #
########################

import os
import unittest

def canonical_path(path):
    return os.path.normcase(os.path.normpath(os.path.realpath(path)))

def find_unittests(testdir):
    """Find all files containing unit tests under a top directory.

    """
    unittests = []
    for root, dirnames, filenames in os.walk(testdir):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            relpath = filepath[len(testdir)+1:]
            if filename == "__init__.py":
                continue

            if filename.endswith(".py"):
                unittests.append(relpath)
    return unittests

def get_topdir():
    up = os.path.dirname
    return canonical_path(up(up(up(__file__))))

def make_suite(use_coverage=False):
    topdir = get_topdir()
    # Make a test suite to put all the tests in.
    suite = unittest.TestSuite()

    if use_coverage:
        # Use the coverage test module to get coverage information.
        import coverage
        coverage.erase()
        coverage.start()
        coverage.exclude('#pragma[: ]+[nN][oO] [cC][oO][vV][eE][rR]')

    # Add unittests
    loader = unittest.TestLoader()
    for testpath in find_unittests(os.path.join(topdir, "wsgiwapi", "unittests")):
        modpath = "wsgiwapi.unittests." + testpath.replace('/', '.')[:-3]
        mod = __import__(modpath, None, None, [''])
        test = loader.loadTestsFromModule(mod)
        suite.addTest(test)

    return suite

def run_tests(use_coverage):
    """Run tests.

    """

    suite = make_suite(use_coverage)

    # Now, run everything.
    runner = unittest.TextTestRunner()
    runner.run(suite)

    if use_coverage:
        # Finished run - stop the coverage tests
        import coverage
        coverage.stop()

def get_coverage():
    topdir = get_topdir()
    import coverage

    # Get the coverage statistics
    stats = []
    modules = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(get_topdir(), 'wsgiwapi')):
        for fname in filenames:
            if not fname.endswith('.py'):
                continue
            fpath = os.path.join(dirpath, fname)
            if '/cpwsgiserver/' in fpath:
                continue
            modules.append(fpath)
    for module in modules:
        (filename, stmtlines, excluded, stmtmissed, stmtmissed_desc) = coverage.analysis2(module)
        if len(stmtlines) == 0:
            continue
        filename = canonical_path(filename)
        if filename.startswith(topdir):
            filename = filename[len(topdir) + 1:]

        lines = open(filename).readlines()
        linenum = len(lines)

        # Sort the lines (probably already in order, but let's double-check)
        stmtlines.sort()
        stmtmissed.sort()

        # Build a compressed list of ranges of lines which have no statements
        # which were executed, but do contain statements.
        missed_ranges = []
        stmtpos = 0
        currrange = None
        for linenum in stmtmissed:
            while stmtlines[stmtpos] < linenum:
                # If there are any statements before the current linenum, we
                # end the current range of missed statements
                currrange = None
                stmtpos += 1
            if currrange is None:
                currrange = [linenum, linenum]
                missed_ranges.append(currrange)
            else:
                currrange[1] = linenum
            stmtpos += 1

        percent = (len(stmtlines) - len(stmtmissed)) * 100.0 / len(stmtlines)
        stats.append((filename, percent, len(stmtlines), missed_ranges))
    return stats

def display_coverage(stats):
    print "Coverage report:"
    max_filename_len  = max([len(stat[0]) for stat in stats])
    for filename, percent, total, missed in stats:
        msg = "%r%s %5.1f%% of %d" % (filename, ' ' * (max_filename_len - len(filename)), percent, total)
        if len(missed) != 0:
            for pos in xrange(len(missed)):
                if missed[pos][0] == missed[pos][1]:
                    missed[pos] = str(missed[pos][0])
                elif missed[pos][0] + 1 == missed[pos][1]:
                    missed[pos] = "%d,%d" % tuple(missed[pos])
                else:
                    missed[pos] = "%d-%d" % tuple(missed[pos])
            msg += "\t Missed: %s" % ','.join(missed)
        print msg

def run(use_coverage=False, use_profiling=False):
    if use_profiling:
        try:
            import cProfile as profile
        except ImportError:
            import profile

        profile.run('run_tests(%r)' % (use_coverage,),
                              os.path.join(get_topdir(), '.runtests.prof'))
    else:
        run_tests(use_coverage)

    if use_coverage:
        display_coverage(get_coverage())
