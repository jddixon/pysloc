#!/usr/bin/python3

# testCssComments.py

import os, sys, unittest

from argparse   import ArgumentParser, Namespace
from pysloc     import __version__, __version_date__
from pysloc     import countLinesInDir, countLinesJava

class TestCssComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
   
    def testNameToFuncMap(self):
        testFile = './commentsForCss'
        lines, sloc = countLinesJava(testFile, self.options, 'css')
        self.assertEqual(lines, 304)
        self.assertEqual(sloc,  154)

if __name__ == '__main__':
    unittest.main()



