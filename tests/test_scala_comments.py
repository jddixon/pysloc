#!/usr/bin/env python3
# testScalaComments.py

""" Test line counters for Scala. """

import unittest

from argparse import Namespace
from pysloc import count_lines_scala


class TestScalaComments(unittest.TestCase):
    """ Test line counters for Scala. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        """ Verify line counters return correct line counts for nown file."""
        test_file = './commentsForScala'
        lines, sloc = count_lines_scala(test_file, self.options, 'scala')
        self.assertEqual(lines, 48)
        self.assertEqual(sloc, 9)


if __name__ == '__main__':
    unittest.main()
