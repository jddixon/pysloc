#!/usr/bin/env python3

# testHtmlComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesHtml


class TestHtmlComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForHtml'
        lines, sloc = countLinesHtml(testFile, self.options, 'html')
        self.assertEqual(lines, 19)
        self.assertEqual(sloc, 5)


if __name__ == '__main__':
    unittest.main()
