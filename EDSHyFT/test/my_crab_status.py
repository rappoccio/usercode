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

##        'TPrimeEDM/TrigData_May23/SingleElectron_ttbsm_424_v9_DataP4',
##        'TPrimeEDM/TrigData_May23/SingleElectron_ttbsm_424_v9_DataP5',
##        'TPrimeEDM/TrigData_May23/ElectronHad_ttbsm_424_v9_DataP6',
##       'TPrimeEDM/TrigData_May23/ElectronHad_ttbsm_424_v9_DataP7a',
##       'TPrimeEDM/TrigData_May23/ElectronHad_ttbsm_424_v9_DataP7b',

          'BPrimeEDM/MC_Ele_May1/TT_TuneZ2_7TeV-pythia6-tauola_ttbsm_424_v9_TTbar',
##          'BPrimeEDM/MC_Ele_May1/TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_424_v9_Fall11',          
##        'BPrimeEDM/MC_Ele_May1/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola_ttbsm_424_v9_Fall11',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-375_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-425_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-525_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-575_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-625_7TeV-madgraph_ttbsm_424_v9_Fall11',        
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-650_7TeV-madgraph_ttbsm_424_v9_Fall11',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-675_7TeV-madgraph_ttbsm_424_v9_Fall11',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-700_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-725_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-750_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-775_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-800_7TeV-madgraph_ttbsm_424_v9_Fall11',
            
           'BPrimeEDM/MC_Apr30/TT_TuneZ2_7TeV-pythia6-tauola_ttbsm_424_v9_TTbar',
##         'BPrimeEDM/MC_Apr30/TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_424_v9_Fall11', 
##         'BPrimeEDM/MC_Apr30/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-375_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-375_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-425_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-525_7TeV-madgraph_ttbsm_424_v9_Fall11',
    
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-575_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-625_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-650_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-675_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-700_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-725_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-750_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-775_7TeV-madgraph_ttbsm_424_v9_Fall11',
##         'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-800_7TeV-madgraph_ttbsm_424_v9_Fall11',
        
    
    ## 'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P1',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P2',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P3a',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P3b',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P4',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P5',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P6a',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P6b',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P7a',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P7b',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P8',
##     'BPrimeEDM/Data_Apr30/SingleMu_ttbsm_424_v9_P9',
    
    
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-350_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-375_7TeV-madgraph_ttbsm_424_v9',   
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-400_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-425_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-450_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-500_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-525_7TeV-madgraph_ttbsm_424_v9',  
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-550_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-550_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-575_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-600_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-625_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-650_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-675_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-700_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-725_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-750_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-775_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/BprimeBprimeToTWTWinc_M-800_7TeV-madgraph_ttbsm_424_v9',
    
   ##  'BPrimeEDM/MC_Apr30/LQToTNutau_M-200_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-250_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-300_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-350_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-400_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-450_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-500_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-550_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-600_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/LQToTNutau_M-650_7TeV-pythia6_ttbsm_424_v9',

##        'BPrimeEDM/MC_Apr30/TprimeTprimeToBWBWinc_M-400_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToBWBWinc_M-450_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToBWBWinc_M-500_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToBWBWinc_M-550_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToBWBWinc_M-600_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/tprime425_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/tprime475_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/tprime525_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/tprime575_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/tprime625_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',

##        'BPrimeEDM/MC_Apr30/TprimeTprimeToTZTZinc_M-350_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToTZTZinc_M-400_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToTZTZinc_M-450_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToTZTZinc_M-500_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToTZTZinc_M-550_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Apr30/TprimeTprimeToTZTZinc_M-600_7TeV-madgraph_ttbsm_424_v9',
##          'BPrimeEDM/MC_Apr30/TprimeTprimeToTZTZinc_M650_7TeV_madgraph_GEN_SIM_privateSample_B_ttbsm_424_v9',
       
##     'BPrimeEDM/MC_Apr30/TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_ttbsm_424_v9',#
##     'BPrimeEDM/MC_Apr30/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/T_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/T_TuneZ2_s-channel_7TeV-powheg-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/WZ_TuneZ2_7TeV_pythia6_tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/WW_TuneZ2_7TeV_pythia6_tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/ZZ_TuneZ2_7TeV_pythia6_tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/TTjets_TuneZ2_scaledown_7TeV-madgraph-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/TTjets_TuneZ2_scaleup_7TeV-madgraph-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/TTjets_TuneZ2_matchingdown_7TeV-madgraph-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/WJetsToLNu_TuneZ2_scaleup_7TeV-madgraph-tauola_ttbsm_424_v9',
##     'BPrimeEDM/MC_Apr30/WJetsToLNu_TuneZ2_scaledown_7TeV-madgraph-tauola_ttbsm_424_v9',#
##     'BPrimeEDM/MC_Apr30/TT_TuneZ2_7TeV-powheg-tauola_ttbsm_424_v9',
         
      ## 'SHyFTHisto/Jan26/SingleElectron_tlbsm_424_v9_P1',
