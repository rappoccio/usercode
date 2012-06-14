#!/bin/python

import subprocess
import commands
import sys
import tokenize

from event_flow_crab import event_flow_crab

tokens = ['step1',
          'scrapingVeto',
          'primaryVertexFilter',
          'HBHENoiseFilter',
          'shyftMuCalo',          
          'shyftMuPF',
          'shyftMuJPT'
          ]

dirs = [
    'TTbarJets-madgraph_shyft_38xOn35x_v2'
]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_crab( files, tokens )
