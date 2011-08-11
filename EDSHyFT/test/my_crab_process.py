#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
'SingleMu_Run2011A-May10ReReco_ttbsm_v8_shyftSubstructureTuples_v8/',
'SingleMu_Run2011A-PromptReco-v4_ttbsm_v8_shyftSubstructureTuples_v8/',
'TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_v8_shyftSubstructureTupleDump_v8/',
    
]

for idir in dirs :
    print '--------------------------------'
    print '--------------------------------'
    print '--------------------------------'    
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
