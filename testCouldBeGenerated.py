#!/usr/bin/python3

# testCouldBeGenerated.py

import os, sys, unittest

from argparse   import ArgumentParser, Namespace
from pysloc     import ( __version__, __version_date__,
                Q)
                
class TestCouldBeGenerated (unittest.TestCase):

    def setUp(self):
        self.options 	        = Namespace()
        self.options.already    = set()
        self.options.verbose    = False
        self.q       	        = Q()

    def tearDown(self):
        pass

    # utility functions #############################################
   
    def expectZeroCounts(self, fileName, lang):
        counter = self.q.getCounter(lang, True)
        self.assertNotEqual(counter, None)

        l, s = counter(fileName, self.options, lang)
        self.assertEqual(l,  0)
        self.assertEqual(s,  0)
            
    # actual unit tests #############################################
   
    def testZeroIfGenerated(self):
        self.expectZeroCounts('couldBeGenerated.pb-c.c',       'c')
        self.expectZeroCounts('couldBeGenerated.pb-c.h',       'c')
        self.expectZeroCounts('couldBeGenerated.pb.cpp',       'cpp')
        self.expectZeroCounts('couldBeGenerated.pb.h',         'cpp')
        self.expectZeroCounts('couldBeGenerated.pb.go',        'cpp')
        self.expectZeroCounts('couldBeGenerated_pb2.py',       'py')
        self.expectZeroCounts('couldBeGeneratedProtos.java',   'java')

if __name__ == '__main__':
    unittest.main()



