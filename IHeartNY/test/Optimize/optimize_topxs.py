# MINIMAL VERSION OF iheartNY script for optimization studies

#! /usr/bin/env python
import os
import glob
import time
import math


# -------------------------------------------------------------------------------------
# define selection values
# -------------------------------------------------------------------------------------

# muons
MIN_MU_PT  = 45.0
MAX_MU_ETA = 2.1
MAX_MU_ISO = 0.12

# electrons
MIN_EL_PT  = 35.0
MAX_EL_ETA = 2.5
MAX_EL_ISO = 0.1

# jets
MIN_JET_PT  = 30.0
MAX_JET_ETA = 2.4


# -------------------------------------------------------------------------------------
# helper function to find electron relative isolation
# -------------------------------------------------------------------------------------

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


# -------------------------------------------------------------------------------------
# helper function to get b-tagging efficiency scale factor (for MC)
# From: https://twiki.cern.ch/twiki/pub/CMS/BtagPOG/SFb-pt_WITHttbar_payload_EPS13.txt
# Tagger: CSVM within 20 < pt < 800 GeV, abs(eta) < 2.4, x = pt
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# actual SF
def getBtagSF(jetPt) :

    if jetPt > 800 :
        jetPt = 800
    SFb = (0.938887+(0.00017124*jetPt)) + (-2.76366e-07*(jetPt*jetPt));
    return float(SFb)
    
# -------------------------------------------------------------------------------------
# uncertainty on SF
def getBtagSFerror(jetPt) :

    ptmin = [20, 30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 600];
    ptmax = [30, 40, 50, 60, 70, 80,100, 120, 160, 210, 260, 320, 400, 500, 600, 800];

    SFb_error = [
        0.0415707,
        0.0204209,
        0.0223227,
        0.0206655,
        0.0199325,
        0.0174121,
        0.0202332,
        0.0182446,
        0.0159777,
        0.0218531,
        0.0204688,
        0.0265191,
        0.0313175,
        0.0415417,
        0.0740446,
        0.0596716 ];

    error = 0
    for iSF in range(0,len(SFb_error) ):
        if jetPt > ptmin[iSF] and jetPt <= ptmax[iSF] :
            error = SFb_error[iSF]
            break

    if jetPt > 800 :
        error = 0.0596716*2

    return float(error)
# -------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------
# define input options
# -------------------------------------------------------------------------------------

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='test_iheartNY',
                  dest='outname',
                  help='Name of output file')

parser.add_option('--isData', metavar='F', action='store_true',
                  default=False,
                  dest='isData',
                  help='Flag for data (True) or MC (False), used to decide whether to apply b-tagging SF')

parser.add_option('--pileup', metavar='F', type='string', action='store',
                  default='none',
                  dest='pileup',
                  help='What pileup histogram should be used? ttbar, wjets, sts, stt, sttw, stsb, sttb, sttwb')

parser.add_option('--lepType', metavar='F', type='string', action='store',
                  default='muon',
                  dest='lepType',
                  help='Lepton type (ele or muon)')

parser.add_option('--useLoose', metavar='F', action='store_true',
                  default=False,
                  dest='useLoose',
                  help='Use loose leptons (exclusive from tight), for QCD studies')

parser.add_option('--jetPtCut', metavar='F', type='float', action='store',
                  default=200.0,
                  dest='jetPtCut',
                  help='CA8 hadronic-side PT cut of leading jet (default is 200.0) [GeV]')

parser.add_option('--mttGenMax', metavar='J', type='float', action='store',
                  default=None,
                  dest='mttGenMax',
                  help='Maximum generator-level m_ttbar [GeV] to stitch together the ttbar samples')

parser.add_option('--bDiscCut', metavar='F', type='float', action='store',
                  default=0.679,
                  dest='bDiscCut',
                  help='b-tagging discriminator cut (default is 0.679, medium working point for CSV tagger)')

parser.add_option('--btagSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='btagSys',
                  help='Systematic variation on b-tagging SF. Options are +1. (up 1 sigma), 0. (nominal), -1. (down 1 sigma). Default is None.')

parser.add_option('--jecSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='jecSys',
                  help='JEC systematic variation. Options are +1. (up 1 sigma), 0. (nominal), -1. (down 1 sigma). Default is None.')

parser.add_option('--jerSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='jerSys',
                  help='JER Systematic variation in fraction. Default is None.')

(options, args) = parser.parse_args()
argv = []

import ROOT
ROOT.gROOT.Macro("rootlogon.C")


# -------------------------------------------------------------------------------------
# jet energy correction uncertainties & smearing
# -------------------------------------------------------------------------------------

# Additional JEC uncertainty for CA8 jets (this is a manual hack to use AK7 corrections on CA8 jets)
flatJecUnc = 0.03

# Read JEC uncertainties
if options.jecSys != None or options.jerSys != None :
    ROOT.gSystem.Load('libCondFormatsJetMETObjects')
    jecParStrAK5 = ROOT.std.string('START53_V27_Uncertainty_AK5PFchs.txt')
    jecUncAK5 = ROOT.JetCorrectionUncertainty( jecParStrAK5 )
    jecParStrAK7 = ROOT.std.string('START53_V27_Uncertainty_AK7PFchs.txt')
    jecUncAK7 = ROOT.JetCorrectionUncertainty( jecParStrAK7 )    


