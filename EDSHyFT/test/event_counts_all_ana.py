#!/bin/python

import subprocess
import commands
import sys
import tokenize

from event_flow_selectors import event_flow_selectors

tokens = ['>= 1 Lepton',
          '== 1 Tight Lepton, Mu Veto',
          '== 1 Lepton',
          'MET Cut',
          '>=1 Jets',
          '>=3 Jets'
          ]

dirs = [
'InclusiveMu15_shyftana_38xOn35x_v18_allsys',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v18_allsys',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v18_allsys',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v18_allsys',
'TTbarJets-madgraph_shyftana_38xOn35x_v18_allsys',
'VqqJets-madgraph_shyftana_38xOn35x_v18_allsys',
'WJets-madgraph_shyftana_38xOn35x_v18_allsys',
'ZJets-madgraph_shyftana_38xOn35x_v18_allsys'
]

labels = [
    'PF',
    'JPT',
#    'Calo'
    ]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_selectors( files, tokens, labels )
