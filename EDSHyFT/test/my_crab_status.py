#!/bin/python

import subprocess
import os

from sys import argv
if len(argv)<2:
    print "usage: python my_crab_status_ele.py COMMAND"
    print "where COMMAND can be status, getoutput, etc"
    exit()

argument=""
for i in argv[1:]:
    argument += i+" "

crabPath='/uscms_data/d2/skhalil/ShyftCrab2011'


crabFiles = [
#'SingleElectron_Run2011A-PromptReco',
#'SingleMu_Run2011A-PromptReco',
#'TTJets_TuneD6T_7TeV-madgraph-tauola_Spring11-PU_S1_START311_V1G1-v1_shyft_414_v1',
#'TToBLNu_TuneZ2_s-channel_7TeV-madgraph_Spring11-PU_S1_START311_V1G1-v1_shyft_414_v1',
#'TToBLNu_TuneZ2_t-channel_7TeV-madgraph_Spring11-PU_S1_START311_V1G1-v1_shyft_414_v1',
#'TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_Spring11-PU_S1_START311_V1G1-v1_shyft_414_v1',
'WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_Spring11-PU_S1_START311_V1G1-v1_shyft_414_v1',
]

for crabFile in crabFiles :
    s = 'crab -' + argument +' -c ' + crabPath + "/" + crabFile
    print s
    subprocess.call( [s], shell=True )

