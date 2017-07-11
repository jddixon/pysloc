#!/usr/bin/env python3
# testRustComments.py

""" Test line counters for Rust. """

import unittest
from argparse import Namespace

from pysloc import count_lines_rust, MapHolder


class TestRustComments(unittest.TestCase):
    """ Test line counters for Rust. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        """ Verify line counts are as expcted for know file. """
        test_file = 'tests/commentsForRust'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_rust(test_file, options, 'occ')
        self.assertEqual(lines, 129)
        self.assertEqual(sloc, 93)


if __name__ == '__main__':
    unittest.main()
