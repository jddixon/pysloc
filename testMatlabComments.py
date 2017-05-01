#!/usr/bin/env python3

# testMatlabComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesMatlab


class TestMatlabComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForMatlab'
        lines, sloc = countLinesMatlab(testFile, self.options, 'matlab')
        self.assertEqual(lines, 49)
        self.assertEqual(sloc, 17)


if __name__ == '__main__':
    unittest.main()
