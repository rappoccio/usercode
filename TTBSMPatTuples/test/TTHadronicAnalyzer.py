#! /usr/bin/env python
import os
import glob
import copy

import ROOT
ROOT.gSystem.Load("libFWCoreFWLite")
ROOT.AutoLibraryLoader.enable()
ROOT.gSystem.Load("libAnalysisBoostedTopAnalysis")

import sys
from DataFormats.FWLite import Events, Handle

from optparse import OptionParser


parser = OptionParser()

parser.add_option('-i', '--inputDir', metavar='F', type='string', action='store',
                  default='Jet_Run2011A-PromptReco-v4_range1_ttbsm_v6_ttbsmTuples_v3',
                  dest='inputDir',
                  help='Input Dir')



parser.add_option('-p', '--prefix', metavar='N', type='string', action='store',
                  default='./',
                  dest='prefix',
                  help='Dir prefix')


(options, args) = parser.parse_args()

#fileDir = "Jet_Run2011A-May10ReReco_ttbsm_v6_ttbsmTuples_v3"
#files = ["./Jet_Run2011A-May10ReReco_ttbsm_v6_ttbsmTuples_v3/res/ttbsm_ultraslim_1_1_XE7.root"]
#remoteDir = "/uscms_data/d2/guofan/analysis/CMSSW_4_1_5/src/Analysis/TTBSMPatTuples/test/"
#Zprime dir "/uscms_data/d2/guofan/analysis/CMSSW_3_8_7_patch2/src/Analysis/TTBSMPatTuples/test/"
files = glob.glob( options.prefix + '/' + options.inputDir + "/res/*.root" )
print files


events = Events (files)

allTopTagHandle = Handle (  "vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >"  )
allTopTagLabel  = ( "ttbsmAna",   "topTagP4")
allTopTagMinMassHandle  = Handle( "std::vector<double>" )
allTopTagMinMassLabel   = ( "ttbsmAna",   "topTagMinMass" )
allTopTagNSubsHandle    = Handle("std::vector<double>" )
allTopTagNSubsLabel     = ( "ttbsmAna",   "topTagNSubjets" )

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

rhoHandle           = Handle("double")
rhoLabel            = ( "ttbsmAna", "rho" )



