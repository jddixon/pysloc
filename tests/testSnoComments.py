#!/usr/bin/env python3

# testSnoComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesSnobol


class TestSnoComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForSno'
        lines, sloc = countLinesSnobol(testFile, self.options, 'sno')
        self.assertEqual(lines, 19)
        self.assertEqual(sloc, 8)


if __name__ == '__main__':
    unittest.main()
