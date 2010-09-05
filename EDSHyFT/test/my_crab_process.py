#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [
'InclusiveMu15_shyft_38xOn35x_v2',
'SingleTop_sChannel-madgraph_shyft_38xOn35x_v2',
'SingleTop_tChannel-madgraph_shyft_38xOn35x_v2',
'SingleTop_tWChannel-madgraph_shyft_38xOn35x_v2',
'TTbarJets-madgraph_shyft_38xOn35x_v2',
'VqqJets-madgraph_shyft_38xOn35x_v2',
'WJets-madgraph_shyft_38xOn35x_v2',
'ZJets-madgraph_shyft_38xOn35x_v2',
'shyft_38xOn35x_v2_r1',
'shyft_38xOn35x_v2_r2',
'shyft_38xOn35x_v2_r3'
]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
