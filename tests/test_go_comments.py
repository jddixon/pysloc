#!/usr/bin/env python3
# testGoComments.py

""" Test counters for the Go programming language. """

import unittest
from argparse import Namespace
from pysloc import count_lines_go


class TestGoComments(unittest.TestCase):
    """ Test counters for the Go programming language. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify line counts returned from known go file are correct. """
        test_file = './commentsForGo'
        lines, sloc = count_lines_go(test_file, self.options, 'go')
        self.assertEqual(lines, 21)
        self.assertEqual(sloc, 7)


if __name__ == '__main__':
    unittest.main()
