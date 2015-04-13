#!/usr/bin/python3

# testGoComments.py

import os, sys, unittest

from argparse   import ArgumentParser, Namespace
from pysloc     import __version__, __version_date__
from pysloc     import countLinesInDir, countLinesGo

class TestGoComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
   
    def testNameToFuncMap(self):
        testFile = './commentsForGo'
        lines, sloc = countLinesGo(testFile, self.options, 'go')
        self.assertEqual(lines, 14)
        self.assertEqual(sloc,   4)

if __name__ == '__main__':
    unittest.main()



