#!/bin/python

import subprocess
import commands
import sys
import tokenize

from event_flow_crab import event_flow_crab

tokens = ['step1',
          'isolatedPatMuons',
          'isolatedPatMuonsPFlow'
#          'scrapingVeto',
#          'primaryVertexFilter',
#          'HBHENoiseFilter',
#          'shyftMuCalo',          
#          'shyftMuPF',
#          'shyftMuJPT'
          ]

dirs = [
#'InclusiveMu15_shyft_38xOn35x_v5',
#'SingleTop_sChannel-madgraph_shyft_38xOn35x_v5',
#'SingleTop_tChannel-madgraph_shyft_38xOn35x_v5',
#'SingleTop_tWChannel-madgraph_shyft_38xOn35x_v5',
#'TTbarJets-madgraph_shyft_38xOn35x_v5',
#'VqqJets-madgraph_shyft_38xOn35x_v5',
'WJets-madgraph_shyft_38xOn35x_v5',
#'ZJets-madgraph_shyft_38xOn35x_v5',
#'shyft_38xOn35x_v5_r1',
#'shyft_38xOn35x_v5_r2',
#'shyft_38xOn35x_v5_r3'
]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_crab( files, tokens )
