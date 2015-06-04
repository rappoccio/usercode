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

# electrons
MIN_EL_PT  = 35.0
MAX_EL_ETA = 2.5

# jets
MIN_JET_PT  = 30.0
MAX_JET_ETA = 2.4

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

parser.add_option('--mttGenMax', metavar='J', type='float', action='store',
                  default=None,
                  dest='mttGenMax',
                  help='Maximum generator-level m_ttbar [GeV] to stitch together the ttbar samples.')

parser.add_option('--lepType', metavar='F', type='string', action='store',
                  default='muon',
                  dest='lepType',
                  help='Lepton type (ele or muon)')

parser.add_option('--pdfSet', metavar='J', type='float', action='store',
                  default=0.0,
                  dest='pdfSet',
                  help='which PDF set is used for ttbar? Options are 0 (CT10), 1 (MSTW), 2 (NNPDF). Default is 0.')

parser.add_option('--pdfSys', metavar='J', type='float', action='store',
                  default=0.0,
                  dest='pdfSys',
                  help='PDF Systematic variation. Options are +1 (scale up 1 sigma), 0 (nominal), -1 (down 1 sigma for 3 PDF sets). Default is 0.0')

parser.add_option('--pileup', metavar='F', type='string', action='store',
                  default='none',
                  dest='pileup',
                  help='What pileup histogram should be used? ttbar, wjets, sts, stt, sttw, stsb, sttb, sttwb')

parser.add_option('--oddeven', metavar='J', type='float', action='store',
                  default=None,
                  dest='oddeven',
                  help='Run on only odd (option==1) even (option==2) events (based on event ID) for unfolding closure test.')


(options, args) = parser.parse_args()
argv = []

import ROOT
ROOT.gROOT.Macro("rootlogon.C")

## array needed for response matrix binning
from array import *

ROOT.gSystem.Load("../RooUnfold-1.1.1/libRooUnfold")


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

class GenTopQuark :
    pdgId = 6                    # 6 = top, -6 = antitop
    p4 = ROOT.TLorentzVector()
    decay = 0                    # 0 = hadronic, 1 = leptonic
    def __init__( self, pdgId, p4, decay ) :
        self.pdgId = pdgId
        self.p4 = p4
        self.decay = decay
    def match( self, jets ) :
        return findClosestInList( self.p4, jets )


import sys
from DataFormats.FWLite import Events, Handle

start_time = time.time()


# -------------------------------------------------------------------------------------
# input and output files
# -------------------------------------------------------------------------------------

print 'Getting these files : ' + options.files

files = glob.glob( options.files )
print files

f = ROOT.TFile(options.outname+".root", "recreate")
name = options.outname


# -------------------------------------------------------------------------------------
# define all the histograms
# -------------------------------------------------------------------------------------

print "Creating histograms"


# read input histogram for PU
if options.pileup=='ttbarQ2up' or options.pileup=='ttbarQ2dn':
    PileFile = ROOT.TFile("../Pileup_plots_scaleupdnnom.root")
else:
    PileFile = ROOT.TFile("../Pileup_plots.root")
PilePlot = PileFile.Get("pweight" + options.pileup)

f.cd()

