#####################################################################
#
# A python script to produce MET plots for the boosted top QCD estimation
# Plots are produced for each step of the selection function
# 
#####################################################################

#! /usr/bin/env python
import os
import glob

#Helper function to find electron relative isolation
def getAeff(eleEta) :
    aEff = 0.0
    if abs(eleEta) < 1.0:
        aEff = 0.13
    if (abs(eleEta) > 1.0 and abs(eleEta) < 1.479):
        aEff = 0.14
    if (abs(eleEta) > 1.479 and abs(eleEta) < 2.0):
        aEff = 0.07
    if (abs(eleEta) > 2.0 and abs(eleEta) < 2.2):
        aEff = 0.09
    if (abs(eleEta) > 2.2 and abs(eleEta) < 2.3):
        aEff = 0.11
    if (abs(eleEta) > 2.3 and abs(eleEta) < 2.4):
        aEff = 0.11
    if abs(eleEta) > 2.4:
        aEff = 0.14
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

parser.add_option('--bDiscCut', metavar='F', type='float', action='store',
                  default=0.679,
                  dest='bDiscCut',
                  help='B discriminator cut')

parser.add_option('--htCut', metavar='F', type='float', action='store',
                  default=150.,
                  dest='htCut',
                  help='HT cut')

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

PileFile = ROOT.TFile("../Pileup_plots.root")
if options.pileup == 'wjets':
	PilePlot = PileFile.Get("pweightwjets")
if options.pileup == 'ttbar':
	PilePlot = PileFile.Get("pweightttbar")
f.cd()

