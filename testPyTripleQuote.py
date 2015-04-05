#!/usr/bin/python3

# testPyTripleQuote.py

import os, sys, unittest
from argparse   import Namespace

from pysloc     import __version__, __version_date__
from pysloc     import countLinesInDir, countLinesPython

class TestPyTripleQuote (unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
   
    def testNameToFuncMap(self):
        testFile = './pyTripleTester'
        options = Namespace()
        options.already = set()
        options.exRE    = None
        options.verbose = False

        lines, sloc = countLinesPython(testFile, options)
        self.assertEqual(lines, 30)
        self.assertEqual(sloc, 13)

if __name__ == '__main__':
    unittest.main()



