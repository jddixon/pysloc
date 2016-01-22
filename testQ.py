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

    #################################################################
    # TEST FILE NAMES beginning with 'yy' should exist in the test
    # directory; those beginning with 'zz' should not exist.
    #################################################################

    def testExt2Lang(self):
        """ exhaustive test of mapping extension to short lang name """

        # expect failure
        self.assertEqual(self.q.ext2Lang(None),    None)
        self.assertEqual(self.q.ext2Lang(''),      None)
        self.assertEqual(self.q.ext2Lang('foo'),   None)

        # expect success
        self.assertEqual(self.q.ext2Lang('C'),    'cpp')
        self.assertEqual(self.q.ext2Lang('cc'),   'cpp')
        self.assertEqual(self.q.ext2Lang('cpp'),  'cpp')
        self.assertEqual(self.q.ext2Lang('c++'),  'cpp')
        self.assertEqual(self.q.ext2Lang('cxx'),  'cpp')
        self.assertEqual(self.q.ext2Lang('h'),    'c')
        self.assertEqual(self.q.ext2Lang('hh'),   'cpp')
        self.assertEqual(self.q.ext2Lang('hpp'),  'cpp')

        self.assertEqual(self.q.ext2Lang('css'),  'css')
        self.assertEqual(self.q.ext2Lang('go'),   'go')
        self.assertEqual(self.q.ext2Lang('gperf'),'gperf')
        self.assertEqual(self.q.ext2Lang('hs'),   'hs')
        self.assertEqual(self.q.ext2Lang('html'), 'html')
        self.assertEqual(self.q.ext2Lang('java'), 'java')
        self.assertEqual(self.q.ext2Lang('js'),   'js')
        self.assertEqual(self.q.ext2Lang('md'),   'md')
        self.assertEqual(self.q.ext2Lang('occ'),  'occ')
        self.assertEqual(self.q.ext2Lang('proto'),'proto')
        self.assertEqual(self.q.ext2Lang('py'),   'py')
        self.assertEqual(self.q.ext2Lang('R'),    'R')      # short name 
        self.assertEqual(self.q.ext2Lang('r'),    'R')      # short name 
        self.assertEqual(self.q.ext2Lang('scala'),'scala')
        self.assertEqual(self.q.ext2Lang('sh'),   'sh')
        self.assertEqual(self.q.ext2Lang('sno'),  'sno')

    def testIrregularExt2Lang(self):
        qCpp = Q('cpp')
        self.assertEqual(qCpp.ext2Lang('h'),    'cpp')

        qOcc = Q('occ')
        self.assertEqual(qOcc.ext2Lang('inc'),  'occ')

    def testGetCounter(self):
        # expect failure if unknown lang and not a command line argument
        self.assertEqual(self.q.getCounter(None,False), None)
        self.assertEqual(self.q.getCounter('',False),   None)
        self.assertEqual(self.q.getCounter('foo',False),None)
       
        # on the command line we are more generous
        self.assertEqual(self.q.getCounter(None,True),  countLinesNotSharp)
        self.assertEqual(self.q.getCounter('',True),    countLinesNotSharp)
        self.assertEqual(self.q.getCounter('foo',True), countLinesNotSharp)
        
        # where the language is known we should always succeed
        # ... whether this is a command line argument
        self.assertEqual(self.q.getCounter('hs',True),    countLinesDoubleDash)
        self.assertEqual(self.q.getCounter('proto',True), countLinesProtobuf)
        self.assertEqual(self.q.getCounter('sno',True),   countLinesSnobol)
       
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
        self.assertEqual(self.q.getLongName('hs'),   'haskell')
        self.assertEqual(self.q.getLongName('html'), 'html')
        self.assertEqual(self.q.getLongName('java'), 'java')
        self.assertEqual(self.q.getLongName('md'),   'markdown')
        self.assertEqual(self.q.getLongName('occ'),  'Occam')
        self.assertEqual(self.q.getLongName('proto'),'proto')
        self.assertEqual(self.q.getLongName('re2c'), 're2c')
        self.assertEqual(self.q.getLongName('scala'),'scala')
        self.assertEqual(self.q.getLongName('sno'),  'snobol4')

    def testGuessLangFromFileName(self):
        # expect failure --------------------------------------------
        lang,isTest = self.q.guessLang('./', None, isCLIArg=True)
        self.assertEqual(lang, None)
        self.assertEqual(isTest, False)

        lang,isTest = self.q.guessLang('./',  '', isCLIArg=True)
        self.assertEqual(lang, None)
        self.assertEqual(isTest, False)
       
        # not recognized but on command line, so use generic counter
        lang,isTest = self.q.guessLang('./',  'yyFoo', isCLIArg=True)
        self.assertEqual(lang, 'gen')
        self.assertEqual(isTest, False)

        # if not recognized and not on command line, fail -----------
        lang,isTest = self.q.guessLang('./',  'yyFoo', isCLIArg=False)
        self.assertEqual(lang, None)
        self.assertEqual(isTest, False)
        
        lang,isTest = self.q.guessLang('./',  'go', isCLIArg=False)
        self.assertEqual(lang, None)
        self.assertEqual(isTest, False)
        
        lang,isTest = self.q.guessLang('./',  'py', isCLIArg=False)
        self.assertEqual(lang, None)
        self.assertEqual(isTest, False)

        # no extension, not on command line -------------------------
        lang,isTest = self.q.guessLang('./',  'joego', isCLIArg=False)
        self.assertEqual(lang, None)
        self.assertEqual(isTest, False)

        lang,isTest = self.q.guessLang('./',  'py', isCLIArg=False)
        self.assertEqual(lang, None)
        self.assertEqual(isTest, False)

        # if known language should always get language --------------
        lang,isTest = self.q.guessLang('./',  'yyFoo.go', isCLIArg=True)
        self.assertEqual(lang, 'go')
        self.assertEqual(isTest, False)
        lang,isTest = self.q.guessLang('./',  'yyFoo.go', isCLIArg=False)
        self.assertEqual(lang, 'go')
        self.assertEqual(isTest, False)
        
        lang,isTest = self.q.guessLang('./',  'yyFoo_test.go', isCLIArg=True)
        self.assertEqual(lang, 'go')
        self.assertEqual(isTest, True)
        lang,isTest = self.q.guessLang('./',  'yyFoo_test.go', isCLIArg=False)
        self.assertEqual(lang, 'go')
        self.assertEqual(isTest, True)
        
        lang,isTest = self.q.guessLang('./',  'yyFoo.occ', isCLIArg=True)
        self.assertEqual(lang, 'occ')
        self.assertEqual(isTest, False)
        lang,isTest = self.q.guessLang('./',  'yyFoo.occ', isCLIArg=False)
        self.assertEqual(lang, 'occ')
        self.assertEqual(isTest, False)
       
        lang,isTest = self.q.guessLang('./',  'yyFoo.py', isCLIArg=True)
        self.assertEqual(lang, 'py')
        self.assertEqual(isTest, False)
        lang,isTest = self.q.guessLang('./',  'yyFoo.py', isCLIArg=False)
        self.assertEqual(lang, 'py')
        self.assertEqual(isTest, False)

        lang,isTest = self.q.guessLang('./',  'testFoo.py', isCLIArg=True)
        self.assertEqual(lang, 'py')
        self.assertEqual(isTest, True)
        lang,isTest = self.q.guessLang('./',  'testFoo.py', isCLIArg=False)
        self.assertEqual(lang, 'py')
        self.assertEqual(isTest, True)

        lang,isTest = self.q.guessLang('./',  'yyFoo.sno', isCLIArg=True)
        self.assertEqual(lang, 'sno')
        self.assertEqual(isTest, False)
        lang,isTest = self.q.guessLang('./',  'yyFoo.sno', isCLIArg=False)
        self.assertEqual(lang, 'sno')
        self.assertEqual(isTest, False)

        # DON'T KNOW TEST PATTERN FOR SNOB
    def testNonCodeExt(self):
        # expect failure
        self.assertEqual(self.q.nonCodeExt(None),       False)
        self.assertEqual(self.q.nonCodeExt(''),         False)
        self.assertEqual(self.q.nonCodeExt('yyFoo'),      False)
        # expect success
        self.assertEqual(self.q.nonCodeExt('jar'),      True)
        self.assertEqual(self.q.nonCodeExt('pyc'),      True)

    def testNotCodeFile(self):
        # expect failure
        self.assertEqual(self.q.notCodeFile(None),              False)
        self.assertEqual(self.q.notCodeFile(''),                False)
        self.assertEqual(self.q.notCodeFile('yyFoo'),           False)
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


