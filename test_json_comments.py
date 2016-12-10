#!/usr/bin/env python3
# testJsonComments.py

""" Test line counters for json. """

import unittest

from argparse import Namespace
from pysloc import count_lines_txt


class TestJsonComments(unittest.TestCase):
    """ Test line counters for json. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify that line counts for known Json file are correct. """
        test_file = './commentsForJson'
        lines, sloc = count_lines_txt(test_file, self.options, 'txt')
        self.assertEqual(lines, 9)
        self.assertEqual(sloc, 9)

if __name__ == '__main__':
    unittest.main()
