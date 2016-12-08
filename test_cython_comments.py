#!/usr/bin/env python3

# testPyComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_python, MapHolder


class TestPyComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_pxd(self):
        test_file = './commentsForCython.pxd'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_python(test_file, options, 'pxd')
        self.assertEqual(lines, 53)
        self.assertEqual(sloc, 23)

    def test_pyx(self):
        test_file = './commentsForCython.pyx'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_python(test_file, options, 'pyx')
        self.assertEqual(lines, 86)
        self.assertEqual(sloc, 48)

if __name__ == '__main__':
    unittest.main()
