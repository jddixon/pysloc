#!/usr/bin/env python3
# testCppComments.py

""" Test counting lines in cpp files. """
import unittest
from argparse import Namespace
from pysloc import count_lines_cpp


class TestCppComments(unittest.TestCase):
    """ Test counting lines in cpp files. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        """ Verify line counts returned from known cpp file are correct. """
        test_file = './commentsForCpp'
        lines, sloc = count_lines_cpp(test_file, self.options, 'cpp')
        self.assertEqual(lines, 152)
        self.assertEqual(sloc, 33)


if __name__ == '__main__':
    unittest.main()
