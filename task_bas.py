#!/usr/bin/env python

# This file will become the 'basilisk'/'bas' task in casa.
# The pipeline class is implemented in a similar way to the
# in-built CASA toolkit implementations.
# Think of the pipeline class as an extension to the CASA toolkit.

import sys
from pipeline import Pipeline
from taskinit import *


def bas(target, fluxcal, phasecal, fringefinder, bpcal, catlist, FLAG_INT,
        FLAG_BATCH, FLAG_DEBUG, FLAG_SILENT, FLAG_LOG, converts,
        StageSelection, confpath, conffile, inpath, inext, outpath, outprefix,
        logpath, logfile, comment, timeformat, prompt):

    # Get all those parameters from above ^
    settings = locals()

    # Inform the CASA logger of what's happening.
    casalog.origin("bas")
    casalog.post("Output from this task is not appended to the CASA log.",
                 priority="INFO")

    # Make sure we can see all the files we need.
    obit_path = "/home/rowell/src/obit/python"
    parseltongue_path = "/usr/local/share/parseltongue/python"
    sys.path.append(obit_path)
    sys.path.append(parseltongue_path)

    # Do what we came here to do.
    p = Pipeline()
    p.set(settings)
    p.start()

    # Return the settings.
    s = p.settings
    return s
