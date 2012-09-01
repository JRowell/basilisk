import os
import subprocess
import time
import random
import sys

# Font effects
underline = "\x1b[1;4m"
black = "\x1b[1;30m"
red = "\x1b[1;31m"
green = "\x1b[1;32m"
yellow = "\x1b[1;33m"
blue = "\x1b[1;34m"
purple = "\x1b[1;35m"
turquoise = "\x1b[1;36m"
normal = "\x1b[0m"

## Strings for boolean operations
poswords = ['1', 'y', 'Y', 'yes', 'Yes', 'YES', 't', 'T', 'true', 'True', 'TRUE']
negwords = ['0', 'n', 'N', 'no', 'No', 'NO', 'f', 'F', 'false', 'False', 'FALSE']

## Stock messages for RandomMsg()
# messages[x][0] = Error messages.
# meesages[x][1] = Success messages.
# messages[x][2] = Waiting messages:
#
# msg_theme_XXXXXX = [["'' - ",
#                      "'' - ",
#                      "'' - ",
#                      "'' - ",
#                      "'' - "],
#                     ["'' - ",
#                      ",, - "],
#                     ["'' - ",
#                      "'' - "]]

msg_theme_wisdom = [["'' - ",
                     "'' - ",
                     "'' - ",
                     "'' - ",
                     "'' - "],
                    ["'' - ",
                     ",, - "],
                    ["'He that can have Patience, can have what he will' - Benjamin Franklin",
                     "'The secret of patience is doing something else in the meanwhile' - anon",
                     "'Patience is bitter, but its fruit is sweet.' - Jean-Jacques Rousseau",
                     "'The two most powerful warriors are patience and time.' - Leo Tolstoy "]]

msg_theme_lotr = [["'The age of Men is over. The time of the Orc has come!' - Gothmog",
                   "'Surety you crave! Sauron gives none.' - The Mouth of Sauron",
                   "'I know what it is you saw, for it is also in my mind.' - Galadriel",
                   "'Against the power of Mordor there can be no victory.' - Saruman",
                   "'He that breaks a thing to find out what it is has left the path of wisdom.' - Gandalf",
                   "'I am servant of the Secret Fire, wielder of the flame of Anor. You cannot pass.' - Gandalf",
                   "'The hasty stroke goes oft astray.' - Aragorn",
                   "'Short cuts make long delays.' - Pippin",
                   "'Thus is it spoken: Oft hope is born, when all is forlorn.' - Legolas",
                   "'The way is shut. It was made by those who are dead, and the dead keep it. The way is shut.' - Legolas"],
                  ["'All's well that ends better.' - Gaffer",
                   "'The battle of Helm's Deep is over; the battle for Middle Earth is about to begin' - Gandalf"],
                  ["'' - "]]

msg_theme_starwars = [["'Help me Obi-Wan Kenobe, you're my only hope.' - Princess Leia",
                       "'I suggest a new strategy, R2. Let the wookiee win.' - C3PO",
                       "'These aren't the droids you're looking for...' - Obi-Wan Kenobe",
                       "'It's against my programming to impersonate a deity.' - C3PO",
                       "'Do or do not... there is no try.' - Yoda",
                       "'Much to learn you still have...' - Yoda",
                       "'R2-D2, you know better than to trust a strange computer.' - C3PO"],
                      ["'The force is strong with this one.' - Darth Vader ",
                       "'Everything that has transpired has done so, according to my design.' - Emperor Palpatine"],
                      ["'' - "]]

msg_theme_startrek = [["'The bureaucratic mentality is the only constant in the universe.' - Dr McCoy",
                       "'Please, Captain, not in front of the Klingons.' - Spock",
                       "'My programming may be inadequate to the task.' - Data",
                       "'Believing oneself to be perfect is often the sign of a delusional mind.' - The Borg Queen",
                       "'Curious how often you humans manage to obtain that which you do not want.' - Spock",
                       "'Initiate auto-destruct sequence. Authorization: Picard, 4 7 Alpha Tango.' - Picard",
                       "'We are the Borg. You will be assimilated. Resistance is futile.' - The Borg"],
                      ["'You have the bridge...' - Picard"],
                      ["'' - "]]

msg_theme_sysadmin = [["'Increased sunspot activity.' - BOFH excuse #390",
                       "'Electromagnetic radiation from satellite debris.' - BOFH excuse #003",
                       "'Cosmic ray particles crashed through the hard disk platter.' - BOFH excuse #051",
                       "'Power company testing new voltage spike (creation) equipment.' - BOFH excuse #102",
                       "'Interference between the keyboard and the chair.' - BOFH excuse #289",
                       "'The AA battery in the wallclock sends magnetic interference.' - BOFH excuse #335",
                       "'We already sent around a notice about that.' - BOFH excuse #391",
                       "'Jupiter is aligned with Mars.' - BOFH excuse #394",
                       "'Firmware update in the coffee machine.' - BOFH excuse #428",
                       "'Sticky bit has come loose.' - BOFH excuse #438"],
                      ["Success!",
                       "Operation completed, but that doesn't mean it's error free.",
                       "Over to you..."],
                      ["'' - "]]

messages = [msg_theme_lotr, msg_theme_starwars, msg_theme_startrek, msg_theme_sysadmin]


def RandomMsg(msglist):
    """Return random message from list."""
    return "\n" + str(random.choice(msglist)) + "\n"


def FindProg(prog):
    """Locate a program and return its path."""
    status = 1
    a = subprocess.Popen(["which", prog], stdout=subprocess.PIPE, stderr=open(os.devnull, "w"))
    path = a.communicate()[0]
    if path == "":
        status = 0
    return [status, path]


def WriteSpeed(source):
    """Return the estimated disk write speed."""
    command = ["dd", "if=" + source, "of=/dev/null", "bs=1K", "count=100000"]
    middleman = subprocess.Popen(command, stderr=subprocess.PIPE)
    results = middleman.communicate()[1]
    speed = float(results.split()[-2])
    units = results.split()[-1]

    # Convert to B/s
    if "K" in units:
        speed = speed * 1000
    elif "M" in units:
        speed = speed * 1000000
    elif "G" in units:
        speed = speed * 1000000000

    return speed


def DirSize(path='.'):
    """Calculate directory size."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total


def timestamp():
    """Return timestamp as a string."""
    return str(time.strftime("[%Y-%m-%d][%H:%M:%S]", time.localtime()))


def GetConfigSection(parser, section):
    """Return dictionary of options from section of config file."""
    dict = {}
    options = parser.options(section)
    for option in options:
        try:
            dict[option] = parser.get(section, option)
        except:
            dict[option] = None
    return dict


def ShowProgress(progress):
    sys.stdout.write('\r[{0}] {1}%'.format('#' * (progress / 10), progress))
    sys.stdout.flush()
