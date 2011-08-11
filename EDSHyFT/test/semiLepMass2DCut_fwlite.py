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

parser.add_option('--minTags', metavar='N', type='int', action='store',
                  default=1,
                  dest='minTags',
                  help='minimum number of tags to consider')


parser.add_option('--muOnly', metavar='F', action='store_true',
                  default=False,
                  dest='muOnly',
                  help='use only muons')

parser.add_option('--useLoose', metavar='F', action='store_true',
                  default=False,
                  dest='useLoose',
                  help='use loose leptons (exclusive from tight)')

parser.add_option('--use2DCut', action='store_true',
                  default=False,
                  dest='use2DCut',
                  help='use 2d cut instead of iso cut')



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
ptMET4 = ROOT.TH1F("ptMET4", "MET", 200, 0., 200.)
htLep0 = ROOT.TH1F("htLep0", "H_{T}^{Lep}", 300, 0., 600.)
htLep1 = ROOT.TH1F("htLep1", "H_{T}^{Lep}", 300, 0., 600.)
htLep2 = ROOT.TH1F("htLep2", "H_{T}^{Lep}", 300, 0., 600.)
htLep3 = ROOT.TH1F("htLep3", "H_{T}^{Lep}", 300, 0., 600.)
htLep4 = ROOT.TH1F("htLep4", "H_{T}^{Lep}", 300, 0., 600.)
ptJet0 = ROOT.TH1F("ptJet0", "p_{T} Of Leading Jet", 300, 0., 600.)


muHist = ROOT.TH1F("muHist", "#mu", 300, 0, 1.0)

mWCand = ROOT.TH1F("mWCand",         "Mass of W Candidate from Hadronic Jets;Mass;Number",  200, 0., 200. )
mTopCand = ROOT.TH1F("mTopCand",         "Mass of Top Candidate from Hadronic Jets;Mass;Number",  300, 0., 600. )

mWCandVsMuCut = ROOT.TH2F("mWCandVsMuCut", "Mass of W candidate versus #mu cut", 20, 0, 200, 10, 0, 1.0)
mWCandVsMTopCand = ROOT.TH2F("mWCandVsMTopCand","WCand+bJet Mass vs WCand mass",200,0.,200.,600,0.,600.)

ptRelVsDRMin = ROOT.TH2F("ptRelVsDRMin", "Mass of W candidate versus #mu cut", 40, 0, 200, 15, 0, 1.5)

events = Events (files)

