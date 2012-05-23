#!/bin/python

import subprocess
import commands
import sys
import tokenize

from event_flow_selectors import event_flow_selectors

tokens = ['== 1 Lepton',
          '>=1 Jets'
          ]

dirs = [
'InclusiveMu15_shyftana_38xOn35x_v2',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v2',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v2',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v2',
'TTbarJets-madgraph_shyftana_38xOn35x_v2',
'VqqJets-madgraph_shyftana_38xOn35x_v2',
'WJets-madgraph_shyftana_38xOn35x_v2',
'ZJets-madgraph_shyftana_38xOn35x_v2'

]

labels = [
    'shyftMuPF',
    'shyftMuJPT',
    'shyftMuCalo'
    ]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_selectors( files, tokens, labels )
