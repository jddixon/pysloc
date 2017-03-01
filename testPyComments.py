#!/usr/bin/env python3

# testPyComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesPython, Q


class TestPyComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForPy'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        lines, sloc = countLinesPython(testFile, options, 'py')
        self.assertEqual(lines, 29)
        self.assertEqual(sloc, 13)

if __name__ == '__main__':
    unittest.main()