# -------------------------------------------------------------------------------------
# define helper classes that use ROOT
# -------------------------------------------------------------------------------------

def findClosestInList( p41, p4list ) :
    minDR = 9999.
    ret = None
    for j in range(0,len(p4list) ):
        dR = p4list[j].DeltaR(p41)
        if dR < minDR :
            minDR = dR
            ret = p4list[j]
    return ret


import sys
from DataFormats.FWLite import Events, Handle


# -------------------------------------------------------------------------------------
# input and output files
# -------------------------------------------------------------------------------------

print 'Getting these files : ' + options.files

files = glob.glob( options.files )
print files

f = ROOT.TFile(options.outname+".root", "recreate")


# -------------------------------------------------------------------------------------
# define all the histograms
# -------------------------------------------------------------------------------------

print "Creating histograms"

# read input histogram for PU
PileFile = ROOT.TFile("../Pileup_plots.root")
PilePlot = PileFile.Get("pweight" + options.pileup)

f.cd()

h_LEPMETvsMET       = ROOT.TH2F("LEPMETvsMET",       ";MET+lepton p_{T} [GeV]; MET [GeV]",                    60, 0., 600., 40, 0., 400.)
h_LEPMETvsBtagJetPt = ROOT.TH2F("LEPMETvsBtagJetPt", ";MET+lepton p_{T} [GeV];p_{T} of btagged jet [GeV]",    60, 0., 600., 40, 0., 400.)
h_LEPMETvsHT        = ROOT.TH2F("LEPMETvsHT",        ";MET+lepton p_{T} [GeV];HT [GeV]",                      60, 0., 600., 100, 0., 2000.)
h_LEPMETvsHTLEP     = ROOT.TH2F("LEPMETvsHTLEP",     ";MET+lepton p_{T} [GeV];HTLEP [GeV]",                   60, 0., 600., 100, 0., 2000.)
h_HTvsMET           = ROOT.TH2F("HTvsMET",           ";HT [GeV]; MET [GeV]",                    100, 0., 2000., 40, 0., 400.)
h_HTvsBtagJetPt     = ROOT.TH2F("HTvsBtagJetPt",     ";HT [GeV];p_{T} of btagged jet [GeV]",    100, 0., 2000., 40, 0., 400.)
h_HTvsHTLEP         = ROOT.TH2F("HTvsHTLEP",         ";HT [GeV];HTLEP [GeV]",                   100, 0., 2000., 100, 0., 2000.)
h_HTLEPvsMET        = ROOT.TH2F("HTLEPvsMET",        ";HTLEP [GeV]; MET [GeV]",                 100, 0., 2000., 40, 0., 400.)
h_HTLEPvsBtagJetPt  = ROOT.TH2F("HTLEPvsBtagJetPt",  ";HTLEP [GeV];p_{T} of btagged jet [GeV]", 100, 0., 2000., 40, 0., 400.)
h_BtagJetPtvsMET    = ROOT.TH2F("BtagJetPtvsMET",    ";p_{T} of btagged jet [GeV];MET [GeV]",   50, 0., 500.,   40, 0., 400.)
  
h_LEPMET_0tag       = ROOT.TH1F("LEPMET_0tag",    "LEPMET, 0 btags;MET+lepton p_{T} [GeV]; Events / 20 GeV",    60,  0., 600.)
h_HT_0tag           = ROOT.TH1F("HT_0tag",        "HT, 0 btags;HT [GeV]; Events / 20 GeV",                      100, 0., 2000.)
h_HTLEP_0tag        = ROOT.TH1F("HTLEP_0tag",     "HTLEP, 0 btags;HTLEP [GeV]; Events / 20 GeV",                100, 0., 2000.)
h_MET_0tag          = ROOT.TH1F("MET_0tag",       "MET, 0 btags;MET [GeV]; Events / 10 GeV",                    40, 0., 400.)

h_LEPMET_btag       = ROOT.TH1F("LEPMET_btag",    "LEPMET, >=1 btag;MET+lepton p_{T} [GeV]; Events / 20 GeV",   60,  0., 600.)
h_HT_btag           = ROOT.TH1F("HT_btag",        "HT, >=1 btag;HT [GeV]; Events / 20 GeV",                     100, 0., 2000.)
h_HTLEP_btag        = ROOT.TH1F("HTLEP_btag",     "HTLEP, >=1 btag;HTLEP [GeV]; Events / 20 GeV",               100, 0., 2000.)
h_MET_btag          = ROOT.TH1F("MET_btag",       "MET, >=1 btag;MET [GeV]; Events / 10 GeV",                   40, 0., 400.)
h_BtagJetPt_btag    = ROOT.TH1F("BtagJetPt_btag", "Btagged jet pt;p_{T} of btagged jet [GeV]; Events / 10 GeV", 50, 0., 500.)


# -------------------------------------------------------------------------------------
# define all variables to be read from input files
# -------------------------------------------------------------------------------------

events = Events (files)

# use the "loose" collections for QCD studies
postfix = ""
if options.useLoose :
    postfix = "Loose"


