#! /usr/bin/env python
import os
import glob

import ROOT

import sys
from DataFormats.FWLite import Events, Handle

fileDir = sys.argv[1]
#fileDir = "Jet_Run2011A-May10ReReco_ttbsm_v6_ttbsmTuples_v3"
#files = ["./Jet_Run2011A-May10ReReco_ttbsm_v6_ttbsmTuples_v3/res/ttbsm_ultraslim_1_1_XE7.root"]
files = glob.glob( fileDir + "/res/*.root" )
print files


events = Events (files)

hemis0Handle   = Handle ("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
hemis0Label    = ( "ttbsmAna", "topTagP4Hemis0" )

hemis0MinMassHandle     = Handle( "std::vector<double>" )
hemis0MinMassLabel  = ( "ttbsmAna", "topTagMinMassHemis0" )

hemis0NSubjetsHandle    = Handle( "std::vector<double>" )
hemis0NSubjetsLabel = ( "ttbsmAna", "topTagNSubjetsHemis0"  )

hemis0TopMassHandle     = Handle( "std::vector<double>" )
hemis0TopMassLabel  = ( "ttbsmAna", "topTagTopMassHemis0" )

hemis0PassHandle        = Handle( "std::vector<int>")
hemis0PassLabel   = ( "ttbsmAna", "topTagPassHemis0" )

hemis1Handle     = Handle( "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
hemis1Label      = ( "ttbsmAna", "wTagP4Hemis1" )

hemis1BdiscHandle         = Handle( "std::vector<double>" )
hemis1BdiscLabel    = ( "ttbsmAna",   "wTagBDiscHemis1" )

hemis1MuHandle           = Handle( "std::vector<double>")
hemis1MuLabel      = ( "ttbsmAna",  "wTagMuHemis1" )

hemis1Jet3Handle    = Handle("int")
hemis1Jet3Label     = ( "ttbsmAna", "jet3Hemis1" )



#f = ROOT.TFile("TTHadronicAnalyzer.root", "recreate")
f = ROOT.TFile( fileDir + ".root", "recreate" )
f.cd()

print "Creating histograms"

nJets             = ROOT.TH1F("nJets",         "Number of Jets",               20, -0.5, 19.5 )
topJetCandEta        = ROOT.TH1F("topJetCandEta",     "Top Cand eta",                 50,   -3.0, 3.0 )
wCandVsTopCandMass      = ROOT.TH2F("wCandVsTopCandMass",  "W Cand Vs Top Cand Mass",  50, 0,  250,  100,  0,  500 )
wCandWithMassVsTopCandMass  = ROOT.TH2F("wCandWithMassVsTopCandMass",  "W Cand Vs Top Cand Mass",  50, 0,  250,  100,  0,  500 )
wCandVsTopCandMassType12    = ROOT.TH2F("wCandVsTopCandMassType12",    "Top Cand Vs W Cand Mass",  50, 0,  250,  100,  0,  500 )
wCandVsTopCandMassType12WithTopTag  = ROOT.TH2F("wCandVsTopCandMassType12WithTopTag",  "Top Cand Vs W Cand Mass", 50,  0,  250,  100,  0,  500 )
wCandMassType12             = ROOT.TH1F("wCandMassType12",             "W Cand Mass",              50, 0,  250 )
wCandMassType12AfterTopTag  = ROOT.TH1F("wCandMassType12AfterTopTag",  "W Cand Mass",              50, 0,  250 )
wCandPtType12               = ROOT.TH1F("wCandPtType12",               "W Cand Pt",                200,  0,  1000 )
wCandPtType12AfterTopTag    = ROOT.TH1F("wCandPtType12AfterTopTag",    "W Cand Pt",                200,  0,  1000 )
nearJetPt                   = ROOT.TH1F("nearJetPt",                   "Near Jet Pt",              200,  0,  1000 )
nearJetPtAfterTopTag        = ROOT.TH1F("nearJetPtAfterTopTag",        "Near Jet Pt",              200,  0,  1000 )
nearJetbValue               = ROOT.TH1F("nearJetbValue",               "Near Jet b Discriminator", 100,  0,  20 )
nearJetbValueAfterTopTag    = ROOT.TH1F("nearJetbValueAfterTopTag",    "Near Jet b Discriminator", 100,  0,  20 )
topJetCandPtSignal          = ROOT.TH1F("topJetCandPtSignal",          "Top Jet Cand Pt",          200,  0,  1000 )
topJetCandPtSideBand        = ROOT.TH1F("topJetCandPtSideBand",        "Top Jet Cand Pt",          200,  0,  1000 )
topJetCandMassSignal        = ROOT.TH1F("topJetCandMassSignal",        "Top Jet Cand Mass",        100,  0,  500 )
topJetCandMassSideBand      = ROOT.TH1F("topJetCandMassSideBand",      "Top Jet Cand Mass",        100,  0,  500 )
topJetNsubsSignal           = ROOT.TH1F("topJetNsubsSignal",           "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
topJetNsubsSideBand         = ROOT.TH1F("topJetNsubsSideBand",         "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
topJetMinMassSignal         = ROOT.TH1F("topJetMinMassSignal",         "Top Jet Min Mass",         100,  0,  500 )
topJetMinMassSideBand       = ROOT.TH1F("topJetMinMassSideBand",       "Top Jet Min Mass",         100,  0,  500 )
pairMassType12              = ROOT.TH1F("pairMassType12",              "Pair Jet Mass",            200,  0,  1000 )
pairMassType12AfterTopTag   = ROOT.TH1F("pairMassType12AfterTopTag",   "Pair Jet Mass",            200,  0,  1000 )
pairMassType12AfterTopTagWithWMass  = ROOT.TH1F("pairMassType12AfterTopTagWithWMass",    "Pair Jet Mass",            200,  0,  1000 )
topJetCandMass              = ROOT.TH1F("topJetCandMass",              "Top Jet Cand Mass",        100,  0,  500 )
topJetCandPt                = ROOT.TH1F("topJetCandPt",                "Top Jet Cand Pt",          400,  0,  2000 )
topTagMass                  = ROOT.TH1F("topTagMass",                  "Top Tag Mass",             100,  0,  500 )
topTagPt                    = ROOT.TH1F("topTagPt",                    "Top Tag Pt",               400,  0,  2000 )
mttMass                     = ROOT.TH1F("mttMass",                     "mTT Mass",                 1000, 0,  5000 )
mttMassWithBTag             = ROOT.TH1F("mttMassWithBTag",             "mTT Mass With BTag",       1000, 0,  5000 )
jet3BTagPt                  = ROOT.TH1F("jet3BTagPt",                  "Jet 3 BTag",               200,   0,  1000 )
mttBkgShape                 = ROOT.TH1F("mttBkgShape",                 "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithMassCut      = ROOT.TH1F("mttBkgShapeWithMassCut",      "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBandMass = ROOT.TH1F("mttBkgShapeWithSideBandMass", "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand1Mass = ROOT.TH1F("mttBkgShapeWithSideBand1Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand2Mass = ROOT.TH1F("mttBkgShapeWithSideBand2Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand3Mass = ROOT.TH1F("mttBkgShapeWithSideBand3Mass",  "mTT Bkg Shape",            1000, 0,  5000 )

signalTopTagEta             = ROOT.TH1F("signalTopTagEta",              "Top Tag Eta",              100,  -3, 3 )
signalJet3TagEta            = ROOT.TH1F("signalJet3TagEta",             "Jet 3 Eta",                100,  -3, 3 )

checkWTag = 0

# loop over events
count = 0
print "Start looping"
for event in events:
    count = count + 1
    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count)


    event.getByLabel (hemis0Label, hemis0Handle)
    topJets = hemis0Handle.product()
    event.getByLabel (hemis1Label, hemis1Handle)
    wJets = hemis1Handle.product()
    event.getByLabel (hemis0MinMassLabel, hemis0MinMassHandle)
    topJetMinMass = hemis0MinMassHandle.product()
    event.getByLabel (hemis0NSubjetsLabel, hemis0NSubjetsHandle)
    topJetNSubjets = hemis0NSubjetsHandle.product()
    event.getByLabel (hemis0TopMassLabel, hemis0TopMassHandle)
    topJetMass = hemis0TopMassHandle.product()
    event.getByLabel (hemis1BdiscLabel, hemis1BdiscHandle)
    wJetBDisc = hemis1BdiscHandle.product()
    event.getByLabel (hemis0PassLabel, hemis0PassHandle )
    topJetPass = hemis0PassHandle.product()
    event.getByLabel (hemis1MuLabel, hemis1MuHandle)
    wJetMu = hemis1MuHandle.product()
    event.getByLabel (hemis1Jet3Label, hemis1Jet3Handle )
    jet3 = (hemis1Jet3Handle.product())[0]

######### calculate pair mass and set cuts here
    nTopCand = 0
    for i in range(0,len(topJets) ) :
      if( topJets[i].pt() > 400 ) :
        nTopCand = nTopCand + 1

    pairMass = 0.0
    ttMass = 0.0
    if nTopCand < 1 or len(wJets) < 2 :
      continue
    if jet3 < 1 :
      print "This is not expected, debug!"
      #print "The third jet is ", jet3, " pt is ", wJets[jet3].pt(), " eta is ", wJets[jet3].eta()
      #print "N hemis1 is ", len(wJets)

    pairMass = (wJets[jet3]+wJets[0]).mass()
    ttMass = (wJets[jet3]+wJets[0]+topJets[0]).mass()

    passKinCuts = (nTopCand == 1) and (wJets[0].pt() > 200)  and (wJetMu[0] < 0.4) and (wJets[jet3].pt() > 30 )
    hasBTag1    = wJetBDisc[jet3] > 3.3
    hasType2Top = wJets[0].mass() > 60 and wJets[0].mass() < 130 and pairMass > 140 and pairMass < 250
    hasTopTag   = topJetMass[0] > 140 and topJetMass[0] < 250 and topJetMinMass[0] > 50 and topJetNSubjets[0] > 2
    SBAndSR     = wJets[0].mass() > 40 and wJets[0].mass() < 150 and pairMass > 100 and pairMass < 300
    SBAndSR2    = wJets[0].mass() > 20 and wJets[0].mass() < 170 and pairMass > 60  and pairMass < 350
    passWiderTopMassCut   =   topJetMass[0] > 100 and topJetMass[0] < 300
    topMassSideBand       =   (topJetMass[0] > 100 and topJetMass[0] < 140) or (topJetMass[0] > 250 and topJetMass[0] < 300)
    for i in range(1,len(wJets) ) :
      if( wJets[i].pt() > 200 and wJets[i].mass() > 60 and wJets[i].mass() < 130 and wJetMu[i] < 0.4 )  :
        checkWTag += 1
        break

######### Plot histograms
    if passKinCuts  :
      nJets.Fill( len(topJets)+len(wJets) )
      topJetCandMass.Fill( topJets[0].mass() )
      topJetCandEta.Fill( topJets[0].eta() )
      topJetCandPt.Fill( topJets[0].pt() )
      wCandMassType12.Fill( wJets[0].mass() )
      wCandPtType12.Fill( wJets[0].pt() )
      pairMassType12.Fill( pairMass )
      nearJetPt.Fill( wJets[jet3].pt() )
      nearJetbValue.Fill( wJetBDisc[jet3] )

      mttBkgShape.Fill( ttMass )
      wCandVsTopCandMassType12.Fill( wJets[0].mass() ,  pairMass )

      if hasTopTag  :
        topTagMass.Fill( topJets[0].mass() )
        topTagPt.Fill( topJets[0].mass() )
        wCandMassType12AfterTopTag.Fill( wJets[0].mass() )
        wCandPtType12AfterTopTag.Fill( wJets[0].pt() )
        nearJetPtAfterTopTag.Fill( wJets[jet3].pt() )
        nearJetbValueAfterTopTag.Fill( wJetBDisc[jet3] )
        pairMassType12AfterTopTag.Fill( pairMass )
        if wJets[0].mass() > 60 and wJets[0].mass() < 130 :
          pairMassType12AfterTopTagWithWMass.Fill( pairMass )
        wCandVsTopCandMassType12WithTopTag.Fill( wJets[0].mass() ,  pairMass )

      if hasType2Top  :
        topJetCandPtSignal.Fill( topJets[0].pt() )
        topJetCandMassSignal.Fill( topJets[0].mass() )
        topJetNsubsSignal.Fill( topJetNSubjets[0] )
        topJetMinMassSignal.Fill( topJetMinMass[0] )
      if SBAndSR and (not hasType2Top) :
        topJetCandPtSideBand.Fill( topJets[0].pt() )
        topJetCandMassSideBand.Fill( topJets[0].mass() )
        topJetNsubsSideBand.Fill( topJetNSubjets[0] )
        topJetMinMassSideBand.Fill( topJetMinMass[0] )

      if SBAndSR and passWiderTopMassCut :
        mttBkgShapeWithMassCut.Fill( ttMass )
      if SBAndSR and (not hasType2Top) and topMassSideBand :
        mttBkgShapeWithSideBandMass.Fill( ttMass )
      if SBAndSR and (not hasType2Top) and passWiderTopMassCut :
        mttBkgShapeWithSideBand1Mass.Fill( ttMass )
      if SBAndSR and (not hasType2Top) :
        mttBkgShapeWithSideBand2Mass.Fill( ttMass )
      if SBAndSR2 and (not SBAndSR ) and passWiderTopMassCut :
        mttBkgShapeWithSideBand3Mass.Fill( ttMass )

      if hasType2Top and hasTopTag :
        mttMass.Fill( ttMass )
        if hasBTag1 :
          mttMassWithBTag.Fill( ttMass )
          jet3BTagPt.Fill( wJets[jet3].pt() )
          signalTopTagEta.Fill( topJets[0].eta() )
          signalJet3TagEta.Fill( wJets[jet3].eta() )

f.cd()
f.Write()
f.Close()

print checkWTag



