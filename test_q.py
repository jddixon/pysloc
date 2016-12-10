#!/usr/bin/env python3
# testQ.py

"""
Tests the operation of the Q class, which knows about counters.
"""

import os
import sys
import unittest
from argparse import Namespace

from pysloc import(MapHolder,
                   count_lines_double_dash, count_lines_fortran, count_lines_java_style,
                   count_lines_not_sharp, count_lines_perl, count_lines_protobuf,
                   count_lines_python, count_lines_snobol, count_lines_tex,
                   count_lines_txt)


class TestQ(unittest.TestCase):

    def setUp(self):
        self.map_holder = MapHolder()

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    #################################################################
    # TEST FILE NAMES beginning with 'yy' should exist in the test
    # directory; those beginning with 'zz' should not exist.
    #################################################################

    def test_ext2lang(self):
        """ exhaustive test of mapping extension to short lang name """

        # expect failure
        self.assertEqual(self.map_holder.ext2lang(None), None)
        self.assertEqual(self.map_holder.ext2lang(''), None)
        self.assertEqual(self.map_holder.ext2lang('foo'), None)

        # expect success
        self.assertEqual(self.map_holder.ext2lang('C'), 'cpp')
        self.assertEqual(self.map_holder.ext2lang('cc'), 'cpp')
        self.assertEqual(self.map_holder.ext2lang('cpp'), 'cpp')
        self.assertEqual(self.map_holder.ext2lang('c++'), 'cpp')
        self.assertEqual(self.map_holder.ext2lang('cxx'), 'cpp')
        self.assertEqual(self.map_holder.ext2lang('counter_'), 'file_name_')
        self.assertEqual(self.map_holder.ext2lang('hh'), 'cpp')
        self.assertEqual(self.map_holder.ext2lang('hpp'), 'cpp')

        self.assertEqual(self.map_holder.ext2lang('adb'), 'ada')
        self.assertEqual(self.map_holder.ext2lang('ads'), 'ada')
        self.assertEqual(self.map_holder.ext2lang('aug'), 'augeas')
        self.assertEqual(self.map_holder.ext2lang('awk'), 'awk')
        self.assertEqual(self.map_holder.ext2lang('css'), 'css')
        self.assertEqual(self.map_holder.ext2lang('flattened'), 'for')
        self.assertEqual(self.map_holder.ext2lang('f90'), 'f90+')
        self.assertEqual(self.map_holder.ext2lang('f95'), 'f90+')
        self.assertEqual(self.map_holder.ext2lang('f03'), 'f90+')
        self.assertEqual(self.map_holder.ext2lang('f08'), 'f90+')
        self.assertEqual(self.map_holder.ext2lang('f15'), 'f90+')
        self.assertEqual(self.map_holder.ext2lang('for'), 'for')
        self.assertEqual(self.map_holder.ext2lang('go'), 'go')
        self.assertEqual(self.map_holder.ext2lang('gperf'), 'gperf')
        self.assertEqual(self.map_holder.ext2lang('hs'), 'hs')
        self.assertEqual(self.map_holder.ext2lang('html'), 'html')
        self.assertEqual(self.map_holder.ext2lang('json'), 'json')
        self.assertEqual(self.map_holder.ext2lang('java'), 'java')
        self.assertEqual(self.map_holder.ext2lang('js'), 'js')
        self.assertEqual(self.map_holder.ext2lang('loc_'), 'lex')
        self.assertEqual(self.map_holder.ext2lang('lisp'), 'lisp')
        self.assertEqual(self.map_holder.ext2lang('m4'), 'm4')
        self.assertEqual(self.map_holder.ext2lang('md'), 'md')
        self.assertEqual(self.map_holder.ext2lang('occ'), 'occ')
        self.assertEqual(self.map_holder.ext2lang('proto'), 'proto')
        self.assertEqual(self.map_holder.ext2lang('pl'), 'perl')
        self.assertEqual(self.map_holder.ext2lang('pm'), 'perl')
        self.assertEqual(self.map_holder.ext2lang('pxd'), 'cython')
        self.assertEqual(self.map_holder.ext2lang('py'), 'py')
        self.assertEqual(self.map_holder.ext2lang('pyx'), 'cython')
        self.assertEqual(self.map_holder.ext2lang('R'), 'R')      # short name
        self.assertEqual(self.map_holder.ext2lang('r'), 'R')      # short name
        self.assertEqual(self.map_holder.ext2lang('scala'), 'scala')
        self.assertEqual(self.map_holder.ext2lang('sh'), 'sh')
        self.assertEqual(self.map_holder.ext2lang('sno'), 'sno')
        self.assertEqual(self.map_holder.ext2lang('tex'), 'tex')
        self.assertEqual(self.map_holder.ext2lang('y'), 'yacc')
        self.assertEqual(self.map_holder.ext2lang('yaml'), 'yaml')

    def test_irregular_ext2lang(self):
        cpp_holder = MapHolder('cpp')
        self.assertEqual(cpp_holder.ext2lang('counter_'), 'cpp')

        occ_holder = MapHolder('occ')
        self.assertEqual(occ_holder.ext2lang('inc'), 'occ')

    def test_get_counter(self):
        # expect failure if unknown lang and not a command line argument
        self.assertEqual(self.map_holder.get_counter(None, False), None)
        self.assertEqual(self.map_holder.get_counter('', False), None)
        self.assertEqual(self.map_holder.get_counter('foo', False), None)

        # on the command line we are more generous
        self.assertEqual(
            self.map_holder.get_counter(
                None, True), count_lines_not_sharp)
        self.assertEqual(
            self.map_holder.get_counter(
                '', True), count_lines_not_sharp)
        self.assertEqual(
            self.map_holder.get_counter(
                'foo', True), count_lines_not_sharp)

        # where the language is known we should always succeed
        # ... whether this is a command line argument
        self.assertEqual(
            self.map_holder.get_counter(
                'ada', True), count_lines_double_dash)
        self.assertEqual(
            self.map_holder.get_counter(
                'awk', True), count_lines_not_sharp)
        self.assertEqual(
            self.map_holder.get_counter(
                'cython',
                True),
            count_lines_python)
        self.assertEqual(
            self.map_holder.get_counter(
                'for', True), count_lines_fortran)
        self.assertEqual(
            self.map_holder.get_counter(
                'hs', True), count_lines_double_dash)
        self.assertEqual(
            self.map_holder.get_counter(
                'json', True), count_lines_txt)
        self.assertEqual(
            self.map_holder.get_counter(
                'lex', True), count_lines_java_style)
        self.assertEqual(
            self.map_holder.get_counter(
                'm4', True), count_lines_not_sharp)
        self.assertEqual(
            self.map_holder.get_counter(
                'occ', True), count_lines_double_dash)
        self.assertEqual(
            self.map_holder.get_counter(
                'perl', True), count_lines_perl)
        self.assertEqual(
            self.map_holder.get_counter(
                'proto',
                True),
            count_lines_protobuf)
        self.assertEqual(
            self.map_holder.get_counter(
                'sno', True), count_lines_snobol)
        self.assertEqual(
            self.map_holder.get_counter(
                'tex', True), count_lines_tex)
        self.assertEqual(
            self.map_holder.get_counter(
                'txt', True), count_lines_txt)
        self.assertEqual(
            self.map_holder.get_counter(
                'yacc', True), count_lines_java_style)
        self.assertEqual(
            self.map_holder.get_counter(
                'yaml', True), count_lines_not_sharp)

        # ... or not
        self.assertEqual(
            self.map_holder.get_counter(
                'py', False), count_lines_python)
        self.assertEqual(
            self.map_holder.get_counter(
                'sno', False), count_lines_snobol)

    def test_get_long_name(self):
        """ sh is omitted """

        # expect failure
        self.assertEqual(self.map_holder.get_long_nme(None), None)
        self.assertEqual(self.map_holder.get_long_nme(''), None)
        self.assertEqual(self.map_holder.get_long_nme('foo'), None)

        # expect success
        self.assertEqual(self.map_holder.get_long_nme('ada'), 'Ada')
        self.assertEqual(self.map_holder.get_long_nme('aug'), 'augeas')
        self.assertEqual(self.map_holder.get_long_nme('awk'), 'awk')
        self.assertEqual(self.map_holder.get_long_nme('cython'), 'cython')
        self.assertEqual(self.map_holder.get_long_nme('for'), 'FORTRAN')
        self.assertEqual(self.map_holder.get_long_nme('gen'), 'generic')
        self.assertEqual(self.map_holder.get_long_nme('go'), 'golang')
        self.assertEqual(self.map_holder.get_long_nme('hs'), 'haskell')
        self.assertEqual(self.map_holder.get_long_nme('html'), 'html')
        self.assertEqual(self.map_holder.get_long_nme('java'), 'java')
        self.assertEqual(self.map_holder.get_long_nme('json'), 'json')
        self.assertEqual(self.map_holder.get_long_nme('m4'), 'm4')
        self.assertEqual(self.map_holder.get_long_nme('md'), 'markdown')
        self.assertEqual(self.map_holder.get_long_nme('objc'), 'Objective C')
        self.assertEqual(self.map_holder.get_long_nme('occ'), 'Occam')
        self.assertEqual(self.map_holder.get_long_nme('perl'), 'Perl')
        self.assertEqual(self.map_holder.get_long_nme('proto'), 'proto')
        self.assertEqual(self.map_holder.get_long_nme('re2c'), 're2c')
        self.assertEqual(self.map_holder.get_long_nme('scala'), 'scala')
        self.assertEqual(self.map_holder.get_long_nme('sno'), 'snobol4')
        self.assertEqual(self.map_holder.get_long_nme('tex'), 'TeX/LaTeX')
        self.assertEqual(self.map_holder.get_long_nme('yaml'), 'yaml')

    def test_guess_lang_from_filename(self):
        # expect failure --------------------------------------------
        lang, is_test = self.map_holder.guess_lang('./', None, is_cli_arg=True)
        self.assertEqual(lang, None)
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang('./', '', is_cli_arg=True)
        self.assertEqual(lang, None)
        self.assertEqual(is_test, False)

        # not recognized but on command line, so use generic counter
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo', is_cli_arg=True)
        self.assertEqual(lang, 'gen')
        self.assertEqual(is_test, False)

        # if not recognized and not on command line, fail -----------
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo', is_cli_arg=False)
        self.assertEqual(lang, None)
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang(
            './', 'go', is_cli_arg=False)
        self.assertEqual(lang, None)
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang(
            './', 'py', is_cli_arg=False)
        self.assertEqual(lang, None)
        self.assertEqual(is_test, False)

        # no extension, not on command line -------------------------
        lang, is_test = self.map_holder.guess_lang(
            './', 'joego', is_cli_arg=False)
        self.assertEqual(lang, None)
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang(
            './', 'py', is_cli_arg=False)
        self.assertEqual(lang, None)
        self.assertEqual(is_test, False)

        # if known language should always get language --------------
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.go', is_cli_arg=True)
        self.assertEqual(lang, 'go')
        self.assertEqual(is_test, False)
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.go', is_cli_arg=False)
        self.assertEqual(lang, 'go')
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo_test.go', is_cli_arg=True)
        self.assertEqual(lang, 'go')
        self.assertEqual(is_test, True)
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo_test.go', is_cli_arg=False)
        self.assertEqual(lang, 'go')
        self.assertEqual(is_test, True)

        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.l', is_cli_arg=True)
        self.assertEqual(lang, 'lex')
        self.assertEqual(is_test, False)
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.l', is_cli_arg=False)
        self.assertEqual(lang, 'lex')
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.occ', is_cli_arg=True)
        self.assertEqual(lang, 'occ')
        self.assertEqual(is_test, False)
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.occ', is_cli_arg=False)
        self.assertEqual(lang, 'occ')
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.py', is_cli_arg=True)
        self.assertEqual(lang, 'py')
        self.assertEqual(is_test, False)
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.py', is_cli_arg=False)
        self.assertEqual(lang, 'py')
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang(
            './', 'test_foo.py', is_cli_arg=True)
        self.assertEqual(lang, 'py')
        self.assertEqual(is_test, True)
        lang, is_test = self.map_holder.guess_lang(
            './', 'test_foo.py', is_cli_arg=False)
        self.assertEqual(lang, 'py')
        self.assertEqual(is_test, True)

        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.sno', is_cli_arg=True)
        self.assertEqual(lang, 'sno')
        self.assertEqual(is_test, False)
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.sno', is_cli_arg=False)
        self.assertEqual(lang, 'sno')
        self.assertEqual(is_test, False)

        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.y', is_cli_arg=True)
        self.assertEqual(lang, 'yacc')
        self.assertEqual(is_test, False)
        lang, is_test = self.map_holder.guess_lang(
            './', 'yy_foo.y', is_cli_arg=False)
        self.assertEqual(lang, 'yacc')
        self.assertEqual(is_test, False)

        # DON'T KNOW TEST PATTERN FOR SNOB
    def tets_non_code_ext(self):
        # expect failure
        self.assertEqual(self.map_holder.non_code_ext(None), False)
        self.assertEqual(self.map_holder.non_code_ext(''), False)
        self.assertEqual(self.map_holder.non_code_ext('yy_foo'), False)
        # expect success
        self.assertEqual(self.map_holder.non_code_ext('jar'), True)
        self.assertEqual(self.map_holder.non_code_ext('md'), True)
        self.assertEqual(self.map_holder.non_code_ext('pyc'), True)

    def test_not_code_file(self):
        # expect failure
        self.assertEqual(self.map_holder.non_code_file(None), False)
        self.assertEqual(self.map_holder.non_code_file(''), False)
        self.assertEqual(self.map_holder.non_code_file('yy_foo'), False)
        # expect success
        self.assertEqual(self.map_holder.non_code_file('__pycache__'), True)
        self.assertEqual(self.map_holder.non_code_file('AUTHORS'), True)
        self.assertEqual(self.map_holder.non_code_file('CONTRIBUTORS'), True)
        self.assertEqual(self.map_holder.non_code_file('COPYING'), True)
        self.assertEqual(self.map_holder.non_code_file(
            'COPYING.AUTOCONF.EXCEPTION'), True)
        self.assertEqual(self.map_holder.non_code_file('COPYING.GNUBL'), True)
        self.assertEqual(self.map_holder.non_code_file('COPYING.LIB'), True)
        self.assertEqual(self.map_holder.non_code_file('LICENSE'), True)
        self.assertEqual(self.map_holder.non_code_file('NEWS'), True)
        self.assertEqual(self.map_holder.non_code_file('PATENTS'), True)
        self.assertEqual(self.map_holder.non_code_file('README'), True)
        self.assertEqual(self.map_holder.non_code_file('TODO'), True)

if __name__ == '__main__':
    unittest.main()
