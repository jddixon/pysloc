#!/usr/bin/env python3

# testFortran90Comments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import count_lines_fortran90


class TestFortran90Comments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_fortran90_comments(self):
        test_file = './commentsForFortran90'
        lang = 'f90+'
        lines, sloc = count_lines_fortran90(test_file, self.options, lang)
        self.assertEqual(lines, 42)
        self.assertEqual(sloc, 9)

if __name__ == '__main__':
    unittest.main()
