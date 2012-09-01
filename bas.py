#
# This file was generated using xslt from its XML file
#
# Copyright 2009, Associated Universities Inc., Washington DC
#
import sys
import os
import casac
import string
from taskinit import casalog
#from taskmanager import tm
import task_bas
def bas(target='', fluxcal='', phasecal='', fringefinder='', bpcal='', catlist='ALL', FLAG_INT='False', FLAG_BATCH='False', FLAG_DEBUG='False', FLAG_SILENT='False', FLAG_LOG='True', converts='', StageSelection='', confpath='./', conffile='default.cfg', inpath='./', inext='', outpath='./', outprefix='output', logpath='./', logfile='default.log', comment='', timeformat='%Y-%m-%d %H:%m:%S', prompt=''):

        """CASA Pipeline.
        """

#
#    The following is work around to avoid a bug with current python translation
#
        mytmp = {}

        mytmp['target'] = target
        mytmp['fluxcal'] = fluxcal
        mytmp['phasecal'] = phasecal
        mytmp['fringefinder'] = fringefinder
        mytmp['bpcal'] = bpcal
        mytmp['catlist'] = catlist
        mytmp['FLAG_INT'] = FLAG_INT
        mytmp['FLAG_BATCH'] = FLAG_BATCH
        mytmp['FLAG_DEBUG'] = FLAG_DEBUG
        mytmp['FLAG_SILENT'] = FLAG_SILENT
        mytmp['FLAG_LOG'] = FLAG_LOG
        mytmp['converts'] = converts
        mytmp['StageSelection'] = StageSelection
        mytmp['confpath'] = confpath
        mytmp['conffile'] = conffile
        mytmp['inpath'] = inpath
        mytmp['inext'] = inext
        mytmp['outpath'] = outpath
        mytmp['outprefix'] = outprefix
        mytmp['logpath'] = logpath
        mytmp['logfile'] = logfile
        mytmp['comment'] = comment
        mytmp['timeformat'] = timeformat
        mytmp['prompt'] = prompt
        pathname="file:///home/user/src/basilisk/"
        trec = casac.cu.torecord(pathname+'bas.xml')

        casalog.origin('bas')
        if trec.has_key('bas') and casac.cu.verify(mytmp, trec['bas']) :
	    result = task_bas.bas(target, fluxcal, phasecal, fringefinder, bpcal, catlist, FLAG_INT, FLAG_BATCH, FLAG_DEBUG, FLAG_SILENT, FLAG_LOG, converts, StageSelection, confpath, conffile, inpath, inext, outpath, outprefix, logpath, logfile, comment, timeformat, prompt)

	else :
	  result = False
        return result
