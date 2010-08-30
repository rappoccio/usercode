#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [

#'TTbarJets-madgraph_shyft_38xOn35x_v1',
#'WJets-madgraph_shyft_38xOn35x_v1',
#'ZJets-madgraph_shyft_38xOn35x_v1',
#'SingleTop_tChannel-madgraph_shyft_38xOn35x_v1',
#'SingleTop_tWChannel-madgraph_shyft_38xOn35x_v1',
#'InclusiveMu15_shyft_38xOn35x_v1',
#'SingleTop_sChannel-madgraph_shyft_38xOn35x_v1'
'VqqJets-madgraph_shyft_38xOn35x_v1',
'WCJets_7TeV-madgraph_shyft_38xOn35x_v1'


]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