# event-level variables 
puHandle  = Handle("int")
puLabel   = ("pileup", "npvRealTrue")
npvHandle = Handle("unsigned int")
npvLabel  = ("pileup", "npv")

rhoHandle = Handle("double")
rhoLabel  = ("kt6PFJets", "rho")

metHandle    = Handle("std::vector<float>")
metLabel     = ("pfShyftTupleMET" + postfix, "pt")
metphiHandle = Handle("std::vector<float>")
metphiLabel  = ("pfShyftTupleMET" + postfix, "phi")

# lepton variables
muonPtHandle    = Handle("std::vector<float>")
muonPtLabel     = ("pfShyftTupleMuons" + postfix, "pt")
muonEtaHandle   = Handle( "std::vector<float>")
muonEtaLabel    = ("pfShyftTupleMuons" + postfix, "eta")
muonPhiHandle   = Handle( "std::vector<float>")
muonPhiLabel    = ("pfShyftTupleMuons" + postfix, "phi")
muonPfisoHandle = Handle( "std::vector<float>")
muonPfisoLabel  = ("pfShyftTupleMuons" + postfix, "pfisoPU")

electronPtHandle      = Handle( "std::vector<float>")
electronPtLabel       = ("pfShyftTupleElectrons" + postfix, "pt")
electronEtaHandle     = Handle( "std::vector<float>")
electronEtaLabel      = ("pfShyftTupleElectrons" + postfix, "eta")
electronPhiHandle     = Handle( "std::vector<float>")
electronPhiLabel      = ("pfShyftTupleElectrons" + postfix, "phi")
electronPfisoCHHandle = Handle( "std::vector<float>")
electronPfisoCHLabel  = ("pfShyftTupleElectrons" + postfix, "pfisoCH")
electronPfisoNHHandle = Handle( "std::vector<float>")
electronPfisoNHLabel  = ("pfShyftTupleElectrons" + postfix, "pfisoNH")
electronPfisoPHHandle = Handle( "std::vector<float>")
electronPfisoPHLabel  = ("pfShyftTupleElectrons" + postfix, "pfisoPH")

# AK5 jet collection
ak5JetPtHandle   = Handle( "std::vector<float>" )
ak5JetPtLabel    = ("pfShyftTupleJets" + postfix + "AK5", "pt")
ak5JetEtaHandle  = Handle( "std::vector<float>" )
ak5JetEtaLabel   = ("pfShyftTupleJets" + postfix + "AK5", "eta")
ak5JetPhiHandle  = Handle( "std::vector<float>" )
ak5JetPhiLabel   = ("pfShyftTupleJets" + postfix + "AK5", "phi")
ak5JetMassHandle = Handle( "std::vector<float>" )
ak5JetMassLabel  = ("pfShyftTupleJets" + postfix + "AK5", "mass")
ak5JetCSVHandle  = Handle( "std::vector<float>" )
ak5JetCSVLabel   = ("pfShyftTupleJets" + postfix + "AK5", "csv")
ak5JetSecvtxMassHandle = Handle( "std::vector<float>" )
ak5JetSecvtxMassLabel  = ("pfShyftTupleJets" + postfix + "AK5", "secvtxMass")

# top-tagged jet collection
topTagPtHandle   = Handle( "std::vector<float>" )
topTagPtLabel    = ("pfShyftTupleJetsLooseTopTag", "pt")
topTagEtaHandle  = Handle( "std::vector<float>" )
topTagEtaLabel   = ("pfShyftTupleJetsLooseTopTag", "eta")
topTagPhiHandle  = Handle( "std::vector<float>" )
topTagPhiLabel   = ("pfShyftTupleJetsLooseTopTag", "phi")
topTagMassHandle = Handle( "std::vector<float>" )
topTagMassLabel  = ("pfShyftTupleJetsLooseTopTag", "mass")
topTagMinMassHandle  = Handle( "std::vector<float>" )
topTagMinMassLabel   = ("pfShyftTupleJetsLooseTopTag", "minMass")
topTagNSubjetsHandle = Handle( "std::vector<float>" )
topTagNSubjetsLabel  = ("pfShyftTupleJetsLooseTopTag", "nSubjets")


# if making response matrix, need generated particles (truth-level)
if options.mttGenMax != None : 
    genParticlesPtHandle     = Handle("std::vector<float>")
    genParticlesPtLabel      = ("pfShyftTupleGenParticles", "pt")
    genParticlesEtaHandle    = Handle("std::vector<float>")
    genParticlesEtaLabel     = ("pfShyftTupleGenParticles", "eta")
    genParticlesPhiHandle    = Handle("std::vector<float>")
    genParticlesPhiLabel     = ("pfShyftTupleGenParticles", "phi")
    genParticlesMassHandle   = Handle("std::vector<float>")
    genParticlesMassLabel    = ("pfShyftTupleGenParticles", "mass")
    genParticlesPdgIdHandle  = Handle("std::vector<float>")
    genParticlesPdgIdLabel   = ("pfShyftTupleGenParticles", "pdgId")
    genParticlesStatusHandle = Handle("std::vector<float>")
    genParticlesStatusLabel  = ("pfShyftTupleGenParticles", "status")


