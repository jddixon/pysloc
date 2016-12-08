#!/usr/bin/env python3

# testCouldBeGenerated.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import (__version__, __version_date__,
                    MapHolder)


class TestCouldBeGenerated (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False
        self.map_holder = MapHolder()

    def tearDown(self):
        pass

    # utility functions #############################################

    def expect_zero_counts(self, file_name, lang):

        self.assertTrue(os.path.exists(file_name))
        counter = self.map_holder.get_counter(lang, True)
        self.assertNotEqual(counter, None)

        loc_, sloc_ = counter(file_name, self.options, lang)
        self.assertEqual(loc_, 0)
        self.assertEqual(sloc_, 0)

    # actual unit tests #############################################

    def test_zero_if_generated(self):
        self.expect_zero_counts('couldBeGenerated.pb-c.c', 'file_name_')
        self.expect_zero_counts('couldBeGenerated.pb-c.h', 'file_name_')
        self.expect_zero_counts('couldBeGenerated.pb.cpp', 'cpp')
        self.expect_zero_counts('couldBeGenerated.pb.h', 'cpp')
        self.expect_zero_counts('couldBeGenerated.pb.go', 'go')
        self.expect_zero_counts('couldBeGenerated_pb2.py', 'py')
        self.expect_zero_counts('couldBeGeneratedProtos.java', 'java')

if __name__ == '__main__':
    unittest.main()
