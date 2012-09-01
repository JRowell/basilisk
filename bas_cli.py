#
# This file was generated using xslt from its XML file
#
# Copyright 2008, Associated Universities Inc., Washington DC
#
import sys
import os
import casac
import string
import time
import inspect
import gc
import numpy
from odict import odict
from taskmanager import tm
from task_bas import bas
from task_bas import casalog

class bas_cli_:
    __name__ = "bas"
    __async__ = {}
    rkey = None
    i_am_a_casapy_task = None
    # The existence of the i_am_a_casapy_task attribute allows help()
    # (and other) to treat casapy tasks as a special case.

    def __init__(self) :
       self.__bases__ = (bas_cli_,)
       self.__doc__ = self.__call__.__doc__

       self.parameters={'target':None, 'fluxcal':None, 'phasecal':None, 'fringefinder':None, 'bpcal':None, 'catlist':None, 'FLAG_INT':None, 'FLAG_BATCH':None, 'FLAG_DEBUG':None, 'FLAG_SILENT':None, 'FLAG_LOG':None, 'converts':None, 'StageSelection':None, 'confpath':None, 'conffile':None, 'inpath':None, 'inext':None, 'outpath':None, 'outprefix':None, 'logpath':None, 'logfile':None, 'comment':None, 'timeformat':None, 'prompt':None,  'async':None}


    def result(self, key=None):
	    #### here we will scan the task-ids in __async__
	    #### and add any that have completed...
	    if key is not None and self.__async__.has_key(key) and self.__async__[key] is not None:
	       ret = tm.retrieve(self.__async__[key])
	       if ret['state'] == "done" :
	          self.__async__[key] = None
	       elif ret['state'] == 'crashed' :
		  self.__async__[key] = None
	       return ret
	    return None


    def __call__(self, target=None, fluxcal=None, phasecal=None, fringefinder=None, bpcal=None, catlist=None, FLAG_INT=None, FLAG_BATCH=None, FLAG_DEBUG=None, FLAG_SILENT=None, FLAG_LOG=None, converts=None, StageSelection=None, confpath=None, conffile=None, inpath=None, inext=None, outpath=None, outprefix=None, logpath=None, logfile=None, comment=None, timeformat=None, prompt=None,  async=None):

        """CASA Pipeline.
        """
	if not hasattr(self, "__globals__") or self.__globals__ == None :
           self.__globals__=sys._getframe(len(inspect.stack())-1).f_globals
        self.__globals__['__last_task'] = 'bas'
        self.__globals__['taskname'] = 'bas'
        ###
        self.__globals__['update_params'](func=self.__globals__['taskname'],printtext=False,ipython_globals=self.__globals__)
        ###
        ###
        #Handle globals or user over-ride of arguments
        #
	function_signature_defaults=dict(zip(self.__call__.func_code.co_varnames,self.__call__.func_defaults))
	useLocalDefaults = False

        for item in function_signature_defaults.iteritems():
                key,val = item
                keyVal = eval(key)
                if (keyVal == None):
                        #user hasn't set it - use global/default
                        pass
                else:
                        #user has set it - use over-ride
			if (key != 'self') :
			   useLocalDefaults = True

	myparams = {}
	if useLocalDefaults :
	   for item in function_signature_defaults.iteritems():
	       key,val = item
	       keyVal = eval(key)
	       exec('myparams[key] = keyVal')
	       self.parameters[key] = keyVal
	       if (keyVal == None):
	           exec('myparams[key] = '+ key + ' = self.itsdefault(key)')
		   keyVal = eval(key)
		   if(type(keyVal) == dict) :
                      if len(keyVal) > 0 :
		         exec('myparams[key] = ' + key + ' = keyVal[len(keyVal)-1][\'value\']')
		      else :
		         exec('myparams[key] = ' + key + ' = {}')

	else :
            async = self.parameters['async']
            myparams['target'] = target = self.parameters['target']
            myparams['fluxcal'] = fluxcal = self.parameters['fluxcal']
            myparams['phasecal'] = phasecal = self.parameters['phasecal']
            myparams['fringefinder'] = fringefinder = self.parameters['fringefinder']
            myparams['bpcal'] = bpcal = self.parameters['bpcal']
            myparams['catlist'] = catlist = self.parameters['catlist']
            myparams['FLAG_INT'] = FLAG_INT = self.parameters['FLAG_INT']
            myparams['FLAG_BATCH'] = FLAG_BATCH = self.parameters['FLAG_BATCH']
            myparams['FLAG_DEBUG'] = FLAG_DEBUG = self.parameters['FLAG_DEBUG']
            myparams['FLAG_SILENT'] = FLAG_SILENT = self.parameters['FLAG_SILENT']
            myparams['FLAG_LOG'] = FLAG_LOG = self.parameters['FLAG_LOG']
            myparams['converts'] = converts = self.parameters['converts']
            myparams['StageSelection'] = StageSelection = self.parameters['StageSelection']
            myparams['confpath'] = confpath = self.parameters['confpath']
            myparams['conffile'] = conffile = self.parameters['conffile']
            myparams['inpath'] = inpath = self.parameters['inpath']
            myparams['inext'] = inext = self.parameters['inext']
            myparams['outpath'] = outpath = self.parameters['outpath']
            myparams['outprefix'] = outprefix = self.parameters['outprefix']
            myparams['logpath'] = logpath = self.parameters['logpath']
            myparams['logfile'] = logfile = self.parameters['logfile']
            myparams['comment'] = comment = self.parameters['comment']
            myparams['timeformat'] = timeformat = self.parameters['timeformat']
            myparams['prompt'] = prompt = self.parameters['prompt']


	result = None

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
        if not trec.has_key('bas') or not casac.cu.verify(mytmp, trec['bas']) :
	    return False

	try :
          saveinputs = self.__globals__['saveinputs']
          saveinputs('bas', 'bas.last', myparams, self.__globals__)
          if async :
	    count = 0
	    keybase =  time.strftime("%y%m%d.%H%M%S")
	    key = keybase + "_" + str(count)
	    while self.__async__.has_key(key) :
	       count += 1
	       key = keybase + "_" + str(count)
            result = tm.execute('bas', target, fluxcal, phasecal, fringefinder, bpcal, catlist, FLAG_INT, FLAG_BATCH, FLAG_DEBUG, FLAG_SILENT, FLAG_LOG, converts, StageSelection, confpath, conffile, inpath, inext, outpath, outprefix, logpath, logfile, comment, timeformat, prompt)
	    print "Use: "
	    print "      tm.retrieve(return_value) # to retrieve the status"
	    print 
	    self.rkey = key
	    self.__async__[key] = result
          else :
              tname = 'bas'
              spaces = ' '*(18-len(tname))
              casalog.post('')
              casalog.post('##########################################')
              casalog.post('##### Begin Task: ' + tname + spaces + ' #####')
              casalog.post('')
              result = bas(target, fluxcal, phasecal, fringefinder, bpcal, catlist, FLAG_INT, FLAG_BATCH, FLAG_DEBUG, FLAG_SILENT, FLAG_LOG, converts, StageSelection, confpath, conffile, inpath, inext, outpath, outprefix, logpath, logfile, comment, timeformat, prompt)
              casalog.post('')
              casalog.post('##### End Task: ' + tname + '  ' + spaces + ' #####')
              casalog.post('##########################################')

	except Exception, instance:
          if(self.__globals__.has_key('__rethrow_casa_exceptions') and self.__globals__['__rethrow_casa_exceptions']) :
             raise
          else :
             print '**** Error **** ',instance

        gc.collect()
        return result
