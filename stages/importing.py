# Python libraries
import logging
import os

# CASA libraries
from tasks import *
from taskinit import *

# My libraries
import utils

log = logging.getLogger()


class importing(object):

    def start(self):
        """Produce one big .ms file for us to play with."""
        log.debug(utils.blue + "importing.start()" + utils.normal)
        self._GetFiles()       # Get the input path and parse files within it.
        self._MakeMS()         # Convert non-.ms files to .ms.
        self._GenSourceDict()  # Create a dictionary of sources.
        self._PickSources()    # Allocate target and cal sources.
        self._cat()            # Concatenate .ms files listed in 'catlist'.
        self.FLAG_IMPORTED = True

    def _GetFiles(self):
        """Get the input path and parse files within it."""
        log.debug(utils.blue + "importing._GetFiles()" + utils.normal)

        # Interactive. Duplicate these next two blocks for outpath rq.
        if self.settings['FLAG_INT'] in utils.poswords:
            while True:
                log.info("In which directory are your data files located?:")
                ans = raw_input(self.settings["prompt"])
                if os.path.exists(ans):
                    self.settings["inpath"] = ans
                    break
                else:
                    log.warning(utils.yellow + "According to my records '" + str(ans) + "' doesn't exist!" + utils.normal)

        if self.settings['inpath'] == "":
            log.info("Using the current directory.")
            self.settings["inpath"] = "./"

        log.info("I'm going to look for data files in '" + self.settings["inpath"] + "'.")

        # Interactive mode only.
        if self.settings['FLAG_INT'] in utils.poswords:
            log.info("Would you like to filter the files by extension? (y/n):")
            ans = raw_input(self.settings["prompt"])
            if ans in utils.poswords:
                log.info("Which file extension do your data files use? (.ms):")
                self.settings['inext'] = raw_input(self.settings["prompt"])
            else:
                self.settings['inext'] = ""

        # Filtering messages.
        if self.settings['inext'] == "":
            log.info("All files are assumed to contain data.")
        else:
            log.info("All '" + self.settings['inext'] + "' files are assumed to contain data.")

        # Create dictionary of all files below the 'inpath' directory.
        for (path, dirs, files) in os.walk(self.settings["inpath"]):
            if path.endswith(".ms"):
                self.settings["allfiles"][self.settings['uid']] = {
                        'apath': path, 'ms': True, 'sources': []}
                self.settings['uid'] += 1
            elif ".ms" not in path:
                for f in files:
                    if f.endswith(self.settings['inext']):
                        log.debug(utils.blue + "[" + str(self.settings['uid']) + "] " +
                                  path + "/" + f + utils.normal)
                        self.settings["allfiles"][self.settings['uid']] = {
                                    'apath': path + "/" + f, 'ms': False,
                                    'sources': []}
                    self.settings['uid'] += 1

        # Create sub-dictionaries of ms and non-ms files.
        for id in self.settings["allfiles"]:
            if self.settings["allfiles"][id]['ms']:
                self.settings["ms"][id] = self.settings["allfiles"][id]
            else:
                self.settings["nonms"][id] = self.settings["allfiles"][id]

        # Tell us the good news.
        log.info("I found " + str(len(self.settings["ms"])) + " .ms files.")
        for id in self.settings["ms"]:
            log.info("[" + str(id) + "] " + self.settings["ms"][id]["apath"])

    def _MakeMS(self):
        """Convert non-.ms files to .ms files in the outpath directory"""
        log.debug(utils.blue + "importing._MakeMS()" + utils.normal)

        # Interactive mode only
        if self.settings["FLAG_INT"] in utils.poswords:
            if len(self.settings["nonms"]) > 0:
                log.debug(utils.blue + "I count " + str(len(self.settings["nonms"])) + " non-ms files." + utils.normal)
                self.settings["converts"] = []
                log.info("The following files are not .ms files:")
                for id in self.settings['nonms']:
                    log.info("[" + str(id) + "] " + self.settings["nonms"][id]['apath'])
                log.info("Use the file numbers to indicate which files (if any) should be converted to .ms files.")
                log.info("To indicate multiple files separate the file numbers with spaces.")
                log.info("E.g. To select file numbers 1, 7 and 12 enter '1 7 12' without quotes.")
                while True:
                    good = True
                    count = 0
                    log.info("Enter your selection now:")
                    list = raw_input(self.settings["prompt"]).split()
                    for item in list:
                        if int(item) not in self.settings["nonms"]:
                            good = False
                            count += 1
                    if good:
                        break
                    else:
                        log.warning(utils.yellow + str(count) + " of your choices is invalid." + utils.normal)
                #  TODO: remove duplicates
                if len(list) > 0:
                    log.info("The following files will be converted to .ms files:")
                    for id in list:
                        id = int(id)
                        convert = self.settings["nonms"][id]['apath']
                        log.info("[" + str(id) + "] " + convert)
                        self.settings["converts"].append(convert)

        # Is there anything to convert?
        if self.settings["converts"]:
            if self.settings["converts"][0] != '':
                log.debug(utils.blue + "I count " + str(len(self.settings["converts"]))
                        + " files to convert." + utils.normal)
                for convert in self.settings["converts"]:
                    self.settings['uid'] += 1
                    ipath = self.settings["inpath"]
                    opath = self.settings["outpath"]
                    filename = convert.split('/')[-1].split('.')[0]
                    convert = ipath.rstrip("/") + "/" + convert
                    converted = opath.rstrip("/") + "/" + filename + ".ms"
                    log.info("Converting: '" + convert + "' --> '" + converted + "'")

                    importfitsidi(fitsidifile=convert, vis=converted)  # CASA task

                    # Make new entries in 'allfiles' and 'ms'
                    self.settings["ms"][self.settings['uid']] = {
                            'apath': converted, 'ms': True, 'sources': []}
                    self.settings["allfiles"][self.settings['uid']] = {
                            'apath': converted, 'ms': True, 'sources': []}
            else:
                log.warning(utils.yellow + "No files will be converted to .ms format." + utils.normal)

    def _GetSources(self, ms):
        """Return a list of sources from a .ms file"""
        log.debug(utils.blue + "importing._GetSources(" + ms + ")" + utils.normal)
        sources = []
        a = mstool.create()
        openedms = a.open(ms)  # Returns 'True' if successful.
        log.debug(utils.blue + "Openedms = " + str(openedms) + utils.normal)
        for key in a.summary()["header"].keys():
            if "field_" in key:
                FieldName = a.summary()['header'][key]['name']
                sources.append(FieldName)
                log.debug(utils.blue + "FieldName = " + str(FieldName) + utils.normal)
        a.close()
        return sources

    def _GenSourceDict(self):
        """Generate a dictionary of sources and which .ms files they belong to."""
        log.debug(utils.blue + "importing._GetSources()" + utils.normal)

        # Do we have some measurement sets to look in?
        if len(self.settings["ms"]) > 0:
            log.info("Looking for sources in the .ms files...")

            # Go over each measurement set.
            for id in self.settings["ms"]:
                log.debug(utils.blue + "File ID = " + str(id) + utils.normal)
                ms = self.settings["ms"][id]["apath"]

                # Get a source list for the measurement set.
                sources = self._GetSources(ms)

                # Associate the sources with the file / measurement set
                log.debug(utils.blue + "001" + utils.normal)
                self.settings["allfiles"][id]["sources"] = sources

                log.debug(utils.blue + "002" + utils.normal)
                self.settings["ms"][id]["sources"] = sources
                found = False

                # Go over each source in the list.
                for source in sources:

                    # Do we know about any sources already?
                    log.debug(utils.blue + "003" + utils.normal)
                    if len(self.settings["sources"]) > 0:

                        # Yes. Is this source one of the ones we already know?
                        log.debug(utils.blue + "004" + utils.normal)
                        for sid in self.settings["sources"]:

                            log.debug(utils.blue + "005" + utils.normal)
                            if self.settings["sources"][sid]["name"] == source:
                                found = True

                                # Yes. Is this measurmenet set associated with the source already?
                                log.debug(utils.blue + "006" + utils.normal)
                                if ms not in self.settings["sources"][sid]["files"]:

                                    # No. Associate the measurment set with the source.
                                    log.debug(utils.blue + "007" + utils.normal)
                                    self.settings["sources"][sid]["files"].append(ms)

                    # No. Increment the global source id (sid) counter and make a new entry
                    # in the source dictionary.
                    if found == False:
                        self.settings['sid'] += 1
                        log.debug(utils.blue + "008" + utils.normal)
                        self.settings["sources"][self.settings['sid']] = {'name': source, 'roles': [], 'files': [ms]}

                log.info("[" + str(id) + "] " + str(ms) + " [" + utils.green + "DONE" + utils.normal + "]")

            # Print a list of source names from the sources dictionary.
            log.info("I found " + str(len(self.settings["sources"])) + " sources.")
            for id in self.settings["sources"]:
                log.info("[" + str(id) + "] " + self.settings["sources"][id]["name"])

        # No measurement sets found.
        else:
            log.error(utils.red + "It appears you have no measurement sets (.ms files)." + utils.normal)
            self.quitter.start(1)

    def _SetSourceRole(self, role):
        """Interactively set source role"""
        log.debug(utils.blue + "importing._SetSource()" + utils.normal)
        while True:
            log.info("Which source is the " + role + "?:")
            ans = raw_input(self.settings["prompt"])
            if len(ans.split()) > 1:
                log.warning(utils.yellow + "You may only select one source." + utils.normal)
            elif not ans:
                log.warning(utils.yellow + "You must choose a source from the source list." + utils.normal)
            elif not ans.isdigit():
                log.warning(utils.yellow + "You may only enter a source number." + utils.normal)
            elif int(ans) not in self.settings["sources"]:
                log.warning(utils.yellow + "'" + str(ans) + "' is not in the source list!" + utils.normal)
            elif "target" in self.settings["sources"][int(ans)]["roles"]:
                log.warning(utils.yellow + "This source has already been designated as the target source." + utils.normal)
            else:
                self.settings["sources"][int(ans)]["roles"].append(role)
                name = self.settings["sources"][int(ans)]["name"]
                log.info("The " + role + " source is '" +  name + "'.")

                # If the source appears in multiple files, which files do you want to use?
                if len(self.settings["sources"][int(ans)]["files"]) > 1:

                    # Print all appearances of the source.
                    log.info("This source appears in the following .ms files:")
                    appearances = []
                    for id in self.settings["ms"]:
                        if name in self.settings["ms"][id]["sources"]:
                            appearances.append(id)
                            log.info("[" + str(id) + "] " + self.settings["ms"][id]["apath"])

                    # Ask user if they want to use all of these files.
                    while True:
                        log.info("Would you like to include the data from all of these files? ([y]/n):")
                        ans2 = raw_input(self.settings["prompt"])

                        # If they do, then add all appearances to 'catlist' (if they aren't already present).
                        if ans2 in utils.poswords:
                            for appearance in appearances:
                                if str(appearance) not in self.settings["catlist"]:
                                    self.settings["catlist"].append(str(appearance))
                            break

                        # If they don't:
                        elif str(ans2) in utils.negwords:

                            # Let the user pick which files they want to use.
                            while True:
                                good = True
                                count = 0
                                log.info("Which files would you like to use?")
                                list = raw_input(self.settings["prompt"]).split()
                                for item in list:
                                    if int(item) not in appearances:
                                        good = False
                                        count += 1
                                if good:
                                    for item in list:
                                        if str(item) not in self.settings["catlist"]:
                                            self.settings["catlist"].append(str(item))
                                    break
                                else:
                                    log.warning(utils.yellow + str(count) + " of your choices is invalid." + utils.normal)
                            break

                        else:
                            log.warning(utils.yellow + "You may only enter 'y' or 'n'." + utils.normal)

                # If the source appears in just one file then add the file to 'catlist'.
                else:
                    for file in self.settings["sources"][int(ans)]["files"]:
                        if file not in self.settings["catlist"]:
                            self.settings["catlist"].append(file)
                break
        return self.settings["sources"][int(ans)]["name"]

    def _PickSources(self):
        """Allocate target and cal source roles"""
        log.debug(utils.blue + "importing._PickSources()" + utils.normal)
        n = len(self.settings["sources"])
        log.debug(utils.blue + "There are " + str(n)
                  + " sources in the source dictionary.")

        # Are there any sources in the source dictionary?
        if n > 0:

            # Interactive mode only
            if self.settings['FLAG_INT'] in utils.poswords:
                self.settings["catlist"] = []
                self.settings["target"] = self._SetSourceRole("target")
                self.settings["fluxcal"] = self._SetSourceRole("fluxcal")
                self.settings["phasecal"] = self._SetSourceRole("phasecal")
                self.settings["fringefinder"] = self._SetSourceRole("fringefinder")
                self.settings["bpcal"] = self._SetSourceRole("bpcal")

            # Batch + CASA mode only - check that the target and cal. sources exist
            # within the specified 'catlist'.
            else:
                target = self.settings["target"]
                log.debug(utils.blue + "target = " + str(target)
                          + utils.normal)

                fluxcal = self.settings["fluxcal"]
                log.debug(utils.blue + "fluxcal = " + str(fluxcal)
                          + utils.normal)

                phasecal = self.settings["phasecal"]
                log.debug(utils.blue + "phasecal = " + str(fluxcal)
                          + utils.normal)

                fringefinder = self.settings["fringefinder"]
                log.debug(utils.blue + "fringefinder = " + str(fringefinder)
                          + utils.normal)

                bpcal = self.settings["bpcal"]
                log.debug(utils.blue + "bpcal = " + str(bpcal)
                          + utils.normal)

                found_target = False
                found_fluxcal = False
                found_phasecal = False
                found_fringefinder = False
                found_bpcal = False

                if self.settings["catlist"][0] == "ALL":
                    self.settings["catlist"] = []
                    for id in self.settings["ms"]:
                        self.settings["catlist"].append(self.settings["ms"][id]["apath"])

                log.info("You've chosen (via 'catlist') to concatenate the following .ms files:")
                for file in self.settings["catlist"]:
                    log.info("* " + str(file))
                    for id in self.settings["ms"]:
                        if self.settings["ms"][id]["apath"] == file:
                            if target in self.settings["ms"][id]["sources"]:
                                found_target = True
                            if fluxcal in self.settings["ms"][id]["sources"]:
                                found_fluxcal = True
                            if phasecal in self.settings["ms"][id]["sources"]:
                                found_phasecal = True
                            if fringefinder in self.settings["ms"][id]["sources"]:
                                found_fringefinder = True
                            if bpcal in self.settings["ms"][id]["sources"]:
                                found_bpcal = True

                log.info("Verifying your choice of target and calibration sources...")
                self._CatlistHasSource("target", target, found_target)
                self._CatlistHasSource("fluxcal", fluxcal, found_fluxcal)
                self._CatlistHasSource("phasecal", phasecal, found_phasecal)
                self._CatlistHasSource("fringefinder", fringefinder, found_fringefinder)
                self._CatlistHasSource("bpcal", bpcal, found_bpcal)

    def _CatlistHasSource(self, role, name, result):
        """Print appropriate log message"""
        log.debug(utils.blue + "importing._CatListHasSource()" + utils.normal)
        if result == False:
            log.error(utils.red + role + " '" + name + "' was not found."
                      + utils.normal)
            self.quitter.start(1)
        else:
            log.info("* " + role + " = '" + name + "' [" + utils.green + "OK" + utils.normal + "]")

    def _cat(self):
        """Concatenate .ms files listed in 'catlist'"""
        log.debug(utils.blue + "importing._cat()" + utils.normal)
        catlist = self.settings["catlist"]

        # If using several .ms files join them together.
        if len(catlist) > 1:
            outms = self.settings["outpath"].rstrip("/") + "/" + self.settings["outprefix"] + ".ms"
            log.info("Concatenating .ms files. This could take a while...")
            concat(vis=catlist, concatvis=outms)  # CASA
            log.info("Finished concatenating .ms files.")
