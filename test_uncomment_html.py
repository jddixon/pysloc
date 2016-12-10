#!/usr/bin/env python3
# testUncommentHtml.py

""" Test function for uncommenting HTML. """

import unittest

from argparse import Namespace
from pysloc import uncomment_html


class TestUncommentHtml(unittest.TestCase):
    """ Test function for uncommenting HTML. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_uncomment_html(self):
        """ Run uncomment logic on snippets of code, verify results. """

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
