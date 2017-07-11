#!/usr/bin/env python3
# testLispComments.py

""" Test line counters for LISP. """

import unittest

from argparse import Namespace
from pysloc import count_lines_lisp, MapHolder


class TestLispComments(unittest.TestCase):
    """ Test line counters for LISP. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_lisp_comments(self):
        """ Verify that line counts for a known LISP file are correct. """

        test_file = 'tests/commentsForLisp'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = count_lines_lisp(test_file, options, 'lisp')
        self.assertEqual(lines, 65)
        self.assertEqual(sloc, 38)


if __name__ == '__main__':
    unittest.main()
