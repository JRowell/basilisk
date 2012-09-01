#! /usr/bin/env python

import unittest
import utils


class test_utils(unittest.TestCase):
    """Test the 'utils' module"""

    def test_RandomMsg(self):
        """utils.RandomMsg() -- Returns legal value?"""
        MsgList = ['a', 'b', 'c', 'd', 'e']
        ans = utils.RandomMsg(MsgList).strip('\n')
        self.assertTrue(ans in MsgList)

if __name__ == '__main__':
    unittest.main()
