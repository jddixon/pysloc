#!/usr/bin/python3

# testK.py

import os, sys, unittest
from argparse   import Namespace

from pysloc     import *

class TestK (unittest.TestCase):

    def setUp(self):
        self.k = K()
        self.pyTotalL           = 0
        self.pyTotalS           = 0
        self.pyTotalTestLines   = 0
        self.pyTotalTestSource  = 0

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def checkCounts(self, lang, expL, expS, expTL, expTS):
        self.assertEqual( self.k != None, True)
        l, s, tl, ts = self.k.getCounts(lang)
        self.assertEqual(l,  expL)
        self.assertEqual(s,  expS)
        self.assertEqual(tl, expTL)
        self.assertEqual(ts, expTS)

    def testK(self):
        # we have a new K.  It should have nothing in it. 
        l, s, tl, ts = self.k.getTotals()
        self.assertEqual(l,  0)
        self.assertEqual(s,  0)
        self.assertEqual(tl, 0)
        self.assertEqual(ts, 0)
    
        self.checkCounts('zz', 0,0,0,0)    # not in map
        self.checkCounts('py', 0,0,0,0)    # not in map

        self.k.addCounts('py', 7,3)
        self.checkCounts('py', 7,3,0,0)
        self.k.addCounts('py', 5,2)
        self.checkCounts('py', 12,5,0,0)
        
        self.k.addTestCounts('py', 8,4)
        self.checkCounts('py', 12,5,8,4)
        self.k.addTestCounts('py', 9,3)
        self.checkCounts('py', 12,5,17,7)

        expected = "py:%d/%d T%.1f%%" % (12+17, 5+7, 700.0/12)
        # DEBUG
        #print("Expected: %s" % expected)
        # END
        self.assertEqual(self.k.prettyCounts('py'), expected)

    def testKAgain(self):
        l, s, tl, ts = self.k.getTotals()
        self.assertEqual(l,  0)
        self.assertEqual(s,  0)
        self.assertEqual(tl, 0)
        self.assertEqual(ts, 0)
    
        self.k.addCounts('py', 7,3)
        self.checkCounts('py', 7,3,0,0)
        self.k.addCounts('py', 5,2)
        self.checkCounts('py', 12,5,0,0)
        
        self.k.addTestCounts('py', 8,0)
        self.checkCounts('py', 12,5,8,0)
        self.k.addTestCounts('py', 9,0)
        self.checkCounts('py', 12,5,17,0)

        # no test source lines, so no test percentage
        expected = "py:%d/%d" % (12+17, 5)
        # DEBUG
        #print("Expected: %s" % expected)
        # END
        self.assertEqual(self.k.prettyCounts('py'), expected)


if __name__ == '__main__':
    unittest.main()