#
#
#
    def paramgui(self, useGlobals=True, ipython_globals=None):
        """
        Opens a parameter GUI for this task.  If useGlobals is true, then any relevant global parameter settings are used.
        """
        import paramgui
	if not hasattr(self, "__globals__") or self.__globals__ == None :
           self.__globals__=sys._getframe(len(inspect.stack())-1).f_globals

        if useGlobals:
	    if ipython_globals == None:
                myf=self.__globals__
            else:
                myf=ipython_globals

            paramgui.setGlobals(myf)
        else:
            paramgui.setGlobals({})

        paramgui.runTask('bas', myf['_ip'])
        paramgui.setGlobals({})

#
#
#
    def defaults(self, param=None, ipython_globals=None, paramvalue=None, subparam=None):
	if not hasattr(self, "__globals__") or self.__globals__ == None :
           self.__globals__=sys._getframe(len(inspect.stack())-1).f_globals
        if ipython_globals == None:
            myf=self.__globals__
        else:
            myf=ipython_globals

        a = odict()
        a['target']  = ''
        a['fluxcal']  = ''
        a['phasecal']  = ''
        a['fringefinder']  = ''
        a['bpcal']  = ''
        a['catlist']  = 'ALL'
        a['FLAG_INT']  = 'False'
        a['FLAG_BATCH']  = 'False'
        a['FLAG_DEBUG']  = 'False'
        a['FLAG_SILENT']  = 'False'
        a['FLAG_LOG']  = 'True'
        a['converts']  = ''
        a['StageSelection']  = ''
        a['confpath']  = './'
        a['conffile']  = 'default.cfg'
        a['inpath']  = './'
        a['inext']  = ''
        a['outpath']  = './'
        a['outprefix']  = 'output'
        a['logpath']  = './'
        a['logfile']  = 'default.log'
        a['comment']  = ''
        a['timeformat']  = '%Y-%m-%d %H:%m:%S'
        a['prompt']  = ''

        a['async']=False

