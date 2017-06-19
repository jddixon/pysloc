#!/usr/bin/env python3
# testProtobufComments.py

""" Verify that line counters for protobuf work correctly. """

import unittest
from argparse import Namespace

from pysloc import count_lines_protobuf, MapHolder


class TestProtobufComments(unittest.TestCase):
    """ Verify that line counters for protobuf work correctly. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_name_to_func_map(self):
        """ Verify that line counts are correct for a known protobuf file. """
        test_file = './commentsForProtobuf'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_protobuf(test_file, options, 'py')
        self.assertEqual(lines, 71)
        self.assertEqual(sloc, 46)


if __name__ == '__main__':
    unittest.main()
