#!/bin/python

import subprocess


dirs = [

'TTbarJets-madgraph_shyftana_38xOn35x_v20_allsys',
'WJets-madgraph_shyftana_38xOn35x_v20_allsys',
'ZJets-madgraph_shyftana_38xOn35x_v20_allsys',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v20_allsys',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v20_allsys',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v20_allsys',
'InclusiveMu15_shyftana_38xOn35x_v20_allsys',
'VqqJets-madgraph_shyftana_38xOn35x_v20_allsys',


]

for idir in dirs :
    s = "hadd " + idir + '.root ' + idir + "/res/*.root"
    print s
    subprocess.call( [s, ""], shell=True )
