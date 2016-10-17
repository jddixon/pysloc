#!/usr/bin/env python3

# testTextComments.py
#
# There aren't any coments in plain text files.  What we do is count
# all lines which aren't empty and don't consist solely of white space.

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesTxt, Q


class TestTextComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForTxt'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        lines, sloc = countLinesTxt(testFile, options, 'txt')
        self.assertEqual(lines, 30)
        self.assertEqual(sloc, 20)

if __name__ == '__main__':
    unittest.main()
