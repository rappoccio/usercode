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
'InclusiveMu15_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'TTbarJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'VqqJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'WJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'ZJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut'

]

labels = [
    'PF',
    'JPT',
    'Calo'
    ]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_selectors( files, tokens, labels )
