#!/usr/bin/env python3

# testRustComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesRust, Q


class TestRustComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForRust'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        lines, sloc = countLinesRust(testFile, options, 'occ')
        self.assertEqual(lines, 129)
        self.assertEqual(sloc, 93)

if __name__ == '__main__':
    unittest.main()
