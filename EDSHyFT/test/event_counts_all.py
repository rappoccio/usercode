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
#'InclusiveMu15_shyft_38xOn35x_v2',
#'SingleTop_sChannel-madgraph_shyft_38xOn35x_v2',
'SingleTop_tChannel-madgraph_shyft_38xOn35x_v2',
#'SingleTop_tWChannel-madgraph_shyft_38xOn35x_v2',
#'TTbarJets-madgraph_shyft_38xOn35x_v2',
#'VqqJets-madgraph_shyft_38xOn35x_v2',
#'WJets-madgraph_shyft_38xOn35x_v2',
#'ZJets-madgraph_shyft_38xOn35x_v2',
#'shyft_38xOn35x_v2_r1',
#'shyft_38xOn35x_v2_r2',
#'shyft_38xOn35x_v2_r3'
]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_crab( files, tokens )
