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
           'BPrimeEDM_8TeV/Sep24/SingleElectron_DataA_tlbsm_53x_v1',
           'BPrimeEDM_8TeV/Sep24/SingleElectron_DataB1_tlbsm_53x_v1',
           'BPrimeEDM_8TeV/Sep24/SingleElectron_DataB2_tlbsm_53x_v1',
           'BPrimeEDM_8TeV/Sep24/SingleElectron_DataB3_tlbsm_53x_v1', 
           'BPrimeEDM_8TeV/Sep24/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_tlbsm_53x_v1',
           'BPrimeEDM_8TeV/Sep24/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_tlbsm_53x_v1',
           'BPrimeEDM_8TeV/Sep24/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_tlbsm_53x_v1',
##           'BPrimeEDM_8TeV/Sep24/T_t-channel_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v1', #Done
           'BPrimeEDM_8TeV/Sep24/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v1',
##           'BPrimeEDM_8TeV/Sep24/T_s-channel_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v1', #Done
##           'BPrimeEDM_8TeV/Sep24/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v1', #Done
##           'BPrimeEDM_8TeV/Sep24/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v1', #Done
##           'BPrimeEDM_8TeV/Sep24/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_tlbsm_53x_v1',#Done
           'BPrimeEDM_8TeV/Sep24/WW_TuneZ2star_8TeV_pythia6_tauola_tlbsm_53x_v1',
##           'BPrimeEDM_8TeV/Sep24/WZ_TuneZ2star_8TeV_pythia6_tauola_tlbsm_53x_v1', #Done
##           'BPrimeEDM_8TeV/Sep24/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph_tlbsm_53x_v1', #Done
    
]

for crabFile in crabFiles :
    s = 'crab -' + argument +' -c ' + crabPath + "/" + crabFile
    print s
    subprocess.call( [s], shell=True )

