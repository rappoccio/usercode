# !/bin/python

import subprocess

idir='/uscms_data/d2/rappocc/analysis/SHyFT/CMSSW_3_8_2_SHyFT/src/Analysis/EDSHyFT/test'

datasets = [
['/TTbarJets-madgraph/srappocc-shyft_38xOn35x_v1-91f2fc34c53b68691c104fb43fa3e9f4/USER', 1],
['/WJets-madgraph/srappocc-shyft_38xOn35x_v1-91f2fc34c53b68691c104fb43fa3e9f4/USER', 5],
['/ZJets-madgraph/srappocc-shyft_38xOn35x_v1-91f2fc34c53b68691c104fb43fa3e9f4/USER', 1], 
['/SingleTop_tWChannel-madgraph/srappocc-shyft_38xOn35x_v1-91f2fc34c53b68691c104fb43fa3e9f4/USER', 1],
['/SingleTop_tChannel-madgraph/srappocc-shyft_38xOn35x_v1-91f2fc34c53b68691c104fb43fa3e9f4/USER', 1],
['/SingleTop_sChannel-madgraph/srappocc-shyft_38xOn35x_v1-91f2fc34c53b68691c104fb43fa3e9f4/USER', 1],
['/InclusiveMu15/srappocc-shyft_38xOn35x_v1-91f2fc34c53b68691c104fb43fa3e9f4/USER', 1]
]

#datasetsServer = [
#    ['/VqqJets-madgraph/Spring10-START3X_V26_S09-v1/GEN-SIM-RECO', 25],
#    ['/WCJets_7TeV-madgraph/Spring10-START3X_V26-v1/GEN-SIM-RECO', 25]
#    ]

for dataset in datasets :
    toks = dataset[0].split('/')
    s = './my_multicrab.pl crab_dummy_anashyft.cfg shyftEDAnalyzer.py '  + dataset[0] + ' shyftana_38xOn35x_v1 -1 ' + str(dataset[1]) + ' condor 0 ' + idir + ' ' + toks[1] + '_shyftana_38xOn35x_v1'
    print s
    subprocess.call( [s], shell=True )


#for dataset in datasetsServer :
#    toks = dataset[0].split('/')
#    s = './my_multicrab.pl crab_dummy_shyft.cfg shyft.py '  + dataset[0] + ' shyft_38xOn35x_v1 -1 ' + str(dataset[1]) + ' glite 1 ' + idir + ' ' + toks[1] + '_shyft_38xOn35x_v1'
#    print s
#    subprocess.call( [s], shell=True )
    
