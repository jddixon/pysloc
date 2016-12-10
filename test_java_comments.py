#!/usr/bin/env python3
# testJavaComments.py

""" Test line counter for Java-like languages. """

import unittest

from argparse import Namespace
from pysloc import count_lines_java


class TestJavaComments(unittest.TestCase):
    """ Test line counter for Java-like languages. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify line counts returned from known Java file are correct. """
        test_file = './commentsForJava'
        lines, sloc = count_lines_java(test_file, self.options, 'java')
        self.assertEqual(lines, 21)
        self.assertEqual(sloc, 7)

if __name__ == '__main__':
    unittest.main()
