#!/usr/bin/env ython

## CASA eMERLIN Data-Reduction Pipeline v0.3

# Python libraries
import os
import sys
import random
import getpass
import ConfigParser
import logging
import time
import datetime
import pkgutil
import pdb
from pprint import pprint

# Other libraries
import utils
import stages

# Instantiate the global logger.
log = logging.getLogger()


class Settings(dict):
    """Singleton settings class"""
    settings = {}

    def __getitem__(self, key):
        return self.settings[key]

    def __setitem__(self, key, item):
        self.settings[key] = item

    def __iter__(self):
        return iter(self.settings.keys())


class Quitter(object):
    """Singleton quitter class"""

    __name__ = "Quit"

    def __init__(self):
        log.debug(utils.blue + "Quitter.__init__()" + utils.normal)
        self.settings = Settings.settings

    def __CleanLog(self):
        """Remove colour strings from the log file"""
        log.debug(utils.blue + "Quitter.__CleanLog()" + utils.normal)
        path = self.settings["logpath"].rstrip("/") + "/" + self.settings["logfile"]
        os.system("cat " + path + " | sed 's/\x1b\[.[0123456789;]*m//g' > " + path)

    def __WriteConfig(self):
        """Save current settings to file."""
        log.debug(utils.blue + "Quitter.WriteConfig()" + utils.normal)
        pass

    def start(self, status=0):
        """Exit safely."""
        log.debug(utils.blue + "Quitter.start()" + utils.normal)
        self.__WriteConfig()
        self.__CleanLog()
        if status == 0:
            log.info("Task Completed without (apparent) errors.")
        for n in list(log.handlers):
            log.removeHandler(n)
        msg = utils.RandomMsg(utils.messages[int(self.settings["MsgTheme"])][0])
        print utils.red + msg + utils.normal
        sys.exit(status)


class Stager(object):
    """Singleton class for processing pipeline stages."""

    def __init__(self):
        """Initialize the stages using .py files in ./stages"""
        log.debug(utils.blue + "Stager.__init__()" + utils.normal)

        # Assign a settings object.
        self.settings = Settings.settings

        # Assign a quitter object.
        self.quitter = Quitter()

    def _PickStage(self):
        """Interactively select next stage to run."""
        log.debug(utils.blue + "Stager.__PickStage()" + utils.normal)
        keys = self.settings["stages"].keys()
        keys.sort()

        # Give the user a second chance if they make a mistake.
        while(True):
            log.info("Which stage shall I run next?")

            # key <---> mid
            for key in keys:
                sname = self.settings['stages'][key].__name__.split('.')[-1].split('_')[-1]
                print "[" + str(key) + "] " + sname
            ans = raw_input(self.settings["prompt"])

            if ans in self.settings["stages"]:
                self.settings["StageSelection"] = ans
                break
            else:
                log.warning(utils.purple + "Invalid stage selection '" +
                            str(ans) + "'." + utils.normal)

        log.info("---------------------------------------")

    def _VerifyStages(self):
        """Verify stage selection."""
        log.debug(utils.blue + "Stager._VerifyStages()" + utils.normal)
        log.info("Verifying stage selection...")
        FLAG_ERROR = False
        for stage in self.settings["StageSelection"]:
            if stage in self.settings["stages"]:
                sname = self.settings["stages"][stage].__name__.split('.')[-1].split('_')[-1]
                log.info("* stage '" + str(stage) + "' -> " + str(sname) +
                         " [" + utils.green + "OK" + utils.normal + "]")
            else:
                log.info("* stage '" + str(stage) + "' -> ? [" + utils.red
                         + "BAD" + utils.normal + "]")

        if FLAG_ERROR == True:
            log.error(utils.red + "Invalid stage selection '" + stage + "'." + utils.normal)
            log.info('Available stages are:')
            pprint(self.settings["stages"])
            self.quitter.start(1)
        log.info("---------------------------------------")

    def _RunStage(self, stage):
        """Run stage."""
        log.debug(utils.blue + 'Stager._RunStage()' + utils.normal)
        log.debug(utils.blue + 'stage = ' + str(stage) + utils.normal)

        # Load in the current stage.
        sname = self.settings['stages'][stage].__name__.split('.')[-1].split('_')[-1]
        log.debug(utils.blue + "sname = " + str(sname) + utils.normal)

        # If not running interactively then we know how many stages will be running.
        # Why not help the user keep track of where we're up to?
        if self.settings['FLAG_INT'] in utils.negwords:
            self.settings['StageCount'] = len(self.settings['StageSelection'])
            log.info(utils.underline + 'STARTING STAGE ' + str(self.settings['StageCounter']) +
                     ' OF ' + str(self.settings['StageCount']) + utils.normal)
        else:
            log.info(utils.underline + "STARTING STAGE '" + str(sname) + "'" + utils.normal)

        # Start the clock!
        StartTime = time.time()
        log.debug(utils.blue + '300 - StartTime = ' + str(StartTime) + utils.normal)
        log.debug(utils.blue + '301 - stage = ' + str(self.settings["stages"][stage])
                  + utils.normal)

        # Create an instance of a stage class
        current_stage = self.settings['stages'][stage]()

        # Assign supplemental members
        current_stage.settings = self.settings
        current_stage.quitter = self.quitter

        # Execute!
        status = current_stage.start()

        # If stage was aborted/skipped part of the way through then print msg.
        if status == "1":
            log.warning(utils.purple + "Stage aborted by user." + utils.normal)

        # Stop the clock!
        EndTime = time.time()
        log.debug(utils.blue + "400 - EndTime = " + str(EndTime) + utils.normal)

        # Work out how long the stage took, then tell the user.
        TotalTime = EndTime - StartTime
        log.debug(utils.blue + "450 - TotalTime = " + str(TotalTime) + utils.normal)
        NiceTime = datetime.timedelta(seconds=TotalTime)
        log.info("STAGE COMPLETED IN " + str(NiceTime))

        self.settings['StageCounter'] += 1
        log.info("---------------------------------------")

    def start(self):
        """Load p stages"""
        log.debug(utils.blue + "Stager.start()" + utils.normal)

        # Get stages from './stages' directory.
        self.settings["stages"] = {'0': Quitter}

        package = stages
        prefix = package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            stage_module = __import__(modname, fromlist="dummy")
            stage_class = getattr(stage_module, stage_module.__name__.split('.')[-1])
            self.settings['stages'][str(self.settings['mid'])] = stage_class
            self.settings['mid'] += 1

        if self.settings["FLAG_INT"] in utils.poswords:
            self.settings["StageSelection"] = []

        # While loop facilitates interactive mode
        # but is escaped when running in other modes.
        while(True):

            # If we're running interactively the the user needs to tell me what to do.
            # A handy list of #s and stages should help them decide!
            if self.settings["FLAG_INT"] in utils.poswords:
                self._PickStage()

            # Verify the user's choice of stages and give some feedback.
            self._VerifyStages()

            # Run stages in StageSelection and time how long each takes.
            for stage in self.settings["StageSelection"]:
                self._RunStage(stage)

            # If we're not running interactively then it's time to exit.
            if self.settings["FLAG_INT"] in utils.negwords:
                return


