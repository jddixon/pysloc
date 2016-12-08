#!/usr/bin/env python3

# testAugeasComments.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_augeas


class TestAugeasComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        test_file = './commentsForAugeas'
        lines, sloc = count_lines_augeas(test_file, self.options, 'ml')
        self.assertEqual(lines, 107)
        self.assertEqual(sloc, 45)

if __name__ == '__main__':
    unittest.main()
