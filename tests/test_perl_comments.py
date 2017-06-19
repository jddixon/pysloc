#!/usr/bin/env python3
# testPerlComments.py

""" Test functioning of line counters for Perl. """

import unittest
from argparse import Namespace

from pysloc import count_lines_perl, MapHolder


class TestPerlComments(unittest.TestCase):
    """ Test functioning of line counters for Perl. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_perl_comments(self):
        """ Verify that line counts for a known Perl file are correct. """

        test_file = './commentsForPerl'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = count_lines_perl(test_file, options, 'perl')
        self.assertEqual(lines, 39)
        self.assertEqual(sloc, 7)


if __name__ == '__main__':
    unittest.main()
