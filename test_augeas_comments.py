#!/usr/bin/env python3
# testAugeasComments.py

""" Test counting lines in augeas files. """

import unittest
from argparse import Namespace
from pysloc import count_lines_augeas


class TestAugeasComments(unittest.TestCase):
    """ Test counting lines in augeas files. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Test counting lines in known test Augeas file. """

        test_file = './commentsForAugeas'
        lines, sloc = count_lines_augeas(test_file, self.options, 'ml')
        self.assertEqual(lines, 107)
        self.assertEqual(sloc, 45)

if __name__ == '__main__':
    unittest.main()
