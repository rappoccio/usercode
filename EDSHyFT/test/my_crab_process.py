#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
##    'DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_shyft_387_v1', 
##    'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_take2_shyft_387_v1', # few still running
##    'TTJets_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1',
##    'TTJets_TuneD6T_largerISRFSR_7TeV-madgraph-tauola_shyft_387_v1',
##    'TTJets_TuneD6T_matchingdown_7TeV-madgraph-tauola_shyft_387_v1',
##    'TTJets_TuneD6T_matchingup_7TeV-madgraph-tauola_shyft_387_v1',
##    'TTJets_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1',
##    'TTJets_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1',
##    'TTJets_TuneD6T_smallerISRFSR_7TeV-madgraph-tauola_shyft_387_v1',
##    'TTJets_TuneZ2_7TeV-madgraph-tauola_shyft_387_v1',
##    'TToBLNu_TuneZ2_s-channel_7TeV-madgraph_shyft_387_v1',
##    'TToBLNu_TuneZ2_t-channel_7TeV-madgraph_shyft_387_v1',
##    'TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_shyft_387_v1', # 1,8,11,14-16,18
##    'VQQJetsToLL_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1',
##    'VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1',
##    'VQQJetsToLL_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1',
##    'Mu_Run2010A-Nov4ReReco_shyft_387_v1',
##    'Mu_Run2010B-Nov4ReReco_shyft_387_v1'

'TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v4',
'WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v4',
'DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_shyftana_387_v4',
'VQQJetsToLL_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v4',
'TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_shyftana_387_v4',
'TToBLNu_TuneZ2_t-channel_7TeV-madgraph_shyftana_387_v4',
'TToBLNu_TuneZ2_s-channel_7TeV-madgraph_shyftana_387_v4',
'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_shyftana_387_v4',

'Mu_Run2010A-Nov4ReReco_shyft_387_v1_shyftanaskim_v4_r1',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_shyftanaskim_v4_r2',
'Mu_Run2010B-Nov4ReReco_shyft_387_v1_shyftanaskim_v4_r3',
'TTJets_TuneD6T_7TeV-madgraph-tauola_shyftanaskim_387_v4',
'WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_shyftanaskim_387_v4'
    
    
]

for idir in dirs :
    print '--------------------------------'
    print '--------------------------------'
    print '--------------------------------'    
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
