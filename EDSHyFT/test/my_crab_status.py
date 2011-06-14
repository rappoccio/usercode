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

crabPath='/uscms_data/d2/skhalil/ShyftTemplates11'


crabFiles = [
    'SingleElectron_ttbsm_423_v6_p1',
    'SingleElectron_ttbsm_423_v6_p2',
    'SingleElectron_ttbsm_423_v6_p3',
    'TTJets_TuneD6T_7TeV-madgraph-tauola_ttbsm_415_v7',
    'WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_ttbsm_415_v7',
    'DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_ttbsm_415_v7',
    'TToBLNu_TuneZ2_t-channel_7TeV-madgraph_ttbsm_415_v7',
    'TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_ttbsm_415_v7',
    'GJets_TuneD6T_HT-40To100_7TeV-madgraph_ttbsm_415_v7',
    'GJets_TuneD6T_HT-100To200_7TeV-madgraph_ttbsm_415_v7',
    'GJets_TuneD6T_HT-200_7TeV-madgraph_ttbsm_415_v7',
    'QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_415_v7',
    'QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_415_v7',
    'QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_415_v7',
    'QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_415_v7',
    'QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_415_v7',
]

for crabFile in crabFiles :
    s = 'crab -' + argument +' -c ' + crabPath + "/" + crabFile
    print s
    subprocess.call( [s], shell=True )

