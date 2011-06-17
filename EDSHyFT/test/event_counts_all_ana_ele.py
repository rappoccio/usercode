#!/bin/python

import subprocess
import commands
import sys
import tokenize

crabPath='/uscms_data/d2/skhalil/ShyftTemplates11'

from event_flow_selectors import event_flow_selectors

tokens = [
    #'Inclusive',
    'Trigger',
   # '== 1 Tight Lepton',
   # '== 1 Tight Lepton, Mu Veto',
    '== 1 Lepton',
    'MET Cut Min',
    #'MET Cut Max',    
    'Conversion Veto B',
    'Dilepton Veto',
    #'Z Veto',
    #'>=1 Jets',
    #'>=2 Jets',
    #'>=3 Jets',
    '>=4 Jets',
    '>=5 Jets',
    ]

dirs = {
    
##     "TTbarJets":               ['TTJets_TuneD6T_7TeV-madgraph-tauola_ttbsm_415_v7'],
##     "WJetsToLNu":              ['WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_ttbsm_415_v7'],
##     "DYJetsToLL":              ['DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_ttbsm_415_v7'],
##     "TToBLNu, s-channel":      ['TToBLNu_TuneZ2_s-channel_7TeV-madgraph_ttbsm_415_v7'],
##     "TToBLNu, t-channel":      ['TToBLNu_TuneZ2_t-channel_7TeV-madgraph_ttbsm_415_v7'],
##     "TToBLNu, tW-channel":     ['TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_ttbsm_415_v7'], 
    
##     "QCD\_EMEn\_Pt20to30":     ['QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_415_v7'],
##     "QCD\_EMEn\_Pt30to80":     ['QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_415_v7'],
##     "QCD\_EMEn\_Pt80to170":    ['QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_415_v7'],
##     "QCD\_BCtoE\_Pt20to30":    ['QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_415_v7'],
##     "QCD\_BCtoE\_Pt30to80":    ['QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_415_v7'],
##     "QCD\_BCtoE\_Pt80to170":   ['QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_415_v7'],
##     "PhotonJets\_Pt40to100":   ['GJets_TuneD6T_HT-40To100_7TeV-madgraph_ttbsm_415_v7'],
##     "PhotonJets\_Pt100to200":  ['GJets_TuneD6T_HT-100To200_7TeV-madgraph_ttbsm_415_v7'],
##     "PhotonJets\_Pt200toInf":  ['GJets_TuneD6T_HT-200_7TeV-madgraph_ttbsm_415_v7'],
    
    
    "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT":   ['SingleElectron_ttbsm_423_v6_p1',
                                                     'SingleElectron_ttbsm_423_v6_p2',
                                                     'SingleElectron_ttbsm_423_v6_p3',]
    
    }

labels = [
   'PF',
   #'PF no MET',
   ]

outstrings=[]
for sample in dirs:
    total_sum={}
    outstring = sample
    for idir in dirs[sample] :
        print "-------------------------------" + idir + "---------------------------------"
        files = commands.getoutput("ls -1 " + crabPath + "/" + idir + "/res/*.stdout").split()
        
        dict1 = event_flow_selectors( files, tokens, labels )
        #print dict1
        for f in dict1:
            if f not in total_sum: total_sum[f]={}
            for l in dict1[f]:
                if l not in total_sum[f]: total_sum[f][l]=0
                total_sum[f][l] += dict1[f][l]


    for t in tokens:
        #outstring +='& {0:<12.1f}'.format(total_sum[t][labels[0]])
        outstring += " & %i"%total_sum[t][labels[0]]
    outstring+="\\\\"
    outstrings.append(outstring)


print "-------------------sum table-----------------"
for i in outstrings:
    print i

