#! /usr/bin/env python

import unittest
import pipeline


class test_pipeline(unittest.TestCase):
    """Test the Settings class"""

    def setUp(self):
        self.TestPipeline = pipeline.Pipeline()

    def test_set(self):
        """pipeline.set() -- Works as expected?"""
        TestDict = {'user': 'Tester'}
        self.TestPipeline.set(TestDict)
        self.assertEquals(self.TestPipeline.settings['user'], 'Tester')

if __name__ == '__main__':
    unittest.main()
