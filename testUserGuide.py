#!/usr/bin/env python3

# testUserGuide.py
#
import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import countLinesInDir, countLinesXml, Q


class TestUserGuide (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testUserGuide(self):
        testFile = './userguide.xml'
        options = Namespace()
        options.already = set()
        options.exRE = None
        options.q = Q()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = countLinesXml(testFile, options, 'xml')
        self.assertEqual(lines, 182)
        # 4 header lines, 13 other blank lines
        self.assertEqual(sloc, 165)

if __name__ == '__main__':
    unittest.main()
