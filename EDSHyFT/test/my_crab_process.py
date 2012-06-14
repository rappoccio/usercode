#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
'InclusiveMu15_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'TTbarJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'WJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'ZJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
'VqqJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',

]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
