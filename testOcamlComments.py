#!/usr/bin/python3

# testOcamlComments.py

import os, sys, unittest

from argparse   import ArgumentParser, Namespace
from pysloc     import __version__, __version_date__
from pysloc     import countLinesInDir, countLinesOcaml

class TestOcamlComments (unittest.TestCase):

    def setUp(self):
        self.options = Namespace()
        self.options.already = set()
        self.options.verbose = False
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
   
    def testNameToFuncMap(self):
        testFile = './commentsForOcaml'
        lines, sloc = countLinesOcaml(testFile, self.options)
        self.assertEqual(lines, 30)
        self.assertEqual(sloc,   9)

if __name__ == '__main__':
    unittest.main()



