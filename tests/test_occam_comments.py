#!/usr/bin/env python3
# testOccamComments.py

""" Test Occam line counters. """

import unittest
from argparse import Namespace

from pysloc import count_lines_double_dash, MapHolder


class TestOccamComments(unittest.TestCase):
    """ Test Occam line counters. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify that line counts from a known occam file are correct. """
        test_file = 'tests/commentsForOccam'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_double_dash(test_file, options, 'occ')
        self.assertEqual(lines, 27)
        self.assertEqual(sloc, 10)


if __name__ == '__main__':
    unittest.main()