### only relevant for m(ttbar)<700 GeV - histos without mttgen cut applied
h_ttbar_mass_all_incl     = ROOT.TH1F("ttbar_mass_all_incl",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_ttbar_mass_pt400_incl   = ROOT.TH1F("ttbar_mass_pt400_incl", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_hadtop_mass_all_incl    = ROOT.TH1F("hadtop_mass_all_incl",   ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_mass_pt400_incl  = ROOT.TH1F("hadtop_mass_pt400_incl", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_pt_all_incl      = ROOT.TH1F("hadtop_pt_all_incl",   ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_hadtop_pt_pt400_incl    = ROOT.TH1F("hadtop_pt_pt400_incl", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_hadtop_eta_all_incl     = ROOT.TH1F("hadtop_eta_all_incl",   ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
h_hadtop_eta_pt400_incl   = ROOT.TH1F("hadtop_eta_pt400_incl", ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
hw_ttbar_mass_all_incl    = ROOT.TH1F("w_ttbar_mass_all_incl",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
hw_ttbar_mass_pt400_incl  = ROOT.TH1F("w_ttbar_mass_pt400_incl", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
hw_hadtop_mass_all_incl   = ROOT.TH1F("w_hadtop_mass_all_incl",   ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_hadtop_mass_pt400_incl = ROOT.TH1F("w_hadtop_mass_pt400_incl", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_hadtop_pt_all_incl     = ROOT.TH1F("w_hadtop_pt_all_incl",   ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_hadtop_pt_pt400_incl   = ROOT.TH1F("w_hadtop_pt_pt400_incl", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_hadtop_eta_all_incl     = ROOT.TH1F("w_hadtop_eta_all_incl",   ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
hw_hadtop_eta_pt400_incl   = ROOT.TH1F("w_hadtop_eta_pt400_incl", ";#eta(hadronic top); Events / 0.025", 240, -3, 3)

### all semileptonic events
h_ttbar_mass_all_emutau   = ROOT.TH1F("ttbar_mass_all_emutau",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_ttbar_mass_pt400_emutau = ROOT.TH1F("ttbar_mass_pt400_emutau", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_hadtop_mass_all_emutau    = ROOT.TH1F("hadtop_mass_all_emutau",   ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_mass_pt400_emutau  = ROOT.TH1F("hadtop_mass_pt400_emutau", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_pt_all_emutau      = ROOT.TH1F("hadtop_pt_all_emutau",   ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_hadtop_pt_pt400_emutau    = ROOT.TH1F("hadtop_pt_pt400_emutau", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_hadtop_eta_all_emutau     = ROOT.TH1F("hadtop_eta_all_emutau",   ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
h_hadtop_eta_pt400_emutau   = ROOT.TH1F("hadtop_eta_pt400_emutau", ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
hw_ttbar_mass_all_emutau   = ROOT.TH1F("w_ttbar_mass_all_emutau",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
hw_ttbar_mass_pt400_emutau = ROOT.TH1F("w_ttbar_mass_pt400_emutau", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
hw_hadtop_mass_all_emutau   = ROOT.TH1F("w_hadtop_mass_all_emutau",   ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_hadtop_mass_pt400_emutau = ROOT.TH1F("w_hadtop_mass_pt400_emutau", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_hadtop_pt_all_emutau     = ROOT.TH1F("w_hadtop_pt_all_emutau",   ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_hadtop_pt_pt400_emutau   = ROOT.TH1F("w_hadtop_pt_pt400_emutau", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_hadtop_eta_all_emutau     = ROOT.TH1F("w_hadtop_eta_all_emutau",   ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
hw_hadtop_eta_pt400_emutau   = ROOT.TH1F("w_hadtop_eta_pt400_emutau", ";#eta(hadronic top); Events / 0.025", 240, -3, 3)

### semileptonic ttbar --> MUON+jets final state
h_ttbar_mass_all   = ROOT.TH1F("ttbar_mass_all",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_ttbar_mass_pt400 = ROOT.TH1F("ttbar_mass_pt400", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
h_ttbar_pt_all     = ROOT.TH1F("ttbar_pt_all",   ";p_{T}(t#bar{t}) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_ttbar_pt_pt400   = ROOT.TH1F("ttbar_pt_pt400", ";p_{T}(t#bar{t}) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_ttbar_mass_all   = ROOT.TH1F("w_ttbar_mass_all",   ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
hw_ttbar_mass_pt400 = ROOT.TH1F("w_ttbar_mass_pt400", ";Mass(t#bar{t}) [GeV]; Events / 10 GeV", 300, 0, 3000)
hw_ttbar_pt_all     = ROOT.TH1F("w_ttbar_pt_all",   ";p_{T}(t#bar{t}) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_ttbar_pt_pt400   = ROOT.TH1F("w_ttbar_pt_pt400", ";p_{T}(t#bar{t}) [GeV]; Events / 5 GeV", 300, 0, 1500)

h_hadtop_mass_all   = ROOT.TH1F("hadtop_mass_all",   ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_mass_pt400 = ROOT.TH1F("hadtop_mass_pt400", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_mass_pt400_pass = ROOT.TH1F("hadtop_mass_pt400_pass", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_hadtop_pt_all     = ROOT.TH1F("hadtop_pt_all",   ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_hadtop_pt_pt400   = ROOT.TH1F("hadtop_pt_pt400", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_hadtop_pt_pt400_pass = ROOT.TH1F("hadtop_pt_pt400_pass", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_hadtop_eta_all     = ROOT.TH1F("hadtop_eta_all",   ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
h_hadtop_eta_pt400   = ROOT.TH1F("hadtop_eta_pt400", ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
h_hadtop_eta_pt400_pass   = ROOT.TH1F("hadtop_eta_pt400_pass", ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
hw_hadtop_mass_all   = ROOT.TH1F("w_hadtop_mass_all",   ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_hadtop_mass_pt400 = ROOT.TH1F("w_hadtop_mass_pt400", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_hadtop_mass_pt400_pass = ROOT.TH1F("w_hadtop_mass_pt400_pass", ";Mass(hadronic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_hadtop_pt_all     = ROOT.TH1F("w_hadtop_pt_all",   ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_hadtop_pt_pt400   = ROOT.TH1F("w_hadtop_pt_pt400", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_hadtop_pt_pt400_pass = ROOT.TH1F("w_hadtop_pt_pt400_pass", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_hadtop_eta_all     = ROOT.TH1F("w_hadtop_eta_all",   ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
hw_hadtop_eta_pt400   = ROOT.TH1F("w_hadtop_eta_pt400", ";#eta(hadronic top); Events / 0.025", 240, -3, 3)
hw_hadtop_eta_pt400_pass   = ROOT.TH1F("w_hadtop_eta_pt400_pass", ";#eta(hadronic top); Events / 0.025", 240, -3, 3)

h_leptop_mass_all   = ROOT.TH1F("leptop_mass_all",   ";Mass(leptonic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_leptop_mass_pt400 = ROOT.TH1F("leptop_mass_pt400", ";Mass(leptonic top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_leptop_pt_all     = ROOT.TH1F("leptop_pt_all",   ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
h_leptop_pt_pt400   = ROOT.TH1F("leptop_pt_pt400", ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_leptop_mass_all   = ROOT.TH1F("w_leptop_mass_all",   ";Mass(leptonic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_leptop_mass_pt400 = ROOT.TH1F("w_leptop_mass_pt400", ";Mass(leptonic top) [GeV]; Events / 1 GeV", 300, 0, 300)
hw_leptop_pt_all     = ROOT.TH1F("w_leptop_pt_all",   ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0, 1500)
hw_leptop_pt_pt400   = ROOT.TH1F("w_leptop_pt_pt400", ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0, 1500)

h_lep_eta_all   = ROOT.TH1F("lep_eta_all",   ";Muon #eta; Events / 0.025", 240, -3, 3)
h_lep_eta_pt400 = ROOT.TH1F("lep_eta_pt400", ";Muon #eta; Events / 0.025", 240, -3, 3)
h_lep_pt_all    = ROOT.TH1F("lep_pt_all",    ";Muon p_{T} [GeV]; Events / 1 GeV", 300, 0, 300)
h_lep_pt_pt400  = ROOT.TH1F("lep_pt_pt400",  ";Muon p_{T} [GeV]; Events / 1 GeV", 300, 0, 300)
hw_lep_eta_all   = ROOT.TH1F("w_lep_eta_all",   ";Muon #eta; Events / 0.025", 240, -3, 3)
hw_lep_eta_pt400 = ROOT.TH1F("w_lep_eta_pt400", ";Muon #eta; Events / 0.025", 240, -3, 3)
hw_lep_pt_all    = ROOT.TH1F("w_lep_pt_all",    ";Muon p_{T} [GeV]; Events / 1 GeV", 300, 0, 300)
hw_lep_pt_pt400  = ROOT.TH1F("w_lep_pt_pt400",  ";Muon p_{T} [GeV]; Events / 1 GeV", 300, 0, 300)

# dummy histogram used only to specify dimensions for reponse matrix
ptbins = array('d',[0.0,200.0,400.0,500.0,600.0,700.0,800.0,1200.0,2000.0])
h_bins = ROOT.TH1F("bins",       ";;", len(ptbins)-1,       ptbins)

h_ptGenTop          = ROOT.TH1F("ptGenTop",          ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_ptGenTop_noweight = ROOT.TH1F("ptGenTop_noweight", ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)

h_ptPartTop_raw          = ROOT.TH1F("ptPartTop_raw",          ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_ptPartTop_raw_noweight = ROOT.TH1F("ptPartTop_raw_noweight", ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)

h_ptPartTop          = ROOT.TH1F("ptPartTop",          ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_massPartTop        = ROOT.TH1F("massPartTop",        ";Mass(particle-level top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_etaPartTop         = ROOT.TH1F("etaPartTop",         ";#eta(particle-level top); Events / 0.025", 240, -3, 3)
h_ptPartTop_noweight   = ROOT.TH1F("ptPartTop_noweight",   ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_massPartTop_noweight = ROOT.TH1F("massPartTop_noweight", ";Mass(particle-level top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_etaPartTop_noweight  = ROOT.TH1F("etaPartTop_noweight",  ";#eta(particle-level top); Events / 0.025", 240, -3, 3)

### for acceptance correction / efficiency, all these are for semileptonic, ttbar->mu+jets only 
# passParton = pt(hadronic, gen-level top quark) > 400 GeV
# passParticle = pass particle-level selection (includes pt(particle-level top jet) > 400 GeV cut)
h_ptPartTop_passParticle       = ROOT.TH1F("ptPartTop_passParticle",   ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
h_massPartTop_passParticle     = ROOT.TH1F("massPartTop_passParticle", ";Mass(particle-level top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_etaPartTop_passParticle      = ROOT.TH1F("etaPartTop_passParticle",  ";#eta(particle-level top); Events / 0.025", 240, -3, 3)
h_ptPartTop_passParticleParton   = ROOT.TH1F("ptPartTop_passParticleParton",   ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
h_massPartTop_passParticleParton = ROOT.TH1F("massPartTop_passParticleParton", ";Mass(particle-level top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_etaPartTop_passParticleParton  = ROOT.TH1F("etaPartTop_passParticleParton",  ";#eta(particle-level top); Events / 0.025", 240, -3, 3)

h_ptPartTop_passParticle_noweight       = ROOT.TH1F("ptPartTop_passParticle_noweight",   ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
h_massPartTop_passParticle_noweight     = ROOT.TH1F("massPartTop_passParticle_noweight", ";Mass(particle-level top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_etaPartTop_passParticle_noweight      = ROOT.TH1F("etaPartTop_passParticle_noweight",  ";#eta(particle-level top); Events / 0.025", 240, -3, 3)
h_ptPartTop_passParticleParton_noweight   = ROOT.TH1F("ptPartTop_passParticleParton_noweight",   ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
h_massPartTop_passParticleParton_noweight = ROOT.TH1F("massPartTop_passParticleParton_noweight", ";Mass(particle-level top) [GeV]; Events / 1 GeV", 300, 0, 300)
h_etaPartTop_passParticleParton_noweight  = ROOT.TH1F("etaPartTop_passParticleParton_noweight",  ";#eta(particle-level top); Events / 0.025", 240, -3, 3)

h_ptGenTop_passParton          = ROOT.TH1F("ptGenTop_passParton",         ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_ptGenTop_passParticleParton  = ROOT.TH1F("ptGenTop_passParticleParton", ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_ptGenTop_passParton_noweight          = ROOT.TH1F("ptGenTop_passParton_noweight",         ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_ptGenTop_passParticleParton_noweight  = ROOT.TH1F("ptGenTop_passParticleParton_noweight", ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)

## current default bin widths
response_pp = ROOT.RooUnfoldResponse(h_bins, h_bins)
response_pp.SetName('response_pt_pp')


# -------------------------------------------------------------------------------------
# define all variables to be read from input files
# -------------------------------------------------------------------------------------

events = Events (files)

# event-level variables 
puHandle  = Handle("int")
puLabel   = ("pileup", "npvRealTrue")
npvHandle = Handle("unsigned int")
npvLabel  = ("pileup", "npv")

# variables for PDF systematics (three different PDF sets)
if options.pdfSys != 0.0 or options.pdfSet != 0.0: 
    pdfWeightCT10Handle  = Handle("std::vector<double>")
    pdfWeightCT10Label   = ("pdfWeights", "ct10weights")
    
    pdfWeightMSTWHandle  = Handle("std::vector<double>")
    pdfWeightMSTWLabel   = ("pdfWeights", "mstwweights")

    pdfWeightNNPDFHandle = Handle("std::vector<double>")
    pdfWeightNNPDFLabel  = ("pdfWeights", "nnpdfweights")

    
# gen-level particles
genParticlesPtHandle     = Handle("std::vector<float>")
genParticlesPtLabel      = ("pfShyftTupleTopQuarks", "pt")
genParticlesEtaHandle    = Handle("std::vector<float>")
genParticlesEtaLabel     = ("pfShyftTupleTopQuarks", "eta")
genParticlesPhiHandle    = Handle("std::vector<float>")
genParticlesPhiLabel     = ("pfShyftTupleTopQuarks", "phi")
genParticlesMassHandle   = Handle("std::vector<float>")
genParticlesMassLabel    = ("pfShyftTupleTopQuarks", "mass")
genParticlesPdgIdHandle  = Handle("std::vector<float>")
genParticlesPdgIdLabel   = ("pfShyftTupleTopQuarks", "pdgId")

# AK5 / CA8 gen jets
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
# need to fill response matrix with weights already from the beginning!
# -------------------------------------------------------------------------------------
weight_response = 1.0

lum = 19.7

sigma_ttbar_NNLO = 245.8 * 1000.
sigma_ttbar_NNLO_Q2up = 252.0 * 1000.
sigma_ttbar_NNLO_Q2dn = 237.4 * 1000.

Nmc_ttbar = 21675970
Nmc_TT_Mtt_700_1000 = 3082812
Nmc_TT_Mtt_1000_Inf = 1249111
Nmc_ttbar_Q2up = 14983686
Nmc_TT_Mtt_700_1000_Q2up = 2243672
Nmc_TT_Mtt_1000_Inf_Q2up = 1241650
Nmc_ttbar_Q2dn = 14545715*89./102.  ## temporary hack -- we're missing part of this dataset
Nmc_TT_Mtt_700_1000_Q2dn = 2170074
Nmc_TT_Mtt_1000_Inf_Q2dn = 1308090

e_TT_Mtt_0_700 = 1.0
e_TT_Mtt_700_1000 = 0.074
e_TT_Mtt_1000_Inf = 0.015
e_TT_Mtt_0_700_Q2up = 1.0
e_TT_Mtt_700_1000_Q2up = 0.074
e_TT_Mtt_1000_Inf_Q2up = 0.014
e_TT_Mtt_0_700_Q2dn = 1.0
e_TT_Mtt_700_1000_Q2dn = 0.081
e_TT_Mtt_1000_Inf_Q2dn = 0.016


## m < 700 GeV
if "max700" in options.outname and "scaleup" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2up * e_TT_Mtt_0_700_Q2up * lum / float(Nmc_ttbar_Q2up)
elif "max700" in options.outname and "scaledown" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2dn * e_TT_Mtt_0_700_Q2dn * lum / float(Nmc_ttbar_Q2dn)
elif "max700" in options.outname :
    weight_response = sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar)
## 700 < m < 100 GeV 
elif "700to1000" in options.outname and "scaleup" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2up * e_TT_Mtt_700_1000_Q2up * lum / float(Nmc_TT_Mtt_700_1000_Q2up)
elif "700to1000" in options.outname and "scaledown" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2dn * e_TT_Mtt_700_1000_Q2dn * lum / float(Nmc_TT_Mtt_700_1000_Q2dn)
elif "700to1000" in options.outname :
    weight_response = sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000)
## 1000 < m < inf GeV
elif "1000toInf" in options.outname and "scaleup" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2up * e_TT_Mtt_1000_Inf_Q2up * lum / float(Nmc_TT_Mtt_1000_Inf_Q2up)
elif "1000toInf" in options.outname and "scaledown" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2dn * e_TT_Mtt_1000_Inf_Q2dn * lum / float(Nmc_TT_Mtt_1000_Inf_Q2dn)
elif "1000toInf" in options.outname:
    weight_response = sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf)


# -------------------------------------------------------------------------------------
# start looping over events
# -------------------------------------------------------------------------------------

ntotal = 0

print "Start looping over events!"

for event in events :
        
    weight = 1.0 #event weight

    if ntotal % 10000 == 0:
      print  '--------- Processing Event ' + str(ntotal)
    ntotal += 1
    
    if options.oddeven != 'none':
        # odd only
        if options.oddeven == 1 and event.object().id().event()%2 == 1 :
            continue
        # event only
        if options.oddeven == 2 and event.object().id().event()%2 == 0 :
            continue
    
    ## various pass/fail for unfolding 
    passParton = False         ## this means pt(gen-level hadronic top) > 400 GeV
    passParticle = False       ## this means "loose particle-level selection" PLUS pt(particle-level top jet) > 400 GeV 
    passParticleLoose = False  ## loose particle-level selection


    # -------------------------------------------------------------------------------------
    # read PU information & do PU reweighting
    # -------------------------------------------------------------------------------------

    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp = puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)


    # -------------------------------------------------------------------------------------
    # If doing PDF systematatics:
    # Get the envelopes of the various PDF sets for this event.
    # Use the max and min values of all of the eigenvectors as the envelope. 
    # -------------------------------------------------------------------------------------

    if options.pdfSys != 0.0 or options.pdfSet != 0.0 :
        
        if options.pdfSet == 1.0 :
            event.getByLabel( pdfWeightMSTWLabel, pdfWeightMSTWHandle )
            if pdfWeightMSTWHandle.isValid() == False :
                continue
            pdfWeight  = pdfWeightMSTWHandle.product()
        elif options.pdfSet == 2.0 :
            event.getByLabel( pdfWeightNNPDFLabel, pdfWeightNNPDFHandle )
            if pdfWeightNNPDFHandle.isValid() == False :
                continue
            pdfWeight = pdfWeightNNPDFHandle.product()
        else :
            event.getByLabel( pdfWeightCT10Label, pdfWeightCT10Handle )
            if pdfWeightCT10Handle.isValid() == False :
                continue
            pdfWeight  = pdfWeightCT10Handle.product()
        

        nMembers = len(pdfWeight)
        nEigenVec = int((nMembers-1)/2) #the list of PDF weights is w0 (==1 for CT10), w1+, w1-, w2+, w2-, ...

        
        this_pdfweight = 1.0

        if options.pdfSys == 0 :   # reweight to a different PDF set
            newweight = pdfWeight[0] 
            weight *= newweight
            this_pdfweight = newweight
        elif options.pdfSet == 2.0 and options.pdfSys > 0 :   # upward PDF uncertainty for NNPDF (non-Hessian set...!!)
            tmpweight = 0.0
            for iw in range(1,nMembers) :
                tmpweight += (1.0 - pdfWeight[iw])*(1.0 - pdfWeight[iw])
            tmpweight = tmpweight/(nMembers-1)
            tmpweight = 1.0 + math.sqrt(tmpweight)
            weight *= tmpweight
            this_pdfweight = tmpweight
        elif options.pdfSet == 2.0 and options.pdfSys < 0 :   # downward PDF uncertainty for NNPDF (non-Hessian set...!!)
            tmpweight = 0.0
            for iw in range(1,nMembers) :
                tmpweight += (1.0 - pdfWeight[iw])*(1.0 - pdfWeight[iw])
            tmpweight = tmpweight/(nMembers-1)
            tmpweight = 1.0 - math.sqrt(tmpweight)
            weight *= tmpweight
            this_pdfweight = tmpweight
        elif options.pdfSys > 0 :   # upward PDF uncertainty
            upweight = 0.0
            for iw in range(0,nEigenVec) :
                tmpweight = 0.0
                if (pdfWeight[1+2*iw] - 1.0) > tmpweight :
                    tmpweight = pdfWeight[0+2*iw] - 1.0
                if (pdfWeight[2+2*iw] - 1.0) > tmpweight :
                    tmpweight = pdfWeight[1+2*iw] - 1.0
                upweight += tmpweight*tmpweight
            upweight = 1.0 + math.sqrt(upweight)
            weight *= upweight
            this_pdfweight = upweight
        else :   # downward PDF uncertainty
            dnweight = 0.0
            for iw in range(0,nEigenVec) :
                tmpweight = 0.0
                if (1.0 - pdfWeight[1+2*iw]) > tmpweight :
                    tmpweight = 1.0 - pdfWeight[0+2*iw]
                if (1.0 - pdfWeight[2+2*iw]) > tmpweight :
                    tmpweight = 1.0 - pdfWeight[1+2*iw]
                dnweight += tmpweight*tmpweight
            dnweight = 1.0 - math.sqrt(dnweight)
            weight *= dnweight
            this_pdfweight = dnweight

        ## ignore potential events with crazy pdf weight (one CT10 pdf up weight...)
        if (this_pdfweight > 100.0):
            print "WARNING!! really large PDF weight for pdfset # " + str(options.pdfSet) + " syst # " + str(options.pdfSys) + ", weight = " + str(this_pdfweight) + " -- i'm ignoring this event!!"
            continue

    
    #endof if doing pdfSys

    # -------------------------------------------------------------------------------------
    # read / store truth information
    # -------------------------------------------------------------------------------------

    topQuarks = []
    genMuons = []
    genElectrons = []
    hadTop = None
    lepTop = None
    ttbar = None
    isSemiLeptonicGen = True
    isMuon = False
    isElectron = False
    
    event.getByLabel( genParticlesPtLabel, genParticlesPtHandle )
    event.getByLabel( genParticlesEtaLabel, genParticlesEtaHandle )
    event.getByLabel( genParticlesPhiLabel, genParticlesPhiHandle )
    event.getByLabel( genParticlesMassLabel, genParticlesMassHandle )
    event.getByLabel( genParticlesPdgIdLabel, genParticlesPdgIdHandle )
    
    genParticlesPt  = genParticlesPtHandle.product()
    genParticlesEta = genParticlesEtaHandle.product()
    genParticlesPhi = genParticlesPhiHandle.product()
    genParticlesMass   = genParticlesMassHandle.product()
    genParticlesPdgId  = genParticlesPdgIdHandle.product()

    p4Top = ROOT.TLorentzVector()
    p4Antitop = ROOT.TLorentzVector()
    topDecay = 0        # 0 = hadronic, 1 = leptonic
    antitopDecay = 0    # 0 = hadronic, 1 = leptonic

    leptonEta = 0
    leptonPt = 0


    # -------------------------------------------------------------------------------------
    # loop over gen particles
    for igen in xrange( len(genParticlesPt) ) :

        if  abs(genParticlesPdgId[igen]) < 6 :
            continue
        if  abs(genParticlesPdgId[igen]) > 16 :
            continue
            
        if genParticlesPdgId[igen] == 6 :
            gen = ROOT.TLorentzVector()
            gen.SetPtEtaPhiM( genParticlesPt[igen], genParticlesEta[igen], genParticlesPhi[igen], genParticlesMass[igen] )                
            p4Top = gen
        elif genParticlesPdgId[igen] == -6 :
            gen = ROOT.TLorentzVector()
            gen.SetPtEtaPhiM( genParticlesPt[igen], genParticlesEta[igen], genParticlesPhi[igen], genParticlesMass[igen] )
            p4Antitop = gen

        # If there is an antilepton (e+, mu+, tau+) then the top is leptonic
        elif ( genParticlesPdgId[igen] == -11 or genParticlesPdgId[igen] == -13 or genParticlesPdgId[igen] == -15) :
            topDecay = 1
        # If there is an lepton (e-, mu-, tau-) then the antitop is leptonic
        elif ( genParticlesPdgId[igen] == 11 or genParticlesPdgId[igen] == 13 or genParticlesPdgId[igen] == 15) :                
            antitopDecay = 1

        if (abs(genParticlesPdgId[igen]) == 13) :
            isMuon = True
            p4Muon = ROOT.TLorentzVector()
            p4Muon.SetPtEtaPhiM( genParticlesPt[igen], genParticlesEta[igen], genParticlesPhi[igen], genParticlesMass[igen] )
            genMuons.append(p4Muon)
            leptonEta = genParticlesEta[igen]
            leptonPt = genParticlesPt[igen]

        if (abs(genParticlesPdgId[igen]) == 11) :
            isElectron = True
            p4Electron = ROOT.TLorentzVector()
            p4Electron.SetPtEtaPhiM( genParticlesPt[igen], genParticlesEta[igen], genParticlesPhi[igen], genParticlesMass[igen] )
            genElectrons.append(p4Electron)
            leptonEta = genParticlesEta[igen]
            leptonPt = genParticlesPt[igen]

    # -------------------------------------------------------------------------------------
    # end loop over gen particles
    # -------------------------------------------------------------------------------------

    topQuarks.append( GenTopQuark( 6, p4Top, topDecay) )
    topQuarks.append( GenTopQuark( -6, p4Antitop, antitopDecay) )
        
    if topDecay + antitopDecay == 1 :
        isSemiLeptonicGen = True
    else :
        isSemiLeptonicGen = False
        
    # consider semi-leptonic ttbar decays only !
    if isSemiLeptonicGen == False :
        continue	
    
    if topDecay == 0 :
        hadTop = topQuarks[0]
        lepTop = topQuarks[1]
    else :
        hadTop = topQuarks[1]
        lepTop = topQuarks[0]
        
    ttbar = hadTop.p4 + lepTop.p4

    
    # -------------------------------------------------------------------------------------
    # fill histograms!        
    # -------------------------------------------------------------------------------------

    ## histograms without mtt gen.level cut
    h_ttbar_mass_all_incl.Fill( ttbar.M() )
    h_hadtop_mass_all_incl.Fill( hadTop.p4.M() )
    h_hadtop_pt_all_incl.Fill( hadTop.p4.Perp() )
    h_hadtop_eta_all_incl.Fill( hadTop.p4.Eta() )
    hw_ttbar_mass_all_incl.Fill( ttbar.M(), weight )
    hw_hadtop_mass_all_incl.Fill( hadTop.p4.M(), weight )
    hw_hadtop_pt_all_incl.Fill( hadTop.p4.Perp(), weight )
    hw_hadtop_eta_all_incl.Fill( hadTop.p4.Eta(), weight )

    if hadTop.p4.Perp() > 400. :
        h_ttbar_mass_pt400_incl.Fill( ttbar.M() )
        h_hadtop_mass_pt400_incl.Fill( hadTop.p4.M() )
        h_hadtop_pt_pt400_incl.Fill( hadTop.p4.Perp() )
        h_hadtop_eta_pt400_incl.Fill( hadTop.p4.Eta() )
        hw_ttbar_mass_pt400_incl.Fill( ttbar.M(), weight )
        hw_hadtop_mass_pt400_incl.Fill( hadTop.p4.M(), weight )
        hw_hadtop_pt_pt400_incl.Fill( hadTop.p4.Perp(), weight )
        hw_hadtop_eta_pt400_incl.Fill( hadTop.p4.Eta(), weight )


    ## cut on generated m(ttbar) if stitching sample
    if options.mttGenMax is not None :
        if ttbar.M() > options.mttGenMax :
            continue

    ## histograms for e+mu+tau final states
    h_ttbar_mass_all_emutau.Fill( ttbar.M() )
    h_hadtop_mass_all_emutau.Fill( hadTop.p4.M() )
    h_hadtop_pt_all_emutau.Fill( hadTop.p4.Perp() )
    h_hadtop_eta_all_emutau.Fill( hadTop.p4.Eta() )
    hw_ttbar_mass_all_emutau.Fill( ttbar.M(), weight )
    hw_hadtop_mass_all_emutau.Fill( hadTop.p4.M(), weight )
    hw_hadtop_pt_all_emutau.Fill( hadTop.p4.Perp(), weight )
    hw_hadtop_eta_all_emutau.Fill( hadTop.p4.Eta(), weight )

    if hadTop.p4.Perp() > 400. :
        h_ttbar_mass_pt400_emutau.Fill( ttbar.M() )
        h_hadtop_mass_pt400_emutau.Fill( hadTop.p4.M() )
        h_hadtop_pt_pt400_emutau.Fill( hadTop.p4.Perp() )
        h_hadtop_eta_pt400_emutau.Fill( hadTop.p4.Eta() )
        hw_ttbar_mass_pt400_emutau.Fill( ttbar.M(), weight )
        hw_hadtop_mass_pt400_emutau.Fill( hadTop.p4.M(), weight )
        hw_hadtop_pt_pt400_emutau.Fill( hadTop.p4.Perp(), weight )
        hw_hadtop_eta_pt400_emutau.Fill( hadTop.p4.Eta(), weight )

    ## now require mu/e+jets final state only
    if ((isMuon == False) or (isElectron == True)) and (options.lepType == "muon"):
		continue
    if ((isMuon == True) or (isElectron == False)) and (options.lepType == "ele"):
		continue

    ## passParton?
    if hadTop.p4.Perp() > 400.0:
        passParton = True

    # -------------------------------------------------------------------------------------
    # fill histograms!        
    # -------------------------------------------------------------------------------------
    
    ## fill rest of histograms        
    h_ttbar_mass_all.Fill( ttbar.M() )
    h_ttbar_pt_all.Fill( ttbar.Perp() )
    h_hadtop_mass_all.Fill( hadTop.p4.M() )
    h_hadtop_pt_all.Fill( hadTop.p4.Perp() )
    h_hadtop_eta_all.Fill( hadTop.p4.Eta() )
    h_leptop_mass_all.Fill( lepTop.p4.M() )
    h_leptop_pt_all.Fill( lepTop.p4.Perp() )
    h_lep_eta_all.Fill(leptonEta)    
    h_lep_pt_all.Fill(leptonPt)

    hw_ttbar_mass_all.Fill( ttbar.M(), weight )
    hw_ttbar_pt_all.Fill( ttbar.Perp(), weight )
    hw_hadtop_mass_all.Fill( hadTop.p4.M(), weight )
    hw_hadtop_pt_all.Fill( hadTop.p4.Perp(), weight )
    hw_hadtop_eta_all.Fill( hadTop.p4.Eta(), weight )
    hw_leptop_mass_all.Fill( lepTop.p4.M(), weight )
    hw_leptop_pt_all.Fill( lepTop.p4.Perp(), weight )
    hw_lep_eta_all.Fill(leptonEta, weight)    
    hw_lep_pt_all.Fill(leptonPt, weight)

    if passParton :
        h_ttbar_mass_pt400.Fill( ttbar.M() )
        h_ttbar_pt_pt400.Fill( ttbar.Perp() )            
        h_hadtop_mass_pt400.Fill( hadTop.p4.M() )
        h_hadtop_pt_pt400.Fill( hadTop.p4.Perp() )
        h_hadtop_eta_pt400.Fill( hadTop.p4.Eta() )
        h_leptop_mass_pt400.Fill( lepTop.p4.M() )
        h_leptop_pt_pt400.Fill( lepTop.p4.Perp() )
        h_lep_eta_pt400.Fill(leptonEta)
        h_lep_pt_pt400.Fill(leptonPt)

        hw_ttbar_mass_pt400.Fill( ttbar.M(), weight )
        hw_ttbar_pt_pt400.Fill( ttbar.Perp(), weight )            
        hw_hadtop_mass_pt400.Fill( hadTop.p4.M(), weight )
        hw_hadtop_pt_pt400.Fill( hadTop.p4.Perp(), weight )
        hw_hadtop_eta_pt400.Fill( hadTop.p4.Eta(), weight )
        hw_leptop_mass_pt400.Fill( lepTop.p4.M(), weight )
        hw_leptop_pt_pt400.Fill( lepTop.p4.Perp(), weight )
        hw_lep_eta_pt400.Fill(leptonEta, weight)
        hw_lep_pt_pt400.Fill(leptonPt, weight)

        if abs(leptonEta)<2.1 and leptonPt>40 :
            h_hadtop_mass_pt400_pass.Fill(hadTop.p4.M())
            h_hadtop_pt_pt400_pass.Fill(hadTop.p4.Perp())
            h_hadtop_eta_pt400_pass.Fill(hadTop.p4.Eta())
            hw_hadtop_mass_pt400_pass.Fill(hadTop.p4.M(), weight)
            hw_hadtop_pt_pt400_pass.Fill(hadTop.p4.Perp(), weight)
            hw_hadtop_eta_pt400_pass.Fill(hadTop.p4.Eta(), weight)

    ## more histograms to compare with unfolding 

    h_ptGenTop.Fill( hadTop.p4.Perp(), weight )
    h_ptGenTop_noweight.Fill( hadTop.p4.Perp() )
        
    if passParton :
        h_ptGenTop_passParton.Fill(hadTop.p4.Perp(), weight)
        h_ptGenTop_passParton_noweight.Fill(hadTop.p4.Perp())


        
    ak5GenJets = []
    ca8GenJets = []

    
    # -------------------------------------------------------------------------------------
    # get AK5 gen jets
    # -------------------------------------------------------------------------------------

    event.getByLabel( ak5GenJetPtLabel, ak5GenJetPtHandle )
    if ak5GenJetPtHandle.isValid() == False :
        response_pp.Miss( hadTop.p4.Perp(), weight*weight_response )
        continue
    event.getByLabel( ak5GenJetEtaLabel, ak5GenJetEtaHandle )
    event.getByLabel( ak5GenJetPhiLabel, ak5GenJetPhiHandle )
    event.getByLabel( ak5GenJetMassLabel, ak5GenJetMassHandle )
    
    ak5GenJetPt   = ak5GenJetPtHandle.product()
    ak5GenJetEta  = ak5GenJetEtaHandle.product()
    ak5GenJetPhi  = ak5GenJetPhiHandle.product()
    ak5GenJetMass = ak5GenJetMassHandle.product()
    
    if len(ak5GenJetPt) == 0 :
        response_pp.Miss( hadTop.p4.Perp(), weight*weight_response )
        continue

    # loop over AK5 gen jets
    for iak5 in xrange( len(ak5GenJetPt) ) :
        p4 = ROOT.TLorentzVector()
        p4.SetPtEtaPhiM( ak5GenJetPt[iak5], ak5GenJetEta[iak5], ak5GenJetPhi[iak5], ak5GenJetMass[iak5] )
        ak5GenJets.append(p4)

        
    # -------------------------------------------------------------------------------------
    # get CA8 gen jets
    # -------------------------------------------------------------------------------------

    event.getByLabel( ca8GenJetPtLabel, ca8GenJetPtHandle )
    if ca8GenJetPtHandle.isValid() == False :
        response_pp.Miss( hadTop.p4.Perp(), weight*weight_response )
        continue
    event.getByLabel( ca8GenJetEtaLabel, ca8GenJetEtaHandle )
    event.getByLabel( ca8GenJetPhiLabel, ca8GenJetPhiHandle )
    event.getByLabel( ca8GenJetMassLabel, ca8GenJetMassHandle )
    
    ca8GenJetPt   = ca8GenJetPtHandle.product()
    ca8GenJetEta  = ca8GenJetEtaHandle.product()
    ca8GenJetPhi  = ca8GenJetPhiHandle.product()
    ca8GenJetMass = ca8GenJetMassHandle.product()
    
    if len(ca8GenJetPt) == 0 :
        response_pp.Miss( hadTop.p4.Perp(), weight*weight_response )
        continue

    # loop over CA8 gen jets
    for ica8 in xrange( len(ca8GenJetPt) ) :
        p4 = ROOT.TLorentzVector()
        p4.SetPtEtaPhiM( ca8GenJetPt[ica8], ca8GenJetEta[ica8], ca8GenJetPhi[ica8], ca8GenJetMass[ica8] )
        ca8GenJets.append(p4)


    # -------------------------------------------------------------------------------------
    # implement particle-level selection
    # -------------------------------------------------------------------------------------

    nGenLeptons = 0
    nGenBJets = 0
    nGenTops = 0
    genLepton = ROOT.TLorentzVector()
    genTops = []

    if (options.lepType == "muon") :
        for iMuon in genMuons:
            if iMuon.Perp() > MIN_MU_PT and abs(iMuon.Eta()) < MAX_MU_ETA:  ## pt>45, |eta|<2.1
                nGenLeptons += 1
                genLepton = iMuon
    else :
        for iEle in genElectrons:
            if iEle.Perp() > MIN_MU_PT and abs(iEle.Eta()) < MAX_MU_ETA:  ## pt>45, |eta|<2.1  (same selection as for muons here!)
                nGenLeptons += 1
                genLepton = iEle

    if nGenLeptons == 1:
        for iak5Gen in ak5GenJets:
            if iak5Gen.DeltaR(genLepton) < ROOT.TMath.Pi() / 2.0 and iak5Gen.Perp() > MIN_JET_PT and abs(iak5Gen.Eta()) < MAX_JET_ETA:
                nGenBJets += 1

        for ica8Gen in ca8GenJets:
            if ica8Gen.DeltaR(genLepton) > ROOT.TMath.Pi() / 2.0 and ica8Gen.Perp() > MIN_JET_PT and abs(ica8Gen.Eta()) < MAX_JET_ETA:
                genTops.append(ica8Gen)
                nGenTops += 1

    if nGenLeptons == 1 and nGenBJets > 0 and nGenTops > 0:
        passParticleLoose = True
            
    if passParticleLoose and genTops[0].Perp() > 400.0 :
        passParticle = True

    if nGenTops > 0:
        h_ptPartTop_raw.Fill( genTops[0].Perp(), weight )
        h_ptPartTop_raw_noweight.Fill( genTops[0].Perp() )

    ## loose particle-level selection w/o 400 cut
    if passParticleLoose == False:
        response_pp.Miss( hadTop.p4.Perp(), weight*weight_response )
    else:
        h_ptPartTop.Fill( genTops[0].Perp(), weight )
        h_ptPartTop_noweight.Fill( genTops[0].Perp() )
        h_etaPartTop.Fill( genTops[0].Eta(), weight )
        h_etaPartTop_noweight.Fill( genTops[0].Eta() )
        h_massPartTop.Fill( genTops[0].M(), weight )
        h_massPartTop_noweight.Fill( genTops[0].M() )
        response_pp.Fill(genTops[0].Perp(), hadTop.p4.Perp(), weight*weight_response)

    ## particle-level selection *with* 400 cut
    if passParticle:
        h_ptPartTop_passParticle.Fill(genTops[0].Perp(), weight) 
        h_ptPartTop_passParticle_noweight.Fill(genTops[0].Perp()) 
        h_etaPartTop_passParticle.Fill(genTops[0].Eta(), weight) 
        h_etaPartTop_passParticle_noweight.Fill(genTops[0].Eta()) 
        h_massPartTop_passParticle.Fill(genTops[0].M(), weight) 
        h_massPartTop_passParticle_noweight.Fill(genTops[0].M()) 

        if passParton: 
            h_ptPartTop_passParticleParton.Fill(genTops[0].Perp(), weight) 
            h_ptPartTop_passParticleParton_noweight.Fill(genTops[0].Perp()) 
            h_etaPartTop_passParticleParton.Fill(genTops[0].Eta(), weight) 
            h_etaPartTop_passParticleParton_noweight.Fill(genTops[0].Eta()) 
            h_massPartTop_passParticleParton.Fill(genTops[0].M(), weight) 
            h_massPartTop_passParticleParton_noweight.Fill(genTops[0].M()) 
            h_ptGenTop_passParticleParton.Fill(hadTop.p4.Perp(), weight)
            h_ptGenTop_passParticleParton_noweight.Fill(hadTop.p4.Perp())

    ## end particle-level selection
    
    
 
# -------------------------------------------------------------------------------------
# END OF LOOPING OVER EVENTS!!!
# -------------------------------------------------------------------------------------

f.cd()

response_pp.Write()

f.Write()
f.Close()

print "Total time = " + str( time.time() - start_time) + " seconds"
