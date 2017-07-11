#!/usr/bin/env python3
# testMatlabComments.py

""" Test line counters for Matlab. """

import unittest

from argparse import Namespace
from pysloc import count_lines_matlab


class TestMatlabComments(unittest.TestCase):
    """ Test line counters for Matlab. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify that line counts for a known Matlab file are correct. """

        test_file = 'tests/commentsForMatlab'
        lines, sloc = count_lines_matlab(test_file, self.options, 'matlab')
        self.assertEqual(lines, 49)
        self.assertEqual(sloc, 17)


if __name__ == '__main__':
    unittest.main()
