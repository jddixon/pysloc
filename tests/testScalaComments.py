#!/usr/bin/env python3

# testScalaComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesScala


class TestScalaComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForScala'
        lines, sloc = countLinesScala(testFile, self.options, 'scala')
        self.assertEqual(lines, 48)
        self.assertEqual(sloc, 9)


if __name__ == '__main__':
    unittest.main()
