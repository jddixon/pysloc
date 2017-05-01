#!/usr/bin/env python3
# testUncommentJava.py

""" Test uncomment function Java-like languages. """

import unittest

from pysloc import uncomment_java


class TestUncommentJava(unittest.TestCase):
    """ Test uncomment function Java-like languages. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_uncomment_java(self):
        """ Verify that uncommenting snippets of Java works correctly. """

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
