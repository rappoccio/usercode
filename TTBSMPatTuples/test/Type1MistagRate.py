#! /usr/bin/env python

import os
import glob

import ROOT

import sys
import random

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, gROOT

from DataFormats.FWLite import Events, Handle

from optparse import OptionParser

parser = OptionParser()

# python Type1AnalyzerOptionParserData.py --prefix . --inputDir Jet_Run2011A-PromptReco-v4_range1_ttbsm_v6_ttbsmTuples_v3
# python Type1AnalyzerOptionParser.py --prefix etaSmearUp --inputDir Zprime_M2000GeV_W20GeV-madgraph_ttbsm_387_v2
parser.add_option('-i', '--inputDir', metavar='F', type='string', action='store',
                  default='Jet_Run2011A-PromptReco-v4_range1_ttbsm_v6_ttbsmTuples_v3',
                  dest='inputDir',
                  help='Input Dir')



parser.add_option('-p', '--prefix', metavar='N', type='string', action='store',
                  default='./',
                  dest='prefix',
                  help='Dir prefix')


(options, args) = parser.parse_args()

files = glob.glob( options.prefix + '/' + options.inputDir + "/res/*.root" )
print files

events = Events (files)
events_mistag = Events (files)

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

hemis1MinMassHandle     = Handle( "std::vector<double>" )              
hemis1MinMassLabel  = ( "ttbsmAna", "topTagMinMassHemis1" )

hemis1NSubjetsHandle    = Handle( "std::vector<double>" )
hemis1NSubjetsLabel = ( "ttbsmAna", "topTagNSubjetsHemis1"  )          

hemis1TopMassHandle     = Handle( "std::vector<double>" )
hemis1TopMassLabel  = ( "ttbsmAna", "topTagTopMassHemis1" )

hemis1PassHandle        = Handle( "std::vector<int>")
hemis1PassLabel   = ( "ttbsmAna", "topTagPassHemis1" )

hemis1BdiscHandle         = Handle( "std::vector<double>" )
hemis1BdiscLabel    = ( "ttbsmAna",   "wTagBDiscHemis1" )

hemis1MuHandle           = Handle( "std::vector<double>")
hemis1MuLabel      = ( "ttbsmAna",  "wTagMuHemis1" )

hemis1Jet3Handle    = Handle("int")
hemis1Jet3Label     = ( "ttbsmAna", "jet3Hemis1" )

f = ROOT.TFile( "./histFiles/"+options.inputDir + ".root", "recreate" )
f.cd()

print "Creating histograms"
topTagPt                    = ROOT.TH1F("topTagPt", "Top Tag Pt", 400,    0,    2000 )
topProbePt                    = ROOT.TH1F("topProbePt", "Top Probe Pt", 400,    0,    2000 )
testTagPt                    = ROOT.TH1F("testTagPt", "Top Tag Pt", 400,    0,    2000 )
testProbePt                    = ROOT.TH1F("testProbePt", "Top Probe Pt", 400,    0,    2000 )
mistag                    = ROOT.TH1F("mistag", "mistag", 400,    0,    2000 )


print "Loop over events - calculate mistag rate"

eventCount = 0
for event in events_mistag:
    eventCount =  eventCount +1
    x = random.random() 
    #print 'event '+ str(eventCount) + ' x = ' + str(x) 
	
    event.getByLabel (hemis0Label, hemis0Handle)
    topJets0 = hemis0Handle.product()
	
    event.getByLabel (hemis0MinMassLabel, hemis0MinMassHandle)
    topJet0MinMass = hemis0MinMassHandle.product()
	
    event.getByLabel (hemis0NSubjetsLabel, hemis0NSubjetsHandle)
    topJet0NSubjets = hemis0NSubjetsHandle.product()
	
    event.getByLabel (hemis0TopMassLabel, hemis0TopMassHandle)
    topJet0Mass = hemis0TopMassHandle.product()
	
    event.getByLabel (hemis0PassLabel, hemis0PassHandle )
    topJet0Pass = hemis0PassHandle.product()
	
    event.getByLabel (hemis1Label, hemis1Handle)
    topJets1 = hemis1Handle.product()
	
    event.getByLabel (hemis1MinMassLabel, hemis1MinMassHandle)
    topJet1MinMass = hemis1MinMassHandle.product()
	
    event.getByLabel (hemis1NSubjetsLabel, hemis1NSubjetsHandle)
    topJet1NSubjets = hemis1NSubjetsHandle.product()
	
    event.getByLabel (hemis1TopMassLabel, hemis1TopMassHandle)
    topJet1Mass = hemis1TopMassHandle.product()
	
    event.getByLabel (hemis1PassLabel, hemis1PassHandle )
    topJet1Pass = hemis1PassHandle.product()
	
    nTopCand0 = 0
    nTopCand1 = 0
    for i in range(0,len(topJets0) ) :
        if( topJets0[i].pt() > 350 ) :
            nTopCand0 = nTopCand0 + 1
    for i in range(0,len(topJets1) ) :
        if( topJets1[i].pt() > 350 ) :
            nTopCand1 = nTopCand1 + 1
	
    pairMass = 0.0
    ttMass = 0.0
    if nTopCand0 < 1:
        continue
    if nTopCand1 < 1:
        continue
    if len(topJet1MinMass) <1:
        continue
	
    ttMass = (topJets0[0]+topJets1[0]).mass()
    passType11KinCuts   = topJets0[0].pt() > 350 and topJets1[0].pt() > 350
    topTag0        = topJet0Mass[0] > 140 and topJet0Mass[0] < 250 and topJet0MinMass[0] > 50 and topJet0NSubjets[0] > 2
    topTag1        = topJet1Mass[0] > 140 and topJet1Mass[0] < 250 and topJet1MinMass[0] > 50 and topJet1NSubjets[0] > 2
    failMinMass0   = topJet0Mass[0] > 140 and topJet0Mass[0] < 250 and topJet0MinMass[0] < 50 
    failMinMass1   = topJet1Mass[0] > 140 and topJet1Mass[0] < 250 and topJet1MinMass[0] < 50
    passType11     = topTag0 and topTag1
    
    if passType11KinCuts :
        if x < 0.5 :
            if not topTag0 :
                topProbePt.Fill( topJets1[0].pt() )    
                if topTag1 :
                    topTagPt.Fill( topJets1[0].pt() )
        if x >= 0.5 :
            if not topTag1 :
                topProbePt.Fill( topJets0[0].pt() )
                if topTag0 :
                    topTagPt.Fill( topJets0[0].pt() )
                                
        if x < 0.5 :
            if failMinMass0 :
                testProbePt.Fill( topJets1[0].pt() )         
                if topTag1 :
                    testTagPt.Fill( topJets1[0].pt() )
        if x >= 0.5 :
            if failMinMass1 :
                testProbePt.Fill( topJets0[0].pt() )
                if topTag0 :
                    testTagPt.Fill( topJets0[0].pt() )



mistag.Divide(topTagPt,topProbePt,1,1,"B");


f.cd()
f.Write()
f.Close()


