#!/usr/bin/env python3

# testOccamComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesDoubleDash, Q


class TestOccamComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForOccam'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        lines, sloc = countLinesDoubleDash(testFile, options, 'occ')
        self.assertEqual(lines, 27)
        self.assertEqual(sloc, 10)


if __name__ == '__main__':
    unittest.main()