#f = ROOT.TFile("TTHadronicAnalyzer.root", "recreate")
f = ROOT.TFile( options.inputDir + ".root", "recreate" )
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
thirdLeadJetbValue          = ROOT.TH1F("thirdLeadJetbValue",           "Third Lead Jet b Discriminator", 100,  0,  20 )
thirdLeadJetPt              = ROOT.TH1F("thirdLeadJetPt",               "Third Lead Jet PT",        200,  0,  1000 )
topJetCandPtSignal          = ROOT.TH1F("topJetCandPtSignal",          "Top Jet Cand Pt",          200,  0,  1000 )
topJetCandPtSideBand        = ROOT.TH1F("topJetCandPtSideBand",        "Top Jet Cand Pt",          200,  0,  1000 )
topJetCandPtAll             = ROOT.TH1F("topJetCandPtAll",             "Top Jet Cand Pt",          200,  0,  1000 )
topJetCandMassSignal        = ROOT.TH1F("topJetCandMassSignal",        "Top Jet Cand Mass",        100,  0,  500 )
topJetCandMassSideBand      = ROOT.TH1F("topJetCandMassSideBand",      "Top Jet Cand Mass",        100,  0,  500 )
topJetCandMassAll           = ROOT.TH1F("topJetCandMassAll",            "Top Jet Cand Mass",        100,  0,  500 )
topJetNsubsSignal           = ROOT.TH1F("topJetNsubsSignal",           "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
topJetNsubsSideBand         = ROOT.TH1F("topJetNsubsSideBand",         "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
topJetNsubsAll              = ROOT.TH1F("topJetNsubsAll",               "Top Jet Cand N Subjets",   10,   -0.5, 9.5 )
topJetMinMassSignal         = ROOT.TH1F("topJetMinMassSignal",         "Top Jet Min Mass",         100,  0,  500 )
topJetMinMassSideBand       = ROOT.TH1F("topJetMinMassSideBand",       "Top Jet Min Mass",         100,  0,  500 )
topJetMinMassAll            = ROOT.TH1F("topJetMinMassAll",             "Top Jet Min Mass",         100,  0,  500 )
pairMassType12              = ROOT.TH1F("pairMassType12",              "Pair Jet Mass",            200,  0,  1000 )
pairMassType12AfterTopTag   = ROOT.TH1F("pairMassType12AfterTopTag",   "Pair Jet Mass",            200,  0,  1000 )
pairMassType12AfterTopTagWithWMass  = ROOT.TH1F("pairMassType12AfterTopTagWithWMass",    "Pair Jet Mass",            200,  0,  1000 )
topJetCandMass              = ROOT.TH1F("topJetCandMass",              "Top Jet Cand Mass",        100,  0,  500 )
topJetCandPt                = ROOT.TH1F("topJetCandPt",                "Top Jet Cand Pt",          400,  0,  2000 )
topTagMass                  = ROOT.TH1F("topTagMass",                  "Top Tag Mass",             100,  0,  500 )
topTagPt                    = ROOT.TH1F("topTagPt",                    "Top Tag Pt",               400,  0,  2000 )
mttMass                     = ROOT.TH1F("mttMass",                     "mTT Mass",                 1000, 0,  5000 )
mttMassJet1MassDown         = ROOT.TH1F("mttMassJet1MassDown",         "mTT Mass",                 1000, 0,  5000 )
mttBkgWithMistag            = ROOT.TH1F("mttBkgWithMistag",            "mTT Mass",                 1000, 0,  5000 )
mttBkgWithMistag.Sumw2()
mttBkgWithMistagModMass     = ROOT.TH1F("mttBkgWithMistagModMass",     "mTT Mass",                 1000, 0,  5000 )
mttBkgWithMistagModMass.Sumw2()
mttBkgWithMistagMod2Mass    = ROOT.TH1F("mttBkgWithMistagMod2Mass",    "mTT Mass",                 1000, 0,  5000 )
mttBkgWithMistagMod2Mass.Sumw2()
mttBkgWithMistagUp          = ROOT.TH1F("mttBkgWithMistagUp",          "mTT Mass",                 1000, 0,  5000 )
mttBkgWithMistagUp.Sumw2()
mttBkgWithMistagDown        = ROOT.TH1F("mttBkgWithMistagDown",        "mTT Mass",                 1000, 0,  5000 )
mttBkgWithMistagDown.Sumw2()
mttMassWithBTag             = ROOT.TH1F("mttMassWithBTag",             "mTT Mass With BTag",       1000, 0,  5000 )
jet3BTagPt                  = ROOT.TH1F("jet3BTagPt",                  "Jet 3 BTag",               200,   0,  1000 )
mttBkgShape                 = ROOT.TH1F("mttBkgShape",                 "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeMassUp           = ROOT.TH1F("mttBkgShapeMassUp",           "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeMassDown         = ROOT.TH1F("mttBkgShapeMassDown",         "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithMassCut      = ROOT.TH1F("mttBkgShapeWithMassCut",      "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBandMass = ROOT.TH1F("mttBkgShapeWithSideBandMass", "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand1Mass = ROOT.TH1F("mttBkgShapeWithSideBand1Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand2Mass = ROOT.TH1F("mttBkgShapeWithSideBand2Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand3Mass = ROOT.TH1F("mttBkgShapeWithSideBand3Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand4Mass = ROOT.TH1F("mttBkgShapeWithSideBand4Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand5Mass = ROOT.TH1F("mttBkgShapeWithSideBand5Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand6Mass = ROOT.TH1F("mttBkgShapeWithSideBand6Mass",  "mTT Bkg Shape",            1000, 0,  5000 )
mttBkgShapeWithSideBand7Mass = ROOT.TH1F("mttBkgShapeWithSideBand7Mass",  "mTT Bkg Shape",            1000, 0,  5000 )

type2TopProbe               = ROOT.TH1F("type2TopProbe",              "Top Probe Pt",               400,  0,  2000 )
type2TopTag                 = ROOT.TH1F("type2TopTag",                "Top Tag Pt",                 400,  0,  2000 )
type2TopTagMass             = ROOT.TH1F("type2TopTagMass",            "Top Tag Mass",               400,  0,  2000 )
type2TopTagExp              = ROOT.TH1F("type2TopTagExp",             "Top Tag Pt Expected",        400,  0,  2000 )
type2TopTagExp.Sumw2()
jet1MassTag                 = ROOT.TH1F("jet1MassTag",                "Jet 1 Mass",                 400,  0,  2000 )
jet1MassMod                 = ROOT.TH1F("jet1MassMod",                "Jet 1 Mass",                 400,  0,  2000 )
jet1MassExp                 = ROOT.TH1F("jet1MassExp",                "Jet 1 Mass",                 400,  0,  2000 )
jet1MassExp.Sumw2()
jet1EtaTag                  = ROOT.TH1F("jet1EtaTag",                 "Jet 1 Eta",                  50,   -2.5, 2.5 )
jet1EtaExp                  = ROOT.TH1F("jet1EtaExp",                 "Jet 1 Eta",                  50,   -2.5, 2.5 )
jet1EtaExp.Sumw2()

jet2Pt                      = ROOT.TH1F("jet2Pt",                     "Jet 2 Pt",                   400,  0,  2000 )
jet2PtExp                   = ROOT.TH1F("jet2PtExp",                  "Jet 2 Pt Exp",               400,  0,  2000 )
jet2PtExp.Sumw2()
jet2MassTag                 = ROOT.TH1F("jet2MassTag",                "Jet 2 Mass",                 400,  0,  2000 )
jet2MassExp                 = ROOT.TH1F("jet2MassExp",                "Jet 2 Mass",                 400,  0,  2000 )
jet2MassExp.Sumw2()
jet2EtaTag                  = ROOT.TH1F("jet2EtaTag",                 "Jet 2 Eta",                  50,   -2.5, 2.5 )
jet2EtaExp                  = ROOT.TH1F("jet2EtaExp",                 "Jet 2 Eta",                  50,   -2.5, 2.5 )
jet2EtaExp.Sumw2()

jet3Pt                      = ROOT.TH1F("jet3Pt",                     "Jet 3 Pt",                   400,  0,  2000 )
jet3PtExp                   = ROOT.TH1F("jet3PtExp",                  "Jet 3 Pt Exp",               400,  0,  2000 )
jet3PtExp.Sumw2()
jet3MassTag                 = ROOT.TH1F("jet3MassTag",                "Jet 3 Mass",                 400,  0,  2000 )
jet3MassExp                 = ROOT.TH1F("jet3MassExp",                "Jet 3 Mass",                 400,  0,  2000 )
jet3MassExp.Sumw2()
jet3EtaTag                  = ROOT.TH1F("jet3EtaTag",                 "Jet 3 Eta",                  50,   -2.5, 2.5 )
jet3EtaExp                  = ROOT.TH1F("jet3EtaExp",                 "Jet 3 Eta",                  50,   -2.5, 2.5 )
jet3EtaExp.Sumw2()



type2TopTagWith1TeV         = ROOT.TH1F("type2TopTagWith1TeV",        "Top Tag Pt",                 400,  0,  2000 )
type2TopTagExpWith1TeV      = ROOT.TH1F("type2TopTagExpWith1TeV",     "Top Tag Pt Expected",        400,  0,  2000 )
type2TopTagExpWith1TeV.Sumw2()
type2TopTagExp800GeV        = ROOT.TH1F("type2TopTagExp800GeV",       "Top Tag Pt Expected",        400,  0,  2000 )
type2TopTagExp800GeV.Sumw2()
type2TopTag800GeV           = ROOT.TH1F("type2TopTag800GeV",          "Top Tag Pt",                 400,  0,  2000 )
type2TopProbe800GeV         = ROOT.TH1F("type2TopProbe800GeV",        "Top Probe Pt",               400,  0,  2000 )
type2KinTopProbe            = ROOT.TH1F("type2KinTopProbe",           "Top Probe Pt",               400,  0,  2000 )
type2KinTopTag              = ROOT.TH1F("type2KinTopTag",             "Top Tag Pt",                 400,  0,  2000 )
type2SideBandProbe          = ROOT.TH1F("type2SideBandProbe",         "Top Probe Pt",               400,  0,  2000 )
type2SideBandTag            = ROOT.TH1F("type2SideBandTag",           "Top Tag Pt",                 400,  0,  2000 )
leadTopProbe                = ROOT.TH1F("leadTopProbe",               "Top Probe Pt",               400,  0,  2000 )
leadTopTag                  = ROOT.TH1F("leadTopTag",                 "Top Tag Pt",                 400,  0,  2000 )
secTopProbe                 = ROOT.TH1F("secTopProbe",                "Top Probe Pt",               400,  0,  2000 )
secTopTag                   = ROOT.TH1F("secTopTag",                  "Top Tag Pt",                 400,  0,  2000 )
randomTopProbe              = ROOT.TH1F("randomTopProbe",             "Top Probe Pt",               400,  0,  2000 )
randomTopTag                = ROOT.TH1F("randomTopTag",               "Top Tag Pt",                 400,  0,  2000 )
antitagProbe                = ROOT.TH1F("antitagProbe",               "Top Probe Pt",               400,  0,  2000 )
antitagTag                  = ROOT.TH1F("antitagTag",                 "Top Tag Pt",                 400,  0,  2000 )

signalTopTagEta             = ROOT.TH1F("signalTopTagEta",              "Top Tag Eta",              100,  -3, 3 )
signalJet3TagEta            = ROOT.TH1F("signalJet3TagEta",             "Jet 3 Eta",                100,  -3, 3 )
evtRho                      = ROOT.TH1F("evtRho",                       "Event Rho",                1001, -1.0, 1000 )

NSubjets                    = ROOT.TH1F("NSubjets",                     "Number of Subjets",        10,   -0.5,   9.5 )
minmass                     = ROOT.TH1F("minmass",                      "Min Mass",                 51,   -5.0,    250 )
NSubjetsWithTopMass         = ROOT.TH1F("NSubjetsWithTopMass",          "Number of Subjets",        10,   -0.5,   9.5 )
minmassWithTopMass          = ROOT.TH1F("minmassWithTopMass",           "Min Mass",                 51,   -5.0,    250 )

NSubjetsVsMinMassAll        = ROOT.TH2F("NSubjetsVsMinMassAll",         "NSubjets Vs Min Mass",     10,   -0.5,   9.5,    51,   -5.0,    250 )
NSubjetsVsMinMassSR         = ROOT.TH2F("NSubjetsVsMinMassSR",          "NSubjets Vs Min Mass",     10,   -0.5,   9.5,    51,   -5.0,    250 )

nJetsSignal                 = ROOT.TH1F("nJetsSignal",                  "N Jets",                   20,   -0.5,   19.5 )

checkWTag = 0
#mistagFile = ROOT.TFile("top_mistag_rate_2011_Lum250_PTCut350_May27cert_HLT270_300_370.root")
mistagFile = ROOT.TFile("MISTAG.root")
#mistag = mistagFile.Get("TYPE12_SR_MISTAG")
mistag = mistagFile.Get("TYPE12_KIN_MISTAG")

#Has to fixe mistag with TH1D()
#mistag1 = ROOT.TH1D()
#mttPredDistModMass          = ROOT.PredictedDistribution( mistag1,  "mttPredDistModMass",   "Mistag Bkg mtt",   1000, 0,  5000 )


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

    event.getByLabel( allTopTagLabel, allTopTagHandle )
    allTopJets  = allTopTagHandle.product()
    event.getByLabel( allTopTagMinMassLabel, allTopTagMinMassHandle )
    allTopJetMinMass  = allTopTagMinMassHandle.product()
    event.getByLabel( allTopTagNSubsLabel, allTopTagNSubsHandle )
    allTopJetNSubs  = allTopTagNSubsHandle.product()

    event.getByLabel( rhoLabel, rhoHandle )
    rho = rhoHandle.product()[0]

######### calculate pair mass and set cuts here
    evtRho.Fill( rho )
    if rho < 0.0 or rho > 100 :
      print "Skip event with nosense rho"
      continue
    nTopCand = 0
    for i in range(0,len(topJets) ) :
      if( topJets[i].pt() > 350 ) :
        nTopCand = nTopCand + 1

    nHighPtJets = 0
    for j in range(0,len(allTopJets) ) :
      if( allTopJets[j].pt() > 350 ) :
        nHighPtJets += 1
    
    ####### Make some top mistag measurement
    if( nHighPtJets == 2 ) :
      leadTagged = (allTopJets[0]).mass() > 140 and (allTopJets[0]).mass() < 250 and allTopJetMinMass[0] > 50 and allTopJetNSubs[0] > 2
      secTagged = (allTopJets[1]).mass() > 140 and (allTopJets[1]).mass() < 250 and allTopJetMinMass[1] > 50 and allTopJetNSubs[1] > 2
      leadTopProbe.Fill( allTopJets[0].pt() )
      secTopProbe.Fill( allTopJets[1].pt() )
      if( leadTagged )  :   leadTopTag.Fill( allTopJets[0].pt() )
      if( secTagged ) :     secTopTag.Fill( allTopJets[1].pt() )
      ri = ROOT.gRandom.Uniform()
      if ri < 0.5 : randomIndex = 0; antiProbeIndex = 1
      else    :     randomIndex = 1; antiProbeIndex = 0
      randomTopProbe.Fill( allTopJets[randomIndex].pt() )
      randomTagged =  (allTopJets[randomIndex]).mass() > 140 and (allTopJets[randomIndex]).mass() < 250 and allTopJetMinMass[randomIndex] > 50 and allTopJetNSubs[randomIndex] > 2
      if randomTagged :   randomTopTag.Fill( allTopJets[randomIndex].pt() )
      if( not randomTagged ) :
        antitagProbe.Fill( allTopJets[antiProbeIndex].pt() )
        antiProbeTagged =  allTopJets[antiProbeIndex].mass() > 140 and allTopJets[antiProbeIndex].mass() < 250 and allTopJetMinMass[antiProbeIndex] > 50 and allTopJetNSubs[antiProbeIndex] > 2
        if( antiProbeTagged ) :   antitagTag.Fill( allTopJets[antiProbeIndex].pt() )



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
    jet1P4_massDown = copy.copy(topJets[0])
    jet1P4_massDown.SetM( max(jet1P4_massDown.mass()-100, 0.0) )
    #print topJets[0].px(), topJets[0].py(), topJets[0].pz(), topJets[0].mass() 
    #print jet1P4_massDown.px(), jet1P4_massDown.py(), jet1P4_massDown.pz(), jet1P4_massDown.mass()
    ttMassJet1MassDown = (wJets[jet3]+wJets[0]+jet1P4_massDown).mass()

    jet1P4_massUp = copy.copy(topJets[0])
    jet1P4_massUp.SetM( jet1P4_massUp.mass()+100 )
    ttMassJet1MassUp = (wJets[jet3]+wJets[0]+jet1P4_massUp).mass()
    #print jet1P4_massUp.px(), jet1P4_massUp.py(), jet1P4_massUp.pz(), jet1P4_massUp.mass()

    type2TopMassPdf = mistagFile.Get( "TYPE2_TOP_TAG_MASS" )
    modJet1Mass = 0.0
    rx = ROOT.gRandom.Uniform()
    massBin = 0
    lowMassBin = type2TopMassPdf.FindBin(140)
    highMassBin = type2TopMassPdf.FindBin(250)
    for i in range( lowMassBin, highMassBin ) :
      x = type2TopMassPdf.Integral(lowMassBin,i)/type2TopMassPdf.Integral(lowMassBin,highMassBin)
      if x > rx :
        massBin = i
        break
    
    modJet1Mass = type2TopMassPdf.GetXaxis().GetBinCenter( massBin )
    jet1MassMod.Fill( modJet1Mass )
    jet1P4_mod = copy.copy( topJets[0] )
    jet1P4_mod.SetM( modJet1Mass )
    ttMassMod = (wJets[jet3]+wJets[0]+jet1P4_mod).mass()
    ttMassMod2 = ttMass
    if  topJets[0].mass() < 140  :
      ttMassMod2 = ttMassMod

    passKinCuts = (nTopCand == 1) and (wJets[0].pt() > 200)  and (wJetMu[0] < 0.4) and (wJets[jet3].pt() > 30 )
    hasBTag1    = wJetBDisc[jet3] > 3.3
    hasType2Top = wJets[0].mass() > 60 and wJets[0].mass() < 130 and pairMass > 140 and pairMass < 250
    hasTopTag   = topJetMass[0] > 140 and topJetMass[0] < 250 and topJetMinMass[0] > 50 and topJetNSubjets[0] > 2
    SBAndSR     = wJets[0].mass() > 40 and wJets[0].mass() < 150 and pairMass > 100 and pairMass < 300
    SBAndSR2    = wJets[0].mass() > 20 and wJets[0].mass() < 170 and pairMass > 60  and pairMass < 350
    passWiderTopMassCut   =   topJetMass[0] > 100 and topJetMass[0] < 300
    passTopMass           =   topJetMass[0] > 140 and topJetMass[0] < 250
    passNSubjetsCut       =   topJetNSubjets[0] > 2
    passMinMassCut        =   topJetMinMass[0] > 50
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
      thirdLeadJetbValue.Fill( wJetBDisc[1] )
      thirdLeadJetPt.Fill( wJets[1].pt() )

      mttBkgShape.Fill( ttMass )
      mttBkgShapeMassUp.Fill( ttMassJet1MassUp )
      mttBkgShapeMassDown.Fill( ttMassJet1MassDown )
      wCandVsTopCandMassType12.Fill( wJets[0].mass() ,  pairMass )

      NSubjets.Fill( topJetNSubjets[0] )
      minmass.Fill( topJetMinMass[0] )
      if passTopMass :
        NSubjetsWithTopMass.Fill( topJetNSubjets[0] )
        minmassWithTopMass.Fill( topJetMinMass[0] )
        #if topJetNSubjets[0] < 3 :
        #  NSubjetsVsMinMassAll.Fill( topJetNSubjets[0], -1. )
        #else :
        NSubjetsVsMinMassAll.Fill( topJetNSubjets[0], topJetMinMass[0] )
        #if topJetNSubjets[0] == 2 :   print topJetMinMass[0]
        #if topJetMinMass[0] > 250 :   print topJetMinMass[0], topJetNSubjets[0]

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

      topJetCandPtAll.Fill( topJets[0].pt() )
      topJetCandMassAll.Fill( topJets[0].mass() )
      topJetNsubsAll.Fill( topJetNSubjets[0] )
      topJetMinMassAll.Fill( topJetMinMass[0] )
      type2KinTopProbe.Fill( topJets[0].pt() )
      if hasTopTag  :   type2KinTopTag.Fill(  topJets[0].pt() )
      if not SBAndSR  :
        type2SideBandProbe.Fill( topJets[0].pt() )
        if hasTopTag  :   type2SideBandTag.Fill( topJets[0].pt() )

      if hasType2Top  :
        topJetCandPtSignal.Fill( topJets[0].pt() )
        topJetCandMassSignal.Fill( topJets[0].mass() )
        topJetNsubsSignal.Fill( topJetNSubjets[0] )
        topJetMinMassSignal.Fill( topJetMinMass[0] )
        if passTopMass :
          NSubjetsVsMinMassSR.Fill( topJetNSubjets[0], topJetMinMass[0] )

        #Apply top mistag rate to estimate bkg
        jet1Pt = topJets[0].pt()
        ptBin = mistag.FindBin( jet1Pt )
        mttBkgWithMistag.Fill( ttMass, mistag.GetBinContent(ptBin) )
        mttBkgWithMistagModMass.Fill( ttMassMod, mistag.GetBinContent(ptBin) )
        #mttPredDistModMass.Accumulate( ttMassMod, jet1Pt, hasTopTag, 1.0 )

        mttBkgWithMistagMod2Mass.Fill( ttMassMod2, mistag.GetBinContent(ptBin) )
        mttBkgWithMistagUp.Fill( ttMass, (mistag.GetBinContent(ptBin)+mistag.GetBinError(ptBin)) )
        mttBkgWithMistagDown.Fill( ttMass, (mistag.GetBinContent(ptBin)-mistag.GetBinError(ptBin)) )
        type2TopTagExp.Fill( topJets[0].pt(), mistag.GetBinContent(ptBin) )
        jet1MassExp.Fill( topJets[0].mass(), mistag.GetBinContent(ptBin) )
        jet1EtaExp.Fill( topJets[0].eta(), mistag.GetBinContent(ptBin) )
        jet2PtExp.Fill( wJets[0].pt(), mistag.GetBinContent(ptBin) )
        jet2MassExp.Fill( wJets[0].mass(), mistag.GetBinContent(ptBin) )
        jet2EtaExp.Fill( wJets[0].eta(), mistag.GetBinContent(ptBin) )
        jet3PtExp.Fill( wJets[1].pt(), mistag.GetBinContent(ptBin) )
        jet3MassExp.Fill( wJets[1].mass(), mistag.GetBinContent(ptBin) )
        jet3EtaExp.Fill( wJets[1].eta(), mistag.GetBinContent(ptBin) )

        #Make Top mistag measurement
        type2TopProbe.Fill( topJets[0].pt() )
        if hasTopTag :  
          type2TopTag.Fill( topJets[0].pt() )
          type2TopTagMass.Fill( topJets[0].mass() )
          jet1MassTag.Fill( topJets[0].mass() )
          jet1EtaTag.Fill( topJets[0].eta() )
          jet2Pt.Fill( wJets[0].pt() )
          jet2MassTag.Fill( wJets[0].mass() )
          jet2EtaTag.Fill( wJets[0].eta() )
          jet3Pt.Fill( wJets[1].pt() )
          jet3MassTag.Fill( wJets[1].mass() )
          jet3EtaTag.Fill( wJets[1].eta() )

        if ttMass > 800 and ttMass < 900 :
          type2TopTagExp800GeV.Fill( topJets[0].pt(), mistag.GetBinContent(ptBin) )
          type2TopProbe800GeV.Fill( topJets[0].pt() )
          if hasTopTag :    type2TopTag800GeV.Fill( topJets[0].pt() )
        if ttMass < 1000 :
          type2TopTagExpWith1TeV.Fill( topJets[0].pt(), mistag.GetBinContent(ptBin) )
          if hasTopTag :  type2TopTagWith1TeV.Fill( topJets[0].pt() )

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
      if ((not passNSubjetsCut) or (not passMinMassCut)) and hasType2Top and passTopMass :
        mttBkgShapeWithSideBand4Mass.Fill( ttMass )
      if ((not passNSubjetsCut) or (not passMinMassCut)) and SBAndSR and passWiderTopMassCut :
        mttBkgShapeWithSideBand5Mass.Fill( ttMass )
      if ((not passNSubjetsCut) or (not passMinMassCut)) and SBAndSR and passTopMass :
        mttBkgShapeWithSideBand6Mass.Fill( ttMass )
      if ((not passNSubjetsCut) or (not passMinMassCut)) and hasType2Top and passWiderTopMassCut :
        mttBkgShapeWithSideBand7Mass.Fill( ttMass )

      if hasType2Top and hasTopTag :
        mttMass.Fill( ttMass )
        mttMassJet1MassDown.Fill( ttMassJet1MassDown )
        nJetsSignal.Fill( len(topJets)+len(wJets) )
        if hasBTag1 :
          mttMassWithBTag.Fill( ttMass )
          jet3BTagPt.Fill( wJets[jet3].pt() )
          signalTopTagEta.Fill( topJets[0].eta() )
          signalJet3TagEta.Fill( wJets[jet3].eta() )

f.cd()
#mttPredDistModMass.SetCalculatedErrors()
#mttPredDistModMass.GetPredictedHist().Write()
#mttPredDistModMass.GetObservedHist().Write()
#mttPredDistModMass.GetTaggableHist().Write()
f.Write()
f.Close()

print checkWTag



