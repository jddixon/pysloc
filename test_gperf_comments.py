#!/usr/bin/env python3

# testGperfComments.py

import os
import sys
import unittest
from argparse import Namespace

from pysloc import (__version__, __version_date__,
                    GPERF_RE,
                    count_lines_in_dir, count_lines_gperf,
                    MapHolder)


class TestGperfComments (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_first_line_pat(self):

        bad_line = '/* ANSI-C code produced by gperf version N.N.N */'
        map_ = GPERF_RE.match(bad_line)
        self.assertEqual(map_, None)

        good_line = '/* ANSI-C code produced by gperf version 1.2.3 */'
        map_ = GPERF_RE.match(good_line)
        self.assertNotEqual(map_, None)
        sloc_ = map_.group(0)
        self.assertTrue(sloc_.startswith('/* ANSI-C'))

    def test_name_to_func_map(self):
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
