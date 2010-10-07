#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [

'TTbarJets-madgraph_shyftana_38xOn35x_v13',
'WJets-madgraph_shyftana_38xOn35x_v13',
'ZJets-madgraph_shyftana_38xOn35x_v13',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v13',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v13',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v13',
'InclusiveMu15_shyftana_38xOn35x_v13',
'VqqJets-madgraph_shyftana_38xOn35x_v13',

'TTbarJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
'WJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
'ZJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
'InclusiveMu15_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
'VqqJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',

'TTbarJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
'WJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
'ZJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
'InclusiveMu15_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
'VqqJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',


]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
