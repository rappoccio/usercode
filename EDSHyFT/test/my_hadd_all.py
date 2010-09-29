#!/bin/python

import subprocess


dirs = [

## 'InclusiveMu15_shyftana_38xOn35x_v7_JES_NoMET',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v7_JES_NoMET',
## 'TTbarJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET',
## 'WJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET',
## 'ZJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET',
## 'VqqJets-madgraph_shyftana_38xOn35x_v7_JES_NoMET',

## 'InclusiveMu15_shyftana_38xOn35x_v8_JES_METCUT',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v8_JES_METCUT',
## 'TTbarJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT',
## 'WJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT',
## 'ZJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT',
## 'VqqJets-madgraph_shyftana_38xOn35x_v8_JES_METCUT',

## 'WJets-madgraph_shyftana_38xOn35x_v9_bdisc',
## 'InclusiveMu15_shyftana_38xOn35x_v9_bdisc',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v9_bdisc',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v9_bdisc',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v9_bdisc',
## 'TTbarJets-madgraph_shyftana_38xOn35x_v9_bdisc',
## 'ZJets-madgraph_shyftana_38xOn35x_v9_bdisc',
## 'VqqJets-madgraph_shyftana_38xOn35x_v9_bdisc'


'WJets-madgraph_shyftana_38xOn35x_v10_bdisc',
'InclusiveMu15_shyftana_38xOn35x_v10_bdisc',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v10_bdisc',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v10_bdisc',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v10_bdisc',
'TTbarJets-madgraph_shyftana_38xOn35x_v10_bdisc',
'ZJets-madgraph_shyftana_38xOn35x_v10_bdisc',
'VqqJets-madgraph_shyftana_38xOn35x_v10_bdisc'
]

for idir in dirs :
    s = "hadd " + idir + '.root ' + idir + "/res/*.root"
    print s
    subprocess.call( [s, ""], shell=True )
