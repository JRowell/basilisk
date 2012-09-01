# Run me from inside CASA

# Load settings into the CASA environment.
StageSelection = '1, 2, 3'
target = '0555+398'
fluxcal = '1331+305'
phasecal = '1407+284'
fringefinder = '1331+305'
bpcal = '1407+284'
catlist = 'ALL'
converts = '0555+398_A, 1331+305_A, 1407+284_A'
inpath = '/home/user/data'
outpath = './'
outprefix = 'output'
logpath = './'
logfile = 'default.log'
FLAG_DEBUG = 'f'

# Inspect
inp(bas)

# Run the 'bas' task
results = bas()
