#!/usr/bin/env python3
# testRMarkdownComments.py

""" Test line couters for R's version of Markdown. """

import unittest
from argparse import Namespace

from pysloc import count_lines_r_markdown, MapHolder


class TestRMarkdownComments(unittest.TestCase):
    """ Test line couters for R's version of Markdown. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name_to_func_map(self):
        """ Verify line counts for known file are as expected. """

        test_file = './commentsForRMarkdown'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        lines, sloc = count_lines_r_markdown(test_file, options, 'Rmd')
        self.assertEqual(lines, 114)
        self.assertEqual(sloc, 53)


if __name__ == '__main__':
    unittest.main()
