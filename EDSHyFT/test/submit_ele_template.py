#! /bin/python

from string import *
import subprocess

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputCfg', metavar='C', type='string', action='store',
                  default='crab_dummy_anashyft_ele.cfg',
                  dest='inputCfg',
                  help='input config tag to be used')

parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='_ttbsm_424_v8',
                  dest='outLabel',
                  help='output tag to be used')

parser.add_option('--outLocation', metavar='L', type='string', action='store',
                  default='/uscms_data/d2/skhalil/ShyftTemplates12a/',
                  dest='outLocation',
                  help='output location to create the crab directories')

parser.add_option('--data', metavar='D', type='int', action='store',
                  default = '0',
                  dest='data',
                  help='submit data jobs')

parser.add_option('--summer11MC', metavar='M', type='int', action='store',
                  default = '0',
                  dest='summer11MC',
                  help='submit summer 11 jobs')

parser.add_option('--eleEtCut', metavar='EC', type='float', action='store',
                  default = '30.0',
                  dest='eleEtCut',
                  help='electron Et threshold')

(options, args) = parser.parse_args()


#############################################################################################################
##
## ****************** submit the MC thrice with eleEtCut=30.0/35.0/45.0***********************
## The reset options are "dataset name, number of jobs, EtCut, useFlavorHistory, inuptSampleName, use42X, 
## ignoreTrigger, allSys, trigger, run range, dataperiod
##
##############################################################################################################
eleEt  = options.eleEtCut

if options.data == 1:
   inputCMSSW = 'shyftEDAnalyzer_ele.py'
   outputLable = '_tlbsm_424_v8'
   crabFileStrs = [
      ['/SingleElectron/skhalil-ttbsm_v8_Run2011-May10ReReco-0d3d9a54f3a29af186ad87df2a0c3ce1/USER',  60, 30.0, 0, 'Data', 1, 0, 0,'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1', '160404-161176', 'p1'],
      ['/SingleElectron/skhalil-ttbsm_v8_Run2011-May10ReReco-0d3d9a54f3a29af186ad87df2a0c3ce1/USER',  60, 30.0, 0, 'Data', 1, 0, 0,'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v2', '161216-163261', 'p2'],
      ['/SingleElectron/skhalil-ttbsm_v8_Run2011-May10ReReco-0d3d9a54f3a29af186ad87df2a0c3ce1/USER',  60, 30.0, 0, 'Data', 1, 0, 0,'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v3', '163286-163869', 'p3'],

      ####______________change the prompt Reco json by hand please________________________________
      #['/SingleElectron/srappocc-ttbsm_v8_Run2011-PromptReco-0d3d9a54f3a29af186ad87df2a0c3ce1/USER',  60, 35.0, 0, 'Data', 1, 0, 0,'HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v3', '165088-165633', 'p4'],
      #['/SingleElectron/srappocc-ttbsm_v8_Run2011-PromptReco-0d3d9a54f3a29af186ad87df2a0c3ce1/USER',  60, 45.0, 0, 'Data', 1, 0, 0,'HLT_Ele42_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1', '165970-166701', 'p5a'],
      #['/SingleElectron/cjenkins-ttbsm_v8_Run2011-PromptReco-0d3d9a54f3a29af186ad87df2a0c3ce1/USER',  60, 45.0, 0, 'Data', 1, 0, 0,'HLT_Ele42_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1', '166763-166967', 'p5b'],
      ]
elif options.summer11MC == 1 and options.data == 0:
   inputCMSSW = 'shyftEDAnalyzer_allsys_ele.py'
   outputLable = '_tlbsm_424_v8'
   crabFileStrs = [

      ###################################################################################################################################
      #                 For Summer 11 use: python submit_ele_template.py --data=0 with option use42X
      ###################################################################################################################################
      
      ['/TTJets_TuneZ2_7TeV-madgraph-tauola/srappocc-ttbsm_v8_Summer11-PU_S4_START42_V11-v1-5c91b0700768331a44f51c8a9892d391/USER',          30, eleEt, 0, 'Top',    1,  1, 1],
      ['/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/srappocc-ttbsm_v8_Summer11-PU_S4_START42_V11-v1-87037ef7c828ea57e128f1ace23a632e/USER',      50, eleEt, 1, 'Wjets',  1,  1, 1],
      ['/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/skhalil-ttbsm_v8_Summer11-PU_S4_START42_V11-v1-87037ef7c828ea57e128f1ace23a632e/USER',  40, eleEt, 1, 'Zjets',  1,  1, 1],
      ]
