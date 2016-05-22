#!/usr/bin/env python3

# testAugeasComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesAugeas


class TestAugeasComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForAugeas'
        lines, sloc = countLinesAugeas(testFile, self.options, 'ml')
        self.assertEqual(lines, 107)
        self.assertEqual(sloc, 45)

if __name__ == '__main__':
    unittest.main()
