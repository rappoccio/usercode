# !/bin/python

import subprocess


crabFiles = [
    [ 'crab_InclusiveMu15_shyftana_38xOn35x_v13_anashyft.cfg',                    'InclusiveMu15_shyftana_38xOn35x_v13'],                  
    [ 'crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',      'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v13'],    
    [ 'crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',      'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v13'],    
    [ 'crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',     'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v13'],   
    [ 'crab_TTbarJets-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',               'TTbarJets-madgraph_shyftana_38xOn35x_v13'],             
    [ 'crab_WJets-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',                   'WJets-madgraph_shyftana_38xOn35x_v13'],                 
    [ 'crab_ZJets-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',                   'ZJets-madgraph_shyftana_38xOn35x_v13'],
    [ 'crab_VqqJets-madgraph_shyftana_38xOn35x_v13_anashyft.cfg',                 'VqqJets-madgraph_shyftana_38xOn35x_v13']
    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
