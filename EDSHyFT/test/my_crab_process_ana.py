#!/bin/python

import subprocess
import sys

command = sys.argv[1]

dirs = [

'InclusiveMu15_shyftana_38xOn35x_v18_allsys',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v18_allsys',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v18_allsys',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v18_allsys',
'TTbarJets-madgraph_shyftana_38xOn35x_v18_allsys',
'WJets-madgraph_shyftana_38xOn35x_v18_allsys',
'ZJets-madgraph_shyftana_38xOn35x_v18_allsys',
'VqqJets-madgraph_shyftana_38xOn35x_v18_allsys',


]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
