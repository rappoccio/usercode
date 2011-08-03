#! /usr/bin/env python
import os
import glob

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--fileDir', metavar='F', type='string', action='store',
                  dest='fileDir',
                  help='Input file')


parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='TTSemilepAnalyzer_antibtag_w_mucut',
                  dest='outname',
                  help='output name')


parser.add_option('--muOnly', metavar='F', action='store_true',
                  default=False,
                  dest='muOnly',
                  help='use only muons')

parser.add_option('--useLoose', metavar='F', action='store_true',
                  default=False,
                  dest='useLoose',
                  help='use loose leptons (exclusive from tight)')

(options, args) = parser.parse_args()

argv = []


import ROOT
ROOT.gROOT.Macro("rootlogon.C")


import sys
from DataFormats.FWLite import Events, Handle

print 'Getting files from this dir: ' + options.fileDir

files = glob.glob( options.fileDir + '/res/*.root' )
print files


f = ROOT.TFile(options.outname + ".root", "recreate")
f.cd()

print "Creating histograms"

nJets = ROOT.TH1F("nJets",         "Number of Jets, p_{T} > 30 GeV;N_{Jets};Number",               20, -0.5, 19.5 )
nMuons = ROOT.TH1F("nMuons",         "Number of Muons, p_{T} > 45 GeV;N_{Muons};Number",               5, -0.5, 4.5 )
nElectrons = ROOT.TH1F("nElectrons",         "Number of Electrons, p_{T} > 60 GeV;N_{Jets};Number",               5, -0.5, 4.5 )

ptMu = ROOT.TH1F("ptMu", "p_{T} of Muon", 200, 0., 200.)
ptMET0 = ROOT.TH1F("ptMET0", "MET", 200, 0., 200.)
ptMET1 = ROOT.TH1F("ptMET1", "MET", 200, 0., 200.)
ptMET2 = ROOT.TH1F("ptMET2", "MET", 200, 0., 200.)
ptMET3 = ROOT.TH1F("ptMET3", "MET", 200, 0., 200.)
htLep0 = ROOT.TH1F("htLep0", "H_{T}^{Lep}", 300, 0., 600.)
htLep1 = ROOT.TH1F("htLep1", "H_{T}^{Lep}", 300, 0., 600.)
htLep2 = ROOT.TH1F("htLep2", "H_{T}^{Lep}", 300, 0., 600.)
htLep3 = ROOT.TH1F("htLep3", "H_{T}^{Lep}", 300, 0., 600.)
ptJet0 = ROOT.TH1F("ptJet0", "p_{T} Of Leading Jet", 300, 0., 600.)


muHist = ROOT.TH1F("muHist", "#mu", 300, 0, 1.0)

mWCand = ROOT.TH1F("mWCand",         "Mass of W Candidate from Hadronic Jets;Mass;Number",  200, 0., 200. )
mTopCand = ROOT.TH1F("mTopCand",         "Mass of Top Candidate from Hadronic Jets;Mass;Number",  300, 0., 600. )

mWCandVsMuCut = ROOT.TH2F("mWCandVsMuCut", "Mass of W candidate versus #mu cut", 20, 0, 200, 10, 0, 1.0)


events = Events (files)

postfix = ""
if options.useLoose :
    postfix = "Loose"

jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJets" + postfix,   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJets" + postfix,   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJets" + postfix,   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJets" + postfix,   "mass" )
jetDa0MassHandle         = Handle( "std::vector<float>" )
jetDa0MassLabel    = ( "pfShyftTupleJets" + postfix,   "da0Mass" )
jetDa1MassHandle         = Handle( "std::vector<float>" )
jetDa1MassLabel    = ( "pfShyftTupleJets" + postfix,   "da1Mass" )
jetSSVHEHandle         = Handle( "std::vector<float>" )
jetSSVHELabel    = ( "pfShyftTupleJets" + postfix,   "ssvhe" )

muonPtHandle         = Handle( "std::vector<float>" )
muonPtLabel    = ( "pfShyftTupleMuons" + postfix,   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuons" + postfix,   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuons" + postfix,   "phi" )
muonPfisoHandle         = Handle( "std::vector<float>" )
muonPfisoLabel    = ( "pfShyftTupleMuons" + postfix,   "pfiso" )

electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectrons" + postfix,   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectrons" + postfix,   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectrons" + postfix,   "phi" )
electronPfisoHandle         = Handle( "std::vector<float>" )
electronPfisoLabel    = ( "pfShyftTupleElectrons" + postfix,   "pfiso" )

metHandle = Handle( "std::vector<float>" )
metLabel = ("pfShyftTupleMET" + postfix,   "pt" )

