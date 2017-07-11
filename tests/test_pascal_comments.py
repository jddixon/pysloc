#!/usr/bin/env python3
# testPascalComments.py

""" Test line counters for Pascal. """

import unittest

from argparse import Namespace
from pysloc import count_lines_pascal


class TestPascalComments(unittest.TestCase):
    """ Test line counters for Pascal. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify that the line counts are as expected for a known file. """

        test_file = 'tests/commentsForPascal'
        lines, sloc = count_lines_pascal(test_file, self.options, 'ml')
        self.assertEqual(lines, 58)
        self.assertEqual(sloc, 18)


if __name__ == '__main__':
    unittest.main()
