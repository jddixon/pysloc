#!/usr/bin/env python3
# testTomlComments.py

""" Test functioning of toml line counters. """

import unittest

from argparse import Namespace
from pysloc import count_lines_not_sharp


class TestTomlComments(unittest.TestCase):
    """ Test functioning of toml line counters. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify line counts for known file are as expected. """

        test_file = 'tests/commentsForToml'
        lines, sloc = count_lines_not_sharp(test_file, self.options, 'toml')
        self.assertEqual(lines, 39)
        self.assertEqual(sloc, 12)


if __name__ == '__main__':
    unittest.main()
