#!/usr/bin/env python3
# testOCamlComments.py

""" Test OCaml line counters. """

import unittest

from argparse import Namespace
from pysloc import count_lines_ocaml


class TestOCamlComments(unittest.TestCase):
    """ Test OCaml line counters. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify that line counts for a known OCaml file are correct. """
        test_file = './commentsForOCaml'
        lines, sloc = count_lines_ocaml(test_file, self.options, 'ml')
        self.assertEqual(lines, 39)
        self.assertEqual(sloc, 15)

if __name__ == '__main__':
    unittest.main()
