#!/usr/bin/python3

# testJavaComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesJava


class TestJavaComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForJava'
        lines, sloc = countLinesJava(testFile, self.options, 'java')
        self.assertEqual(lines, 21)
        self.assertEqual(sloc, 7)

if __name__ == '__main__':
    unittest.main()
