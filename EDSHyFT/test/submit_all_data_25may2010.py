# !/bin/python

import subprocess

idir='/uscms/home/rappocc/SHyFT/CMSSW_3_6_1_SHyFT/src/Analysis/SHyFT/test'

datasets = [
'/MinimumBias/Commissioning10-May6thPDSkim2_SD_EG-v1/RECO',
'/MinimumBias/Commissioning10-May6thPDSkim2_SD_Mu-v1/RECO',
'/MinimumBias/Commissioning10-May6thPDSkim2_SD_JetMETTau-v1/RECO',
]

for dataset in datasets :
    toks = dataset.split('/')
    toks2 = toks[2].split('-')
    outdir = 'shyft_' + toks2[1] + '-' + toks2[2]
    s = './my_multicrab.pl crab_dummy.cfg shyft_data_35x.py '  + dataset + ' ' + outdir + ' -1 5 condor 0 ' + idir + ' ' + outdir
    print s
    subprocess.call( [s], shell=True )



datasets = [
'/Mu/Run2010A-PromptReco-v1/RECO',
'/EG/Run2010A-PromptReco-v1/RECO',
'/JetMETTau/Run2010A-PromptReco-v1/RECO'
]



for dataset in datasets :
    toks = dataset.split('/')
    toks2 = toks[2].split('-')
    outdir = 'shyft_' + toks[1] + '-' + toks2[2]
    s = './my_multicrab.pl crab_dummy.cfg shyft_data_35x.py '  + dataset + ' ' + outdir + ' -1 5 condor 0 ' + idir + ' ' + outdir
    print s
    subprocess.call( [s], shell=True )



datasets = [
'/Mu/Run2010A-PromptReco-v2/RECO',
'/EG/Run2010A-PromptReco-v2/RECO',
'/JetMETTau/Run2010A-PromptReco-v2/RECO'
]



for dataset in datasets :
    toks = dataset.split('/')
    toks2 = toks[2].split('-')
    outdir = 'shyft_' + toks[1] + '-' + toks2[2]
    s = './my_multicrab.pl crab_dummy.cfg shyft_data.py '  + dataset + ' ' + outdir + ' -1 5 condor 0 ' + idir + ' ' + outdir
    print s
    subprocess.call( [s], shell=True )


