#!/usr/bin/env python3

# testJavaComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_java


class TestJavaComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        test_file = './commentsForJava'
        lines, sloc = count_lines_java(test_file, self.options, 'java')
        self.assertEqual(lines, 21)
        self.assertEqual(sloc, 7)

if __name__ == '__main__':
    unittest.main()
