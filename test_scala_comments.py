#!/usr/bin/env python3

# testScalaComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_scala


class TestScalaComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        test_file = './commentsForScala'
        lines, sloc = count_lines_scala(test_file, self.options, 'scala')
        self.assertEqual(lines, 48)
        self.assertEqual(sloc, 9)

if __name__ == '__main__':
    unittest.main()
