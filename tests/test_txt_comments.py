#!/usr/bin/env python3
# testTextComments.py

"""
Test line counters for simple text files.

There aren't any comments in plain text files.  What we do is count
all lines which aren't empty and don't consist solely of white space.
"""

import unittest
from argparse import Namespace

from pysloc import count_lines_txt, MapHolder


class TestTxtComments(unittest.TestCase):
    """ Test line counters for simple text files. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify the line counts return for a known text file are correct. """

        test_file = 'tests/commentsForTxt'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_txt(test_file, options, 'txt')
        self.assertEqual(lines, 30)
        self.assertEqual(sloc, 20)


if __name__ == '__main__':
    unittest.main()
