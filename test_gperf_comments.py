#!/usr/bin/env python3
# testGperfComments.py

""" Test that line counters work correctly for Gperf. """

import unittest
from argparse import Namespace

from pysloc import (GPERF_RE, count_lines_gperf, MapHolder)


class TestGperfComments(unittest.TestCase):
    """ Test that line counters work correctly for Gperf. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_first_line_pat(self):
        """ Verify that the first line pattern matcher works correctly. """

        bad_line = '/* ANSI-C code produced by gperf version N.N.N */'
        map_ = GPERF_RE.match(bad_line)
        self.assertEqual(map_, None)

        good_line = '/* ANSI-C code produced by gperf version 1.2.3 */'
        map_ = GPERF_RE.match(good_line)
        self.assertNotEqual(map_, None)
        sloc_ = map_.group(0)
        self.assertTrue(sloc_.startswith('/* ANSI-C'))

    def test_name_to_func_map(self):
        """ Verify that the Gperf counters work correctly on known file. """

        test_file = './commentsForGperf'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_gperf(test_file, options, 'gperf')
        self.assertEqual(lines, 5)
        self.assertEqual(sloc, 2)


if __name__ == '__main__':
    unittest.main()
