#! /usr/bin/env python

import unittest
from stages import importing
from pipeline import Settings


class test_stage_importing(unittest.TestCase):
    """Test the 'importing' stage"""

    def setUp(self):
        self.TestImporting = importing.importing()
        self.TestImporting.settings = Settings()

    def test_AddSettings(self):
        """stages.Importing._AddSettings() -- Extra settings added correctly?"""
        self.TestImporting._AddSettings()
        self.assertTrue('fluxcal' in self.TestImporting.settings)

if __name__ == '__main__':
    unittest.main()
