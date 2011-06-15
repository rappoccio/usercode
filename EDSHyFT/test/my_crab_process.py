#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
'SingleElectron_Run2011A-May10ReReco_ttbsm_v8_shyftSubstructureTuples_v3/',
'SingleElectron_Run2011A-PromptReco-v4_ttbsm_v8_shyftSubstructureTuples_v3/',
'SingleMu_Run2011A-May10ReReco_ttbsm_v8_shyftSubstructureTuples_v3/',
'SingleMu_Run2011A-PromptReco-v4_ttbsm_v8_shyftSubstructureTuples_v3/'

    
]

for idir in dirs :
    print '--------------------------------'
    print '--------------------------------'
    print '--------------------------------'    
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
