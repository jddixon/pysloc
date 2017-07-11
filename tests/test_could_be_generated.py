#!/usr/bin/env python3
# testCouldBeGenerated.py

""" Test line counter for 'could be generated' files. """

import os
import unittest

from argparse import Namespace
from pysloc import MapHolder


class TestCouldBeGenerated(unittest.TestCase):
    """ Test line counter for 'could be generated' files. """

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False
        self.map_holder = MapHolder()

    def tearDown(self):
        pass

    def expect_zero_counts(self, file_name, lang):
        """ Verify test file returns zero counts. """

        self.assertTrue(os.path.exists(file_name))
        counter = self.map_holder.get_counter(lang, True)
        self.assertNotEqual(counter, None)

        loc_, sloc_ = counter(file_name, self.options, lang)
        self.assertEqual(loc_, 0)
        self.assertEqual(sloc_, 0)

    def test_zero_if_generated(self):
        """ Verify test files return zero counts. """
        self.expect_zero_counts('tests/couldBeGenerated.pb-c.h', 'c')
        self.expect_zero_counts('tests/couldBeGenerated.pb-c.c', 'c')
        self.expect_zero_counts('tests/couldBeGenerated.pb.cpp', 'cpp')
        self.expect_zero_counts('tests/couldBeGenerated.pb.h', 'cpp')
        self.expect_zero_counts('tests/couldBeGenerated.pb.go', 'go')
        self.expect_zero_counts('tests/couldBeGenerated_pb2.py', 'py')
        self.expect_zero_counts('tests/couldBeGeneratedProtos.java', 'java')


if __name__ == '__main__':
    unittest.main()
