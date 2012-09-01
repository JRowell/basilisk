#! /usr/bin/env python

import unittest
import pipeline


class test_settings(unittest.TestCase):
    """Test the Settings class"""

    def setUp(self):
        self.TestSettings = pipeline.Settings()

    def test_AssignValToKey(self):
        """pipeline.Settings.settings[key] = value -- Works as expected?"""
        self.TestSettings['test'] = 'Hello'
        self.assertEquals(self.TestSettings['test'], 'Hello')

    def test_singleton(self):
        """pipeline.Settings -- Is a singleton?"""
        self.TestSettings2 = pipeline.Settings()
        self.TestSettings2['test'] = 'Goodbye'
        self.assertEquals(self.TestSettings['test'], 'Goodbye')

if __name__ == '__main__':
    unittest.main()
