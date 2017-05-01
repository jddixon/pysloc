#!/usr/bin/env python3
# testOctaveComments.py

""" Test line counters for Octave. """

import unittest

from argparse import Namespace
from pysloc import count_lines_occam


class TestOctaveComments(unittest.TestCase):
    """ Test line counters for Octave. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        """ Verify that line counts for a known Octave file are correct. """
        test_file = './commentsForOctave'
        lines, sloc = count_lines_occam(test_file, self.options, 'octave')
        self.assertEqual(lines, 79)
        self.assertEqual(sloc, 25)


if __name__ == '__main__':
    unittest.main()
