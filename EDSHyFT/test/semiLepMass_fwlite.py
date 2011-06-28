#! /usr/bin/env python
import os
import glob

import ROOT
ROOT.gROOT.Macro("rootlogon.C")


import sys
from DataFormats.FWLite import Events, Handle

fileDir = sys.argv[1]
files = glob.glob( fileDir + "/res/*.root" )
print files


f = ROOT.TFile("TTSemilepAnalyzer.root", "recreate")
f.cd()

print "Creating histograms"

nJets = ROOT.TH1F("nJets",         "Number of Jets, p_{T} > 30 GeV;N_{Jets};Number",               20, -0.5, 19.5 )
nMuons = ROOT.TH1F("nMuons",         "Number of Muons, p_{T} > 45 GeV;N_{Muons};Number",               5, -0.5, 4.5 )
nElectrons = ROOT.TH1F("nElectrons",         "Number of Electrons, p_{T} > 60 GeV;N_{Jets};Number",               5, -0.5, 4.5 )

mWCand = ROOT.TH1F("mWCand",         "Mass of W Candidate from Hadronic Jets;Mass;Number",  200, 0., 200. )


events = Events (files)


jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJets",   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJets",   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJets",   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJets",   "mass" )
jetDa0MassHandle         = Handle( "std::vector<float>" )
jetDa0MassLabel    = ( "pfShyftTupleJets",   "da0Mass" )
jetDa1MassHandle         = Handle( "std::vector<float>" )
jetDa1MassLabel    = ( "pfShyftTupleJets",   "da1Mass" )
jetSSVHEHandle         = Handle( "std::vector<float>" )
jetSSVHELabel    = ( "pfShyftTupleJets",   "ssvhe" )

muonPtHandle         = Handle( "std::vector<float>" )
muonPtLabel    = ( "pfShyftTupleMuons",   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuons",   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuons",   "phi" )

electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectrons",   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectrons",   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectrons",   "phi" )

# loop over events
count = 0
print "Start looping"
for event in events:
    count = count + 1
    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count)


    event.getByLabel (jetPtLabel, jetPtHandle)
    jetPts = jetPtHandle.product()


    nJetsVal = 0
    for jetPt in jetPts:
        if jetPt > 30.0 :
            nJetsVal += 1
    
    nJets.Fill( nJetsVal )

    # Require >= 2 jets above 30 GeV
    if nJetsVal < 2 :
        continue

    # Require leading jet pt to be pt > 200 GeV
    if jetPts[0] < 200.0 :
        continue

    event.getByLabel (jetSSVHELabel, jetSSVHEHandle)
    jetSSVHEs = jetSSVHEHandle.product()

    ntags = 0
    for ssvhe in jetSSVHEs :
        if ssvhe > 2.74 :
            ntags += 1

    if ntags < 1 :
        continue

    #Require exactly one lepton (e or mu)

    lepType = 0 # Let 0 = muon, 1 = electron    
    event.getByLabel (muonPtLabel, muonPtHandle)
    muonPts = muonPtHandle.product()

    nMuonsVal = 0
    for muonPt in muonPts:
        if muonPt > 45.0 :
            nMuonsVal += 1
            lepType = 0
    
    nMuons.Fill( nMuonsVal )

    event.getByLabel (electronPtLabel, electronPtHandle)
    electronPts = electronPtHandle.product()

    nElectronsVal = 0
    for electronPt in electronPts:
        if electronPt > 60.0 :
            nElectronsVal += 1
            lepType = 1
    
    nElectrons.Fill( nElectronsVal )

    if nMuonsVal + nElectronsVal != 1 :
        continue


    # Now look at the rest of the lepton information.
    # We will classify jets based on hemispheres, defined
    # by the lepton.

    lepMass = 0.0
    if lepType == 0 :
        event.getByLabel (muonEtaLabel, muonEtaHandle)
        muonEtas = muonEtaHandle.product()
        event.getByLabel (muonPhiLabel, muonPhiHandle)
        muonPhis = muonPhiHandle.product()

        lepPt = muonPts[0]
        lepEta = muonEtas[0]
        lepPhi = muonPhis[0]
        lepMass = 0.105
    else :
        event.getByLabel (electronEtaLabel, electronEtaHandle)
        electronEtas = electronEtaHandle.product()
        event.getByLabel (electronPhiLabel, electronPhiHandle)
        electronPhis = electronPhiHandle.product()

        lepPt = electronPts[0]
        lepEta = electronEtas[0]
        lepPhi = electronPhis[0]

    lepP4 = ROOT.TLorentzVector()
    lepP4.SetPtEtaPhiM( lepPt, lepEta, lepPhi, lepMass )

    
    # Break the jets up by hemisphere
    event.getByLabel (jetEtaLabel, jetEtaHandle)
    jetEtas = jetEtaHandle.product()
    event.getByLabel (jetPhiLabel, jetPhiHandle)
    jetPhis = jetPhiHandle.product()
    event.getByLabel (jetMassLabel, jetMassHandle)
    jetMasss = jetMassHandle.product()
    event.getByLabel (jetDa0MassLabel, jetDa0MassHandle)
    jetDa0Masses = jetDa0MassHandle.product()
    event.getByLabel (jetDa1MassLabel, jetDa1MassHandle)
    jetDa1Masses = jetDa1MassHandle.product()

    hadJets = []
    hadJetsMu = []
    lepJets = []

    for ijet in range(0,len(jetPts)) :
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasss[ijet] )
        if jet.DeltaR( lepP4 ) > ROOT.TMath.Pi() / 2.0 :
            hadJets.append( jet )
            mu0 = jetDa0Masses[ijet] / jetMasss[ijet]
            mu1 = jetDa1Masses[ijet] / jetMasss[ijet]
            mu = mu0
            if mu1 > mu0 :
                mu = mu1
            hadJetsMu.append( mu )
        else :
            lepJets.append( jet )


    highestMassJetIndex = 0
    highestJetMass = -1.0
    for ijet in range(0,len(hadJets)):
        if hadJets[ijet].M() > highestJetMass and hadJetsMu[ijet] < 0.4 :
            highestJetMass = hadJets[ijet].M()
            highestMassJetIndex = ijet

    
    mWCand.Fill( highestJetMass )

f.cd()
f.Write()
f.Close()
