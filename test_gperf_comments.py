#!/usr/bin/env python3

# testGperfComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import (__version__, __version_date__,
                    GPERF_RE,
                    countLinesInDir, countLinesGperf,
                    Q)


class TestGperfComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testFirstLinePat(self):

        badLine = '/* ANSI-C code produced by gperf version N.N.N */'
        m = GPERF_RE.match(badLine)
        self.assertEqual(m, None)

        goodLine = '/* ANSI-C code produced by gperf version 1.2.3 */'
        m = GPERF_RE.match(goodLine)
        self.assertNotEqual(m, None)
        s = m.group(0)
        self.assertTrue(s.startswith('/* ANSI-C'))

    def testNameToFuncMap(self):
        testFile = './commentsForGperf'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        lines, sloc = countLinesGperf(testFile, options, 'gperf')
        self.assertEqual(lines, 5)
        self.assertEqual(sloc, 2)

if __name__ == '__main__':
    unittest.main()
