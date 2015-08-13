#!/usr/bin/python3

# testUncommentJava.py

import os, sys, unittest

from argparse   import ArgumentParser, Namespace
from pysloc     import __version__, __version_date__
from pysloc     import uncommentJava

class TestUncommentJava (unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
   
    def testUncommentJava(self):
        line = ''
        code, inComment = uncommentJava(line, True)
        self.assertEqual(code, '')
        self.assertEqual(inComment, True)

        code, inComment = uncommentJava(line, False)
        self.assertEqual(code, '')
        self.assertEqual(inComment, False)

        line = '/**/'

        code, inComment = uncommentJava(line, False)
        self.assertEqual(code, '')
        self.assertEqual(inComment, False)
        
        line = '/*'

        code, inComment = uncommentJava(line, False)
        self.assertEqual(code, '')
        self.assertEqual(inComment, True)
        
        line = '*/'

        code, inComment = uncommentJava(line, True)
        self.assertEqual(code, '')
        self.assertEqual(inComment, False)

        line = 'a/* */b/**/c'

        code, inComment = uncommentJava(line, False)
        self.assertEqual(code, 'abc')
        self.assertEqual(inComment, False)

        line = '//'

        code, inComment = uncommentJava(line, False)
        self.assertEqual(code, '')
        self.assertEqual(inComment, False)
        
        line = '/* abc //'

        code, inComment = uncommentJava(line, False)
        self.assertEqual(code, '')
        self.assertEqual(inComment, True)
        
        line = 'abc // def '

        code, inComment = uncommentJava(line, False)
        self.assertEqual(code, 'abc ')
        self.assertEqual(inComment, False)
        
if __name__ == '__main__':
    unittest.main()



