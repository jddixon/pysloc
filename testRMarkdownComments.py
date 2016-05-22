#!/usr/bin/env python3

# testRMarkdownComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesRMarkdown, Q


class TestRMarkdownComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForRMarkdown'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        lines, sloc = countLinesRMarkdown(testFile, options, 'Rmd')
        self.assertEqual(lines, 114)
        self.assertEqual(sloc, 53)

if __name__ == '__main__':
    unittest.main()