# loop over events
count = 0
print "Start looping"
for event in events:
    count = count + 1
    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count)




    #Require exactly one lepton (e or mu)

    lepType = 0 # Let 0 = muon, 1 = electron    
    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
        continue
    muonPts = muonPtHandle.product()

    if options.useLoose :
        event.getByLabel (muonPfisoLabel, muonPfisoHandle)
        if not muonPfisoHandle.isValid():
            continue
        muonPfisos = muonPfisoHandle.product()
        event.getByLabel (electronPfisoLabel, electronPfisoHandle)
        if not electronPfisoHandle.isValid():
            continue
        electronPfisos = electronPfisoHandle.product()


    

    nMuonsVal = 0
    for imuonPt in range(0,len(muonPts)):
        muonPt = muonPts[imuonPt]
        if muonPt > 45.0 :
            if options.useLoose :
#                print 'imu = ' + str(imuonPt) + ', iso/pt = ' + str( muonPfisos[imuonPt] ) + '/' + str(muonPt) + ' = ' + str(muonPfisos[imuonPt]/muonPt)
                if muonPfisos[imuonPt] / muonPt < 0.2 :
                    continue
                else :
                    nMuonsVal += 1
                    lepType = 0
            else :
                nMuonsVal += 1
                lepType = 0                
                    
    nMuons.Fill( nMuonsVal )
    if nMuonsVal > 0 :
        ptMu.Fill( muonPts[0] )

    event.getByLabel (electronPtLabel, electronPtHandle)
    electronPts = electronPtHandle.product()

    nElectronsVal = 0
    if nMuonsVal == 0 :
        for ielectronPt in range(0,len(electronPts)):
            electronPt = electronPts[ielectronPt]
            if electronPt > 45.0 :
                if options.useLoose :
                    if electronPfisos[ielectronPt] / electronPt < 0.2 :
                        continue
                    else :
                        nElectronsVal += 1
                        lepType = 1
                else :
                    nElectronsVal += 1
                    lepType = 1
                        
    nElectrons.Fill( nElectronsVal )


    if not options.muOnly :
        if nMuonsVal + nElectronsVal != 1 :
            continue
    else :
        if nMuonsVal != 1:
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

        
    event.getByLabel (metLabel, metHandle)
    mets = metHandle.product()
    met = mets[0]

    htLepVal = met + lepP4.Perp()

    htLep0.Fill( htLepVal )
    ptMET0.Fill( met )

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

    htLep1.Fill( htLepVal )
    ptMET1.Fill( met )
    ptJet0.Fill( jetPts[0] )

    # Require leading jet pt to be pt > 200 GeV
    if jetPts[0] < 200.0 :
        continue

    htLep2.Fill( htLepVal )
    ptMET2.Fill( met )
    event.getByLabel (jetSSVHELabel, jetSSVHEHandle)
    jetSSVHEs = jetSSVHEHandle.product()

    ntags = 0
    for ssvhe in jetSSVHEs :
        if ssvhe > 2.74 :
            ntags += 1

    if ntags < 1 :
        continue

    htLep3.Fill( htLepVal )
    ptMET3.Fill( met )
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
    hadJetsBDisc = []
    lepJets = []

    for ijet in range(0,len(jetPts)) :
        if jetPts[ijet] > 30.0 :
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasss[ijet] )
            if jet.DeltaR( lepP4 ) > ROOT.TMath.Pi() / 2.0 :
                hadJets.append( jet )
                hadJetsBDisc.append( jetSSVHEs[ijet] )
                mu0 = jetDa0Masses[ijet] / jetMasss[ijet]
                mu1 = jetDa1Masses[ijet] / jetMasss[ijet]
                mu = mu0
                if mu1 > mu0 :
                    mu = mu1
                hadJetsMu.append( mu )
            else :
                lepJets.append( jet )


    highestMassJetIndex = -1
    highestJetMass = -1.0
    bJetCandIndex = -1
    for ijet in range(0,len(hadJets)):
        if hadJets[ijet].M() > highestJetMass  and hadJetsBDisc[ijet] < 2.74 :
            highestJetMass = hadJets[ijet].M()
            highestMassJetIndex = ijet
        if hadJetsBDisc[ijet] > 2.74 and bJetCandIndex == -1 :
            bJetCandIndex = ijet



    if highestJetMass >= 0 :
        muHist.Fill( hadJetsMu[highestMassJetIndex] )
        mWCandVsMuCut.Fill( highestJetMass, hadJetsMu[highestMassJetIndex] )
        if hadJetsMu[highestMassJetIndex] < 0.4 :
            mWCand.Fill( highestJetMass )
            scale = 1.0
            if bJetCandIndex >= 0 and abs(highestJetMass - 80.4) < 20 :
                hadJets[highestMassJetIndex] *= scale
                hadJets[bJetCandIndex] *= scale
                topCandP4 = hadJets[highestMassJetIndex] + hadJets[bJetCandIndex]
                mTopCand.Fill( topCandP4.M() )
            
f.cd()
f.Write()
f.Close()
