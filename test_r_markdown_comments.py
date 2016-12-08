#!/usr/bin/env python3

# testRMarkdownComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_r_markdown, MapHolder


class TestRMarkdownComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        test_file = './commentsForRMarkdown'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_r_markdown(test_file, options, 'Rmd')
        self.assertEqual(lines, 114)
        self.assertEqual(sloc, 53)

if __name__ == '__main__':
    unittest.main()
