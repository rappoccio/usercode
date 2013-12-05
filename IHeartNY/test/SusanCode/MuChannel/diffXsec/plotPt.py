#! /usr/bin/env python
import os
import glob

#Helper function to find closest of <listOf> to <refObj>
def findClosestObj( refObj, listOf ) :
    minDR = 9999.
    ret = -1
    for indx in range(0,len(listOf) ):
        dR = refObj.DeltaR(listOf[indx])
        if dR < minDR :
            minDR = refObj.DeltaR(listOf[indx])
            ret = indx
    return ret

#Helper function to find electron relative isolation
def getAeff(eleEta) :
    aEff = 0.0
    if abs(eleEta) < 1.0:
        aEff = 0.21
    if (abs(eleEta) > 1.0 and abs(eleEta) < 1.479):
        aEff = 0.21
    if (abs(eleEta) > 1.479 and abs(eleEta) < 2.0):
        aEff = 0.11
    if (abs(eleEta) > 2.0 and abs(eleEta) < 2.2):
        aEff = 0.14
    if (abs(eleEta) > 2.2 and abs(eleEta) < 2.3):
        aEff = 0.18
    if (abs(eleEta) > 2.3 and abs(eleEta) < 2.4):
        aEff = 0.19
    if abs(eleEta) > 2.4:
        aEff = 0.26
    return float(aEff) 

from optparse import OptionParser

parser = OptionParser()

#Describe all command line options

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='TTSemilepAnalyzer_antibtag_w_mucut',
                  dest='outname',
                  help='output name')

parser.add_option('--pileup', metavar='F', type='string', action='store',
                  default='none',
                  dest='pileup',
                  help='ttbar or wjets')

parser.add_option('--useLoose', metavar='F', action='store_true',
                  default=False,
                  dest='useLoose',
                  help='use loose leptons (exclusive from tight)')

parser.add_option('--htCut', metavar='F', type='float', action='store',
                  default=150.,
                  dest='htCut',
                  help='HT cut')

parser.add_option('--bDiscCut', metavar='F', type='float', action='store',
                  default=0.679,
                  dest='bDiscCut',
                  help='B discriminator cut')

(options, args) = parser.parse_args()

import ROOT
ROOT.gROOT.Macro("rootlogon.C")

import sys
from DataFormats.FWLite import Events, Handle

print 'Getting these files : ' + options.files

files = glob.glob( options.files )
print files

f = ROOT.TFile(options.outname + ".root", "recreate")
name = options.outname

print "Creating histograms"

PileFile = ROOT.TFile("Pileup_plots.root")
if options.pileup == 'wjets':
	PilePlot = PileFile.Get("pweightwjets")
if options.pileup == 'ttbar':
	PilePlot = PileFile.Get("pweightttbar")
f.cd()

ptTopCandHist = ROOT.TH1F("ptTopCandHist", "p_{T} of Semi-boosted Top Candidate;p_{T} (GeV);Events / 50 GeV", 18, 300., 1200.)
ptTopTagHist = ROOT.TH1F("ptTopTagHist", "p_{T} of Top Jet;p_{T} (GeV);Events / 50 GeV", 18, 300., 1200. )
ptTopLowHist = ROOT.TH1F("ptTopLowHist", "p_{T} of leptonic top;p_{T} (GeV);Events / 50 GeV", 18, 300., 1200.)
mTtBoostHist = ROOT.TH1F("mTtBoostHist", "Mass of ttbar pair (fully boosted);Mass (GeV);Events / 50 GeV", 28, 600., 2000.)
mTtSemiHist = ROOT.TH1F("mTtSemiHist", "Mass of ttbar pair (semi boosted);Mass (GeV);Events / 50 GeV", 28, 600., 2000.)
ptTtBoostHist = ROOT.TH1F("ptTtBoostHist", "p_{T} of ttbar pair (fully boosted);p_{T} (GeV);Events / 50 GeV", 30, 0., 1500.)
ptTtSemiHist = ROOT.TH1F("ptTtSemiHist", "p_{T} of ttbar pair (semi boosteD);p_{T} (GeV);Events / 50 GeV", 30, 0., 1500.)