class Pipeline(object):
    """
    Pipline class is the workhorse of the Basilisk system.

    Before you can execute an instance of the Pipeline class,
    a minimal set of parameters must be specified.

    piplines can execute in several modes:

        1) Interactive - prompts
        2) Batch - no prompts
        3) Debug - verbose output
        4) Silent - no output
        5) Logging - writes message to file

    The default mode is 'interactive'. To enable other modes,
    set the relevant flags.
    """

    def __init__(self):
        """Initialize the pipeline object"""
        self.settings = Settings.settings
        self.quitter = Quitter()
        self.stager = Stager()

        pipeline_settings = {
                             "allfiles": {},
                             "ms": {},
                             "nonms": {},
                             "converts": "",
                             "catlist": "",
                             "StageSelection": "",
                             "stages": {},
                             "StageCount": 0,  # No. stages in p.
                             "StageCounter": 1,  # Current stage
                             "mid": 1,  # Module (stage) IDs
                             "user": str(getpass.getuser()),
                             "host": str(os.uname()[1]),
                             "MsgTheme": random.choice([0, 1, 2, 3]),
                             "prompt": ">>> ",
                             "conffile": "",
                             "confpath": "",
                             "logfile": "",
                             "logpath": "",
                             "timeformat": "",
                             "comment": "",
                             "inpath": "",
                             "outpath": "",
                             "inext": "",
                             "outprefix": "",
                             "FLAG_INT": "",
                             "FLAG_BATCH": "",
                             "FLAG_DEBUG": "",
                             "FLAG_LOG": "",
                             "FLAG_SILENT": "",
                             "FLAG_DEPS": "True",
                             "dependencies": ["casapy", "ParselTongue"],
                             "sources": {},
                             "target": "",
                             "fluxcal": "",
                             "phasecal": "",
                             "fringefinder": "",
                             "bpcal": "",
                             "uid": 0,  # Unique (file) IDs
                             "sid": -1  # Source IDs
                            }

        # Add the pipeline settings to the global settings.
        self.settings.update(pipeline_settings)
        pdb.set_trace

    # MAIN ENTRY POINT!
    def start(self):
        """Master control sequence."""
        self._InitLog()        # Init. the logger.
        self._ReadConfig()     # Parse config file.
        self._ConfLog()        # Configure the logger.
        self._banner()         # Print banner.
        self._deps()           # Check dependencies.
        self.stager.start()
        self.quitter.start(0)
        # RETURN TO CASA! ->

    def set(self, dic):
        """Access function for configuring settings."""
        # Go through the input settings dictionary...
        for key in dic:
            # find all the settings which have been set...
            if dic[key] != "":
                if key in self.settings:
                    # assign the value of the setting.
                    self.settings[key] = dic[key]

    def set2(self, dic):
        """Access function for configuring settings."""
        log.info('Applying config...')
        # Go through the input settings dictionary...
        for key in dic:
            # find all the settings which have been set...
            if dic[key] != "":
                if key in self.settings:
                    # assign the value of the setting.
                    log.info("* '" + str(key) + "' [" + utils.green + "SET"
                             + utils.normal + "]")
                    self.settings[key] = dic[key]
                else:
                    log.info("* '" + str(key) + "' [" + utils.red + "UNKNOWN"
                             + utils.normal + "]")
            else:
                log.info("* '" + str(key) + "' [" + utils.red + "EMPTY"
                         + utils.normal + "]")
        log.info("---------------------------------------")

    def _ReadConfig(self):
        """Parse the batch-mode config file."""
        # Is interactive mode enabled?
        if self.settings["FLAG_INT"] in utils.poswords:
            return

        # Is batch mode enabled?
        if self.settings["FLAG_BATCH"] in utils.poswords:
            log.debug(utils.blue + "_ReadConfig()" + utils.normal)
            parser = ConfigParser.ConfigParser()

            # Distinguish between upper and lower case variable names.
            parser.optionxform = str

            conf = (self.settings["confpath"] + "/" +
                   self.settings["conffile"])
            conf = conf.replace('//', '/')

            # Open config file.
            try:
                f = open(conf)
            except IOError:
                log.error(utils.red + "Cannot read config file '" + conf +
                          "'." + utils.normal)
                self.quitter.start(1)

            # Parse config file.
            try:
                parser.readfp(f)
            except ConfigParser.MissingSectionHeaderError:
                log.error(utils.red + "Config file '" + conf +
                          "' contains no sections." + utils.normal)
                self.quitter.start(1)
            except ConfigParser.ParsingError:
                log.error(utils.red + "Unable to parse config file '" + conf +
                          "'." + utils.normal)
                self.quitter.start(1)
            except:
                log.error(utils.red +
                          "I'm having trouble reading your config file." +
                          utils.normal)
                self.quitter.start(1)

            # If running in a non-interactive mode we require a few essentials.
            # Check for essential settings.
            FLAG_BAD = False
            log.info("Checking '" + str(conf) + "' for essentials...")
            FLAG_BAD = self._ChkSetting(parser, 'inpath', ['NEG', ''])
            FLAG_BAD = self._ChkSetting(parser, 'catlist', ['NEG', ''])
            FLAG_BAD = self._ChkSetting(parser, 'StageSelection', ['NEG', ''])
            FLAG_BAD = self._ChkSetting(parser, 'target', ['NEG', ''])
            FLAG_BAD = self._ChkSetting(parser, 'fluxcal', ['NEG', ''])
            FLAG_BAD = self._ChkSetting(parser, 'phasecal', ['NEG', ''])
            FLAG_BAD = self._ChkSetting(parser, 'fringefinder', ['NEG', ''])
            FLAG_BAD = self._ChkSetting(parser, 'bpcal', ['NEG', ''])
            log.info("---------------------------------------")

            # Were any essentials reported missing or invalid?
            if FLAG_BAD == True:
                self.quitter.start(1)

            # Apply config.
            configDict = utils.GetConfigSection(parser, 'pipeline')
            self.set2(configDict)

        # Transform config file's comma-delimited strings into python lists.
        # Q. Why is this necessary?
        # A. I don't know how to implement list-type parameters in the CASA task
        # XML file. To get around this, the list-type parameters are registered
        # as string-type. A comma-delimited list is written to the string which
        # is then converted to python list here.
        self.settings["converts"] = self.settings["converts"].replace(' ', '').split(',')
        self.settings["catlist"] = self.settings["catlist"].replace(' ', '').split(',')
        self.settings["StageSelection"] = self.settings["StageSelection"].replace(' ', '').split(',')

    def _ChkSetting(self, parser, setting, valid):
        """Check config setting is on the list of valid settings."""
        section = 'pipeline'
        FLAG_BAD = False
        if parser.has_option(section, setting):
            val = parser.get(section, setting)
            if "NEG" in valid:
                if val in valid:
                    log.info('* ' + str(setting) + ' [' + utils.red + 'INVALID'
                             + utils.normal + ']')
                    FLAG_BAD = True
                else:
                    log.info('* ' + str(setting) + ' [' + utils.green + 'FOUND'
                             + utils.normal + ']')
            elif val not in valid:
                log.info('* ' + str(setting) + ' [' + utils.red + 'INVALID'
                         + utils.normal + ']')
                FLAG_BAD = True
        else:
            log.info('* ' + str(setting) + ' [' + utils.red + 'MISSING'
                     + utils.normal + ']')
            FLAG_BAD = True
        return FLAG_BAD

    def _InitLog(self):
        """Initialize the logger"""
        log.setLevel(logging.DEBUG)
        f = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%m:%S")
        h = logging.StreamHandler()
        h.setFormatter(f)
        h.setLevel(logging.INFO)
        log.addHandler(h)
        s = open('snake.txt', 'r')
        s.readline()
        for line in s:
            print(utils.green + line.rstrip('\n') + utils.normal)
        log.info("---------------------------------------")
        log.info("          ~ B A S I L I S K ~")
        log.info("---------------------------------------")

    def _ConfLog(self):
        """Reconfigure the logger"""
        # Apply user's preferences to the log format.
        f = logging.Formatter("%(asctime)s " + "[%(levelname)s] %(message)s",
                              self.settings["timeformat"])
        log.handlers[0].setFormatter(f)
        if self.settings["FLAG_DEBUG"] in utils.poswords:
            log.handlers[0].setLevel(logging.DEBUG)
            log.debug(utils.blue + "_ConfLog --> 'DEBUG' mode" + utils.normal)
        elif self.settings["FLAG_SILENT"] in utils.poswords:
            log.handlers[0].setLevel(logging.CRITICAL)
            log.debug(utils.blue + "_ConfLog --> 'SILENT/CRITICAL' mode" + utils.normal)
        else:
            log.handlers[0].setLevel(logging.INFO)
            log.debug(utils.blue + "_ConfLog --> 'INFO' mode" + utils.normal)

        # Shall we log to file?
        if self.settings["FLAG_LOG"] in utils.poswords:
            h_file = logging.FileHandler(self.settings["logpath"] +
                                         self.settings["logfile"])
            h_file.setFormatter(f)
            h_file.setLevel(logging.DEBUG)
            log.addHandler(h_file)

    def _banner(self):
        """Display the welcome message"""
        log.debug(utils.blue + "_banner()" + utils.normal)
        log.info("User: " + str(self.settings["user"]) + "@" +
                str(self.settings["host"]))
        log.info("Comment: " + str(self.settings["comment"]))
        log.info("Config file: '" + str(self.settings["conffile"]) + "'")
        log.info("Config path: '" + str(self.settings["confpath"]) + "'")
        log.info("Log file: '" + str(self.settings["logfile"]) + "'")
        log.info("Log path: '" + str(self.settings["logpath"]) + "'")
        log.info("Logging: " + str(self.settings["FLAG_LOG"]))
        log.info("Debugging: " + str(self.settings["FLAG_DEBUG"]))
        log.info("Silent: " + str(self.settings["FLAG_SILENT"]))
        log.info("Interactive mode: " + str(self.settings["FLAG_INT"]))
        log.info("Batch mode: " + str(self.settings["FLAG_BATCH"]))
        log.info("Input path: '" + str(self.settings["inpath"]) + "'")
        log.info("Input extension: '" + str(self.settings["inext"]) + "'")
        log.info("Output path: '" + str(self.settings["outpath"]) + "'")
        log.info("Output prefix: '" + str(self.settings["outprefix"]) + "'")
        s = 'Stage selection:'
        for stage in self.settings['StageSelection']:
            s += (' ' + str(stage) + ',')
        log.info(s.rstrip(','))
        log.info("---------------------------------------")

    def _deps(self):
        """Check that all essential dependencies."""
        log.debug(utils.blue + "_deps()." + utils.normal)
        log.info("Checking dependencies...")

        for dep in self.settings['dependencies']:
            if utils.FindProg(dep)[0]:
                log.info("* " + dep + " [" + utils.green + "FOUND" +
                         utils.normal + "]")
            else:
                log.info("* " + dep + " [" + utils.red + "NOT FOUND" +
                         utils.normal + "]")
                self.settings["FLAG_DEPS"] = "False"

        if self.settings["FLAG_DEPS"] in utils.negwords:
            log.warning(utils.yellow + "One or more dependencies are missing."
                        + utils.normal)

        log.info("---------------------------------------")

if __name__ == "__main__":

    try:
        p = Pipeline()
        p.start()
    except:
        log.error("Failed to intantiate the pipeline!")
