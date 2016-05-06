#!/usr/bin/python3

# testR2CComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesDoubleDash, Q


class TestR2CComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForR2C'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        lines, sloc = countLinesDoubleDash(testFile, options, 'occ')
        self.assertEqual(lines, 0)
        self.assertEqual(sloc, 0)

if __name__ == '__main__':
    unittest.main()