dRmuLepBjetHist = ROOT.TH1F("dRmuLepBjetHist", "dR between mu and lep Bjet;dR;Events / 0.1", 30, 0., 3.)
dRmuHadBjetHist = ROOT.TH1F("dRmuHadBjetHist", "dR between mu and had Bjet;dR;Events / 0.1", 30, 0., 3.)
dRmuWjetHist = ROOT.TH1F("dRmuWjetHist", "dR between mu and W;dR;Events / 0.1", 30, 0., 3.)
dRmuBoostTopHist = ROOT.TH1F("dRmuBoostTopHist", "dR between mu and top jet;dR;Events / 0.1", 30, 0., 3.)
dRmuSemiTopHist = ROOT.TH1F("dRmuSemiTopHist", "dR between mu and top cand;dR;Events / 0.1", 30, 0., 3.)
dRttBoostHist = ROOT.TH1F("dRttBoostHist", "ttbar pair dR, boosted;dR;Events / 0.1", 30, 0., 3.)
dRttSemiHist = ROOT.TH1F("dRttSemiHist", "ttbar pair dR, semi-boosted;dR;Events / 0.1", 30, 0., 3.)

events = Events (files)

postfix = ""
if options.useLoose :
    postfix = "Loose"

puHandle    	= 	Handle("int")
puLabel     	= 	( "pileup", "npvRealTrue" )

jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "mass" )
jetCSVHandle         = Handle( "std::vector<float>" )
jetCSVLabel    = ( "pfShyftTupleJets" + postfix + "AK5",   "csv" )

topTagPtHandle         = Handle( "std::vector<float>" )
topTagPtLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "pt" )
topTagEtaHandle         = Handle( "std::vector<float>" )
topTagEtaLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "eta" )
topTagPhiHandle         = Handle( "std::vector<float>" )
topTagPhiLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "phi" )
topTagMassHandle         = Handle( "std::vector<float>" )
topTagMassLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "mass" )
topTagMinMassHandle         = Handle( "std::vector<float>" )
topTagMinMassLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "minMass" )
topTagNSubjetsHandle         = Handle( "std::vector<float>" )
topTagNSubjetsLabel    = ( "pfShyftTupleJetsLooseTopTag" ,   "nSubjets" )

muonPtHandle         = Handle( "std::vector<float>" )
muonPtLabel    = ( "pfShyftTupleMuons" + postfix,   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuons" + postfix,   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuons" + postfix,   "phi" )
muonPfisoHandle         = Handle( "std::vector<float>" )
muonPfisoLabel    = ( "pfShyftTupleMuons" + postfix,   "pfisoPU" )

electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectrons" + postfix,   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectrons" + postfix,   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectrons" + postfix,   "phi" )
electronPfisoCHHandle         = Handle( "std::vector<float>" )
electronPfisoCHLabel    = ( "pfShyftTupleElectrons" + postfix,   "pfisoCH" )
electronPfisoNHHandle         = Handle( "std::vector<float>" )
electronPfisoNHLabel    = ( "pfShyftTupleElectrons" + postfix,   "pfisoNH" )
electronPfisoPHHandle         = Handle( "std::vector<float>" )
electronPfisoPHLabel    = ( "pfShyftTupleElectrons" + postfix,   "pfisoPH" )

rhoHandle         = Handle( "double" )
rhoLabel    = ( "kt6PFJets",   "rho" )

metHandle = Handle( "std::vector<float>" )
metLabel = ("pfShyftTupleMET" + postfix,   "pt" )

metphiHandle = Handle( "std::vector<float>" )
metphiLabel = ("pfShyftTupleMET" + postfix,   "phi" )

mptv=0  #Counts number of times muonPtHandle.isValid() fails

# loop over events
count = 0
count0 = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0

print "Start looping"