##       'SHyFTHisto/Jan26/SingleElectron_tlbsm_424_v9_P2',
##       'SHyFTHisto/Jan26/SingleElectron_tlbsm_424_v9_P3',
##       'SHyFTHisto/Jan26/SingleElectron_tlbsm_424_v9_P4',
##       'SHyFTHisto/Jan26/SingleElectron_tlbsm_424_v9_P5',
      
      ## 'ntuplesShyft/Jan21/SingleElectron_ttbsm_v9_DataP1',
##       'ntuplesShyft/Jan21/SingleElectron_ttbsm_v9_DataP2',
##       'ntuplesShyft/Jan21/SingleElectron_ttbsm_v9_DataP3',
##       'ntuplesShyft/Jan21/SingleElectron_ttbsm_v9_DataP4',
##       'ntuplesShyft/Jan21/SingleElectron_ttbsm_v9_DataP5',
##       'ntuplesShyft/Jan21/ElectronHad_ttbsm_v9_DataP6',
##       'ntuplesShyft/Jan21/ElectronHad_ttbsm_v9_DataP7a',
##       'ntuplesShyft/Jan21/ElectronHad_ttbsm_v9_DataP7b',
##       'ntuplesShyft/Jan18/ElectronHad_ttbsm_v9_DataP8a',

##      'ntuplesShyft/Jan18/TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_v9_Top',
##      'ntuplesShyft/Jan18/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_ttbsm_v9_Wjets', ##
##      'ntuplesShyft/Jan18/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_ttbsm_v9_ZJets',
##      'ntuplesShyft/Jan18/T_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_v9_SingleTopT',
##      'ntuplesShyft/Jan18/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_v9_SingleTopbarT',
##      'ntuplesShyft/Jan18/T_TuneZ2_s-channel_7TeV-powheg-tauola_ttbsm_v9_SingleTopS',
##      'ntuplesShyft/Jan18/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola_ttbsm_v9_SingleTopbarS',
##      'ntuplesShyft/Jan18/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_ttbsm_v9_SingleToptW',
##      'ntuplesShyft/Jan18/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_ttbsm_v9_SingleTopbartW',
##      'ntuplesShyft/Jan18/GJets_TuneZ2_40_HT_100_7TeV-madgraph_ttbsm_v9_PhoJet40100',
##      'ntuplesShyft/Jan18/GJets_TuneZ2_100_HT_200_7TeV-madgraph_ttbsm_v9_PhoJet100200',
##      'ntuplesShyft/Jan18/GJets_TuneZ2_200_HT_inf_7TeV-madgraph_ttbsm_v9_PhoJet200Inf',
##     'ntuplesShyft/Jan18/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_v9_BCtoE2030',
##     'ntuplesShyft/Jan18/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_v9_BCtoE3080',
##     'ntuplesShyft/Jan18/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia_ttbsm_v9_BCtoE80170',
##     'ntuplesShyft/Jan18/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_v9_EMEn2030',
##     'ntuplesShyft/Jan18/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia_ttbsm_v9_EMEn3080', ##
##     'ntuplesShyft/Jan18/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_v9_EMEn80170',
##     'ntuplesShyft/Jan18/WJetsToLNu_TuneZ2_scaleup_7TeV-madgraph-tauola_ttbsm_v9_WjetsDown',
##     'ntuplesShyft/Jan18/WJetsToLNu_TuneZ2_scaledown_7TeV-madgraph-tauola_ttbsm_v9_WjetsUp',
##     'ntuplesShyft/Jan18/TTjets_TuneZ2_matchingdown_7TeV-madgraph-tauola_ttbsm_v9_TopMatchDown',
##     'ntuplesShyft/Jan18/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola_ttbsm_v9_TopMatchUp',
##        'ntuplesShyft/Jan18/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_ttbsm_v9_Mu_QCD',
##       'ntuplesShyft/Jan18/TTjets_TuneZ2_scaledown_7TeV-madgraph-tauola_ttbsm_v9_TopDown',
##       'ntuplesShyft/Jan18/TTjets_TuneZ2_scaleup_7TeV-madgraph-tauola_ttbsm_v9_TopUp',
       ## 'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP1',
##        'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP2',
##        'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP3a',
##        'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP3b',
##        'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP4',
##        'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP5',
##        'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP6a',
##        'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP6b',
##        'ntuplesShyft/Jan18/SingleMu_ttbsm_v9_DataP7',
       
