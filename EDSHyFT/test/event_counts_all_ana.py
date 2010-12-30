#!/bin/python

import subprocess
import commands
import sys
import tokenize

from event_flow_selectors import event_flow_selectors

tokens = ['Inclusive',
          '>= 1 Lepton',
          '== 1 Tight Lepton, Mu Veto',
          '== 1 Lepton',
          'MET Cut',
          '>=1 Jets',
          '>=3 Jets'
          ]

dirs = [
'Mu_Run2010A-Nov4ReReco_shyft_387_v1_shyftana_v1',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_shyftana_v1_HLT_Mu15Region',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_shyftana_v1_HLT_Mu9Region',
'DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_shyftana_387_v3',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_shyftana_387_v3',
'TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v3',
'TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v3_pu',
'TToBLNu_TuneZ2_s-channel_7TeV-madgraph_shyftana_387_v3',
'TToBLNu_TuneZ2_t-channel_7TeV-madgraph_shyftana_387_v3',
'TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_shyftana_387_v3',
'VQQJetsToLL_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v3',
'WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v3',

]

labels = [
    'PF',
#    'Calo'
    ]

for idir in dirs :
    print "-------------------------------" + idir + "---------------------------------"
    files = commands.getoutput("ls -1 " + idir + "/res/*.stdout").split()
    event_flow_selectors( files, tokens, labels )
