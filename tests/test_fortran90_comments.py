#!/usr/bin/env python3
# testFortran90Comments.py

""" Test line counters for Fortran90. """

import unittest

from argparse import Namespace
from pysloc import count_lines_fortran90


class TestFortran90Comments(unittest.TestCase):
    """ Test line counters for Fortran90. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_fortran90_comments(self):
        """ Verify that line counts for a known FORTRA90 file are correct. """

        test_file = './commentsForFortran90'
        lang = 'f90+'
        lines, sloc = count_lines_fortran90(test_file, self.options, lang)
        self.assertEqual(lines, 42)
        self.assertEqual(sloc, 9)


if __name__ == '__main__':
    unittest.main()
