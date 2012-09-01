#! /usr/bin/env python

import unittest
import pipeline


class test_quitter(unittest.TestCase):
    """Test the Quitter class"""

    def setUp(self):
        self.TestQuitter = pipeline.Quitter()
        self.TestQuitter.settings['logpath'] = '.'
        self.TestQuitter.settings['logfile'] = 'test.log'
        self.TestQuitter.settings['MsgTheme'] = 1
        self.TestPipeline = pipeline.Pipeline()
        self.TestPipeline._InitLog()

    def test_start(self):
        """pipeline.Quitter.start() -- Throws SystemExit exception?"""
        self.assertRaises(SystemExit, self.TestQuitter.start, 0)

if __name__ == '__main__':
    unittest.main()
