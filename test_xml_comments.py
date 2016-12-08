#!/usr/bin/env python3

# testXmlComments.py
#
import os
import sys
import unittest
from argparse import Namespace

from pysloc import __version__, __version_date__
from pysloc import count_lines_in_dir, count_lines_xml, MapHolder


class TestXmlComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_xml_comments(self):
        test_file = './commentsForXml'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = count_lines_xml(test_file, options, 'xml')
        self.assertEqual(lines, 29)
        self.assertEqual(sloc, 6)

if __name__ == '__main__':
    unittest.main()
