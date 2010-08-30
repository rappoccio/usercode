# !/bin/python

import subprocess

idir='/uscms_data/d2/rappocc/analysis/SHyFT/CMSSW_3_8_2_SHyFT/src/Analysis/EDSHyFT/test'




crabFiles = [
   [ 'crab_InclusiveMu15_shyftana_38xOn35x_v1_anashyft.cfg',                    'InclusiveMu15_shyftana_38xOn35x_v1'],                  
   [ 'crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v1_anashyft.cfg',      'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v1'],    
   [ 'crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v1_anashyft.cfg',      'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v1'],    
   [ 'crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v1_anashyft.cfg',     'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v1'],   
   [ 'crab_TTbarJets-madgraph_shyftana_38xOn35x_v1_anashyft.cfg',               'TTbarJets-madgraph_shyftana_38xOn35x_v1'],             
   [ 'crab_WJets-madgraph_shyftana_38xOn35x_v1_anashyft.cfg',                   'WJets-madgraph_shyftana_38xOn35x_v1'],                 
   [ 'crab_ZJets-madgraph_shyftana_38xOn35x_v1_anashyft.cfg',                    'ZJets-madgraph_shyftana_38xOn35x_v1']                  
    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
