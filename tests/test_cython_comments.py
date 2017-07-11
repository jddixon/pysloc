#!/usr/bin/env python3
# testCythonComments.py

""" Test counting lines in Cython files. """

import unittest
from argparse import Namespace
from pysloc import count_lines_python, MapHolder


class TestPyComments(unittest.TestCase):
    """ Test counting lines in Cython files. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pxd(self):
        """ Verify line counts returned by known .pxd file are correct. """
        test_file = 'tests/commentsForCython.pxd'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_python(test_file, options, 'pxd')
        self.assertEqual(lines, 53)
        self.assertEqual(sloc, 23)

    def test_pyx(self):
        """ Verify line counts returned by known .pyx file are correct. """
        test_file = 'tests/commentsForCython.pyx'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_python(test_file, options, 'pyx')
        self.assertEqual(lines, 86)
        self.assertEqual(sloc, 48)


if __name__ == '__main__':
    unittest.main()
