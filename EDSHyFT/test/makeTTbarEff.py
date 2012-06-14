#! /usr/bin/env python

import ROOT
import sys
import array
import math
from DataFormats.FWLite import Events, Handle

filesLong = [
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_10_1_VxQ.root'
]

files = [
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_10_1_VxQ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_11_1_rEG.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_12_1_bNX.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_13_1_zpn.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_14_1_7Jl.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_15_1_zO3.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_16_1_Cmr.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_17_1_rCB.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_18_1_lqt.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_19_1_3p7.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_1_1_6sD.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_20_1_6AT.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_21_1_0Ea.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_22_1_gd5.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_23_1_SQA.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_24_1_FXF.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_25_1_dtq.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_26_1_25I.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_2_1_q0c.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_3_1_CPU.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_4_1_jsa.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_5_1_eho.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_6_1_Zrb.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_7_1_Hxz.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_8_1_wSc.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v4/11c19408717a8a2546a9b3c7cb40b7a6/shyft_382_mc_9_1_PA5.root',
    
    ]
events = Events (files)
calohandle  = Handle ("std::vector<pat::Jet>")
jpthandle  = Handle ("std::vector<pat::Jet>")
pfhandle  = Handle ("std::vector<pat::Jet>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
calolabel = ("selectedPatJets")
jptlabel = ("selectedPatJetsAK5JPT")
pflabel = ("selectedPatJetsPFlow")


f = ROOT.TFile("ttbarEff.root", "RECREATE")
f.cd()

binsPt = array.array( 'f', [0., 15., 20., 25., 30., 40., 60., 80., 100., 150., 300.] )
binsEta = array.array( 'f', [0., 1.4, 2.4] )

nbinsPt = len(binsPt)
nbinsEta = len(binsEta)

caloFbcp = ROOT.TH3F("caloFbcp", "Calo F_{bcp}", 3, 0, 3, 3, 0, 3, 6, 0, 6 )

caloBTags  = ROOT.TH2F("caloBTags", "Calo BTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
caloBJets  = ROOT.TH2F("caloBJets", "Calo BJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
caloBDisc  = ROOT.TH1F("caloBDisc", "Calo BDisc", 50, 0., 5.0 )

caloCTags  = ROOT.TH2F("caloCTags", "Calo CTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
caloCJets  = ROOT.TH2F("caloCJets", "Calo CJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
caloCDisc  = ROOT.TH1F("caloCDisc", "Calo CDisc", 50, 0., 5.0 )

caloLFTags  = ROOT.TH2F("caloLFTags", "Calo LFTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
caloLFJets  = ROOT.TH2F("caloLFJets", "Calo LFJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
caloLFDisc  = ROOT.TH1F("caloLFDisc", "Calo LFDisc", 50, 0., 5.0 )

caloGTags  = ROOT.TH2F("caloGTags", "Calo GTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
caloGJets  = ROOT.TH2F("caloGJets", "Calo GJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
caloGDisc  = ROOT.TH1F("caloGDisc", "Calo GDisc", 50, 0., 5.0 )

pfFbcp = ROOT.TH3F("pfFbcp", "Calo F_{bcp}", 3, 0, 3, 3, 0, 3, 6, 0, 6 )


pfBTags  = ROOT.TH2F("pfBTags", "Pf BTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
pfBJets  = ROOT.TH2F("pfBJets", "Pf BJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
pfBDisc  = ROOT.TH1F("pfBDisc", "Pf BDisc", 50, 0., 5.0 )

pfCTags  = ROOT.TH2F("pfCTags", "Pf CTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
pfCJets  = ROOT.TH2F("pfCJets", "Pf CJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
pfCDisc  = ROOT.TH1F("pfCDisc", "Pf CDisc", 50, 0., 5.0 )

pfLFTags  = ROOT.TH2F("pfLFTags", "Pf LFTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
pfLFJets  = ROOT.TH2F("pfLFJets", "Pf LFJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
pfLFDisc  = ROOT.TH1F("pfLFDisc", "Pf LFDisc", 50, 0., 5.0 )

pfGTags  = ROOT.TH2F("pfGTags", "Pf GTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
pfGJets  = ROOT.TH2F("pfGJets", "Pf GJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
pfGDisc  = ROOT.TH1F("pfGDisc", "Pf GDisc", 50, 0., 5.0 )

jptFbcp = ROOT.TH3F("jptFbcp", "Calo F_{bcp}", 3, 0, 3, 3, 0, 3, 6, 0, 6 )

jptBTags  = ROOT.TH2F("jptBTags", "Jpt BTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
jptBJets  = ROOT.TH2F("jptBJets", "Jpt BJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
jptBDisc  = ROOT.TH1F("jptBDisc", "Jpt BDisc", 50, 0., 5.0 )

jptCTags  = ROOT.TH2F("jptCTags", "Jpt CTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
jptCJets  = ROOT.TH2F("jptCJets", "Jpt CJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
jptCDisc  = ROOT.TH1F("jptCDisc", "Jpt CDisc", 50, 0., 5.0 )

jptLFTags  = ROOT.TH2F("jptLFTags", "Jpt LFTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
jptLFJets  = ROOT.TH2F("jptLFJets", "Jpt LFJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
jptLFDisc  = ROOT.TH1F("jptLFDisc", "Jpt LFDisc", 50, 0., 5.0 )

jptGTags  = ROOT.TH2F("jptGTags", "Jpt GTags", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
jptGJets  = ROOT.TH2F("jptGJets", "Jpt GJets", nbinsPt-1, binsPt, nbinsEta-1, binsEta )
jptGDisc  = ROOT.TH1F("jptGDisc", "Jpt GDisc", 50, 0., 5.0 )

calohists = [
    [caloBJets, caloBTags, caloBDisc],
    [caloCJets, caloCTags, caloCDisc],
    [caloGJets, caloGTags, caloGDisc],
    [caloLFJets, caloLFTags, caloLFDisc],    
    ]

pfhists = [
    [pfBJets, pfBTags, pfBDisc],
    [pfCJets, pfCTags, pfCDisc],
    [pfGJets, pfGTags, pfGDisc],
    [pfLFJets, pfLFTags, pfLFDisc],    
    ]

jpthists = [
    [jptBJets, jptBTags, jptBDisc],
    [jptCJets, jptCTags, jptCDisc],
    [jptGJets, jptGTags, jptGDisc],
    [jptLFJets, jptLFTags, jptLFDisc],    
    ]


#### Helper class to fill histograms
def fillHists( jet, discname, bhists, chists, ghists, lfhists ) :
    pt = jet.pt()
    if pt > 299. :
        pt = 299.
    flav = abs( jet.partonFlavour() )
    disc =jet.bDiscriminator(discname) 
    tagged = disc > 1.74 
    if flav == 5 :
        bhists[0].Fill( pt, math.fabs(jet.eta()) )
        if tagged :
            bhists[1].Fill( pt, math.fabs(jet.eta() ) )
        bhists[2].Fill( disc )
    elif flav == 4:
        chists[0].Fill( pt, math.fabs(jet.eta()) )
        if tagged :
            chists[1].Fill( pt, math.fabs(jet.eta() ) )
            chists[2].Fill( disc )
    elif flav == 21:
        ghists[0].Fill( pt, math.fabs(jet.eta()) )
        if tagged :
            ghists[1].Fill( pt, math.fabs(jet.eta() ) )
        ghists[2].Fill( disc )
    else :
        lfhists[0].Fill( pt, math.fabs(jet.eta()) )
        if tagged :
            lfhists[1].Fill( pt, math.fabs(jet.eta() ) )
        lfhists[2].Fill( disc )            


### Helper class to get the jet product, and drive the helper to
### fill histograms
def runJets( disc, ptCut, handle, label, hists ) :

    nb = 0
    nc = 0
    np = 0
    # use getByLabel, just like in cmsRun
    event.getByLabel (label, handle)
    # get the product
    jets = handle.product()
    for jet in jets :
        if abs(jet.partonFlavour()) == 5:
            nb += 1
        elif abs(jet.partonFlavour()) == 4:
            nc += 1
        else :
            np += 1
        if jet.pt() > ptCut :
            fillHists( jet,disc,
                       hists[0], hists[1], hists[2], hists[3]
                       )
    return [nb,nc,np]

# loop over events
i = 0
for event in events:
    i = i + 1
    if i % 10000 == 0:
        print 'Processing event ' + str(i)


    [caloNb, caloNc, caloNp] = runJets(  'simpleSecondaryVertexBJetTags',             
                                         30.,
                                         calohandle,
                                         calolabel,
                                         calohists )
    if caloNb > 2 :
        caloNb = 2
    if caloNc > 2 :
        caloNc = 2
    if caloNp > 5 :
        caloNp = 5
    caloFbcp.Fill( caloNb, caloNc, caloNp )


    [jptNb, jptNc, jptNp] = runJets( 'simpleSecondaryVertexHighEffBJetTags',             
                                     30.,
                                     jpthandle,
                                     jptlabel,
                                     jpthists )
    if jptNb > 2 :
        jptNb = 2
    if jptNc > 2 :
        jptNc = 2
    if jptNp > 5 :
        jptNp = 5
    jptFbcp.Fill( jptNb, jptNc, jptNp )


    [pfNb, pfNc, pfNp] = runJets( 'simpleSecondaryVertexHighEffBJetTags',             
                                  25.,
                                  pfhandle,
                                  pflabel,
                                  pfhists )
    if pfNb > 2 :
        pfNb = 2
    if pfNc > 2 :
        pfNc = 2
    if pfNp > 5 :
        pfNp = 5
    pfFbcp.Fill( pfNb, pfNc, pfNp )

f.cd()
for iihist in calohists :
    for jjhist in iihist :
        jjhist.Write()

for iihist in pfhists :
    for jjhist in iihist :
        jjhist.Write()

for iihist in jpthists :
    for jjhist in iihist :
        jjhist.Write()


caloFbcp.Write()
jptFbcp.Write()
pfFbcp.Write()
f.Close()

