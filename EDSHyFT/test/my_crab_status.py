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

crabPath='/uscms_data/d2/skhalil/'


crabFiles = [
    'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_160404-161176_p1',
    'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_161216-163261_p2',
    'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_163286-163869_p3',
    'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_165088-165633_p4',
    'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_165970-166701_p5a',
    'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_166763-166967_p5b',
    'ShyftTemplates12a/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    'ShyftTemplates12a/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    'ShyftTemplates12a/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8',
    'ShyftTemplates12b/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    'ShyftTemplates12b/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    'ShyftTemplates12b/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8',
    'ShyftTemplates12c/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    'ShyftTemplates12c/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    'ShyftTemplates12c/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8',
    
]

for crabFile in crabFiles :
    s = 'crab -' + argument +' -c ' + crabPath + "/" + crabFile
    print s
    subprocess.call( [s], shell=True )

