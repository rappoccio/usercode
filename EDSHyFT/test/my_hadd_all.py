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


## 'WJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
## 'InclusiveMu15_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
## 'TTbarJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
## 'ZJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut',
## 'VqqJets-madgraph_shyftana_38xOn35x_v12_btagReweighted_JES_NoMETCut'




## 'TTbarJets-madgraph_shyftana_38xOn35x_v13',
## 'WJets-madgraph_shyftana_38xOn35x_v13',
## 'ZJets-madgraph_shyftana_38xOn35x_v13',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v13',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v13',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v13',
## 'InclusiveMu15_shyftana_38xOn35x_v13',
## 'VqqJets-madgraph_shyftana_38xOn35x_v13',

## 'TTbarJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
## 'WJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
## 'ZJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
## 'InclusiveMu15_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',
## 'VqqJets-madgraph_shyftana_38xOn35x_v14_btagReweighted_JES_NoMETCut',

## 'TTbarJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
## 'WJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
## 'ZJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
## 'InclusiveMu15_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',
## 'VqqJets-madgraph_shyftana_38xOn35x_v15_btagReweighted_JES_METCut',



## 'TTbarJets-madgraph_shyftana_38xOn35x_v17_allsys',
## 'WJets-madgraph_shyftana_38xOn35x_v17_allsys',
## 'ZJets-madgraph_shyftana_38xOn35x_v17_allsys',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v17_allsys',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v17_allsys',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v17_allsys',
## 'InclusiveMu15_shyftana_38xOn35x_v17_allsys',
## 'VqqJets-madgraph_shyftana_38xOn35x_v17_allsys',

## 'TTbarJets-madgraph_shyftana_38xOn35x_v18_allsys',
## 'WJets-madgraph_shyftana_38xOn35x_v18_allsys',
## 'ZJets-madgraph_shyftana_38xOn35x_v18_allsys',
## 'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v18_allsys',
## 'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v18_allsys',
## 'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v18_allsys',
## 'InclusiveMu15_shyftana_38xOn35x_v18_allsys',
## 'VqqJets-madgraph_shyftana_38xOn35x_v18_allsys',


'TTbarJets-madgraph_shyftana_38xOn35x_v19_allsys',
'WJets-madgraph_shyftana_38xOn35x_v19_allsys',
'ZJets-madgraph_shyftana_38xOn35x_v19_allsys',
'SingleTop_tWChannel-madgraph_shyftana_38xOn35x_v19_allsys',
'SingleTop_tChannel-madgraph_shyftana_38xOn35x_v19_allsys',
'SingleTop_sChannel-madgraph_shyftana_38xOn35x_v19_allsys',
'InclusiveMu15_shyftana_38xOn35x_v19_allsys',
'VqqJets-madgraph_shyftana_38xOn35x_v19_allsys',


]

for idir in dirs :
    s = "hadd " + idir + '.root ' + idir + "/res/*.root"
    print s
    subprocess.call( [s, ""], shell=True )
