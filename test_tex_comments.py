#!/usr/bin/env python3

# testTexComments.py
#
import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_tex, MapHolder


class TestTexComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_tex_comments(self):
        test_file = './commentsForTeX'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = count_lines_tex(test_file, options, 'tex')
        self.assertEqual(lines, 32)
        self.assertEqual(sloc, 6)

if __name__ == '__main__':
    unittest.main()
