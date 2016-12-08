#!/usr/bin/env python3

# testUncommentHtml.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import uncomment_html


class TestUncommentHtml (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_uncomment_html(self):
        line = ''
        code, in_comment = uncomment_html(line, True)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, True)

        code, in_comment = uncomment_html(line, False)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, False)

        line = '<!---->'

        code, in_comment = uncomment_html(line, False)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, False)

        line = '<!--'

        code, in_comment = uncomment_html(line, False)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, True)

        line = '-->'

        code, in_comment = uncomment_html(line, True)
        self.assertEqual(code, '')
        self.assertEqual(in_comment, False)

        line = 'a<!-- -->b<!---->c'

        code, in_comment = uncomment_html(line, False)
        self.assertEqual(code, 'abc')
        self.assertEqual(in_comment, False)

if __name__ == '__main__':
    unittest.main()
