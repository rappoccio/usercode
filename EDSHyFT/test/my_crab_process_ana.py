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
'VqqJets-madgraph_shyftana_38xOn35x_v13'


]

for idir in dirs :
    s = "crab -" + command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
