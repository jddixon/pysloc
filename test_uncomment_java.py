#!/usr/bin/env python3

# testUncommentJava.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import uncomment_java


class TestUncommentJava (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_uncomment_java(self):
        line = ''
        code, in_comment = uncomment_java(line, True)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, True)

        code, in_comment = uncomment_java(line, False)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, False)

        line = '/**/'

        code, in_comment = uncomment_java(line, False)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, False)

        line = '/*'

        code, in_comment = uncomment_java(line, False)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, True)

        line = '*/'

        code, in_comment = uncomment_java(line, True)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, False)

        line = 'a/* */b/**/c'

        code, in_comment = uncomment_java(line, False)
        self.assertEqual(code, 'abc')
        self.assertEqual(in_comment, False)

        line = '//'

        code, in_comment = uncomment_java(line, False)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, False)

        line = '/* abc //'

        code, in_comment = uncomment_java(line, False)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, True)

        line = 'abc // def '

        code, in_comment = uncomment_java(line, False)
        self.assertEqual(code, 'abc ')
        self.assertEqual(in_comment, False)

if __name__ == '__main__':
    unittest.main()
