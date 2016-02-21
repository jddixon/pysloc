#!/usr/bin/python3

# testPerlComments.py 
#
import os, sys, unittest
from argparse   import Namespace

from pysloc     import __version__, __version_date__
from pysloc     import countLinesInDir, countLinesPerl, Q

class TestPerlComments (unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
   
    def testPerlComments(self):
        testFile = './commentsForPerl'
        options = Namespace()
        options.already = set()
        options.exRE    = None
        options.q       = Q()
        options.verbose = False

        # XXX possible error reading file, possible errors parsing data

        lines, sloc = countLinesPerl(testFile, options, 'perl')
        self.assertEqual(lines, 39)
        self.assertEqual(sloc,   7)

if __name__ == '__main__':
    unittest.main()

