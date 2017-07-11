#!/usr/bin/env python3
# test_snobol_comments.py

""" Test functioning of Snobol line counters. """

import unittest

from argparse import Namespace
from pysloc import count_lines_snobol


class TestSnoComments(unittest.TestCase):
    """ Test functioning of Snobol line counters. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify line counts for known file are as expected. """

        test_file = 'tests/commentsForSno'
        lines, sloc = count_lines_snobol(test_file, self.options, 'sno')
        self.assertEqual(lines, 19)
        self.assertEqual(sloc, 8)


if __name__ == '__main__':
    unittest.main()
