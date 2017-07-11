#!/usr/bin/env python3
# testXmlComments.py

""" Test line counters for XML documents. """

import unittest
from argparse import Namespace

from pysloc import count_lines_xml, MapHolder


class TestXmlComments(unittest.TestCase):
    """ Test line counters for XML documents. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_xml_comments(self):
        """ Verify that line counts from a known XML file are correct. """
        test_file = 'tests/commentsForXml'
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
