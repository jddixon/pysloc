#!/usr/bin/env python3
# testHtmlComments.py

""" Test HTML counters. """

import unittest

from argparse import Namespace
from pysloc import count_lines_html


class TestHtmlComments(unittest.TestCase):
    """ Test HTML counters. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify line counts returned from known HTML files are correct. """
        test_file = './commentsForHtml'
        lines, sloc = count_lines_html(test_file, self.options, 'html')
        self.assertEqual(lines, 19)
        self.assertEqual(sloc, 5)


if __name__ == '__main__':
    unittest.main()
