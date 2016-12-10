#!/usr/bin/env python3
# testHaskellComments.py

""" Test line counter for the Haskell programmig language. """

import unittest
from argparse import Namespace
from pysloc import count_lines_double_dash, MapHolder


class TestHaskellComments(unittest.TestCase):
    """ Test line counter for the Haskell programmig language. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        """ Verify line counts returned from known Haskell file are correct. """
        test_file = './commentsForHaskell'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_double_dash(test_file, options, 'occ')
        self.assertEqual(lines, 27)
        self.assertEqual(sloc, 10)

if __name__ == '__main__':
    unittest.main()
