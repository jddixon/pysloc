#!/usr/bin/env python3

# testPascalComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesPascal


class TestPascalComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForPascal'
        lines, sloc = countLinesPascal(testFile, self.options, 'ml')
        self.assertEqual(lines, 58)
        self.assertEqual(sloc, 18)

if __name__ == '__main__':
    unittest.main()
