#!/usr/bin/env python3
# testUserGuide.py

""" Test XML counters on a user guide formatted in XML. """

import unittest
from argparse import Namespace

from pysloc import count_lines_xml, MapHolder


class TestUserGuide(unittest.TestCase):
    """ Test XML counters on a user guide formatted in XML. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_guide(self):
        """
        Verify that line counts returned for a manually counted
        XML User Guide are as expected.
        """
        test_file = 'tests/userguide.xml'
        options = Namespace()
        options.already = set()
        options.ex_re = None
        options.map_holder = MapHolder()
        options.verbose = False

        # possible error reading file, possible errors parsing data

        lines, sloc = count_lines_xml(test_file, options, 'xml')
        self.assertEqual(lines, 182)
        # 4 header lines, 13 other blank lines
        self.assertEqual(sloc, 165)


if __name__ == '__main__':
    unittest.main()
