# !/bin/python

import subprocess

crabFiles = [
    ['crab_InclusiveMu15_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut_anashyft.cfg',                  'InclusiveMu15_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut'],
    ['crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut_anashyft.cfg',    'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut'],
    ['crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut_anashyft.cfg',    'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut'],
    ['crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut_anashyft.cfg',   'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut'],
    ['crab_TTbarJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut_anashyft.cfg',             'TTbarJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut'],
    ['crab_WJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut_anashyft.cfg',                 'WJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut'],
    ['crab_ZJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut_anashyft.cfg',                 'ZJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut'],
    ['crab_VqqJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut_anashyft.cfg',               'VqqJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut']
    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
