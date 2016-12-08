#!/usr/bin/env python3

# testUserGuide.py
#
import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_xml, MapHolder


class TestUserGuide (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_user_guide(self):
        test_file = './userguide.xml'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = count_lines_xml(test_file, options, 'xml')
        self.assertEqual(lines, 182)
        # 4 header lines, 13 other blank lines
        self.assertEqual(sloc, 165)

if __name__ == '__main__':
    unittest.main()
