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
MAX_MU_ISO_FOR_CLEANING = 0.20

# electrons
MIN_EL_PT  = 35.0
MAX_EL_ETA = 2.5
MAX_EL_ISO = 0.1
MAX_EL_ISO_FOR_CLEANING = 0.15

# jets
MIN_JET_PT  = 30.0
MAX_JET_ETA = 2.4


# -------------------------------------------------------------------------------------
# helper class for leptons and different isolations
# -------------------------------------------------------------------------------------
class Lepton :
    def __init__(self, p4, leptype, isoForCleaning, isoPU ) :
        self.p4_ = p4
        self.leptype_ = leptype
        self.isoForCleaning_ = isoForCleaning
        self.isoPU_ = isoPU
        self.wasCleaned_ = None
        self.goodForVeto_ = None
        self.goodForPrimary_ = None
    def __str__(self) :
        s = 'Lep    {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f}), iso {5:6.2f}, cleaning iso {6:6.2f}'.format( 0, self.p4().Perp(), self.p4().Eta(), self.p4().Phi(), self.p4().M(), self.isoPU_, self.isoForCleaning_ )
        return s
    def p4(self) :
        return self.p4_
    def leptype(self) :
        return self.leptype_
    def getIsoForCleaning(self) :
        return self.isoForCleaning_
    def getIsoPU(self ):
        return self.isoPU_
    def setAsCleaned ( self, value = True ) :
        self.wasCleaned_ = value
    def setGoodForVeto( self, value = True ) :
        self.goodForVeto_ = value
    def setGoodForPrimary ( self, value = True ) :
        self.goodForPrimary_ = value
    def wasCleaned(self) :
        return self.wasCleaned_
    def goodForVeto(self) :
        return self.goodForVeto_
    def goodForPrimary (self) :
        return self.goodForPrimary_


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
# Lepton trigger * ID SF
def getMuonSF(muEta) :

    muSF = 1.0
    if abs(muEta) < 0.9 :
        muSF = 0.9815 * 0.9930
    elif abs(muEta) < 1.2 :
        muSF = 0.9622 * 0.9942
    else :
        muSF = 0.9906 * 0.9968

    return float(muSF)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Jet energy resolution (nominal, up/down) for AK5 jets
def getJER(jetEta, jerType) :

    jerSF = 1.0

    if ( (jerType==0 or jerType==-1 or jerType==1) == False):
        print "ERROR: Can't get JER! use type=0 (nom), -1 (down), +1 (up)"
        return float(jerSF)

    etamin = [0.0,0.5,1.1,1.7,2.3,2.8,3.2]
    etamax = [0.5,1.1,1.7,2.3,2.8,3.2,5.0]
    
    scale_nom = [1.079,1.099,1.121,1.208,1.254,1.395,1.056]
    scale_dn  = [1.053,1.071,1.092,1.162,1.192,1.332,0.865]
    scale_up  = [1.105,1.127,1.150,1.254,1.316,1.458,1.247]

    for iSF in range(0,len(scale_nom)) :
        if abs(jetEta) >= etamin[iSF] and abs(jetEta) < etamax[iSF] :
            if jerType < 0 :
                jerSF = scale_dn[iSF]
            elif jerType > 0 :
                jerSF = scale_up[iSF]
            else :
                jerSF = scale_nom[iSF]
            break

    return float(jerSF)
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

parser.add_option('--doQCD', metavar='F', action='store_true',
                  default=False,
                  dest='doQCD',
                  help='Use loose leptons (exclusive from tight), for QCD studies')

parser.add_option('--use2Dcut', metavar='F', action='store_true',
                  default=True,
                  dest='use2Dcut',
                  help='Use 2D cut instead of relative isolation')

parser.add_option('--jetPtCut', metavar='F', type='float', action='store',
                  default=200.0,
                  dest='jetPtCut',
                  help='CA8 hadronic-side PT cut of leading jet (default is 200.0) [GeV]')

parser.add_option('--mttGenMax', metavar='J', type='float', action='store',
                  default=None,
                  dest='mttGenMax',
                  help='Maximum generator-level m_ttbar [GeV] to stitch together the ttbar samples.')

parser.add_option('--semilep', metavar='J', type='float',action='store',
                  default=None,
                  dest='semilep',
                  help='Select only semileptonic ttbar decays (1) or only non-semileptonic ttbar decays (-1) or no such cut (None)')

parser.add_option('--bDiscCut', metavar='F', type='float', action='store',
                  default=0.679,
                  dest='bDiscCut',
                  help='b-tagging discriminator cut (default is 0.679, medium working point for CSV tagger)')

parser.add_option('--jerSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='jerSys',
                  help='JER Systematic variation in fraction. Default is None.')


(options, args) = parser.parse_args()
argv = []

import ROOT
ROOT.gROOT.Macro("rootlogon.C")

## array needed for response matrix binning
from array import *



# -------------------------------------------------------------------------------------
# jet energy correction uncertainties & smearing
# -------------------------------------------------------------------------------------

# Read JEC uncertainties
if options.jerSys != None :
    ROOT.gSystem.Load('libCondFormatsJetMETObjects')
    jecParStrAK5 = ROOT.std.string('START53_V27_Uncertainty_AK5PFchs.txt')
    jecUncAK5 = ROOT.JetCorrectionUncertainty( jecParStrAK5 )
    jecParStrAK7 = ROOT.std.string('START53_V27_Uncertainty_AK7PFchs.txt')
    jecUncAK7 = ROOT.JetCorrectionUncertainty( jecParStrAK7 )    


# -------------------------------------------------------------------------------------
# define helper classes that use ROOT
# -------------------------------------------------------------------------------------

def findClosestJet( ijet, hadJets ) :
    minDR = 9999.
    ret = -1
    for jjet in range(0,len(hadJets) ):
        if ijet == jjet :
            continue
        dR = hadJets[ijet].DeltaR(hadJets[jjet])
        if dR < minDR :
            minDR = hadJets[ijet].DeltaR(hadJets[jjet])
            ret = jjet
    return ret


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
PileFile = ROOT.TFile("Pileup_plots.root")
PilePlot = PileFile.Get("pweight" + options.pileup)

