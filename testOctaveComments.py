#!/usr/bin/env python3

# testOctaveComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesOctave


class TestOctaveComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testNameToFuncMap(self):
        testFile = './commentsForOctave'
        lines, sloc = countLinesOctave(testFile, self.options, 'octave')
        self.assertEqual(lines, 79)
        self.assertEqual(sloc, 25)

if __name__ == '__main__':
    unittest.main()