postfix = ""
if options.useLoose or options.use2DCut :
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

    

    nMuonsVal = 0
    for imuonPt in range(0,len(muonPts)):
        muonPt = muonPts[imuonPt]
        if muonPt > 45.0 :
            nMuonsVal += 1
            lepType = 0
                
    nMuons.Fill( nMuonsVal )

    if nMuonsVal < 1 :
        continue

    # Plot the number of muons with pt > 30.
    # Require at least one.
    ptMu.Fill( muonPts[0] )


    # Plot the number of jets with pt > 30.
    # Require at least two
    event.getByLabel (jetPtLabel, jetPtHandle)
    jetPts = jetPtHandle.product()

    nJetsVal = 0
    for ijet in range(0,len(jetPts)) :
        if jetPts[ijet] > 30.0 :
            nJetsVal += 1  
    # Require >= 2 jets above 30 GeV
    if nJetsVal < 2 :
        continue

    # Now look at the rest of the lepton information.
    # We will classify jets based on hemispheres, defined
    # by the lepton.

    lepMass = 0.0
    event.getByLabel (muonEtaLabel, muonEtaHandle)
    muonEtas = muonEtaHandle.product()
    event.getByLabel (muonPhiLabel, muonPhiHandle)
    muonPhis = muonPhiHandle.product()



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

    event.getByLabel (jetSSVHELabel, jetSSVHEHandle)
    jetSSVHEs = jetSSVHEHandle.product()

    # Break the jets up by hemisphere.
    # Also compute the 2d cut parameters
    # (dR between the lepton and the nearest jet,
    # and the ptRel between the lepton and the nearest jet)
    hadJets = []
    hadJetsMu = []
    hadJetsBDisc = []
    lepJets = []
    lepPt = muonPts[0]
    lepEta = muonEtas[0]
    lepPhi = muonPhis[0]
    lepMass = 0.105
    lepP4 = ROOT.TLorentzVector()
    lepP4.SetPtEtaPhiM( lepPt, lepEta, lepPhi, lepMass )
    dRMin = 999.0
    ptRel = -1.0
    nJetsVal = 0
    for ijet in range(0,len(jetPts)) :
        if jetPts[ijet] > 30.0 :
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasss[ijet] )
            dR = jet.DeltaR( lepP4 )
            if dR > ROOT.TMath.Pi() / 2.0 :
                hadJets.append( jet )
                hadJetsBDisc.append( jetSSVHEs[ijet] )
                mu0 = jetDa0Masses[ijet] / jetMasss[ijet]
                mu1 = jetDa1Masses[ijet] / jetMasss[ijet]
                mu = mu0
                if mu1 > mu0 :
                    mu = mu1
                hadJetsMu.append( mu )
            else :
                if dR < dRMin :
                    #print 'dR = ' + str(dR)
                    #print 'jet = {0:6.2f}, {1:6.2f}, {2:6.2f}, {3:6.2f}'.format( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasss[ijet] )
                    #print 'lep = {0:6.2f}, {1:6.2f}, {2:6.2f}, {3:6.2f}'.format( lepPt, lepEta, lepPhi, lepMass )
                    dRMin = dR
                    ptRel = jet.Perp( lepP4.Vect() )
                lepJets.append( jet )

    # Fill the njets plot
    nJets.Fill( nJetsVal )             
    # Fill the 2D cut plot
    ptRelVsDRMin.Fill( ptRel, dRMin )

    # Compute htLep and fill plots
    event.getByLabel (metLabel, metHandle)
    mets = metHandle.product()
    met = mets[0]

    htLepVal = met + lepP4.Perp()

    htLep0.Fill( htLepVal )
    ptMET0.Fill( met )


    # Compute the 2d cut
    pass2D = dRMin > 0.5 or ptRel > 25.0


    # If using signal selection ( not loose ), then
    # require the 2d cut to continue.
    # Otherwise, you're using the loose selection,
    # so require failure of the 2d cut for a sideband
    if not options.useLoose :
        if not pass2D :
            continue
    else :
        if pass2D :
            continue


    # Plot HTLep and MET for this stage of the selection.
    # Also plot the leading jet PT before we cut on it. 
    htLep1.Fill( htLepVal )
    ptMET1.Fill( met )
    ptJet0.Fill( jetPts[0] )

    # Require leading jet pt to be pt > 200 GeV
    if jetPts[0] < 200.0 :
        continue


    # Plot HTLep and MET for this stage of the selection.
    htLep2.Fill( htLepVal )
    ptMET2.Fill( met )



    # Now require >= N btags
    ntags = 0
    for ssvhe in jetSSVHEs :
        if ssvhe > 2.74 :
            ntags += 1
    if ntags < options.minTags :
        continue

    # Plot HTLep and MET for this stage of the selection.
    htLep3.Fill( htLepVal )
    ptMET3.Fill( met )



    # Select the hadronic W and b candidates in the "type 2" hemisphere:
    #   W candidate: 
    #     - b-tag veto
    #     - highest mass jet in hadronic hemisphere
    #   b candidate:
    #     - Leading pt tagged jet in the hadronic hemisphere
    highestMassJetIndex = -1
    highestJetMass = -1.0
    bJetCandIndex = -1
    for ijet in range(0,len(hadJets)):
        if hadJets[ijet].M() > highestJetMass  and hadJetsBDisc[ijet] < 2.74 :
            highestJetMass = hadJets[ijet].M()
            highestMassJetIndex = ijet
        if hadJetsBDisc[ijet] > 2.74 and bJetCandIndex == -1 :
            bJetCandIndex = ijet


    # Now select on mu cut, and select type 2 top candidate
    if highestJetMass >= 0 :
        muHist.Fill( hadJetsMu[highestMassJetIndex] )
        mWCandVsMuCut.Fill( highestJetMass, hadJetsMu[highestMassJetIndex] )
        if hadJetsMu[highestMassJetIndex] < 0.4 :
            mWCand.Fill( highestJetMass )
            if bJetCandIndex >= 0 :
                topCandP4 = hadJets[highestMassJetIndex] + hadJets[bJetCandIndex]
                mWCandVsMTopCand.Fill( highestJetMass, topCandP4.M() )
                if abs(highestJetMass - 80.4) < 20 :
                    mTopCand.Fill( topCandP4.M() )

f.cd()
f.Write()
f.Close()