elif options.summer11MC == 0 and options.data == 0:
   inputCMSSW = 'shyftEDAnalyzer_allsys_ele.py'
   outputLable = '_tlbsm_415_v7'   
   crabFileStrs = [
     
      ###################################################################################################################################
      #__________For tprime use: python submit_ele_template.py --data=0 --inputCfg=crab_dummy_anashyft_ele_ph01.cfg______________
      ###################################################################################################################################
      
      ## ['/bprime350_tWtW_Fall10MG7TeV_AlexisLHE_atFermilab/cjenkins-tprime350_tWtW_Fall10MG7TeV-6a29f0fac22a95bcd534f59b8047bd70/USER',         60, eleEt, 0, 'TPrime_350', 0, 1, 1],
##       ['/tprime400_bWbW_Fall10MG7TeV_AlexisLHE_v1/cjenkins-tprime400_bWbW_Fall10MG7TeV-6a29f0fac22a95bcd534f59b8047bd70/USER',                 60, eleEt, 0, 'TPrime_400', 0, 1, 1],
##       ['/tprime450_bWbW_Fall10MG7TeV_AlexisLHE_v1/cjenkins-tprime450_bWbW_Fall10MG7TeV-42f4ff88835227db14d5f742f29d61de/USER',                 60, eleEt, 0, 'TPrime_400', 0, 1, 1],

      #################################################################################################################################################################
      #['/TTJets_TuneD6T_7TeV-madgraph-tauola/vasquez-ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',          30, eleEt, 0, 'Top',        0,  1, 1],
      #['/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/skhalil-ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',      50, eleEt, 1, 'Wjets',      0,  1, 1],
      #['/DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola/vasquez-ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER', 40, eleEt, 1, 'Zjets',      0,  1, 1],
      ['/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/skhalil-ttbsm_v7_Summer11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',       30, eleEt, 0, 'SingleTopT',  0, 1, 1],
      ['/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/skhalil-ttbsm_v7_Summer11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',      30, eleEt, 0, 'SingleToptW', 0, 1, 1],
      ['/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/skhalil-ttbsm_v7_Summer11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',       30, eleEt, 0, 'SingleTopS',  0, 1, 1],
      ['/GJets_TuneD6T_HT-40To100_7TeV-madgraph/vasquez-ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',       25, eleEt, 0, 'PhoJet40100', 0, 1, 1],
      ['/GJets_TuneD6T_HT-100To200_7TeV-madgraph/vasquez-ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',      25, eleEt, 0, 'PhoJet100200',0, 1, 1],
      ['/GJets_TuneD6T_HT-200_7TeV-madgraph/vasquez-ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',           25, eleEt, 0, 'PhoJet200Inf',0, 1, 1],
      ['/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6/skhalil-ttbsm_v7_Summer11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',      40, eleEt, 0, 'BCtoE2030',   0, 1, 1],
      ['/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6/skhalil-ttbsm_v7_Summer11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',      40, eleEt, 0, 'BCtoE3080',   0, 1, 1],
      ['/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia6/skhalil-ttbsm_v7_Summer11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER' ,    40, eleEt, 0, 'BCtoE80170',  0, 1, 1],
      ['/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6/samvel-ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',  60, eleEt, 0, 'EMEn2030',    0, 1, 1],
      ['/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6/skhalil-ttbsm_v7_Summer11-PU_S1_-START311_V1G1-v1-6a29f0fac22a95bcd534f59b8047bd70/USER',60, eleEt, 0, 'EMEn80170',   0, 1, 1],
      
      ###################################################################################################################################
      #__________For SHyFT PAT tuple use : run "shyftEDAnalyzer_allsys_ele.py" with option ttbsmPAT = 0"______________
      ###################################################################################################################################
      #['/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/makouski-shyft_414_v2-4102b2143a05266d07e3ed7d177f56c8/USER',   60, eleEt,  0, 'EMEn3080', 0, 1, 1],
      ]

for crabFileStr in crabFileStrs :
    print '------------------------- Operating on sample ' + crabFileStr[0] + ' ---------------------------'
    f = open(options.inputCfg, 'r')
    instring = f.read()

    # Get the dataset name, without the user-level stuff
    baseList = crabFileStr[0].split('/')
    
    if options.data == 1:
       outname = baseList[1] + options.outLabel+'_'+str(crabFileStr[9])+'_'+str(crabFileStr[10])
       outlocation = options.outLocation + baseList[1] + outputLable+'_'+str(crabFileStr[9])+'_'+str(crabFileStr[10])
    else:
       outname = baseList[1] + options.outLabel
       outlocation = options.outLocation + baseList[1] + outputLable
    
    # now do all of the substitutions
    a0 = instring.replace( 'DUMMY_DATASET', crabFileStr[0] )
    a1 = a0.replace( 'DUMMY_UI_DIR', outlocation)
    a2 = a1.replace( 'DUMMY_NJOBS', str(crabFileStr[1]) )
    a3 = a2.replace( 'DUMMY_CMSSW', inputCMSSW )
    a4 = a3.replace( 'DUMMY_THRESHOLD', str(crabFileStr[2]) )
    a5 = a4.replace( 'DUMMY_USEFLAVORHISTORY', str(crabFileStr[3]) )
    a6 = a5.replace( 'DUMMY_SAMPLENAMEINPUT', crabFileStr[4] )
    a7 = a6.replace( 'DUMMY_USE42X', str(crabFileStr[5]) )
    a8 = a7.replace( 'DUMMY_IGNORETRIGGER', str(crabFileStr[6]) )
    a9 = a8.replace( 'DUMMY_ALLSYS', str(crabFileStr[7]) )

    if options.data == 1:
       a10 = (a9.replace( ' allSys=0', '')).replace('total_number_of_events = -1', 'total_number_of_lumis = -1')
       #print crabFileStr[7]
       a11 = (a10.replace( 'DUMMY_TRIGGER', str(crabFileStr[8]) )).replace('DUMMY_RUNS', str(crabFileStr[9]) )
    else:
       a10 = (a9.replace( 'lumi_mask=Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v2.txt', '')).replace(' triggerName=DUMMY_TRIGGER', '')
       a11 = a10.replace( 'runselection = DUMMY_RUNS', '')
       
    # Dump the contents of the crab config to the screen
    print '------ Config : ------- '
    print a11
    

    # open the output file
    crabName = 'crab_' + outname + '.cfg'
    fout = open( crabName, 'w')
    # write the text to the output file
    fout.write( a11 )
    fout.close()
    print '------ CRAB starting up! ------'
    # now create the job:
    s = 'crab -create -cfg ' + crabName
    print s
    # and submit:
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + outlocation
    print s
    subprocess.call( [s], shell=True )