# if doing JER corrections, need the gen jets (for AK5 and CA8 jets)
if options.jerSys != None :
    ak5GenJetPtHandle   = Handle("std::vector<float>")
    ak5GenJetPtLabel    = ("pfShyftTupleAK5GenJets", "pt")
    ak5GenJetEtaHandle  = Handle("std::vector<float>")
    ak5GenJetEtaLabel   = ("pfShyftTupleAK5GenJets", "eta")
    ak5GenJetPhiHandle  = Handle("std::vector<float>")
    ak5GenJetPhiLabel   = ("pfShyftTupleAK5GenJets", "phi")
    ak5GenJetMassHandle = Handle("std::vector<float>")
    ak5GenJetMassLabel  = ("pfShyftTupleAK5GenJets", "mass")

    ca8GenJetPtHandle   = Handle("std::vector<float>")
    ca8GenJetPtLabel    = ("pfShyftTupleCA8GenJets", "pt")
    ca8GenJetEtaHandle  = Handle("std::vector<float>")
    ca8GenJetEtaLabel   = ("pfShyftTupleCA8GenJets", "eta")
    ca8GenJetPhiHandle  = Handle("std::vector<float>")
    ca8GenJetPhiLabel   = ("pfShyftTupleCA8GenJets", "phi")
    ca8GenJetMassHandle = Handle("std::vector<float>")
    ca8GenJetMassLabel  = ("pfShyftTupleCA8GenJets", "mass")


# -------------------------------------------------------------------------------------
# start looping over events
# -------------------------------------------------------------------------------------

print "Start looping over events!"

ntotal = 0

