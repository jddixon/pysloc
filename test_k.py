#!/usr/bin/env python3
# testK.py

"""
Test the operation of the K class, which returns a counter for
a language.
"""

import unittest

from pysloc import CountHolder


class TestK(unittest.TestCase):

    def setUp(self):
        self.k__ = CountHolder()
        self.py_tot_loc = 0
        self.py_tot_sloc = 0
        self.py_tot_tloc = 0
        self.py_tot_sloc = 0

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def check_counts(self, lang, exp_loc, exp_sloc,
                     exp_test_loc, exp_test_sloc):
        self.assertEqual(self.k__ is not None, True)
        loc_, sloc_, test_loc, test_sloc = self.k__.get_counts(lang)
        self.assertEqual(loc_, exp_loc)
        self.assertEqual(sloc_, exp_sloc)
        self.assertEqual(test_loc, exp_test_loc)
        self.assertEqual(test_sloc, exp_test_sloc)

    def test_k(self):
        # we have a new K.  It should have nothing in it.
        loc_, sloc_, test_loc, test_sloc = self.k__.get_totals()
        self.assertEqual(loc_, 0)
        self.assertEqual(sloc_, 0)
        self.assertEqual(test_loc, 0)
        self.assertEqual(test_sloc, 0)

        self.check_counts('zz', 0, 0, 0, 0)    # not in map
        self.check_counts('py', 0, 0, 0, 0)    # not in map

        self.k__.add_counts('py', 7, 3)
        self.check_counts('py', 7, 3, 0, 0)
        self.k__.add_counts('py', 5, 2)
        self.check_counts('py', 12, 5, 0, 0)

        self.k__.add_test_counts('py', 8, 4)
        self.check_counts('py', 12, 5, 8, 4)
        self.k__.add_test_counts('py', 9, 3)
        self.check_counts('py', 12, 5, 17, 7)

        expected = "py:%d/%d T%.1f%%" % (12 + 17, 5 + 7, 700.0 / 12)
        # DEBUG
        #print("Expected: %s" % expected)
        # END
        self.assertEqual(self.k__.pretty_counts('py'), expected)

    def test_k_again(self):
        loc_, sloc_, test_loc, test_sloc = self.k__.get_totals()
        self.assertEqual(loc_, 0)
        self.assertEqual(sloc_, 0)
        self.assertEqual(test_loc, 0)
        self.assertEqual(test_sloc, 0)

        self.k__.add_counts('py', 7, 3)
        self.check_counts('py', 7, 3, 0, 0)
        self.k__.add_counts('py', 5, 2)
        self.check_counts('py', 12, 5, 0, 0)

        self.k__.add_test_counts('py', 8, 0)
        self.check_counts('py', 12, 5, 8, 0)
        self.k__.add_test_counts('py', 9, 0)
        self.check_counts('py', 12, 5, 17, 0)

        # no test source lines, so no test percentage
        expected = "py:%d/%d" % (12 + 17, 5)
        # DEBUG
        #print("Expected: %s" % expected)
        # END
        self.assertEqual(self.k__.pretty_counts('py'), expected)


if __name__ == '__main__':
    unittest.main()
