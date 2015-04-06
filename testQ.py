#!/usr/bin/python3

# testQ.py

import os, sys, unittest
from argparse   import Namespace

from pysloc     import *

class TestQ (unittest.TestCase):

    def setUp(self):
        self.q = Q()
    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testExt2Lang(self):
        """ exhaustive test of mapping extension to short lang name """

        # expect failure
        self.assertEqual(self.q.ext2Lang(None),    None)
        self.assertEqual(self.q.ext2Lang(''),      None)
        self.assertEqual(self.q.ext2Lang('foo'),   None)
        # expect success
        self.assertEqual(self.q.ext2Lang('go'),   'go')
        self.assertEqual(self.q.ext2Lang('html'), 'html')
        self.assertEqual(self.q.ext2Lang('java'), 'java')
        self.assertEqual(self.q.ext2Lang('md'),   'md')
        self.assertEqual(self.q.ext2Lang('py'),   'py')
        self.assertEqual(self.q.ext2Lang('sh'),   'sh')
        self.assertEqual(self.q.ext2Lang('sno'),  'sno')

    def testGetCounter(self):
        # expect failure if unknown lang and not a command line argument
        self.assertEqual(self.q.getCounter(None,False), None)
        self.assertEqual(self.q.getCounter('',False),   None)
        self.assertEqual(self.q.getCounter('foo',False),None)
       
        # on the command line we are more generous
        self.assertEqual(self.q.getCounter(None,True),  countLinesGeneric)
        self.assertEqual(self.q.getCounter('',True),    countLinesGeneric)
        self.assertEqual(self.q.getCounter('foo',True), countLinesGeneric)
        
        # where the language is known we should always succeed
        # ... whether this is a command line argument
        self.assertEqual(self.q.getCounter('py',True),  countLinesPython)
        self.assertEqual(self.q.getCounter('sno',True), countLinesSnobol)
       
        # ... or not
        self.assertEqual(self.q.getCounter('py',False), countLinesPython)
        self.assertEqual(self.q.getCounter('sno',False),countLinesSnobol)


    def testGetLongName(self):
        """ sh is omitted """

        # expect failure
        self.assertEqual(self.q.getLongName(None),    None)
        self.assertEqual(self.q.getLongName(''),      None)
        self.assertEqual(self.q.getLongName('foo'),   None)
        # expect success
        self.assertEqual(self.q.getLongName('gen'),  'generic')
        self.assertEqual(self.q.getLongName('go'),   'golang')
        self.assertEqual(self.q.getLongName('html'), 'html')
        self.assertEqual(self.q.getLongName('java'), 'java')
        self.assertEqual(self.q.getLongName('md'),   'markdown')
        self.assertEqual(self.q.getLongName('py'),   'python')
        self.assertEqual(self.q.getLongName('sno'),  'snobol4')

    def testNonCodeExt(self):
        # expect failure
        self.assertEqual(self.q.nonCodeExt(None),       False)
        self.assertEqual(self.q.nonCodeExt(''),         False)
        self.assertEqual(self.q.nonCodeExt('foo'),      False)
        # expect success
        self.assertEqual(self.q.nonCodeExt('jar'),      True)
        self.assertEqual(self.q.nonCodeExt('pyc'),      True)

    def testNotCodeFile(self):
        # expect failure
        self.assertEqual(self.q.notCodeFile(None),    False)
        self.assertEqual(self.q.notCodeFile(''),      False)
        self.assertEqual(self.q.notCodeFile('foo'),   False)
        # expect success
        self.assertEqual(self.q.notCodeFile('__pycache__'),     True)
        self.assertEqual(self.q.notCodeFile('AUTHORS'),         True)
        self.assertEqual(self.q.notCodeFile('CONTRIBUTORS'),    True)
        self.assertEqual(self.q.notCodeFile('COPYING'),         True)
        self.assertEqual(self.q.notCodeFile('COPYING.AUTOCONF.EXCEPTION'), True)
        self.assertEqual(self.q.notCodeFile('COPYING.GNUBL'),   True)
        self.assertEqual(self.q.notCodeFile('COPYING.LIB'),     True)
        self.assertEqual(self.q.notCodeFile('LICENSE'),         True)
        self.assertEqual(self.q.notCodeFile('NEWS'),            True)
        self.assertEqual(self.q.notCodeFile('PATENTS'),         True)
        self.assertEqual(self.q.notCodeFile('README'),          True)
        self.assertEqual(self.q.notCodeFile('TODO'),            True)

if __name__ == '__main__':
    unittest.main()