f.cd()

ptbins = array('d',[30, 40, 50, 60, 70, 80, 100, 120, 160, 220, 300, 400, 600, 800])


### filled for preselected events
h_btageff_C_den_b = ROOT.TH1F("btageff_C_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_C_den_c = ROOT.TH1F("btageff_C_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_C_den_l = ROOT.TH1F("btageff_C_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_C_num_b = ROOT.TH1F("btageff_C_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_C_num_c = ROOT.TH1F("btageff_C_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_C_num_l = ROOT.TH1F("btageff_C_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_C_num_b = ROOT.TH1F("btagvtxeff_C_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_C_num_c = ROOT.TH1F("btagvtxeff_C_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_C_num_l = ROOT.TH1F("btagvtxeff_C_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)

h_btageff_M_den_b = ROOT.TH1F("btageff_M_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_M_den_c = ROOT.TH1F("btageff_M_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_M_den_l = ROOT.TH1F("btageff_M_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_M_num_b = ROOT.TH1F("btageff_M_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_M_num_c = ROOT.TH1F("btageff_M_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_M_num_l = ROOT.TH1F("btageff_M_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_M_num_b = ROOT.TH1F("btagvtxeff_M_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_M_num_c = ROOT.TH1F("btagvtxeff_M_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_M_num_l = ROOT.TH1F("btagvtxeff_M_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)

h_btageff_H_den_b = ROOT.TH1F("btageff_H_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_H_den_c = ROOT.TH1F("btageff_H_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_H_den_l = ROOT.TH1F("btageff_H_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_H_num_b = ROOT.TH1F("btageff_H_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_H_num_c = ROOT.TH1F("btageff_H_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btageff_H_num_l = ROOT.TH1F("btageff_H_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_H_num_b = ROOT.TH1F("btagvtxeff_H_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_H_num_c = ROOT.TH1F("btagvtxeff_H_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h_btagvtxeff_H_num_l = ROOT.TH1F("btagvtxeff_H_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)


### filled for CA8 > 200 GeV
h2_btageff_C_den_b = ROOT.TH1F("btageff2_C_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_C_den_c = ROOT.TH1F("btageff2_C_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_C_den_l = ROOT.TH1F("btageff2_C_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_C_num_b = ROOT.TH1F("btageff2_C_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_C_num_c = ROOT.TH1F("btageff2_C_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_C_num_l = ROOT.TH1F("btageff2_C_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_C_num_b = ROOT.TH1F("btagvtxeff2_C_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_C_num_c = ROOT.TH1F("btagvtxeff2_C_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_C_num_l = ROOT.TH1F("btagvtxeff2_C_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)

h2_btageff_M_den_b = ROOT.TH1F("btageff2_M_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_M_den_c = ROOT.TH1F("btageff2_M_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_M_den_l = ROOT.TH1F("btageff2_M_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_M_num_b = ROOT.TH1F("btageff2_M_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_M_num_c = ROOT.TH1F("btageff2_M_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_M_num_l = ROOT.TH1F("btageff2_M_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_M_num_b = ROOT.TH1F("btagvtxeff2_M_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_M_num_c = ROOT.TH1F("btagvtxeff2_M_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_M_num_l = ROOT.TH1F("btagvtxeff2_M_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)

h2_btageff_H_den_b = ROOT.TH1F("btageff2_H_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_H_den_c = ROOT.TH1F("btageff2_H_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_H_den_l = ROOT.TH1F("btageff2_H_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_H_num_b = ROOT.TH1F("btageff2_H_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_H_num_c = ROOT.TH1F("btageff2_H_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btageff_H_num_l = ROOT.TH1F("btageff2_H_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_H_num_b = ROOT.TH1F("btagvtxeff2_H_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_H_num_c = ROOT.TH1F("btagvtxeff2_H_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h2_btagvtxeff_H_num_l = ROOT.TH1F("btagvtxeff2_H_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)


### filled for events with muons and 2 AK5 jets > 30 GeV
h3_btageff_C_den_b = ROOT.TH1F("btageff3_C_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_C_den_c = ROOT.TH1F("btageff3_C_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_C_den_l = ROOT.TH1F("btageff3_C_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_C_num_b = ROOT.TH1F("btageff3_C_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_C_num_c = ROOT.TH1F("btageff3_C_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_C_num_l = ROOT.TH1F("btageff3_C_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_C_num_b = ROOT.TH1F("btagvtxeff3_C_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_C_num_c = ROOT.TH1F("btagvtxeff3_C_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_C_num_l = ROOT.TH1F("btagvtxeff3_C_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)

h3_btageff_M_den_b = ROOT.TH1F("btageff3_M_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_M_den_c = ROOT.TH1F("btageff3_M_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_M_den_l = ROOT.TH1F("btageff3_M_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_M_num_b = ROOT.TH1F("btageff3_M_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_M_num_c = ROOT.TH1F("btageff3_M_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_M_num_l = ROOT.TH1F("btageff3_M_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_M_num_b = ROOT.TH1F("btagvtxeff3_M_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_M_num_c = ROOT.TH1F("btagvtxeff3_M_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_M_num_l = ROOT.TH1F("btagvtxeff3_M_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)

h3_btageff_H_den_b = ROOT.TH1F("btageff3_H_den_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_H_den_c = ROOT.TH1F("btageff3_H_den_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_H_den_l = ROOT.TH1F("btageff3_H_den_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_H_num_b = ROOT.TH1F("btageff3_H_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_H_num_c = ROOT.TH1F("btageff3_H_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btageff_H_num_l = ROOT.TH1F("btageff3_H_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_H_num_b = ROOT.TH1F("btagvtxeff3_H_num_b", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_H_num_c = ROOT.TH1F("btagvtxeff3_H_num_c", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)
h3_btagvtxeff_H_num_l = ROOT.TH1F("btagvtxeff3_H_num_l", ";Efficiency;jet p_{T} [GeV]", len(ptbins)-1, ptbins)


### old
#h2_btageff_den_b = ROOT.TH2F("btageff_den_b", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)
#h2_btageff_den_c = ROOT.TH2F("btageff_den_c", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)
#h2_btageff_den_l = ROOT.TH2F("btageff_den_l", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)
#h2_btageff_num_b = ROOT.TH2F("btageff_num_b", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)
#h2_btageff_num_c = ROOT.TH2F("btageff_num_c", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)
#h2_btageff_num_l = ROOT.TH2F("btageff_num_l", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)
#h2_btagvtxeff_num_b = ROOT.TH2F("btagvtxeff_num_b", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)
#h2_btagvtxeff_num_c = ROOT.TH2F("btagvtxeff_num_c", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)
#h2_btagvtxeff_num_l = ROOT.TH2F("btagvtxeff_num_l", ";jet p_{T} [GeV];jet #eta", 100, 0, 1000, 60, -3, 3)



# -------------------------------------------------------------------------------------
# define all variables to be read from input files
# -------------------------------------------------------------------------------------

events = Events (files)

# use the "loose" collections for QCD studies
postfix = ""
postfixLepton = "Loose"
if options.doQCD or options.use2Dcut :
	postfix = "Loose"


# event-level variables 
puHandle  = Handle("int")
puLabel   = ("pileup", "npvRealTrue")
npvHandle = Handle("unsigned int")
npvLabel  = ("pileup", "npv")

rhoHandle = Handle("double")
rhoLabel  = ("kt6PFJets", "rho")

# lepton variables
muonPtHandle    = Handle("std::vector<float>")
muonPtLabel     = ("pfShyftTupleMuons" + postfixLepton, "pt")
muonEtaHandle   = Handle( "std::vector<float>")
muonEtaLabel    = ("pfShyftTupleMuons" + postfixLepton, "eta")
muonPhiHandle   = Handle( "std::vector<float>")
muonPhiLabel    = ("pfShyftTupleMuons" + postfixLepton, "phi")
muonPfisoHandle = Handle( "std::vector<float>")
muonPfisoLabel  = ("pfShyftTupleMuons" + postfixLepton, "pfisoPU")
muonPfisoHandleFromCleaning = Handle( "std::vector<float>")
muonPfisoLabelFromCleaning  = ("pfShyftTupleMuons" + postfixLepton, "pfiso")

electronPtHandle      = Handle( "std::vector<float>")
electronPtLabel       = ("pfShyftTupleElectrons" + postfixLepton, "pt")
electronEtaHandle     = Handle( "std::vector<float>")
electronEtaLabel      = ("pfShyftTupleElectrons" + postfixLepton, "eta")
electronPhiHandle     = Handle( "std::vector<float>")
electronPhiLabel      = ("pfShyftTupleElectrons" + postfixLepton, "phi")
electronPfisoCHHandle = Handle( "std::vector<float>")
electronPfisoCHLabel  = ("pfShyftTupleElectrons" + postfixLepton, "pfisoCH")
electronPfisoNHHandle = Handle( "std::vector<float>")
electronPfisoNHLabel  = ("pfShyftTupleElectrons" + postfixLepton, "pfisoNH")
electronPfisoPHHandle = Handle( "std::vector<float>")
electronPfisoPHLabel  = ("pfShyftTupleElectrons" + postfixLepton, "pfisoPH")
electronPfisoHandleFromCleaning = Handle( "std::vector<float>")
electronPfisoLabelFromCleaning  = ("pfShyftTupleElectrons" + postfixLepton, "pfiso")

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
ak5JetFlavorHandle  = Handle( "std::vector<float>" )
ak5JetFlavorLabel   = ("pfShyftTupleJets" + postfix + "AK5", "flavor")

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
if options.mttGenMax is not None or options.semilep is not None: 
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
# also need the gen jets when doing particle-level unfolding
if options.jerSys != None:
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
# reset various counters
# -------------------------------------------------------------------------------------

ntotal = 0       # total number of events


# -------------------------------------------------------------------------------------
# start looping over events
# -------------------------------------------------------------------------------------

print "Start looping over events!"

for event in events :
    
    weight = 1.0 #event weight

    mttbarGen = -1.0

    if ntotal % 10000 == 0 :
      print  '--------- Processing Event ' + str(ntotal)
    ntotal += 1

    #print ""
    #print "event # " + str(ntotal)
    
    
    # -------------------------------------------------------------------------------------
    # read PU information & do PU reweighting
    # -------------------------------------------------------------------------------------

    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp = puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)

      
    # -------------------------------------------------------------------------------------
    # For unfolding stuides (i.e. if makeResponse == True):
    # Find the top and antitop quarks.
    # We also need to find the decay mode of the top and antitop quarks.
    # To do so, we look for leptons, and use their charge to assign
    # the correct decay mode to the correct quark. 
    # the below is also run if mttGenMax cut is to be applied 
    # or if splitting semileponic vs non-semileptonic ttbar decays
    # -------------------------------------------------------------------------------------

    topQuarks = []
    genMuons = []
    hadTop = None
    lepTop = None
    isSemiLeptonicGen = True
    isMuon = False
    
    if options.mttGenMax is not None or options.semilep is not None:
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
        topDecay = 0        # 0 = hadronic, 1 = leptonic
        antitopDecay = 0    # 0 = hadronic, 1 = leptonic
        
        # loop over gen particles
        for igen in xrange( len(genParticlesPt) ) :

            if genParticlesStatus[igen] != 3 :
                continue
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
        
        topQuarks.append( GenTopQuark( 6, p4Top, topDecay) )
        topQuarks.append( GenTopQuark( -6, p4Antitop, antitopDecay) )
        
        if (topDecay + antitopDecay == 1) and (isMuon == True) :
            isSemiLeptonicGen = True
        else :
            isSemiLeptonicGen = False

        # If we are filling the response matrix, don't
        # consider "volunteer" events that pass the selection
        # even though they aren't really semileptonic events. 

        if not (options.semilep < 0) and isSemiLeptonicGen == False :
            continue	

        if options.semilep > 0 and isSemiLeptonicGen == False:
            continue
        if options.semilep < 0 and isSemiLeptonicGen == True:
            continue
        
        if topDecay == 0 :
            hadTop = topQuarks[0]
            lepTop = topQuarks[1]
        else :
            hadTop = topQuarks[1]
            lepTop = topQuarks[0]

    
        # cut on generated m(ttbar) if stitching sample
        ttbarGen = hadTop.p4 + lepTop.p4
        mttbarGen = ttbarGen.M()

        if options.mttGenMax is not None :
            if mttbarGen > options.mttGenMax :
                continue

        # endif (making response matrix)

    
    # -------------------------------------------------------------------------------------
    # read gen jets if doing JER systematics or 2-step unfolding
    # -------------------------------------------------------------------------------------

    ak5GenJets = []
    ca8GenJets = []
    
    if options.jerSys != None:
        event.getByLabel( ak5GenJetPtLabel, ak5GenJetPtHandle )
        if ak5GenJetPtHandle.isValid() == False :
            continue
        event.getByLabel( ak5GenJetEtaLabel, ak5GenJetEtaHandle )
        event.getByLabel( ak5GenJetPhiLabel, ak5GenJetPhiHandle )
        event.getByLabel( ak5GenJetMassLabel, ak5GenJetMassHandle )

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

        event.getByLabel( ca8GenJetPtLabel, ca8GenJetPtHandle )
        if ca8GenJetPtHandle.isValid() == False :
            continue
        event.getByLabel( ca8GenJetEtaLabel, ca8GenJetEtaHandle )
        event.getByLabel( ca8GenJetPhiLabel, ca8GenJetPhiHandle )
        event.getByLabel( ca8GenJetMassLabel, ca8GenJetMassHandle )
        
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
    # read AK5 jet information
    # -------------------------------------------------------------------------------------

    event.getByLabel (ak5JetPtLabel, ak5JetPtHandle)
    if ak5JetPtHandle.isValid() == False : 
        continue
    
    ak5JetPts = ak5JetPtHandle.product()
    event.getByLabel (ak5JetEtaLabel, ak5JetEtaHandle)
    ak5JetEtas = ak5JetEtaHandle.product()
    event.getByLabel (ak5JetPhiLabel, ak5JetPhiHandle)
    ak5JetPhis = ak5JetPhiHandle.product()
    event.getByLabel (ak5JetMassLabel, ak5JetMassHandle)
    ak5JetMasss = ak5JetMassHandle.product()
    
    jetsFor2D = []
    for ijet in xrange( len(ak5JetPts) ) :
        if ak5JetPts[ijet] > 25 :
            theJet = ROOT.TLorentzVector()
            theJet.SetPtEtaPhiM( ak5JetPts[ijet], ak5JetEtas[ijet], ak5JetPhis[ijet], ak5JetMasss[ijet] )
            jetsFor2D.append(theJet)

    
    # -------------------------------------------------------------------------------------
    # find, categorize & count leptons
    # -------------------------------------------------------------------------------------
    
    nMuons = 0
    nMuonsForVeto = 0
    nElectrons = 0
    nElectronsForVeto = 0
    igoodMu = -1
    igoodEle = -1


    # Loop through the leptons.
    # We have several categories :
    #    1. Already cleaned via PF2PAT/PFBRECO top projection
    #    2. "Good enough" for a dilepton veto
    #    3. "Good" for primary lepton selection

    muons = []
    electrons = []
    leptons = []
    
    event.getByLabel (electronPtLabel, electronPtHandle)
    if electronPtHandle.isValid() :
        electronPts = electronPtHandle.product()
        event.getByLabel (electronPfisoCHLabel, electronPfisoCHHandle)
        electronPfisoCHs = electronPfisoCHHandle.product()
        event.getByLabel (electronPfisoNHLabel, electronPfisoNHHandle)
        electronPfisoNHs = electronPfisoNHHandle.product()
        event.getByLabel (electronPfisoPHLabel, electronPfisoPHHandle)
        electronPfisoPHs = electronPfisoPHHandle.product()
        event.getByLabel (electronPfisoLabelFromCleaning, electronPfisoHandleFromCleaning)
        electronPfisosFromCleaning = electronPfisoHandleFromCleaning.product()
        event.getByLabel (electronEtaLabel, electronEtaHandle)
        electronEtas = electronEtaHandle.product()
        event.getByLabel (electronPhiLabel, electronPhiHandle)
        electronPhis = electronPhiHandle.product()
        event.getByLabel (rhoLabel, rhoHandle)
        rho = rhoHandle.product()

        for ielectronPt in range(0,len(electronPts)) :
            electronPt = electronPts[ielectronPt]
            electronEta = electronEtas[ielectronPt]
            electronPhi = electronPhis[ielectronPt]
            electronPfisoFromCleaning = electronPfisosFromCleaning[ielectronPt]
            electronPfiso = electronPfisoCHs[ielectronPt] + max(0.0, electronPfisoNHs[ielectronPt] + electronPfisoPHs[ielectronPt] - rho[0] * getAeff(electronEtas[ielectronPt]))
            electronMass = 0.0
            p4 = ROOT.TLorentzVector()
            p4.SetPtEtaPhiM( electronPt, electronEta, electronPhi, electronMass )
            electron = Lepton( p4, 1, electronPfisoFromCleaning / electronPt, electronPfiso / electronPt)

            # Lepton with "pileup unsafe" isolation as was done
            # upstream in PF2PAT / PFBRECO top projection
            # to flag if it is already removed from the jet inputs.
            if electron.getIsoForCleaning() < MAX_EL_ISO_FOR_CLEANING :
                electron.setAsCleaned()

            # additional cleaning was done at SHyFT-making level for leptons for QCD studies
            if (options.doQCD or options.use2Dcut) and electron.getIsoForCleaning() > MAX_EL_ISO_FOR_CLEANING :
                electron.setAsCleaned()

            # Lepton with pileup safe isolation, and check if we want
            # signal or control region (for ABCD QCD estimate)
            if (electronPt > MIN_EL_PT and abs(electronEta) < MAX_EL_ETA ) :

                eleJet = findClosestInList( electron.p4(), jetsFor2D )

                # relative isolation cut
                if not options.use2Dcut :
                    if electronPfiso / electronPt < MAX_EL_ISO :
                        electron.setGoodForVeto()
                        nElectronsForVeto += 1
                    if not options.doQCD and electronPfiso / electronPt < MAX_EL_ISO :
                        nElectrons += 1
                        igoodEle = ielectronPt
                        electron.setGoodForPrimary()
                    elif options.doQCD and electron.getIsoForCleaning() > MAX_EL_ISO_FOR_CLEANING : #for now, use leptons with PU-unsafe iso > 0.15 for QCD
                        nElectrons += 1
                        igoodEle = ielectronPt
                        electron.setGoodForPrimary()
                # 2D isolation cut 
                else :
                    if electron.p4().DeltaR(eleJet) > 0.5 or electron.p4().Perp(eleJet.Vect()) > 25 :
                        electron.setGoodForVeto()
                        nElectronsForVeto += 1
                    if not options.doQCD and (electron.p4().DeltaR(eleJet) > 0.5 or electron.p4().Perp(eleJet.Vect()) > 25) :
                        nElectrons += 1
                        igoodEle = ielectronPt
                        electron.setGoodForPrimary()
                    elif options.doQCD and electron.p4().DeltaR(eleJet) < 0.5 and electron.p4().Perp(eleJet.Vect()) < 25 : 
                        nElectrons += 1
                        igoodEle = ielectronPt
                        electron.setGoodForPrimary()
                                    
            electrons.append(electron)


    event.getByLabel (muonPtLabel, muonPtHandle)
    if muonPtHandle.isValid() : 
        muonPts = muonPtHandle.product()
        event.getByLabel (muonPfisoLabel, muonPfisoHandle)
        muonPfisos = muonPfisoHandle.product()
        event.getByLabel (muonPfisoLabelFromCleaning, muonPfisoHandleFromCleaning)
        muonPfisosFromCleaning = muonPfisoHandleFromCleaning.product()
        event.getByLabel (muonEtaLabel, muonEtaHandle)
        muonEtas = muonEtaHandle.product()
        event.getByLabel (muonPhiLabel, muonPhiHandle)
        muonPhis = muonPhiHandle.product()

        for imuonPt in range(0,len(muonPts)) :
            muonPt = muonPts[imuonPt]
            muonEta = muonEtas[imuonPt]
            muonPhi = muonPhis[imuonPt]
            muonPfisoFromCleaning = muonPfisosFromCleaning[imuonPt]
            muonPfiso = muonPfisos[imuonPt]
            muonMass = 0.105
            p4 = ROOT.TLorentzVector()
            p4.SetPtEtaPhiM( muonPt, muonEta, muonPhi, muonMass )
            muon = Lepton( p4, 0, muonPfisoFromCleaning / muonPt, muonPfiso / muonPt)
            
            # Lepton with "pileup unsafe" isolation as was done
            # upstream in PF2PAT / PFBRECO top projection
            # to flag if it is already removed from the jet inputs.
            if muon.getIsoForCleaning() < MAX_MU_ISO_FOR_CLEANING :
                muon.setAsCleaned()

            # additional cleaning was done at SHyFT-making level for leptons for QCD studies
            if (options.doQCD or options.use2Dcut) and muon.getIsoForCleaning() > MAX_MU_ISO_FOR_CLEANING :
                muon.setAsCleaned()

            # Lepton with pileup safe isolation, and check if we want
            # signal or control region (for ABCD QCD estimate)
            if (muonPt > MIN_MU_PT and abs(muonEta) < MAX_MU_ETA ) :

                muJet = findClosestInList( muon.p4(), jetsFor2D )
                
                # relative isolation cut
                if not options.use2Dcut :
                    if muonPfiso / muonPt < MAX_MU_ISO :
                        muon.setGoodForVeto()
                        nMuonsForVeto += 1
                    if not options.doQCD and muonPfiso / muonPt < MAX_MU_ISO :
                        muon.setGoodForPrimary()
                        nMuons += 1
                        igoodMu = imuonPt
                    elif options.doQCD and muon.getIsoForCleaning() > MAX_MU_ISO_FOR_CLEANING : #for now, use leptons with PU-unsafe iso > 0.20 for QCD
                        muon.setGoodForPrimary()
                        nMuons += 1
                        igoodMu = imuonPt
                # 2D isolation cut
                else :
                    if muon.p4().DeltaR(muJet) > 0.5 or muon.p4().Perp(muJet.Vect()) > 25 :
                        muon.setGoodForVeto()
                        nMuonsForVeto += 1
                    if not options.doQCD and (muon.p4().DeltaR(muJet) > 0.5 or muon.p4().Perp(muJet.Vect()) > 25) :
                        muon.setGoodForPrimary()
                        nMuons += 1
                        igoodMu = imuonPt
                    elif options.doQCD and muon.p4().DeltaR(muJet) < 0.5 and muon.p4().Perp(muJet.Vect()) < 25 :
                        muon.setGoodForPrimary()
                        nMuons += 1
                        igoodMu = imuonPt

            muons.append(muon)


                    
    # -------------------------------------------------------------------------------------
    # muon channel
    # -------------------------------------------------------------------------------------

    cut1 = nMuons == 1 and nElectronsForVeto <= 0

    if nMuons > 1: 
        print "WARNING! This shouldn't happen! More than one muon!!!" 
    if nElectronsForVeto > 0: 
        print "WARNING! This shouldn't happen! More than one veto-electron!!!" 
    

    # -------------------------------------------------------------------------------------
    # electron channel
    # -------------------------------------------------------------------------------------

    cut2 = nElectrons == 1 and nMuonsForVeto <= 0

    
    # -------------------------------------------------------------------------------------
    # fill nbr of leptons plots & require exactly one lepton
    # -------------------------------------------------------------------------------------
    cut = None
    muonSF = 1.0
    if options.lepType == "muon":
        cut = cut1
        if nMuons == 1 and options.isData == False :
            muEta = muons[igoodMu].p4().Eta()
            muonSF = getMuonSF(muEta)
            weight = weight*muonSF
    else :
        cut = cut2
    
    leptons = muons + electrons
        
    if cut == False or cut == None: 
        continue

    
    # -------------------------------------------------------------------------------------
    # Now look at the rest of the lepton information.
    # We will classify jets based on hemispheres, defined by the lepton.
    # -------------------------------------------------------------------------------------

    if options.lepType == "ele" :
        lepton = electrons[igoodEle]
    else :
        lepton = muons[igoodMu]
    

    # -------------------------------------------------------------------------------------
    # loop over AK 5 jets
    # -------------------------------------------------------------------------------------

    ak5Jets = [] #list of smeared/corrected jets
    ht = 0.0

    for ijet in xrange( len(ak5JetPts) ) :

        # get the jets
        thisJet = ROOT.TLorentzVector()
        thisJet.SetPtEtaPhiM( ak5JetPts[ijet], ak5JetEtas[ijet], ak5JetPhis[ijet], ak5JetMasss[ijet] )

        jetScale = 1.0

        # first check if there are leptons that were not cleaned
        for ilepton in leptons :
            if ilepton.p4().DeltaR( thisJet ) < 0.5 and ilepton.wasCleaned() == False and ilepton.goodForPrimary() == True :
                print 'LEPTON WAS NOT CLEANED : '
                print ilepton
                thisJet = thisJet - ilepton.p4()
                
        # next smear the jets
        if options.jerSys != None :
            genJet = findClosestInList( thisJet, ak5GenJets )
            #scale = options.jerSys  #JER nominal=0.1, up=0.2, down=0.0
            my_jerSys = 0
            if options.jerSys == 0.2 :
                my_jerSys = 1
            elif options.jerSys == 0.0 :
                my_jerSys = -1
            scale = getJER(ak5JetEtas[ijet], my_jerSys) #JER nominal=0, up=+1, down=-1
            recopt = thisJet.Perp()
            genpt = genJet.Perp()
            deltapt = (recopt-genpt)*(scale-1.0)
            ptscale = max(0.0, (recopt+deltapt)/recopt)
            jetScale *= ptscale
        
        # scale the jet & add to list
        thisJet = thisJet * jetScale
        ak5Jets.append( thisJet )

        # make selection on the corrected jets!!
        if (thisJet.Perp() < MIN_JET_PT or abs(thisJet.Eta()) > MAX_JET_ETA) :
            continue
                
    
    # -------------------------------------------------------------------------------------
    # read CSV value and secondary vertex mass
    # -------------------------------------------------------------------------------------

    event.getByLabel (ak5JetCSVLabel, ak5JetCSVHandle)
    ak5JetCSVs = ak5JetCSVHandle.product()
    event.getByLabel (ak5JetSecvtxMassLabel, ak5JetSecvtxMassHandle)
    ak5JetSecvtxMasses = ak5JetSecvtxMassHandle.product()
    event.getByLabel (ak5JetFlavorLabel, ak5JetFlavorHandle)
    ak5JetFlavors = ak5JetFlavorHandle.product()

    
    nJets = 0.0
    i_goodjets = []
    csvs = []     
    vtxmasses = []
    flavors = []

    for ijet in range(0,len(ak5Jets)) :
        if ak5Jets[ijet].Perp() > MIN_JET_PT and abs(ak5Jets[ijet].Eta()) < MAX_JET_ETA:
            nJets += 1.0
            i_goodjets.append(ijet)
            csvs.append(ak5JetCSVs[ijet])
            vtxmasses.append(ak5JetSecvtxMasses[ijet])
            flavors.append(ak5JetFlavors[ijet])
    
    
    # -------------------------------------------------------------------------------------
    # STEP (1): require >= 2 AK5 jets above 30 GeV
    # -------------------------------------------------------------------------------------

    if nJets < 2 :
        continue


    # loop over CSV discriminator values
    for ijet in range(0,len(csvs)) :

        j_pt = ak5Jets[i_goodjets[ijet]].Perp()
        j_eta = ak5Jets[i_goodjets[ijet]].Eta()

        j_csv = csvs[ijet]
        j_vtxmass = vtxmasses[ijet]
        j_flavor = flavors[ijet]

        # all jets (denominator)
        if abs(j_flavor) == 5: # b-jet
            if abs(j_eta) < 0.8 :
                h3_btageff_C_den_b.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h3_btageff_M_den_b.Fill(j_pt, weight)
            else :
                h3_btageff_H_den_b.Fill(j_pt, weight)
        elif abs(j_flavor) == 4: # c-jet
            if abs(j_eta) < 0.8 :
                h3_btageff_C_den_c.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h3_btageff_M_den_c.Fill(j_pt, weight)
            else :
                h3_btageff_H_den_c.Fill(j_pt, weight)
        else: # light jet
            if abs(j_eta) < 0.8 :
                h3_btageff_C_den_l.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h3_btageff_M_den_l.Fill(j_pt, weight)
            else :
                h3_btageff_H_den_l.Fill(j_pt, weight)

        # jets passing b-tagging cut
        if j_csv > options.bDiscCut:
            if abs(j_flavor) == 5: # b-jet
                if abs(j_eta) < 0.8 :
                    h3_btageff_C_num_b.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h3_btageff_M_num_b.Fill(j_pt, weight)
                else :
                    h3_btageff_H_num_b.Fill(j_pt, weight)
            elif abs(j_flavor) == 4: # c-jet
                if abs(j_eta) < 0.8 :
                    h3_btageff_C_num_c.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h3_btageff_M_num_c.Fill(j_pt, weight)
                else :
                    h3_btageff_H_num_c.Fill(j_pt, weight)
            else: # light jet
                if abs(j_eta) < 0.8 :
                    h3_btageff_C_num_l.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h3_btageff_M_num_l.Fill(j_pt, weight)
                else :
                    h3_btageff_H_num_l.Fill(j_pt, weight)

        ## now the same thing, but checking b-tagging + vtxmass>0 cut            
        if j_csv > options.bDiscCut and j_vtxmass > 0.0:
            if abs(j_flavor) == 5: # b-jet
                if abs(j_eta) < 0.8 :
                    h3_btagvtxeff_C_num_b.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h3_btagvtxeff_M_num_b.Fill(j_pt, weight)
                else :
                    h3_btagvtxeff_H_num_b.Fill(j_pt, weight)
            elif abs(j_flavor) == 4: # c-jet
                if abs(j_eta) < 0.8 :
                    h3_btagvtxeff_C_num_c.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h3_btagvtxeff_M_num_c.Fill(j_pt, weight)
                else :
                    h3_btagvtxeff_H_num_c.Fill(j_pt, weight)
            else: # light jet
                if abs(j_eta) < 0.8 :
                    h3_btagvtxeff_C_num_l.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h3_btagvtxeff_M_num_l.Fill(j_pt, weight)
                else :
                    h3_btagvtxeff_H_num_l.Fill(j_pt, weight)
        
    #print "done with b-tagging checks!"

    
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

        # first check if there are leptons that were not cleaned
        for ilepton in leptons :
            if ilepton.p4().DeltaR( thisJet ) < 0.5 and ilepton.wasCleaned() == False and ilepton.goodForPrimary() :
                print 'LEPTON WAS NOT CLEANED : '
                print ilepton
                thisJet = thisJet - ilepton.p4()

        
        # next smear the jets (for CA8 jets, used the flat JER of 0.10, or 0.0/0.2 for down/up)
        if options.jerSys != None :
            genJet = findClosestInList( thisJet, ca8GenJets )
            scale = options.jerSys
            recopt = thisJet.Perp()
            genpt = genJet.Perp()
            deltapt = (recopt-genpt)*scale
            ptscale = max(0.0, (recopt+deltapt)/recopt)
            jetScale *= ptscale

        # scale the jet
        thisJet = thisJet * jetScale
        
        # make selection on the corrected jet variables!
        if (thisJet.Perp() < MIN_JET_PT or abs(thisJet.Eta()) > MAX_JET_ETA):
            continue

        # add jet to list
        ca8Jets.append( thisJet )
        


    # -------------------------------------------------------------------------------------
    # define hadronic (CA8)/leptonic (AK5) side jet, apply b-tagging, etc. 
    # -------------------------------------------------------------------------------------

    hadJets = []      # CA8 jets with dR(jet,lepton) > pi/2
    hadJetsIndex = [] # identifier in full CA8 jet collection for CA8 jets with dR(jet,lepton) > pi/2
    lepJets = []      # AK5 jets with dR(jet,lepton) < pi/2
    lepcsvs = []      # CSV values of AK5 jets with dR(jet,lepton) < pi/2
    lepVtxMass = []   # secondary vertex mass of AK5 jets with dR(jet,lepton) < pi/2
    lepFlavors = []   # Jet flavors of AK5 jets with dR(jet,lepton) < pi/2

    # loop over AK5 jets (leptonic side)
    for ijet in range(0,len(ak5Jets)) :
        if ak5Jets[ijet].Perp() > MIN_JET_PT and abs(ak5Jets[ijet].Eta()) < MAX_JET_ETA:
            jet = ak5Jets[ijet]
            if jet.DeltaR(lepton.p4()) < ROOT.TMath.Pi() / 2.0 :
                lepJets.append(jet)
                lepcsvs.append(ak5JetCSVs[ijet])
                lepVtxMass.append(ak5JetSecvtxMasses[ijet])
                lepFlavors.append(ak5JetFlavors[ijet])
                

    # loop over CA8 jets (hadronic side)
    for ijet in range(0,len(ca8Jets)) :
        if ca8Jets[ijet].Perp() > MIN_JET_PT and abs(ca8Jets[ijet].Eta()) < MAX_JET_ETA:
            jet = ca8Jets[ijet]
            if jet.DeltaR( lepton.p4() ) > ROOT.TMath.Pi() / 2.0 :
                hadJets.append( jet )
                hadJetsIndex.append( ijet )


    
    # -------------------------------------------------------------------------------------
    # STEP (3+4): require >=1 leptonic-side AK5 jet, >=1 hadronic-side CA8 jet with pt > 400
    # -------------------------------------------------------------------------------------

    if len(lepJets) < 1 or len(hadJets) < 1 or hadJets[0].Perp() < options.jetPtCut :
        continue

    
    # loop over CSV discriminator values of leptonic-side AK5 jets
    for ijet in range(0,len(lepcsvs)) :
        lepjet = lepJets[ijet]

        j_pt = lepjet.Perp()
        j_eta = lepjet.Eta()

        j_csv = lepcsvs[ijet]
        j_vtxmass = lepVtxMass[ijet]
        j_flavor = lepFlavors[ijet]

        # all jets (denominator)
        if abs(j_flavor) == 5: # b-jet
            if abs(j_eta) < 0.8 :
                h2_btageff_C_den_b.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h2_btageff_M_den_b.Fill(j_pt, weight)
            else :
                h2_btageff_H_den_b.Fill(j_pt, weight)
        elif abs(j_flavor) == 4: # c-jet
            if abs(j_eta) < 0.8 :
                h2_btageff_C_den_c.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h2_btageff_M_den_c.Fill(j_pt, weight)
            else :
                h2_btageff_H_den_c.Fill(j_pt, weight)
        else: # light jet
            if abs(j_eta) < 0.8 :
                h2_btageff_C_den_l.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h2_btageff_M_den_l.Fill(j_pt, weight)
            else :
                h2_btageff_H_den_l.Fill(j_pt, weight)

        # jets passing b-tagging cut
        if j_csv > options.bDiscCut:
            if abs(j_flavor) == 5: # b-jet
                if abs(j_eta) < 0.8 :
                    h2_btageff_C_num_b.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h2_btageff_M_num_b.Fill(j_pt, weight)
                else :
                    h2_btageff_H_num_b.Fill(j_pt, weight)
            elif abs(j_flavor) == 4: # c-jet
                if abs(j_eta) < 0.8 :
                    h2_btageff_C_num_c.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h2_btageff_M_num_c.Fill(j_pt, weight)
                else :
                    h2_btageff_H_num_c.Fill(j_pt, weight)
            else: # light jet
                if abs(j_eta) < 0.8 :
                    h2_btageff_C_num_l.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h2_btageff_M_num_l.Fill(j_pt, weight)
                else :
                    h2_btageff_H_num_l.Fill(j_pt, weight)

        ## now the same thing, but checking b-tagging + vtxmass>0 cut            
        if j_csv > options.bDiscCut and j_vtxmass > 0.0:
            if abs(j_flavor) == 5: # b-jet
                if abs(j_eta) < 0.8 :
                    h2_btagvtxeff_C_num_b.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h2_btagvtxeff_M_num_b.Fill(j_pt, weight)
                else :
                    h2_btagvtxeff_H_num_b.Fill(j_pt, weight)
            elif abs(j_flavor) == 4: # c-jet
                if abs(j_eta) < 0.8 :
                    h2_btagvtxeff_C_num_c.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h2_btagvtxeff_M_num_c.Fill(j_pt, weight)
                else :
                    h2_btagvtxeff_H_num_c.Fill(j_pt, weight)
            else: # light jet
                if abs(j_eta) < 0.8 :
                    h2_btagvtxeff_C_num_l.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h2_btagvtxeff_M_num_l.Fill(j_pt, weight)
                else :
                    h2_btagvtxeff_H_num_l.Fill(j_pt, weight)
        
    #print "done with b-tagging checks!"


    if hadJets[0].Perp() < 400.0 :
        continue


    # -------------------------------------------------------------------------------------
    # these are events to be used for checking b-tagging efficiency !!!
    # -------------------------------------------------------------------------------------

    
    # loop over CSV discriminator values of leptonic-side AK5 jets
    for ijet in range(0,len(lepcsvs)) :
        lepjet = lepJets[ijet]

        j_pt = lepjet.Perp()
        j_eta = lepjet.Eta()

        j_csv = lepcsvs[ijet]
        j_vtxmass = lepVtxMass[ijet]
        j_flavor = lepFlavors[ijet]

        # all jets (denominator)
        if abs(j_flavor) == 5: # b-jet
            if abs(j_eta) < 0.8 :
                h_btageff_C_den_b.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h_btageff_M_den_b.Fill(j_pt, weight)
            else :
                h_btageff_H_den_b.Fill(j_pt, weight)
        elif abs(j_flavor) == 4: # c-jet
            if abs(j_eta) < 0.8 :
                h_btageff_C_den_c.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h_btageff_M_den_c.Fill(j_pt, weight)
            else :
                h_btageff_H_den_c.Fill(j_pt, weight)
        else: # light jet
            if abs(j_eta) < 0.8 :
                h_btageff_C_den_l.Fill(j_pt, weight)
            elif abs(j_eta) < 1.6 :
                h_btageff_M_den_l.Fill(j_pt, weight)
            else :
                h_btageff_H_den_l.Fill(j_pt, weight)

        # jets passing b-tagging cut
        if j_csv > options.bDiscCut:
            if abs(j_flavor) == 5: # b-jet
                if abs(j_eta) < 0.8 :
                    h_btageff_C_num_b.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h_btageff_M_num_b.Fill(j_pt, weight)
                else :
                    h_btageff_H_num_b.Fill(j_pt, weight)
            elif abs(j_flavor) == 4: # c-jet
                if abs(j_eta) < 0.8 :
                    h_btageff_C_num_c.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h_btageff_M_num_c.Fill(j_pt, weight)
                else :
                    h_btageff_H_num_c.Fill(j_pt, weight)
            else: # light jet
                if abs(j_eta) < 0.8 :
                    h_btageff_C_num_l.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h_btageff_M_num_l.Fill(j_pt, weight)
                else :
                    h_btageff_H_num_l.Fill(j_pt, weight)

        ## now the same thing, but checking b-tagging + vtxmass>0 cut            
        if j_csv > options.bDiscCut and j_vtxmass > 0.0:
            if abs(j_flavor) == 5: # b-jet
                if abs(j_eta) < 0.8 :
                    h_btagvtxeff_C_num_b.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h_btagvtxeff_M_num_b.Fill(j_pt, weight)
                else :
                    h_btagvtxeff_H_num_b.Fill(j_pt, weight)
            elif abs(j_flavor) == 4: # c-jet
                if abs(j_eta) < 0.8 :
                    h_btagvtxeff_C_num_c.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h_btagvtxeff_M_num_c.Fill(j_pt, weight)
                else :
                    h_btagvtxeff_H_num_c.Fill(j_pt, weight)
            else: # light jet
                if abs(j_eta) < 0.8 :
                    h_btagvtxeff_C_num_l.Fill(j_pt, weight)
                elif abs(j_eta) < 1.6 :
                    h_btagvtxeff_M_num_l.Fill(j_pt, weight)
                else :
                    h_btagvtxeff_H_num_l.Fill(j_pt, weight)
        
    #print "done with b-tagging checks!"


print ""
print "end of btagging.py"
print ""
 
# -------------------------------------------------------------------------------------
# END OF LOOPING OVER EVENTS!!!
# -------------------------------------------------------------------------------------


f.cd()
f.Write()
f.Close()


