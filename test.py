#! /usr/bin/env python

import unittest

from tests import test_utils
from tests import test_settings
from tests import test_quitter
from tests import test_stager
from tests import test_pipeline

#===============|IMPORT STAGE TEST MODULES|===============#
# 1. Import the test modules for your own stages HERE!
from tests import test_stage_importing

#=========================|END|===========================#


def run():

    # Create test 'loader'.
    loader = unittest.TestLoader()

    # Add tests for auxillary modules.
    suite = loader.loadTestsFromModule(test_utils)

    # Add tests for pipeline classes.
    suite.addTests(loader.loadTestsFromModule(test_settings))
    suite.addTests(loader.loadTestsFromModule(test_quitter))
    suite.addTests(loader.loadTestsFromModule(test_stager))
    suite.addTests(loader.loadTestsFromModule(test_pipeline))

    #===============|IMPORT STAGE TEST MODULES|===============#
    # 2. Load your test modules HERE!
    suite.addTests(loader.loadTestsFromModule(test_stage_importing))

    #=========================|END|===========================#

    # Create test 'runner'.
    runner = unittest.TextTestRunner(verbosity=2)

    # Launch tests.
    runner.run(suite)

if __name__ == '__main__':
    run()
