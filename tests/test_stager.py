#! /usr/bin/env python

import unittest
import pipeline


class test_stager(unittest.TestCase):
    """Test the Stager class"""

    def setUp(self):
        self.TestStager = pipeline.Stager()
        self.TestStager.settings["stages"] = ['a', 'b']

    def test_VerifyStages_invalid(self):
        """pipeline.Stager._VerifyStages() -- Raises SystemExit exception on bad choice?"""
        self.TestStager.settings["StageSelection"] = 'c'
        self.assertRaises(SystemExit, self.TestStager._VerifyStages)

if __name__ == '__main__':
    unittest.main()
