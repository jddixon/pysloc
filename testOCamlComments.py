#!/usr/bin/env python3

# testOCamlComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesOCaml


class TestOCamlComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForOCaml'
        lines, sloc = countLinesOCaml(testFile, self.options, 'ml')
        self.assertEqual(lines, 39)
        self.assertEqual(sloc, 15)

if __name__ == '__main__':
    unittest.main()