histMET0 = ROOT.TH1F("histMET0", "MET", 40, 0., 400.)
histMET1 = ROOT.TH1F("histMET1", "MET", 40, 0., 400.)
histMET2 = ROOT.TH1F("histMET2", "MET", 40, 0., 400.)
histMET3 = ROOT.TH1F("histMET3", "MET", 40, 0., 400.)
histMET4 = ROOT.TH1F("histMET4", "MET", 40, 0., 400.)
histMET5 = ROOT.TH1F("histMET5", "MET", 40, 0., 400.)
histMET6 = ROOT.TH1F("histMET6", "MET", 40, 0., 400.)
histMET7 = ROOT.TH1F("histMET7", "MET", 40, 0., 400.)
histMET8 = ROOT.TH1F("histMET8", "MET", 40, 0., 400.)
histMET9 = ROOT.TH1F("histMET9", "MET", 40, 0., 400.)

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

    event.getByLabel (electronPtLabel, electronPtHandle)
    if not electronPtHandle.isValid():
        continue
    electronPts = electronPtHandle.product()

    event.getByLabel (electronPfisoCHLabel, electronPfisoCHHandle)
    if not electronPfisoCHHandle.isValid():
        continue
    electronPfisoCHs = electronPfisoCHHandle.product()

    event.getByLabel (electronPfisoNHLabel, electronPfisoNHHandle)
    if not electronPfisoNHHandle.isValid():
        continue
    electronPfisoNHs = electronPfisoNHHandle.product()

    event.getByLabel (electronPfisoPHLabel, electronPfisoPHHandle)
    if not electronPfisoPHHandle.isValid():
        continue
    electronPfisoPHs = electronPfisoPHHandle.product()

    event.getByLabel (electronEtaLabel, electronEtaHandle)
    electronEtas = electronEtaHandle.product()
    event.getByLabel (electronPhiLabel, electronPhiHandle)
    electronPhis = electronPhiHandle.product()

    event.getByLabel (rhoLabel, rhoHandle)
    if not rhoHandle.isValid():
        continue
    rho = rhoHandle.product()

    nElectronsVal = 0
    goodEles = []
    for ielectronPt in range(0,len(electronPts)):
        electronPt = electronPts[ielectronPt]
        electronPfiso = electronPfisoCHs[ielectronPt] + max(0.0, electronPfisoNHs[ielectronPt] + electronPfisoPHs[ielectronPt] - rho[0] * getAeff(electronEtas[ielectronPt]))
        if electronPfiso / electronPt < 0. :
            continue
        if (electronPt > 35.0 and abs(electronEtas[ielectronPt]) < 2.5) :
            if options.useLoose :
                if electronPfiso / electronPt < 0.1 :
                    continue
                nElectronsVal += 1
                goodEles.append(ielectronPt)
            else :
            	if electronPfiso / electronPt > 0.1 :
		    continue
                nElectronsVal += 1
                goodEles.append(ielectronPt)

    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp 		= 	puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)

    # Get MET for plots
    event.getByLabel (metLabel, metHandle)
    mets = metHandle.product()
    met = mets[0]
        
    # Require exactly one electron
    if nElectronsVal != 1:
        continue    
    count0 += 1

    # 1st MET histogram -- cuts: ==1 ele
    histMET0.Fill( met,weight) 

    event.getByLabel (muonPtLabel, muonPtHandle)
    muonPts = muonPtHandle.product()
    event.getByLabel (muonEtaLabel, muonEtaHandle)
    muonEtas = muonEtaHandle.product()
    event.getByLabel (muonPfisoLabel, muonPfisoHandle)
    muonPfisos = muonPfisoHandle.product()

    nMuonVal = 0
    for imuonPt in range(0,len(muonPts)):
        if (muonPts[imuonPt] > 45. and abs(muonEtas[imuonPt]) < 2.1 and muonPfisos[imuonPt] / muonPts[imuonPt] < 0.12):
            nMuonVal += 1

    # Require exactly 0 muons
    if nMuonVal != 0:
        continue
    count1 += 1

    #MET histogram -- cuts: ==1 ele, ==0 mu
    histMET1.Fill(met, weight)

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
    lepPt = electronPts[goodEles[0]]
    lepEta = electronEtas[goodEles[0]]
    lepPhi = electronPhis[goodEles[0]]
    lepMass = 0.0

    lepP4 = ROOT.TLorentzVector()
    lepP4.SetPtEtaPhiM( lepPt, lepEta, lepPhi, lepMass )
        
    nJetsVal = 0
    ntagslep = 0
    for ijet in range(0,len(jetPts)) :
        if (jetPts[ijet] > 30.0 and abs(jetEtas[ijet]) < 2.5):
            nJetsVal += 1
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasses[ijet] )
            if jet.DeltaR( lepP4 ) < ROOT.TMath.Pi() / 2.0 : 
                if jetCSVs[ijet] > options.bDiscCut :
                    ntagslep += 1

    # Require >= 2 jets above 30 GeV
    if nJetsVal < 2 :
        continue

    # MET histogram -- cuts: ==1 ele and ==0 mu, >= 2 jets
    histMET2.Fill( met,weight )
    count2 += 1
    
    # Require at least 1 btag
    if ntagslep < 1 :
        continue

    # MET histogram -- cuts: ==1 ele, ==0 mu, >= 2 jets, >= 1 btag 
    histMET3.Fill( met,weight )
    count3 += 1

    # Require HT > HT cut (150 or 225)
    htLepVal = met + lepP4.Perp()
    if (htLepVal < options.htCut) :
        continue
    count4 += 1
    histMET4.Fill(met, weight)

    # Require MET > 20
    if met < 20.:
        continue
    count5 += 1 
    histMET5.Fill(met,weight)

    # Get the top jet
    event.getByLabel (topTagPtLabel, topTagPtHandle)
    if not topTagPtHandle.isValid():
        continue
    topTagPt = topTagPtHandle.product()
    if len(topTagPt) <= 0:
        continue
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

    topjet = ROOT.TLorentzVector()
    topjet.SetPtEtaPhiM( topTagPt[0], topTagEta[0], topTagPhi[0], topTagMass[0] )

    # Require top jet and lepton to be in opposite hemispheres
    if (topjet.DeltaR( lepP4) < ROOT.TMath.Pi() / 2.0) :
        continue

    # Require top jet to have >=3 subjets
    if topTagNSub[0] <= 2:
        continue
    count6 += 1
    histMET6.Fill(met,weight)

    # Require min mass of pairwise subjets to be 50 GeV
    if topTagMinMass[0] < 50. :
        continue
    count7 += 1
    histMET7.Fill(met, weight)

    # Require top jet mass > 140 GeV, < 250 GeV
    if (topTagMass[0] < 140. or topTagMass[0] > 250.):
        continue
    count8 += 1
    histMET8.Fill(met, weight)

    # Require top jet pt > 400 GeV
    if (topTagPt[0] < 400.):
        continue
    count9 += 1
    histMET9.Fill(met, weight)

# Print out cutflow results
print  '*** Cutflow table ***'
print  'Total Events: ' + str(count)
print  'Exactly one electron: ' + str(count0)
print  'Exactly zero muons: ' + str(count1)
print  'At least 2 jets: ' + str(count2)
print  'At least one btag: ' + str(count3)
print  'HT > ' + str(options.htCut) + ' GeV: ' + str(count4)
print  'MET > 20 GeV: ' + str(count5)
print  'At least three subjets: ' + str(count6)
print  'Min mass > 50 GeV: ' + str(count7)
print  '140 GeV < Top jet mass < 250 GeV: ' + str(count8) 
print  'Top jet pt > 400 GeV: ' + str(count9)


f.cd()
f.Write()
f.Close()
