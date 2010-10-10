# !/bin/python

import subprocess

crabFiles = [

    ['crab_InclusiveMu15_shyftana_38xOn35x_v15_btagReweighted_JES_METCut_anashyft.cfg',                  'InclusiveMu15_shyftana_38xOn35x_v15_btagReweighted_JES_METCut'],
    ['crab_SingleTop_sChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut_anashyft.cfg',    'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut'],
    ['crab_SingleTop_tChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut_anashyft.cfg',    'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut'],
    ['crab_SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut_anashyft.cfg',   'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut'],
    ['crab_TTbarJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut_anashyft.cfg',             'TTbarJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut'],
    ['crab_WJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut_anashyft.cfg',                 'WJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut'],
    ['crab_ZJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut_anashyft.cfg',                 'ZJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut'],
    ['crab_VqqJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut_anashyft.cfg',               'VqqJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut'],
    
    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
