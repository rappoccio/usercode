# !/bin/python

import subprocess

idir='/uscms_data/d2/rappocc/analysis/SHyFT/CMSSW_3_8_3_SHyFT/src/Analysis/EDSHyFT/test'

datasets = [
['/TTbarJets-madgraph/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 25],
['/WJets-madgraph/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 100],
['/ZJets-madgraph/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 25],
['/SingleTop_tChannel-madgraph/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 10],
['/SingleTop_tWChannel-madgraph/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 10],
['/InclusiveMu15/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 25],
['/SingleTop_sChannel-madgraph/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 10]
]

datasetsServer = [
#    ['/VqqJets-madgraph/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 25]
#    ['/WCJets_7TeV-madgraph/Spring10-START3X_V26-v1/GEN-SIM-RECO', 25]
    ]

for dataset in datasets :
    toks = dataset[0].split('/')
    s = './my_multicrab.pl crab_dummy_shyft.cfg shyft.py '  + dataset[0] + ' shyft_38xOn35x_v5 -1 ' + str(dataset[1]) + ' condor 0 ' + idir + ' ' + toks[1] + '_shyft_38xOn35x_v5'
    print s
    subprocess.call( [s], shell=True )


for dataset in datasetsServer :
    toks = dataset[0].split('/')
    s = './my_multicrab.pl crab_dummy_shyft.cfg shyft.py '  + dataset[0] + ' shyft_38xOn35x_v5 -1 ' + str(dataset[1]) + ' glite 1 ' + idir + ' ' + toks[1] + '_shyft_38xOn35x_v5'
    print s
    subprocess.call( [s], shell=True )
    