for event in events:
    weight = 1.0
    count = count + 1
    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count)

    #Require exactly one lepton (e or mu)

    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
	mptv+=1
        continue
    muonPts = muonPtHandle.product()
    if len(muonPts) <= 0:
        continue

    event.getByLabel (muonPfisoLabel, muonPfisoHandle)
    if not muonPfisoHandle.isValid():
        continue
    muonPfisos = muonPfisoHandle.product()

    event.getByLabel (muonEtaLabel, muonEtaHandle)
    muonEtas = muonEtaHandle.product()
    event.getByLabel (muonPhiLabel, muonPhiHandle)
    muonPhis = muonPhiHandle.product()

    nMuonsVal = 0
    nGoodMuonsVal = 0
    for imuonPt in range(0,len(muonPts)):
        nMuonsVal += 1
        muonPt = muonPts[imuonPt]
        if (muonPt > 45.0 and abs(muonEtas[imuonPt]) < 2.1):
            if options.useLoose :
                if muonPfisos[imuonPt] / muonPt < 0.12 :
                    continue
                nGoodMuonsVal += 1
            else :
            	if muonPfisos[imuonPt] / muonPt > 0.12 :
		    continue
                nGoodMuonsVal += 1

    if nGoodMuonsVal != 1:
        continue
    count0 += 1

    event.getByLabel (electronPtLabel, electronPtHandle)
    electronPts = electronPtHandle.product()
    event.getByLabel (electronPfisoCHLabel, electronPfisoCHHandle)
    electronPfisoCHs = electronPfisoCHHandle.product()
    event.getByLabel (electronPfisoNHLabel, electronPfisoNHHandle)
    electronPfisoNHs = electronPfisoNHHandle.product()
    event.getByLabel (electronPfisoPHLabel, electronPfisoPHHandle)
    electronPfisoPHs = electronPfisoPHHandle.product()
    event.getByLabel (electronEtaLabel, electronEtaHandle)
    electronEtas = electronEtaHandle.product()
    event.getByLabel (electronPhiLabel, electronPhiHandle)
    electronPhis = electronPhiHandle.product()

    event.getByLabel (rhoLabel, rhoHandle)
    rho = rhoHandle.product()

    nElectronsVal = 0
    nGoodElectronsVal = 0
    for ielectronPt in range(0,len(electronPts)):
        nElectronsVal += 1
        electronPt = electronPts[ielectronPt]
        electronPfiso = electronPfisoCHs[ielectronPt] + max(0.0, electronPfisoNHs[ielectronPt] + electronPfisoPHs[ielectronPt] - rho[0] * getAeff(electronEtas[ielectronPt]))
        if (electronPt > 35.0 and abs(electronEtas[ielectronPt]) < 2.5 and electronPfiso / electronPt < 0.1):
            nGoodElectronsVal += 1

    if nGoodElectronsVal != 0:
        continue
    count1 += 1

    # Get jet information
    event.getByLabel (jetPtLabel, jetPtHandle)
    if not jetPtHandle.isValid():
        continue
    jetPts = jetPtHandle.product()
    if len(jetPts) <= 0:
        continue
    event.getByLabel (jetEtaLabel, jetEtaHandle)
    jetEtas = jetEtaHandle.product()
    event.getByLabel (jetPhiLabel, jetPhiHandle)
    jetPhis = jetPhiHandle.product()
    event.getByLabel (jetMassLabel, jetMassHandle)
    jetMasses = jetMassHandle.product()
    event.getByLabel (jetCSVLabel, jetCSVHandle)
    jetCSVs = jetCSVHandle.product()

    # First break the jets up by hemisphere
    lepPt = muonPts[0]
    lepEta = muonEtas[0]
    lepPhi = muonPhis[0]
    lepMass = 0.105

    lepP4 = ROOT.TLorentzVector()
    lepP4.SetPtEtaPhiM( lepPt, lepEta, lepPhi, lepMass )

    event.getByLabel (metLabel, metHandle)
    mets = metHandle.product()
    event.getByLabel (metphiLabel, metphiHandle)
    metphis = metphiHandle.product()
    met = mets[0]
    metP4 = ROOT.TLorentzVector()
    metP4.SetPtEtaPhiM(met, 0., metphis[0], 0.)

    htLepVal = met + lepP4.Perp()

    hadJets = []       #Collection of jets in opposite hemisphere from lepton
    hadJetsBDisc = []  #Btag discriminators of hadJets
    lepBjet = ROOT.TLorentzVector()
        
    nJetsVal = 0
    ntagslep = 0
    lepBjetIndex = -1
    for ijet in range(0,len(jetPts)) :
        if (jetPts[ijet] > 30.0 and abs(jetEtas[ijet]) < 2.5):
            nJetsVal += 1
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasses[ijet] )
            if jet.DeltaR( lepP4 ) < ROOT.TMath.Pi() / 2.0 : 
                if jetCSVs[ijet] > options.bDiscCut :
                    if ntagslep == 0:
                        lepBjet = jet
                    ntagslep += 1
            else :
                hadJets.append(jet)
                hadJetsBDisc.append(jetCSVs[ijet])

    # Require >= 2 jets above 30 GeV
    if nJetsVal < 2 :
        continue
    count2 += 1
        
    # Require >=1 btagged jet
    if ntagslep < 1:
        continue
    count3 += 1
    
    # Require HT > 150 (225?)
    if (htLepVal < options.htCut) :
        continue
    count4 += 1

    # Require MET > 20
    if met < 20.:
        continue
    count5 += 1

    ###################################
    # Here ends the pre-top selection #
    ###################################

    highestMassJetIndex = -1
    highestJetMass = -1.0
    bJetCandIndex = -1
    # Find highest mass jet for W-candidate
    for ijet in range(0,len(hadJets)):
        antitagged = hadJetsBDisc[ijet] < options.bDiscCut or options.bDiscCut < 0.0 
        if hadJets[ijet].M() > highestJetMass and antitagged :
            highestJetMass = hadJets[ijet].M()
            highestMassJetIndex = ijet
            
    # Find b-jet candidate
    for ijet in range(0,len(hadJets)):
        if ijet == highestMassJetIndex :
            continue
        if hadJetsBDisc[ijet] > options.bDiscCut :
            bJetCandIndex = ijet
            break

    nonBoostTopP4 = lepP4 + lepBjet + metP4

    event.getByLabel (topTagPtLabel, topTagPtHandle)
    topTagPt = topTagPtHandle.product()
    event.getByLabel (topTagEtaLabel, topTagEtaHandle)
    topTagEta = topTagEtaHandle.product()
    event.getByLabel (topTagPhiLabel, topTagPhiHandle)
    topTagPhi = topTagPhiHandle.product()
    event.getByLabel (topTagMassLabel, topTagMassHandle)
    topTagMass = topTagMassHandle.product()
    event.getByLabel (topTagMinMassLabel, topTagMinMassHandle)
    topTagMinMass = topTagMinMassHandle.product()
    event.getByLabel (topTagNSubjetsLabel, topTagNSubjetsHandle)
    topTagNSub = topTagNSubjetsHandle.product()

    toptagged = False

    if len(topTagPt) > 0:        
        topjet = ROOT.TLorentzVector()
        topjet.SetPtEtaPhiM( topTagPt[0], topTagEta[0], topTagPhi[0], topTagMass[0] )

        # Require top jet and lepton to be in opposite hemispheres
        # Require at least 3 subjets
        if topjet.DeltaR( lepP4) > ROOT.TMath.Pi() / 2.0 and topTagNSub[0] >= 3:
            count6 += 1
            # Require min mass > 50 GeV
            if topTagMinMass[0] > 50. :
                count7 += 1
                # Require top jet mass > 140 GeV, < 250 GeV
                if (topTagMass[0] > 140. and topTagMass[0] < 250.):
                    count8 += 1
                    toptagged = True

    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp 		= 	puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)

    if highestMassJetIndex > 0 and bJetCandIndex > 0 and not toptagged:
        topCandP4 = hadJets[highestMassJetIndex] + hadJets[bJetCandIndex]
        ttSemiP4 = nonBoostTopP4 + topCandP4
        
        ptTopCandHist.Fill(topCandP4.Perp(), weight )
        mTtSemiHist.Fill(ttSemiP4.M(), weight)
        ptTtSemiHist.Fill(ttSemiP4.Perp(), weight)
        
        dRmuHadBjetHist.Fill(lepP4.DeltaR(hadJets[bJetCandIndex]), weight)
        dRmuWjetHist.Fill(lepP4.DeltaR(hadJets[highestMassJetIndex]), weight)
        dRmuSemiTopHist.Fill(lepP4.DeltaR(topCandP4), weight)
        dRttSemiHist.Fill(nonBoostTopP4.DeltaR(topCandP4), weight) 

    # Require top jet pt > 400 GeV
    if toptagged and topTagPt[0] > 400.:
        count9 += 1

        ttBoostP4 = nonBoostTopP4 + topjet
        
        ptTopTagHist.Fill(topTagPt[0], weight)
        mTtBoostHist.Fill(ttBoostP4.M(), weight)
        ptTtBoostHist.Fill(ttBoostP4.Perp(), weight)
        ptTopLowHist.Fill(nonBoostTopP4.Perp(), weight)

        dRmuLepBjetHist.Fill(lepP4.DeltaR(lepBjet), weight)
        dRmuBoostTopHist.Fill(lepP4.DeltaR(topjet), weight)
        dRttBoostHist.Fill(nonBoostTopP4.DeltaR(topjet), weight)

print  '*** Cutflow table ***'
print  'Total Events: ' + str(count)
print  'isvalid() cuts: ' + str(mptv)
print  'Exactly one muon: ' + str(count0)
print  'Exactly zero electrons: ' + str(count1)
print  'At least 2 jets: ' + str(count2)
print  'At least 1 btag: ' + str(count3)
print  'HT > ' + str(options.htCut) + ' GeV: ' + str(count4)
print  'MET > 20 GeV: ' + str(count5)
print  'At least 3 subjets: ' + str(count6)
print  'Min mass > 50 GeV: ' + str(count7)
print  '140 GeV < top jet mass < 250 GeV: ' + str(count8)
print  'Top jet pt > 400 GeV: ' + str(count9)

f.cd()
f.Write()
f.Close()
