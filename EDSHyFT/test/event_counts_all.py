#!/bin/python

import subprocess
import commands
import sys
import tokenize

from event_flow_crab import event_flow_crab

tokens = ['step1',
#          'isolatedPatMuons',
#          'isolatedPatMuonsPFlow'
          'scrapingVeto',
          'primaryVertexFilter',
          'HBHENoiseFilter',
#          'shyftMuCalo',          
#          'shyftMuPF',
#          'shyftMuJPT'
          ]

dirs = [
'Mu_Run2010A-Nov4ReReco_shyft_387_v1',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1'
]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_crab( files, tokens )