for event in events :

    ntotal += 1
    weight = 1.0 #event weight
    
    if ntotal % 10000 == 0 :
      print  '--------- Processing Event ' + str(ntotal)
    

    # -------------------------------------------------------------------------------------
    # read PU information & do PU reweighting
    # -------------------------------------------------------------------------------------

    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp = puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)

    event.getByLabel (npvLabel, npvHandle)
    numvert = npvHandle.product()
    nvtx = float(numvert[0])

    
    # -------------------------------------------------------------------------------------
    # find top quark for mtt cut
    # -------------------------------------------------------------------------------------

    if options.mttGenMax != None :
        event.getByLabel( genParticlesPtLabel, genParticlesPtHandle )
        event.getByLabel( genParticlesEtaLabel, genParticlesEtaHandle )
        event.getByLabel( genParticlesPhiLabel, genParticlesPhiHandle )
        event.getByLabel( genParticlesMassLabel, genParticlesMassHandle )
        event.getByLabel( genParticlesPdgIdLabel, genParticlesPdgIdHandle )
        event.getByLabel( genParticlesStatusLabel, genParticlesStatusHandle )

        genParticlesPt  = genParticlesPtHandle.product()
        genParticlesEta = genParticlesEtaHandle.product()
        genParticlesPhi = genParticlesPhiHandle.product()
        genParticlesMass   = genParticlesMassHandle.product()
        genParticlesPdgId  = genParticlesPdgIdHandle.product()
        genParticlesStatus = genParticlesStatusHandle.product()
        
        p4Top = ROOT.TLorentzVector()
        p4Antitop = ROOT.TLorentzVector()

        # loop over gen particles
        for igen in xrange( len(genParticlesPt) ) :

            if genParticlesStatus[igen] != 3 or abs(genParticlesPdgId[igen]) != 6 :
                continue
            
            if genParticlesPdgId[igen] == 6 :
                gen = ROOT.TLorentzVector()
                gen.SetPtEtaPhiM( genParticlesPt[igen], genParticlesEta[igen], genParticlesPhi[igen], genParticlesMass[igen] )                    
                p4Top = gen
            elif genParticlesPdgId[igen] == -6 :
                gen = ROOT.TLorentzVector()
                gen.SetPtEtaPhiM( genParticlesPt[igen], genParticlesEta[igen], genParticlesPhi[igen], genParticlesMass[igen] )
                p4Antitop = gen
    
        # cut on generated m(ttbar) if stitching sample 
        ttbarGen = p4Top + p4Antitop
        mttbarGen = ttbarGen.M()
        if mttbarGen > options.mttGenMax :
            continue
    #endif mttgenmax != none

    
    # -------------------------------------------------------------------------------------
    # find & count leptons
    # -------------------------------------------------------------------------------------
    
    nMuons = 0
    nElectrons = 0
    igoodMu = -1
    igoodEle = -1


    # -------------------------------------------------------------------------------------
    # muon channel
    # -------------------------------------------------------------------------------------

    if options.lepType == "muon":
        event.getByLabel (muonPtLabel, muonPtHandle)
        if not muonPtHandle.isValid():
            continue
        muonPts = muonPtHandle.product()

        event.getByLabel (muonPfisoLabel, muonPfisoHandle)
        if not muonPfisoHandle.isValid():
            continue
        muonPfisos = muonPfisoHandle.product()

        event.getByLabel (muonEtaLabel, muonEtaHandle)
        muonEtas = muonEtaHandle.product()

        # loop over muons and make selection
        for imuonPt in range(0,len(muonPts)):
            muonPt = muonPts[imuonPt]
            if muonPt > MIN_MU_PT and abs(muonEtas[imuonPt]) < MAX_MU_ETA :
                if options.useLoose :
                    if muonPfisos[imuonPt] / muonPt < MAX_MU_ISO :
                        continue
                    else :
                        nMuons += 1
                        igoodMu = imuonPt
                else :
                    if muonPfisos[imuonPt] / muonPt > MAX_MU_ISO :
                        continue
                    nMuons += 1
                    igoodMu = imuonPt


        # get information for electron veto
        event.getByLabel (electronPtLabel, electronPtHandle)
        if electronPtHandle.isValid() :
            electronPts = electronPtHandle.product()
            event.getByLabel (electronPfisoCHLabel, electronPfisoCHHandle)
            electronPfisoCHs = electronPfisoCHHandle.product()
            event.getByLabel (electronPfisoNHLabel, electronPfisoNHHandle)
            electronPfisoNHs = electronPfisoNHHandle.product()
            event.getByLabel (electronPfisoPHLabel, electronPfisoPHHandle)
            electronPfisoPHs = electronPfisoPHHandle.product()
            event.getByLabel (electronEtaLabel, electronEtaHandle)
            electronEtas = electronEtaHandle.product()

            event.getByLabel (rhoLabel, rhoHandle)
            rho = rhoHandle.product()

            # loop over electrons
            for ielectronPt in range(0,len(electronPts)) :
                electronPt = electronPts[ielectronPt]
                electronEta = electronEtas[ielectronPt]
                electronPfiso = electronPfisoCHs[ielectronPt] + max(0.0, electronPfisoNHs[ielectronPt] + electronPfisoPHs[ielectronPt] - rho[0] * getAeff(electronEtas[ielectronPt]))
                if (electronPt > MIN_EL_PT and abs(electronEta) < MAX_EL_ETA and electronPfiso / electronPt < MAX_EL_ISO) :
                    nElectrons += 1


    # -------------------------------------------------------------------------------------
    # electron channel
    # -------------------------------------------------------------------------------------

    if options.lepType == "ele" :
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

        # loop over electrons and make selection
        for ielectronPt in range(0,len(electronPts)):
            electronPt = electronPts[ielectronPt]
            electronPfiso = electronPfisoCHs[ielectronPt] + max(0.0, electronPfisoNHs[ielectronPt] + electronPfisoPHs[ielectronPt] - rho[0] * getAeff(electronEtas[ielectronPt]))
            if electronPt > MIN_EL_PT and abs(electronEtas[ielectronPt]) < MAX_EL_ETA :
                if options.useLoose :
                    if electronPfiso / electronPt < MAX_EL_ETA :
                        continue
                    else :
                        nElectrons += 1
                        igoodEle = ielectronPt
                else :
                    if electronPfiso / electronPt > MAX_EL_ETA :
                        continue
                    nElectrons += 1
                    igoodEle = ielectronPt

        # get information for muon veto
        event.getByLabel (muonPtLabel, muonPtHandle)
        if muonPts.isValid() :
            muonPts = muonPtHandle.product()
            event.getByLabel (muonPfisoLabel, muonPfisoHandle)
            muonPfisos = muonPfisoHandle.product()
            event.getByLabel (muonEtaLabel, muonEtaHandle)
            muonEtas = muonEtaHandle.product()

            # loop over muons
            for imuonPt in range(0,len(muonPts)) :
                muonPt = muonPts[imuonPt]
                muonEta = muonEtas[imuonPt]
                muonPfiso = muonPfisos[imuonPt]
                if (muonPt > MIN_MU_PT and abs(muonEta) < MAX_MU_ETA and muonPfiso / muonPt < MAX_MU_ISO) :
                    nMuons += 1

    
    # -------------------------------------------------------------------------------------
    # require exactly one lepton
    # -------------------------------------------------------------------------------------
            
    if options.lepType == "muon" :
        if nMuons != 1 :
            continue
        if nElectrons != 0 :
            continue
	
    if options.lepType == "ele" :
        if nElectrons != 1 :
            continue
        if nMuons != 0 : 
            continue


    # -------------------------------------------------------------------------------------
    # Now look at the rest of the lepton information.
    # We will classify jets based on hemispheres, defined by the lepton.
    # -------------------------------------------------------------------------------------

    if options.lepType == "muon" :
        event.getByLabel (muonPhiLabel, muonPhiHandle)
        muonPhis = muonPhiHandle.product()

        lepPt  = muonPts[igoodMu]
        lepEta = muonEtas[igoodMu]
        lepPhi = muonPhis[igoodMu]
        lepMass = 0.105
        lepPfIso = muonPfisos[igoodMu]

    if options.lepType == "ele" :
        event.getByLabel (electronPhiLabel, electronPhiHandle)
        electronPhis = electronPhiHandle.product()

        electronPfiso = electronPfisoCHs[igoodEle] + max(0.0, electronPfisoNHs[igoodEle] + electronPfisoPHs[igoodEle] - rho[0] * getAeff(electronEtas[igoodEle]))

        lepPt  = electronPts[igoodEle]
        lepEta = electronEtas[igoodEle]
        lepPhi = electronPhis[igoodEle]
        lepMass = 0.0
        lepPfIso = electronPfiso

    lepP4 = ROOT.TLorentzVector()
    lepP4.SetPtEtaPhiM( lepPt, lepEta, lepPhi, lepMass )

        
    # -------------------------------------------------------------------------------------
    # read AK5 jet information
    # -------------------------------------------------------------------------------------

    event.getByLabel (ak5JetPtLabel, ak5JetPtHandle)
    ak5JetPts = ak5JetPtHandle.product()
    event.getByLabel (ak5JetEtaLabel, ak5JetEtaHandle)
    ak5JetEtas = ak5JetEtaHandle.product()
    event.getByLabel (ak5JetPhiLabel, ak5JetPhiHandle)
    ak5JetPhis = ak5JetPhiHandle.product()
    event.getByLabel (ak5JetMassLabel, ak5JetMassHandle)
    ak5JetMasss = ak5JetMassHandle.product()
    event.getByLabel (ak5JetCSVLabel, ak5JetCSVHandle)
    ak5JetCSVs = ak5JetCSVHandle.product()
    event.getByLabel (ak5JetSecvtxMassLabel, ak5JetSecvtxMassHandle)
    ak5JetSecvtxMasses = ak5JetSecvtxMassHandle.product()


    # -------------------------------------------------------------------------------------
    # read gen jets if doing JER systematics
    # -------------------------------------------------------------------------------------

    ak5GenJets = []
    ca8GenJets = []
    if len(ak5JetPts) > 0 and options.jerSys != None :

        event.getByLabel( ak5GenJetPtLabel, ak5GenJetPtHandle )
        event.getByLabel( ak5GenJetEtaLabel, ak5GenJetEtaHandle )
        event.getByLabel( ak5GenJetPhiLabel, ak5GenJetPhiHandle )
        event.getByLabel( ak5GenJetMassLabel, ak5GenJetMassHandle )
        event.getByLabel( ca8GenJetPtLabel, ca8GenJetPtHandle )
        event.getByLabel( ca8GenJetEtaLabel, ca8GenJetEtaHandle )
        event.getByLabel( ca8GenJetPhiLabel, ca8GenJetPhiHandle )
        event.getByLabel( ca8GenJetMassLabel, ca8GenJetMassHandle )

        if ak5GenJetPtHandle.isValid() == False :
            continue

        ak5GenJetPt   = ak5GenJetPtHandle.product()
        ak5GenJetEta  = ak5GenJetEtaHandle.product()
        ak5GenJetPhi  = ak5GenJetPhiHandle.product()
        ak5GenJetMass = ak5GenJetMassHandle.product()

        if len(ak5GenJetPt) == 0 :
            continue

        # loop over AK5 gen jets
        for iak5 in xrange( len(ak5GenJetPt) ) :
            p4 = ROOT.TLorentzVector()
            p4.SetPtEtaPhiM( ak5GenJetPt[iak5], ak5GenJetEta[iak5], ak5GenJetPhi[iak5], ak5GenJetMass[iak5] )
            ak5GenJets.append(p4)

        if ca8GenJetPtHandle.isValid() == False :
            continue

        ca8GenJetPt   = ca8GenJetPtHandle.product()
        ca8GenJetEta  = ca8GenJetEtaHandle.product()
        ca8GenJetPhi  = ca8GenJetPhiHandle.product()
        ca8GenJetMass = ca8GenJetMassHandle.product()
        
        if len(ca8GenJetPt) == 0 :
            continue

        # loop over CA8 gen jets
        for ica8 in xrange( len(ca8GenJetPt) ) :
            p4 = ROOT.TLorentzVector()
            p4.SetPtEtaPhiM( ca8GenJetPt[ica8], ca8GenJetEta[ica8], ca8GenJetPhi[ica8], ca8GenJetMass[ica8] )
            ca8GenJets.append(p4)


    # -------------------------------------------------------------------------------------
    # read MET 
    # -------------------------------------------------------------------------------------

    event.getByLabel (metLabel, metHandle)
    mets = metHandle.product()
    metRaw = mets[0]
    event.getByLabel (metphiLabel, metphiHandle)
    metphis = metphiHandle.product()
    metphi = metphis[0]
    met_px = metRaw * math.cos( metphi )
    met_py = metRaw * math.sin( metphi )
    


    # -------------------------------------------------------------------------------------
    # loop over AK 5 jets
    # -------------------------------------------------------------------------------------

    ak5Jets = [] #list of smeared/corrected jets
    ht = 0.0

    for ijet in xrange( len(ak5JetPts) ) :

        # get the uncorrected jets
        thisJet = ROOT.TLorentzVector()
        thisJet.SetPtEtaPhiM( ak5JetPts[ijet], ak5JetEtas[ijet], ak5JetPhis[ijet], ak5JetMasss[ijet] )
        jetScale = 1.0

        # first smear the jets
        if options.jerSys != None :
            genJet = findClosestInList( thisJet, ak5GenJets )
            scale = options.jerSys  #JER nominal=0.1, up=0.2, down=0.0
            recopt = thisJet.Perp()
            genpt = genJet.Perp()
            deltapt = (recopt-genpt)*scale
            ptscale = max(0.0, (recopt+deltapt)/recopt)
            jetScale *= ptscale
        
        # then do the jet corrections
        if options.jecSys != None :
            jecUncAK5.setJetEta( ak5JetEtas[ijet] )
            jecUncAK5.setJetPt( ak5JetPts[ijet] )                    
            upOrDown = bool(options.jecSys > 0.0)
            unc = abs(jecUncAK5.getUncertainty(upOrDown))
            jetScale += unc * options.jecSys

        # remove the uncorrected/smeared jets from MET
        met_px = met_px + thisJet.Px()
        met_py = met_py + thisJet.Py()
        
        # scale the jet & add to list
        thisJet = thisJet * jetScale
        ak5Jets.append( thisJet )

        # add back the corrected jets to MET
        met_px = met_px - thisJet.Px()
        met_py = met_py - thisJet.Py()

        # make selection on the corrected jets!!
        if (thisJet.Perp() < MIN_JET_PT or abs(thisJet.Eta()) > MAX_JET_ETA) :
            continue

        # calculate HT (scalar sum of jet pt)
        ht += thisJet.Perp()
            
    
    # -------------------------------------------------------------------------------------
    # define met and htlep
    # -------------------------------------------------------------------------------------
    
    met = math.sqrt(met_px*met_px + met_py*met_py)
    metv = ROOT.TLorentzVector()
    metv.SetPtEtaPhiM( met, 0.0, metphi, 0.0)

    # HT_lep = scalar sum of jet pt (HT) & lepton pt
    htLep = ht + lepP4.Perp()

    # MET+lepton pt variable
    lepmet = met + lepP4.Perp()

    
    # -------------------------------------------------------------------------------------
    # require >= 2 AK5 jets above 30 GeV
    # -------------------------------------------------------------------------------------

    nJets = 0
    for ijet in range(0,len(ak5Jets)) :
        if ak5Jets[ijet].Perp() > MIN_JET_PT and abs(ak5Jets[ijet].Eta()) < MAX_JET_ETA:
            nJets += 1

    if nJets < 2 :
        continue

    
    # -------------------------------------------------------------------------------------
    # read variables for CA8 jets
    # -------------------------------------------------------------------------------------

    event.getByLabel (topTagPtLabel, topTagPtHandle)
    if topTagPtHandle.isValid() == False :
        continue
    topTagPt = topTagPtHandle.product()    

    event.getByLabel (topTagPhiLabel, topTagPhiHandle)
    topTagPhi = topTagPhiHandle.product()
    event.getByLabel (topTagEtaLabel, topTagEtaHandle)
    topTagEta = topTagEtaHandle.product()
    event.getByLabel (topTagMassLabel, topTagMassHandle)
    topTagMass = topTagMassHandle.product()
    event.getByLabel (topTagMinMassLabel, topTagMinMassHandle)
    topTagMinMass = topTagMinMassHandle.product()
    event.getByLabel (topTagNSubjetsLabel, topTagNSubjetsHandle)
    topTagNSub = topTagNSubjetsHandle.product()


    ca8Jets = []  #list of smeared & corrected CA8 jets
    
    # loop over top-tagged jets
    for ijet in xrange( len(topTagPt) ) :
        
        # get the uncorrected jets
        thisJet = ROOT.TLorentzVector()
        thisJet.SetPtEtaPhiM( topTagPt[ijet], topTagEta[ijet], topTagPhi[ijet], topTagMass[ijet] )
        jetScale = 1.0

        # first smear the jets
        if options.jerSys != None :
            genJet = findClosestInList( thisJet, ca8GenJets )
            scale = options.jerSys
            recopt = thisJet.Perp()
            genpt = genJet.Perp()
            deltapt = (recopt-genpt)*scale
            ptscale = max(0.0, (recopt+deltapt)/recopt)
            jetScale *= ptscale

        # then do the jet corrections
        if options.jecSys != None :
            jecUncAK7.setJetEta( topTagEta[ijet] )
            jecUncAK7.setJetPt( topTagPt[ijet] )                    
            upOrDown = bool(options.jecSys > 0.0)
            unc1 = abs(jecUncAK7.getUncertainty(upOrDown))
            unc2 = flatJecUnc
            unc = math.sqrt(unc1*unc1 + unc2*unc2)
            jetScale += unc * options.jecSys

        # scale the jet
        thisJet = thisJet * jetScale
        
        # make selection on the corrected jet variables!
        if (thisJet.Perp() < MIN_JET_PT or abs(thisJet.Eta()) > MAX_JET_ETA):
            continue

        # add jet to list
        ca8Jets.append( thisJet )
               


    # -------------------------------------------------------------------------------------
    # require >=1 leptonic-side AK5 jet, >=1 hadronic-side CA8 jet with pt > jetPtCut
    # -------------------------------------------------------------------------------------

    hadJets = []      # CA8 jets with dR(jet,lepton) > pi/2
    hadJetsIndex = [] # identifier in full CA8 jet collection for CA8 jets with dR(jet,lepton) > pi/2
    lepJets = []      # AK5 jets with dR(jet,lepton) < pi/2
    lepcsvs = []      # CSV values of AK5 jets with dR(jet,lepton) < pi/2
    lepVtxMass = []   # secondary vertex mass of AK5 jets with dR(jet,lepton) < pi/2

    # loop over AK5 jets (leptonic side)
    for ijet in range(0,len(ak5Jets)) :
        if ak5Jets[ijet].Perp() > MIN_JET_PT and abs(ak5Jets[ijet].Eta()) < MAX_JET_ETA:
            jet = ak5Jets[ijet]
            if jet.DeltaR(lepP4) < ROOT.TMath.Pi() / 2.0 :
                lepJets.append(jet)
                lepcsvs.append(ak5JetCSVs[ijet])
                lepVtxMass.append(ak5JetSecvtxMasses[ijet])                    
                    
    # loop over CA8 jets (hadronic side)
    for ijet in range(0,len(ca8Jets)) :
        if ca8Jets[ijet].Perp() > MIN_JET_PT :
            jet = ca8Jets[ijet]
            if jet.DeltaR( lepP4 ) > ROOT.TMath.Pi() / 2.0 :
                hadJets.append( jet )
                hadJetsIndex.append( ijet )

    # require leptonic and hadronic side jets 
    if len(lepJets) < 1 or len(hadJets) < 1 or hadJets[0].Perp() < options.jetPtCut :
        continue
            

    # -------------------------------------------------------------------------------------
    # loop over the top-tagged jets in opposite hemisphere from lepton and
    # apply selection for "good" top-tagged jet 
    # -------------------------------------------------------------------------------------

    passSelection = False

    for ijet in range(0,len(hadJets)) :
        topjet = hadJets[ijet]
        itop = hadJetsIndex[ijet]

        if topjet.Perp() < 400.:  # top-tagged jet pt > 400 GeV
            continue
        if topTagNSub[itop] < 3:  # nsubjets >= 3
            continue 
        if topTagMinMass[itop] < 50.:  # min pairwise subjet mass > 50 GeV
            continue 
        if topjet.M() < 140. or topjet.M() > 250.:  # top-tagged jet mass [140, 250] GeV
            continue

        passSelection = True
    

    if passSelection == False:
        continue
    
    # -------------------------------------------------------------------------------------
    # EVENT PASSES MINIMAL SELECTION !!!!!
    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # check for b-tagged jet
    # -------------------------------------------------------------------------------------

    ntagslep = 0      # number of b-tagged jets
    i_leadbtag = -1   # identifier for finding leading b-tagged jet
    bjet_pt = 0       # pt of leading b-tagged jet
    bjet_vtxmass = 0  # secondary vertex mass of leading b-tagged jet
    bjet_eta = 0      # eta of leading b-tagged jet
    
    # loop over CSV discriminator values of leptonic-side AK5 jets
    for ijet in range(0,len(lepcsvs)) :
        lepjet = lepJets[ijet]
        lepcsv = lepcsvs[ijet]
        if lepcsv > options.bDiscCut :
            ntagslep += 1
            if (lepjet.Perp() > bjet_pt) :
                bjet_pt = lepjet.Perp()
                bjet_eta = lepjet.Eta()
                bjet_vtxmass = lepVtxMass[ijet]
                i_leadbtag = ijet

    # Fill Ntags inclusive histograms
    h_HTvsMET.Fill(ht,met,weight)
    h_HTvsHTLEP.Fill(ht,htLep,weight)
    h_HTLEPvsMET.Fill(htLep,met,weight)
    h_LEPMETvsMET.Fill(lepmet,met,weight)
    h_LEPMETvsHT.Fill(lepmet,ht,weight)
    h_LEPMETvsHTLEP.Fill(lepmet,htLep,weight)
    
    # Fill 0 btag histograms
    if ntagslep == 0:
        h_HT_0tag.Fill(ht, weight)
        h_HTLEP_0tag.Fill(htLep, weight)
        h_LEPMET_0tag.Fill(lepmet, weight)
        h_MET_0tag.Fill(met, weight)

    # Fill >=1 btag histograms (with proper weights)
    if ntagslep >= 1:
        # apply b-tagging SF 
        bweight = weight
        if options.isData == False :
            btagSF = getBtagSF(bjet_pt)
            if options.btagSys != None :
                btagSFerr = getBtagSFerror(bjet_pt)
                if options.btagSys > 0 :
                    btagSF += btagSFerr
                else :
                    btagSF -= btagSFerr
            bweight *= btagSF
    
        h_HTvsBtagJetPt.Fill(ht,bjet_pt,bweight)
        h_HTLEPvsBtagJetPt.Fill(htLep,bjet_pt,bweight)
        h_LEPMETvsBtagJetPt.Fill(lepmet,bjet_pt,bweight)
        h_BtagJetPtvsMET.Fill(bjet_pt,met,bweight)

        h_HT_btag.Fill(ht, bweight)
        h_HTLEP_btag.Fill(htLep, bweight)
        h_LEPMET_btag.Fill(lepmet, bweight)
        h_MET_btag.Fill(met, bweight)
        h_BtagJetPt_btag.Fill(bjet_pt, bweight)


# -------------------------------------------------------------------------------------
# END OF LOOPING OVER EVENTS!!!
# -------------------------------------------------------------------------------------

f.cd()
f.Write()
f.Close()


