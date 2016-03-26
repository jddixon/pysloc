#!/usr/bin/python3

# testLispComments.py
#
import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesLisp, Q


class TestLispComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testLispComments(self):
        testFile = './commentsForLisp'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = countLinesLisp(testFile, options, 'lisp')
        self.assertEqual(lines, 65)
        self.assertEqual(sloc, 38)

if __name__ == '__main__':
    unittest.main()
