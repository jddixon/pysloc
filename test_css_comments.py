#!/usr/bin/env python3
# testCssComments.py

""" Test counting lines in CSS files. """

import unittest
from argparse import Namespace
from pysloc import count_lines_java


class TestCssComments(unittest.TestCase):
    """ Test counting lines in CSS files. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        """ Verify correct line counts returned from known CSS file. """

        test_file = './commentsForCss'
        lines, sloc = count_lines_java(test_file, self.options, 'css')
        self.assertEqual(lines, 304)
        self.assertEqual(sloc, 154)


if __name__ == '__main__':
    unittest.main()
