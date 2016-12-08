#!/usr/bin/env python3

# testFortranComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import count_lines_fortran


class TestFortranComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        test_file = './commentsForFortran'
        lines, sloc = count_lines_fortran(test_file, self.options, 'for')
        self.assertEqual(lines, 32)
        self.assertEqual(sloc, 8)

if __name__ == '__main__':
    unittest.main()
