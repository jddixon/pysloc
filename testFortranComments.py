#!/usr/bin/python3

# testFortranComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesFortran


class TestFortranComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForFortran'
        lines, sloc = countLinesFortran(testFile, self.options, 'for')
        self.assertEqual(lines, 32)
        self.assertEqual(sloc, 8)

if __name__ == '__main__':
    unittest.main()
