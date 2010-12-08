#!/bin/python

import subprocess


dirs = [

## 'VQQJetsToLL_TuneD6T_scaleup_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'TTJets_TuneZ2_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'TTJets_TuneD6T_smallerISRFSR_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'TTJets_TuneD6T_scaleup_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'TTJets_TuneD6T_scaledown_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'TTJets_TuneD6T_matchingup_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'TTJets_TuneD6T_matchingdown_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',
## 'TTJets_TuneD6T_largerISRFSR_7TeV-madgraph-tauola_shyftana_387_v1_simplesys',

'TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v1',
'WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v1',
'DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_shyftana_387_v1',
'VQQJetsToLL_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v1',
'TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_shyftana_387_v1',
'TToBLNu_TuneZ2_t-channel_7TeV-madgraph_shyftana_387_v1',
'TToBLNu_TuneZ2_s-channel_7TeV-madgraph_shyftana_387_v1',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_shyftana_387_v1',



]

for idir in dirs :
    s = "hadd " + idir + '.root ' + idir + "/res/*.root"
    print s
    subprocess.call( [s, ""], shell=True )
