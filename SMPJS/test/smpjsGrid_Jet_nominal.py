# !/bin/python
import subprocess
import glob
import copy
import re
import sys

print 'arguments on the command line are'
print sys.argv

index = int(sys.argv[1]) - 1
nsplit=5
files='/eos/uscms/store/user/smpjs/srappocc/Jet_Run2011_ttbsm_v10beta_tuples_lite_5fbinv/res/\*.root'

print 'index is ' + str(index)
print 'nsplit is ' + str(nsplit)

s = 'python smpjs_tuple_analyzer_fwlite.py --files={0:s} --nsplit={1:d} --isplit={2:d}'.format(
    files, nsplit, index
    )
print 'executing ' + s
subprocess.call( [s], shell=True )