### This function sets the default values but also will return the list of
### parameters or the default value of a given parameter
        if(param == None):
                myf['__set_default_parameters'](a)
        elif(param == 'paramkeys'):
                return a.keys()
        else:
            if(paramvalue==None and subparam==None):
               if(a.has_key(param)):
                  return a[param]
               else:
                  return self.itsdefault(param)
            else:
               retval=a[param]
               if(type(a[param])==dict):
                  for k in range(len(a[param])):
                     valornotval='value'
                     if(a[param][k].has_key('notvalue')):
                        valornotval='notvalue'
                     if((a[param][k][valornotval])==paramvalue):
                        retval=a[param][k].copy()
                        retval.pop(valornotval)
                        if(subparam != None):
                           if(retval.has_key(subparam)):
                              retval=retval[subparam]
                           else:
                              retval=self.itsdefault(subparam)
		     else:
                        retval=self.itsdefault(subparam)
               return retval


#
#
    def check_params(self, param=None, value=None, ipython_globals=None):
      if ipython_globals == None:
          myf=self.__globals__
      else:
          myf=ipython_globals
#      print 'param:', param, 'value:', value
      try :
         if str(type(value)) != "<type 'instance'>" :
            value0 = value
            value = myf['cu'].expandparam(param, value)
            matchtype = False
            if(type(value) == numpy.ndarray):
               if(type(value) == type(value0)):
                  myf[param] = value.tolist()
               else:
                  #print 'value:', value, 'value0:', value0
                  #print 'type(value):', type(value), 'type(value0):', type(value0)
                  myf[param] = value0
                  if type(value0) != list :
                     matchtype = True
            else :
               myf[param] = value
            value = myf['cu'].verifyparam({param:value})
            if matchtype:
               value = False
      except Exception, instance:
         #ignore the exception and just return it unchecked
         myf[param] = value
      return value
#
#
    def description(self, key='bas', subkey=None):
        desc={'bas': 'CASA Pipeline.',
               'target': 'Name of target source.',
               'fluxcal': 'Name of flux calibration source.',
               'phasecal': 'Name of phase calibration source.',
               'fringefinder': 'Name of the fringefinder source.',
               'bpcal': 'Name of the bandpass calibration source.',
               'catlist': 'Comma-separated list of .ms files to use.',
               'FLAG_INT': 'Run in batch mode.',
               'FLAG_BATCH': 'Run in batch mode.',
               'FLAG_DEBUG': 'Enable debugging messages.',
               'FLAG_SILENT': 'Suppress all console output.',
               'FLAG_LOG': 'Enable logging to file.',
               'converts': 'A list of files to convert to .ms files.',
               'StageSelection': 'Comma-separated list of stages to use.',
               'confpath': 'Absolute path to the config file.',
               'conffile': 'Name of the config file.',
               'inpath': 'Absolute path for the input data directory.',
               'inext': 'File extension of input data files.',
               'outpath': 'Absolute path of the output data files.',
               'outprefix': 'Filename prefix for the output data files.',
               'logpath': 'Absolute path of the log file.',
               'logfile': 'Name for the log file.',
               'comment': 'Meaningful comment to help distinguish each run.',
               'timeformat': 'Format of the log file and console timestamps.',
               'prompt': 'Add a prompt string after the log file and console timestamps.',

               'async': 'If true the taskname must be started using bas(...)'
              }

        if(desc.has_key(key)) :
           return desc[key]

    def itsdefault(self, paramname) :
        a = {}
        a['target']  = ''
        a['fluxcal']  = ''
        a['phasecal']  = ''
        a['fringefinder']  = ''
        a['bpcal']  = ''
        a['catlist']  = 'ALL'
        a['FLAG_INT']  = 'False'
        a['FLAG_BATCH']  = 'False'
        a['FLAG_DEBUG']  = 'False'
        a['FLAG_SILENT']  = 'False'
        a['FLAG_LOG']  = 'True'
        a['converts']  = ''
        a['StageSelection']  = ''
        a['confpath']  = './'
        a['conffile']  = 'default.cfg'
        a['inpath']  = './'
        a['inext']  = ''
        a['outpath']  = './'
        a['outprefix']  = 'output'
        a['logpath']  = './'
        a['logfile']  = 'default.log'
        a['comment']  = ''
        a['timeformat']  = '%Y-%m-%d %H:%m:%S'
        a['prompt']  = ''

        #a = sys._getframe(len(inspect.stack())-1).f_globals

        if a.has_key(paramname) :
	      return a[paramname]
bas_cli = bas_cli_()
