#!/usr/bin/env python3

# testOccamComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_double_dash, MapHolder


class TestOccamComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        test_file = './commentsForOccam'
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
