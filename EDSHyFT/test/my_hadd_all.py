#!/bin/python

import subprocess


dirs = [

'TTbarJets-madgraph_shyftana_38xOn35x_v2',
'WJets-madgraph_shyftana_38xOn35x_v2',
'ZJets-madgraph_shyftana_38xOn35x_v2',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v2',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v2',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v2',
'InclusiveMu15_shyftana_38xOn35x_v2',
'VqqJets-madgraph_shyftana_38xOn35x_v2'


]

for idir in dirs :
    s = "hadd " + idir + '.root ' + idir + "/res/*.root"
    print s
    subprocess.call( [s, ""], shell=True )
