#!/usr/bin/env python3

# testTexComments.py
#
import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesTeX, Q


class TestTexComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testTexComments(self):
        testFile = './commentsForTeX'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = countLinesTeX(testFile, options, 'tex')
        self.assertEqual(lines, 32)
        self.assertEqual(sloc, 6)

if __name__ == '__main__':
    unittest.main()
