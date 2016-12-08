#!/usr/bin/env python3

# testTextComments.py
#
# There aren't any coments in plain text files.  What we do is count
# all lines which aren't empty and don't consist solely of white space.

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_txt, MapHolder


class TestTextComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        test_file = './commentsForTxt'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_txt(test_file, options, 'txt')
        self.assertEqual(lines, 30)
        self.assertEqual(sloc, 20)

if __name__ == '__main__':
    unittest.main()
