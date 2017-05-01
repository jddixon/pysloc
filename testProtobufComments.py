#!/usr/bin/env python3

# testProtobufComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesProtobuf, Q


class TestProtobufComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForProtobuf'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        lines, sloc = countLinesProtobuf(testFile, options, 'py')
        self.assertEqual(lines, 71)
        self.assertEqual(sloc, 46)


if __name__ == '__main__':
    unittest.main()
