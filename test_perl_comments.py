#!/usr/bin/env python3

# testPerlComments.py
#
import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_perl, MapHolder


class TestPerlComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_perl_comments(self):
        test_file = './commentsForPerl'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = count_lines_perl(test_file, options, 'perl')
        self.assertEqual(lines, 39)
        self.assertEqual(sloc, 7)

if __name__ == '__main__':
    unittest.main()
