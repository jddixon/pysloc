#!/usr/bin/env python3
# testFortranComments.py

""" Test line counts from FORTRAN files for correctness. """

import unittest

from argparse import Namespace
from pysloc import count_lines_fortran


class TestFortranComments(unittest.TestCase):
    """ Test line counts from FORTRAN files for correctness. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify line counts returned from known *.for file are correct. """
        test_file = './commentsForFortran'
        lines, sloc = count_lines_fortran(test_file, self.options, 'for')
        self.assertEqual(lines, 32)
        self.assertEqual(sloc, 8)

if __name__ == '__main__':
    unittest.main()
