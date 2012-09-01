#
# User defined tasks setup.
# Generated from buildmytask.
#

if sys.path[1] != '/home/user/src/basilisk':
  sys.path.insert(1, '/home/user/src/basilisk')
from odict import odict
if not globals().has_key('mytasks') :
  mytasks = odict()

mytasks['basilisk'] = 'Does nothing in particular.'
mytasks['bas'] = 'CASA Pipeline.'

if not globals().has_key('task_location') :
  task_location = odict()

for key in mytasks.keys() :
  task_location[key] = '/home/user/src/basilisk'
  tasksum[key] = mytasks[key]

from basilisk_cli import  basilisk_cli as basilisk
from bas_cli import  bas_cli as bas
