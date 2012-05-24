# !/bin/python
import subprocess
import glob
import copy
import re
import sys

print 'arguments on the command line are'
print sys.argv

index = int(sys.argv[1]) - 1
nsplit= int(sys.argv[2])
resttoks =sys.argv[3:]

dataOrMC = '_data'
for tok in resttoks:
    if '--useMC' in tok :
        dataOrMC = ''

rest = ''
for tok in resttoks :
    rest += ' ' + tok

print 'index is ' + str(index)
print 'nsplit is ' + str(nsplit)
print 'other command line arguments are ' + rest

s = 'python smpjs_tuple_analyzer_fwlite' + dataOrMC + '.py --nsplit={0:d} --isplit={1:d} {2:s}'.format(
    nsplit, index, rest
    )
print 'executing ' + s
subprocess.call( [s], shell=True )
