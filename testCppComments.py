#!/usr/bin/env python3

# testCppComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesCpp


class TestCppComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForCpp'
        lines, sloc = countLinesCpp(testFile, self.options, 'go')
        self.assertEqual(lines, 152)
        self.assertEqual(sloc, 33)


if __name__ == '__main__':
    unittest.main()
