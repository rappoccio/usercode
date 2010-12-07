#!/bin/python

import subprocess


dirs = [

'VQQJetsToLL_TuneD6T_scaleup_7TeV-madgraph-tauola_shyftana_387_v1',
'VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola_shyftana_387_v1',
'TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v1',
'TTJets_TuneZ2_7TeV-madgraph-tauola_shyftana_387_v1',
'TTJets_TuneD6T_smallerISRFSR_7TeV-madgraph-tauola_shyftana_387_v1',
'TTJets_TuneD6T_scaleup_7TeV-madgraph-tauola_shyftana_387_v1',
'TTJets_TuneD6T_scaledown_7TeV-madgraph-tauola_shyftana_387_v1',
'TTJets_TuneD6T_matchingup_7TeV-madgraph-tauola_shyftana_387_v1',
'TTJets_TuneD6T_matchingdown_7TeV-madgraph-tauola_shyftana_387_v1',
'TTJets_TuneD6T_largerISRFSR_7TeV-madgraph-tauola_shyftana_387_v1',


]

for idir in dirs :
    s = "hadd " + idir + '.root ' + idir + "/res/*.root"
    print s
    subprocess.call( [s, ""], shell=True )