##      'ntuplesShyft/Jan18/TTJets_TuneZ2_mass161_5_7TeV-madgraph-tauola_ttbsm_v9_Mass161_5',
##      'ntuplesShyft/Jan18/TTJets_TuneZ2_mass163_5_7TeV-madgraph-tauola_ttbsm_v9_Mass163_5',
##      'ntuplesShyft/Jan18/TTJets_TuneZ2_mass166_5_7TeV-madgraph-tauola_ttbsm_v9_Mass166_5',
##      'ntuplesShyft/Jan18/TTJets_TuneZ2_mass169_5_7TeV-madgraph-tauola_ttbsm_v9_Mass169_5',
##        'ntuplesShyft/Jan18/TTJets_TuneZ2_mass175_5_7TeV-madgraph-tauola_ttbsm_v9_Mass175_5',
##      'ntuplesShyft/Jan18/TTJets_TuneZ2_mass178_5_7TeV-madgraph-tauola_ttbsm_v9_Mass178_5',
##      'ntuplesShyft/Jan18/TTJets_TuneZ2_mass181_5_7TeV-madgraph-tauola_ttbsm_v9_Mass181_5',
##      'ntuplesShyft/Jan18/TTJets_TuneZ2_mass184_5_7TeV-madgraph-tauola_ttbsm_v9_Mass184_5',
    
##    # 'TPrimeEDM/TrigData_Dec21/SingleElectron_ttbsm_424_v9_DataP4',
##    # 'TPrimeEDM/TrigData_Dec21/SingleElectron_ttbsm_424_v9_DataP5',
   # 'TPrimeEDM/TrigData_Dec29/ElectronHad_ttbsm_424_v9_tprimeP9',
   # 'TPrimeEDM/TrigData_Dec29/ElectronHad_ttbsm_424_v9_tprimeP10',

    
    #'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_160404-161176_p1',
    #'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_161216-163261_p2',
    #'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_163286-163869_p3',
    #'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_165088-165633_p4',
    #'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_165970-166701_p5a',
    #'ShyftTemplates12a/SingleElectron_tlbsm_424_v8_166763-166967_p5b',

    #'ShyftTemplates12/SingleElectron_tlbsm_424_v8_160404-161176_p1',
    #'ShyftTemplates12/SingleElectron_tlbsm_424_v8_161216-163261_p2',
    #'ShyftTemplates12/SingleElectron_tlbsm_424_v8_163286-163869_p3',
    #'ShyftTemplates12/SingleElectron_tlbsm_424_v8_165088-165633_p4',
    #'ShyftTemplates12/SingleElectron_tlbsm_424_v8_165970-166701_p5a',
    #'ShyftTemplates12/SingleElectron_tlbsm_424_v8_166763-166967_p5b',
    
    #'ShyftTemplates12a/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    #'ShyftTemplates12a/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    #'ShyftTemplates12a/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8',
    #'ShyftTemplates12b/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    #'ShyftTemplates12b/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    #'ShyftTemplates12b/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8',
    #'ShyftTemplates12c/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    #'ShyftTemplates12c/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8',
    #'ShyftTemplates12c/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8',

####_____Ending SHyFT_________####
    ##     'BPrimeEDM/MC_Dec13/BprimeBprimeToTWTWinc_M-350_7TeV-madgraph_ttbsm_424_v9',#done
##     'BPrimeEDM/MC_Dec13/BprimeBprimeToTWTWinc_M-400_7TeV-madgraph_ttbsm_424_v9',#done
##     'BPrimeEDM/MC_Dec13/BprimeBprimeToTWTWinc_M-450_7TeV-madgraph_ttbsm_424_v9',#done
##     'BPrimeEDM/MC_Dec13/BprimeBprimeToTWTWinc_M-500_7TeV-madgraph_ttbsm_424_v9',#done
##     'BPrimeEDM/MC_Dec13/BprimeBprimeToTWTWinc_M-550_7TeV-madgraph_ttbsm_424_v9',#done
##     'BPrimeEDM/MC_Dec13/BprimeBprimeToTWTWinc_M-600_7TeV-madgraph_ttbsm_424_v9',#done

##        'BPrimeEDM/MC_Nov13/LQToTNutau_M-200_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov13/LQToTNutau_M-250_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov13/LQToTNutau_M-300_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov13/LQToTNutau_M-350_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov13/LQToTNutau_M-400_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov23/LQToTNutau_M-450_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov23/LQToTNutau_M-500_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov23/LQToTNutau_M-550_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov23/LQToTNutau_M-600_7TeV-pythia6_ttbsm_424_v9',#done
##        'BPrimeEDM/MC_Nov23/LQToTNutau_M-650_7TeV-pythia6_ttbsm_424_v9',#done
  ####______BPrime______________####
    
