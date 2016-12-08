#!/usr/bin/env python3

# testJsonComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_txt


class TestJsonComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        test_file = './commentsForJson'
        lines, sloc = count_lines_txt(test_file, self.options, 'txt')
        self.assertEqual(lines, 9)
        self.assertEqual(sloc, 9)

if __name__ == '__main__':
    unittest.main()
