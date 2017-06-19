#!/usr/bin/env python3

# testUncommentHtml.py

import os
import sys
import unittest

from argparse import ArgumentParser, Namespace
from pysloc import __version__, __version_date__
from pysloc import uncommentHtml


class TestUncommentHtml (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testUncommentHtml(self):
        line = ''
        code, inComment = uncommentHtml(line, True)
        self.assertEqual(code, '')
        self.assertEqual(inComment, True)

        code, inComment = uncommentHtml(line, False)
        self.assertEqual(code, '')
        self.assertEqual(inComment, False)

        line = '<!---->'

        code, inComment = uncommentHtml(line, False)
        self.assertEqual(code, '')
        self.assertEqual(inComment, False)

        line = '<!--'

        code, inComment = uncommentHtml(line, False)
        self.assertEqual(code, '')
        self.assertEqual(inComment, True)

        line = '-->'

        code, inComment = uncommentHtml(line, True)
        self.assertEqual(code, '')
        self.assertEqual(inComment, False)

        line = 'a<!-- -->b<!---->c'

        code, inComment = uncommentHtml(line, False)
        self.assertEqual(code, 'abc')
        self.assertEqual(inComment, False)


if __name__ == '__main__':
    unittest.main()