##      'BPrimeEDM/MC_Ele_May1/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/GJets_TuneZ2_40_HT_100_7TeV-madgraph_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/GJets_TuneZ2_100_HT_200_7TeV-madgraph_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/GJets_TuneZ2_200_HT_inf_7TeV-madgraph_ttbsm_424_v9',
    
    
##      'BPrimeEDM/MC_Ele_May1/TTJets_TuneZ2_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/T_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/T_TuneZ2_s-channel_7TeV-powheg-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/WZ_TuneZ2_7TeV_pythia6_tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/WW_TuneZ2_7TeV_pythia6_tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/ZZ_TuneZ2_7TeV_pythia6_tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TTjets_TuneZ2_scaledown_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TTjets_TuneZ2_scaleup_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/WJetsToLNu_TuneZ2_scaledown_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/WJetsToLNu_TuneZ2_scaleup_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TTjets_TuneZ2_matchingdown_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TT_TuneZ2_7TeV-powheg-tauola_ttbsm_424_v9',

##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-350_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-375_7TeV-madgraph_ttbsm_424_v9',   
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-400_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-425_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-450_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-500_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-525_7TeV-madgraph_ttbsm_424_v9',  
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-550_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-550_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-575_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-600_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-625_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-650_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-675_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-700_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-725_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-750_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-775_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/BprimeBprimeToTWTWinc_M-800_7TeV-madgraph_ttbsm_424_v9',
    

##      'BPrimeEDM/MC_Ele_May1/TprimeTprimeToBWBWinc_M-400_7TeV-madgraph_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TprimeTprimeToBWBWinc_M-450_7TeV-madgraph_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TprimeTprimeToBWBWinc_M-500_7TeV-madgraph_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TprimeTprimeToBWBWinc_M-550_7TeV-madgraph_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/TprimeTprimeToBWBWinc_M-600_7TeV-madgraph_ttbsm_424_v9',    
##      'BPrimeEDM/MC_Ele_May1/tprime425_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/tprime475_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/tprime525_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/tprime575_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',
##      'BPrimeEDM/MC_Ele_May1/tprime625_bWbW_Summer11MG7TeV_JackLHE_atFermilab_ttbsm_424_v9',

##        'BPrimeEDM/MC_Ele_May1/TprimeTprimeToTZTZinc_M-350_7TeV-madgraph_ttbsm_424_v9', ##
##        'BPrimeEDM/MC_Ele_May1/TprimeTprimeToTZTZinc_M-400_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/TprimeTprimeToTZTZinc_M-450_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/TprimeTprimeToTZTZinc_M-500_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/TprimeTprimeToTZTZinc_M-550_7TeV-madgraph_ttbsm_424_v9',
##        'BPrimeEDM/MC_Ele_May1/TprimeTprimeToTZTZinc_M-600_7TeV-madgraph_ttbsm_424_v9',
##          'BPrimeEDM/MC_Ele_May1/TprimeTprimeToTZTZinc_M650_7TeV_madgraph_GEN_SIM_privateSample_B_ttbsm_424_v9',

##     'BPrimeEDM/Data_Ele_May1/SingleElectron_ttbsm_424_v9_P1',
##     'BPrimeEDM/Data_Ele_May1/SingleElectron_ttbsm_424_v9_P2',
##     'BPrimeEDM/Data_Ele_May1/SingleElectron_ttbsm_424_v9_P3',
##     'BPrimeEDM/Data_Ele_May1/SingleElectron_ttbsm_424_v9_P4',
##     'BPrimeEDM/Data_Ele_May1/SingleElectron_ttbsm_424_v9_P5',
##     'BPrimeEDM/Data_Ele_May1/ElectronHad_ttbsm_424_v9_P6',
##     'BPrimeEDM/Data_Ele_May1/ElectronHad_ttbsm_424_v9_P7a',
##     'BPrimeEDM/Data_Ele_May1/ElectronHad_ttbsm_424_v9_P7b',
##     'BPrimeEDM/Data_Ele_May1/ElectronHad_ttbsm_424_v9_P8a',
##     'BPrimeEDM/Data_Ele_May1/ElectronHad_ttbsm_424_v9_P8b',
##     'BPrimeEDM/Data_Ele_May1/ElectronHad_ttbsm_424_v9_P8c',
##     'BPrimeEDM/Data_Ele_May1/ElectronHad_ttbsm_424_v9_P9',
##     'BPrimeEDM/Data_Ele_May1/ElectronHad_ttbsm_424_v9_P10',

    
]

for crabFile in crabFiles :
    s = 'crab -' + argument +' -c ' + crabPath + "/" + crabFile
    print s
    subprocess.call( [s], shell=True )

