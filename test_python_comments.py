#!/usr/bin/env python3
# testPyComments.py

""" Test functioning of Python line counters. """

import unittest
from argparse import Namespace

from pysloc import count_lines_python, MapHolder


class TestPyComments(unittest.TestCase):
    """ Test functioning of Python line counters. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify that line counts for known python file are correct. """

        test_file = './commentsForPy'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_python(test_file, options, 'py')
        self.assertEqual(lines, 29)
        self.assertEqual(sloc, 13)


if __name__ == '__main__':
    unittest.main()
