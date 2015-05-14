# Updated 1/16/14 with electron selection, added MET cut, etc.
# Updated 3/12/14 to update the definition of HT (was previously jet-HT, need ALL HT)
# Updated 3/12/14 to redefine the cut flow.
#     0 : Valid muon or electron passing ("!useLoose") or failing ("useLoose") isolation
#     1 : >= 2 jets with pt > 30 GeV
#     2 : HTLEP > htLepCut (default 0)
#     3 : >= 1 leptonic-side jets with pt > 30 GeV, >= 1 hadronic side jet with pt > jetPtCut (default 200 GeV)
#     4 : HT > htCut (default 0)
#     5 : >= 1 b-tag on the leading leptonic jet
#     6 : >= 1 t-tag on the leading hadronic jet
# Update 4/2/14: various bug fixes and cleanup of code, details here: http://hep.pha.jhu.edu:8080/top/982
# Update 5/5/14: redefine cut flow
#     0 : Valid muon or electron passing ("!useLoose") or failing ("useLoose") isolation
#     1 : >= 2 jets with pt > 30 GeV
#     2 : HTLEP > htLepCut (default 0)
#     3 : >= 1 leptonic-side jets with pt > 30 GeV, >= 1 hadronic side jet with pt > jetPtCut (default 200 GeV)
#     4 : >= 1 hadronic side jet with pt > 400 GeV
#     5 : HT > htCut (default 0)
#     6 : >= 1 t-tag on the leading hadronic jet
#     7 : >= 1 b-tag on the leading leptonic jet with vtxMass > 0
# Update 5/8/14: fix lepton selecton :
#          --> First get all lepton information
#          --> Then calculate isolation info
#          --> Next loop over jets :
#              >> If lepton was already cleaned (non-pu isolation satisfied), do nothing.
#              >> If lepton was NOT cleaned (non-pu isolation failed, pu-corrected iso satisfied), remove p4 from jet

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
# helper function to get b-tagging efficiency scale factor (for MC) for LIGHT JETS 
# From: https://twiki.cern.ch/twiki/pub/CMS/BtagRecommendation53XReReco/SFlightFuncs_EPS2013.C
# Tagger: CSVM within 20 < pt < 1000 GeV (850 for eta>1.6), abs(eta) < 2.4, x = pt
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# SF for light-jets
#
# **** WE DON'T NEED THIS (?), KEEP IT IN JUST IN CASE ****
#
# -------------------------------------------------------------------------------------
def getBtagSF_light(jetPt,jetEta,sys) :

    if jetPt > 850 and abs(jetEta) > 1.6: 
        jetPt = 850
    if jetPt > 1000:
        jetPt = 1000

    ## nominal value
    if (sys==0):
        if abs(jetEta) < 0.8:
            SFlight = ((1.07541+(0.00231827*jetPt))+(-4.74249e-06*(jetPt*jetPt)))+(2.70862e-09*(jetPt*(jetPt*jetPt)))
        elif abs(jetEta) < 1.6:
            SFlight = ((1.05613+(0.00114031*jetPt))+(-2.56066e-06*(jetPt*jetPt)))+(1.67792e-09*(jetPt*(jetPt*jetPt)))
        elif abs(jetEta) < 2.4:
            SFlight = ((1.05625+(0.000487231*jetPt))+(-2.22792e-06*(jetPt*jetPt)))+(1.70262e-09*(jetPt*(jetPt*jetPt)))
        else:
            print "Invalid jet eta range!!!"
            SFlight = 1.0
    ## up-varied
    elif (sys==1):
        if abs(jetEta) < 0.8:
            SFlight = ((1.18638+(0.00314148*jetPt))+(-6.68993e-06*(jetPt*jetPt)))+(3.89288e-09*(jetPt*(jetPt*jetPt)))
        elif abs(jetEta) < 1.6:
            SFlight = ((1.16624+(0.00151884*jetPt))+(-3.59041e-06*(jetPt*jetPt)))+(2.38681e-09*(jetPt*(jetPt*jetPt)))
        elif abs(jetEta) < 2.4:
            SFlight = ((1.15575+(0.000693344*jetPt))+(-3.02661e-06*(jetPt*jetPt)))+(2.39752e-09*(jetPt*(jetPt*jetPt)))
        else:
            print "Invalid jet eta range!!!"
            SFlight = 1.0
    ## down-varied
    elif (sys==-1):
        if abs(jetEta) < 0.8:
            SFlight = ((0.964527+(0.00149055*jetPt))+(-2.78338e-06*(jetPt*jetPt)))+(1.51771e-09*(jetPt*(jetPt*jetPt)))
        elif abs(jetEta) < 1.6:
            SFlight = ((0.946051+(0.000759584*jetPt))+(-1.52491e-06*(jetPt*jetPt)))+(9.65822e-10*(jetPt*(jetPt*jetPt)))
        elif abs(jetEta) < 2.4:
            SFlight = ((0.956736+(0.000280197*jetPt))+(-1.42739e-06*(jetPt*jetPt)))+(1.0085e-09*(jetPt*(jetPt*jetPt)))
        else:
            print "Invalid jet eta range!!!"
            SFlight = 1.0
    else:
        print "Invalid light-jet b-tagging SF option!!!"
        SFlight = 1.0
    
    return float(SFlight)

# -------------------------------------------------------------------------------------
# MC b-tagging efficiency
#
# **** WE DON'T NEED THIS (?), KEEP IT IN JUST IN CASE ****
#
# -------------------------------------------------------------------------------------
def getBtagEff(jetPt, jetEta, jetFlavor) :

    if jetPt > 800.0:
        jetPt = 800.0
    if jetPt < 30.0 or abs(jetEta) > 2.4:
        print "This jet shouldn't have passed our selection!!!!!!!!!"
        return float(0.0)

    ptmin = [30, 50, 70, 100, 160, 220, 300, 400]
    ptmax = [50, 70, 100, 160, 220, 300, 400, 800]

    ## efficiencies
    eff_b_C = [0.657105, 0.714398, 0.743294, 0.754371, 0.725513, 0.671324, 0.581024, 0.476708]
    eff_b_M = [0.60698, 0.668257, 0.701126, 0.708266, 0.672969, 0.619897, 0.535795, 0.465189]
    eff_b_H = [0.548226, 0.597592, 0.6355, 0.633576, 0.599783, 0.556137, 0.534634, 0.514862]
    
    eff_c_C = [0.190518, 0.207722, 0.216882, 0.219563, 0.187907, 0.169981, 0.116069, 0.0909977]
    eff_c_M = [0.165894, 0.18293, 0.196692, 0.213846, 0.179415, 0.154544, 0.125904, 0.13197]
    eff_c_H = [0.149837, 0.160211, 0.180663, 0.181549, 0.15813, 0.137798, 0.097816, 0.1459]

    eff_l_C = [0.0120545, 0.00989127, 0.0107686, 0.0112309, 0.0133013, 0.0116046, 0.0123252, 0.0171984]
    eff_l_M = [0.0131259, 0.0109459, 0.0110449, 0.0118005, 0.0141589, 0.011822, 0.0176869, 0.0247197]
    eff_l_H = [0.0186674, 0.0155701, 0.0166389, 0.0183861, 0.0227545, 0.0270767, 0.0308926, 0.0365164]


    ## loop to find right bin
    effMC = 0.0
    for iEff in range(0,len(eff_b_C) ):
        if jetPt > ptmin[iEff] and jetPt <= ptmax[iEff] :

            ## b-jets
            if (abs(jetFlavor) == 5):
                if abs(jetEta) < 0.8:
                    effMC = eff_b_C[iEff]
                    break
                elif abs(jetEta) < 1.6:
                    effMC = eff_b_M[iEff]
                    break
                else:
                    effMC = eff_b_H[iEff]
                    break
            ## c-jets
            elif (abs(jetFlavor) == 4):
                if abs(jetEta) < 0.8:
                    effMC = eff_c_C[iEff]
                    break
                elif abs(jetEta) < 1.6:
                    effMC = eff_c_M[iEff]
                    break
                else:
                    effMC = eff_c_H[iEff]
                    break
            ## light-jets
            else:
                if abs(jetEta) < 0.8:
                    effMC = eff_l_C[iEff]
                    break
                elif abs(jetEta) < 1.6:
                    effMC = eff_l_M[iEff]
                    break
                else:
                    effMC = eff_l_H[iEff]
                    break
    
    return float(effMC)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Muon trigger * ID SF
def getMuonSF(muEta) :

    ## from here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffs#22Jan2013_ReReco_of_2012_data_re
    ## ID: https://indico.cern.ch/getFile.py/access?contribId=1&resId=2&materialId=slides&confId=257630
    ## trigger: https://indico.cern.ch/getFile.py/access?contribId=2&resId=0&materialId=slides&confId=257000

    muSF = 1.0
    if abs(muEta) < 0.9 :
        muSF = 0.9827 * 0.9925
    elif abs(muEta) < 1.2 :
        muSF = 0.9622 * 0.9928
    else :
        muSF = 0.9906 * 0.9960

    return float(muSF)

# -------------------------------------------------------------------------------------
# Electron trigger * ID SF
def getElectronSF(elEta, elPt) :

    ## from here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentification#Triggering_MVA
    
    ## electron ID
    if elPt > 199. :
        elPt = 199.
    
    f_elSF = ROOT.TFile("electrons_scale_factors.root")
    h_elSF = f_elSF.Get("electronsDATAMCratio_FO_ID")
    
    ibin = h_elSF.FindBin(abs(elEta), elPt)
    elSF_ID = h_elSF.GetBinContent(ibin)

    ## electron trigger (uncertainty is statistical only), from AN-2014/035
    # eff_data = 88.5 +/- 0.7 %
    # eff_MC = 94.1 +/- 0.2 %

    elSF_trig = 0.94

    elSF = elSF_ID * elSF_trig
    
    return float(elSF)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Top-tagging SF
def getToptagSF(jetEta, pdfSet, pdfSys, isElec) :

    toptagSF = 1.0
    if abs(jetEta) < 1.0 :
        if "madgraph" in options.outname and "TTJet" in options.outname:
            toptagSF = 0.985
        else:
            toptagSF = 1.173
    else :
        if "madgraph" in options.outname and "TTJet" in options.outname:
            toptagSF = 0.644
        else:
            toptagSF = 0.704

    toptag_post = 1.0
    #if (pdfSet==1 and pdfSys==0 and isElec==False):
    #    toptag_post = 1.10649440886
    #if (pdfSet==1 and pdfSys==1 and isElec==False):
    #    toptag_post = 1.06707266216
    #if (pdfSet==1 and pdfSys==-1 and isElec==False):
    #    toptag_post = 1.13966730776
    #if (pdfSet==1 and pdfSys==0 and isElec):
    #    toptag_post = 1.09579275566
    #if (pdfSet==1 and pdfSys==1 and isElec):
    #    toptag_post = 1.07216881228
    #if (pdfSet==1 and pdfSys==-1 and isElec):
    #    toptag_post = 1.11804095015        

    toptagSF = toptagSF * toptag_post
    
    return float(toptagSF)


# Top-tagging SF error
def getToptagSFerror(jetEta, pdfSet, pdfSys, isElec) :

    toptagSFerr = 0.0
    if abs(jetEta) < 1.1 :
        toptagSFerr = 0.092
    else :
        toptagSFerr = 0.110

    return float(toptagSFerr)
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
                  help='What pileup histogram should be used? ttbar, wjets, sts, stt, sttw, stsb, sttb, sttwb, ttbarQ2dn, ttbarQ2up')

parser.add_option('--ptWeight', metavar='F', action='store_true',
                  default=False,
                  dest='ptWeight',
                  help='Do top pt reweighting (for MC)')

parser.add_option('--set', metavar='F', type='string', action='store',
                  default='madgraph',
                  dest='set',
                  help='Using madgraph, mcatnlo or powheg for the ttbar event weights (used if ptWeight=True)')

parser.add_option('--lepType', metavar='F', type='string', action='store',
                  default='muon',
                  dest='lepType',
                  help='Lepton type (ele or muon)')

parser.add_option('--doQCD', metavar='F', action='store_true',
                  default=False,
                  dest='doQCD',
                  help='Use loose leptons (exclusive from tight), for QCD studies')

parser.add_option('--use2Dcut', metavar='F', action='store_true',
                  default=False,
                  dest='use2Dcut',
                  help='Use 2D cut instead of relative isolation')

parser.add_option('--printEvents', metavar='F', action='store_true',
                  default=False,
                  dest='printEvents',
                  help='Print events that pass selection (run:lumi:event)')

parser.add_option('--useTriangular', metavar='F', action='store_true',
                  default=True,
                  dest='useTriangular',
                  help='Use triangular cut to reject electron QCD?')

parser.add_option('--metCut', metavar='F', type='float', action='store',
                  default=None,
                  dest='metCut',
                  help='MET cut (default is None) [GeV]')

parser.add_option('--htCut', metavar='F', type='float', action='store',
                  default=None,
                  dest='htCut',
                  help='HT cut (default is None) [GeV]. HT defined as scalar sum of pt of jets.')

parser.add_option('--htLepCut', metavar='F', type='float', action='store',
                  default=None,
                  dest='htLepCut',
                  help='Cut on MET+lepton pt (default is None) [GeV].')

parser.add_option('--jetPtCut', metavar='F', type='float', action='store',
                  default=200.0,
                  dest='jetPtCut',
                  help='CA8 hadronic-side PT cut of leading jet (default is 200.0) [GeV]')

parser.add_option('--mttGenMax', metavar='J', type='float', action='store',
                  default=None,
                  dest='mttGenMax',
                  help='Maximum generator-level m_ttbar [GeV] to stitch together the ttbar samples.')

parser.add_option('--makeResponse', metavar='M', action='store_true',
                  default=False,
                  dest='makeResponse',
                  help='Make response matrix for top pt unfolding')

parser.add_option('--semilep', metavar='J', type='float',action='store',
                  default=None,
                  dest='semilep',
                  help='Select only semileptonic ttbar decays (1) or only non-semileptonic ttbar decays (-1) or no such cut (None)')

parser.add_option('--bDiscCut', metavar='F', type='float', action='store',
                  default=0.679,
                  dest='bDiscCut',
                  help='b-tagging discriminator cut (default is 0.679, medium working point for CSV tagger)')

parser.add_option('--btagSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='btagSys',
                  help='Systematic variation on b-tagging SF. Options are +1. (up 1 sigma), 0. (nominal), -1. (down 1 sigma). Default is None.')

parser.add_option('--toptagSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='toptagSys',
                  help='Systematic variation on top-tagging efficiency. Default is None.')

parser.add_option('--jecSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='jecSys',
                  help='JEC systematic variation. Options are +1. (up 1 sigma), 0. (nominal), -1. (down 1 sigma). Default is None.')

parser.add_option('--jerSys', metavar='J', type='float', action='store',
                  default=None,
                  dest='jerSys',
                  help='JER Systematic variation in fraction. Default is None.')

parser.add_option('--pdfSet', metavar='J', type='float', action='store',
                  default=0.0,
                  dest='pdfSet',
                  help='which PDF set is used for ttbar? Options are 0 (CT10), 1 (MSTW), 2 (NNPDF). Default is 0.')

parser.add_option('--pdfSys', metavar='J', type='float', action='store',
                  default=0.0,
                  dest='pdfSys',
                  help='PDF Systematic variation. Options are +1 (scale up 1 sigma), 0 (nominal), -1 (down 1 sigma for 3 PDF sets). Default is 0.0')

parser.add_option('--oddeven', metavar='J', type='float', action='store',
                  default=None,
                  dest='oddeven',
                  help='Run on only odd (option==1) even (option==2) events (based on event ID) for unfolding closure test.')

parser.add_option('--debug', metavar='D', action='store_true',
                  default=False,
                  dest='debug',
                  help='Print debugging info')

parser.add_option('--WjetsHF', metavar='F', type='string', action='store',
                  default=None,
                  dest='WjetsHF',
                  help='Distinguish Wbb (WjetsHF=wbb) / Wcc (WjetsHF=wcc) / Wc (WjetsHF=wc) / W+light (WjetsHF=wl) jets final states')


(options, args) = parser.parse_args()
argv = []

import ROOT
ROOT.gROOT.Macro("rootlogon.C")

## array needed for response matrix binning
from array import *

if options.makeResponse == True:
    ROOT.gSystem.Load("RooUnfold-1.1.1/libRooUnfold")


# -------------------------------------------------------------------------------------
# jet energy correction uncertainties & smearing
# -------------------------------------------------------------------------------------

# Additional JEC uncertainty for CA8 jets (this is a manual hack to use AK7 corrections on CA8 jets)
flatJecUnc = 0.01

ROOT.gSystem.Load('libCondFormatsJetMETObjects')

# Read JEC uncertainties
if options.jecSys != None or options.jerSys != None :
    jecParStrAK5 = ROOT.std.string('START53_V27_Uncertainty_AK5PFchs.txt')
    jecUncAK5 = ROOT.JetCorrectionUncertainty( jecParStrAK5 )
    jecParStrAK7 = ROOT.std.string('START53_V27_Uncertainty_AK7PFchs.txt')
    jecUncAK7 = ROOT.JetCorrectionUncertainty( jecParStrAK7 )    

# read nominal JEC corrections for AK7 jets to be applied to CA8 jets
if options.isData == False:
    jecNomStrAK7 = [
        'START53_V27_L1FastJet_AK7PFchs.txt',
        'START53_V27_L2Relative_AK7PFchs.txt',
        'START53_V27_L3Absolute_AK7PFchs.txt'
        ]
else:
    jecNomStrAK7 = [
        'FT_53_V21_AN6_L1FastJet_AK7PFchs.txt',
        'FT_53_V21_AN6_L2Relative_AK7PFchs.txt',
        'FT_53_V21_AN6_L3Absolute_AK7PFchs.txt',
        'FT_53_V21_AN6_L2L3Residual_AK7PFchs.txt',
        ]

v_jecNomAK7 = ROOT.std.vector(ROOT.JetCorrectorParameters)()
for ijecStr in jecNomStrAK7 :
    ijec = ROOT.JetCorrectorParameters( ijecStr )
    v_jecNomAK7.push_back( ijec )
jecNomAK7 = ROOT.FactorizedJetCorrector(v_jecNomAK7)



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

cutflow = {
    'Stage 0: ':0,
    'Stage 1: ':0,
    'Stage 2: ':0,
    'Stage 3: ':0,
    'Stage 4: ':0,
    'Stage 5: ':0,
    'Stage 6: ':0,
    'Stage 7: ':0,
    }

start_time = time.time()


# -------------------------------------------------------------------------------------
# input and output files
# -------------------------------------------------------------------------------------

print 'Getting these files : ' + options.files

files = glob.glob( options.files )
print files

ptwstring=''
if options.ptWeight == True :
	ptwstring='_ptWeighted'

f = ROOT.TFile(options.outname + ptwstring+".root", "recreate")
name = options.outname+ptwstring


# -------------------------------------------------------------------------------------
# define all the histograms
# -------------------------------------------------------------------------------------

print "Creating histograms"

# read input histogram for PU
if options.pileup=='ttbarQ2up' or options.pileup=='ttbarQ2dn':
    PileFile = ROOT.TFile("Pileup_plots_scaleupdnnom.root")
else:
    PileFile = ROOT.TFile("Pileup_plots.root")
PilePlot = PileFile.Get("pweight" + options.pileup)

f.cd()

h_nvtx_pre   = ROOT.TH1F("nvtx_pre",   ";Number of PV (pre reweighting);Events / 1",  50,-0.5,49.5)
h_nvtx_post  = ROOT.TH1F("nvtx_post",  ";Number of PV (post reweighting);Events / 1", 50,-0.5,49.5)
h_nvtx0_pre  = ROOT.TH1F("nvtx0_pre",  ";Number of PV (pre reweighting);Events / 1",  50,-0.5,49.5)
h_nvtx0_post = ROOT.TH1F("nvtx0_post", ";Number of PV (post reweighting);Events / 1", 50,-0.5,49.5)

h_mttbarGen0 = ROOT.TH1F("mttbarGen0", "; gen-level m(t#bar{t}) [GeV]; Events / 10 GeV", 250, 0, 2500)
h_mttbarGen1 = ROOT.TH1F("mttbarGen1", "; gen-level m(t#bar{t}) [GeV]; Events / 10 GeV", 250, 0, 2500)
h_mttbarGen2 = ROOT.TH1F("mttbarGen2", "; gen-level m(t#bar{t}) [GeV]; Events / 10 GeV", 250, 0, 2500)
h_mttbarGen3 = ROOT.TH1F("mttbarGen3", "; gen-level m(t#bar{t}) [GeV]; Events / 10 GeV", 250, 0, 2500)
h_mttbarGen4 = ROOT.TH1F("mttbarGen4", "; gen-level m(t#bar{t}) [GeV]; Events / 10 GeV", 250, 0, 2500)
h_mttbarGen5 = ROOT.TH1F("mttbarGen5", "; gen-level m(t#bar{t}) [GeV]; Events / 10 GeV", 250, 0, 2500)
h_mttbarGen6 = ROOT.TH1F("mttbarGen6", "; gen-level m(t#bar{t}) [GeV]; Events / 10 GeV", 250, 0, 2500)
h_mttbarGen7 = ROOT.TH1F("mttbarGen7", "; gen-level m(t#bar{t}) [GeV]; Events / 10 GeV", 250, 0, 2500)


# numbers of different objects
#h_nMuons     = ROOT.TH1F("nMuons",     "Number of muons, p_{T} > 45 GeV;N_{Muons};Number / event",         5, -0.5, 4.5)
#h_nElectrons = ROOT.TH1F("nElectrons", "Number of electrons, p_{T} > 35 GeV;N_{Electrons};Number / event", 5, -0.5, 4.5)

#h_nJets0     = ROOT.TH1F("nJets0",     "Number of jets, p_{T} > 30 GeV;N_{jets};Number / event", 20, -0.5, 19.5)  #AK5 jets
#h_nJets1     = ROOT.TH1F("nJets1",     "Number of jets, p_{T} > 30 GeV;N_{jets};Number / event", 20, -0.5, 19.5)
#h_nJets2     = ROOT.TH1F("nJets2",     "Number of jets, p_{T} > 30 GeV;N_{jets};Number / event", 20, -0.5, 19.5)
#h_nJets3     = ROOT.TH1F("nJets3",     "Number of jets, p_{T} > 30 GeV;N_{jets};Number / event", 20, -0.5, 19.5)
#h_nJets4     = ROOT.TH1F("nJets4",     "Number of jets, p_{T} > 30 GeV;N_{jets};Number / event", 20, -0.5, 19.5)
#h_nJets5     = ROOT.TH1F("nJets5",     "Number of jets, p_{T} > 30 GeV;N_{jets};Number / event", 20, -0.5, 19.5)
#h_nJets6     = ROOT.TH1F("nJets6",     "Number of jets, p_{T} > 30 GeV;N_{jets};Number / event", 20, -0.5, 19.5)

#h_nBJets0    = ROOT.TH1F("nBJets0",    "Number of b-tagged jets, p_{T} > 30 GeV;N_{b-jets};Number / event", 10, -0.5, 9.5)
#h_nBJets1    = ROOT.TH1F("nBJets1",    "Number of b-tagged jets, p_{T} > 30 GeV;N_{b-jets};Number / event", 10, -0.5, 9.5)
#h_nBJets2    = ROOT.TH1F("nBJets2",    "Number of b-tagged jets, p_{T} > 30 GeV;N_{b-jets};Number / event", 10, -0.5, 9.5)
#h_nBJets3    = ROOT.TH1F("nBJets3",    "Number of b-tagged jets, p_{T} > 30 GeV;N_{b-jets};Number / event", 10, -0.5, 9.5)
#h_nBJets4    = ROOT.TH1F("nBJets4",    "Number of b-tagged jets, p_{T} > 30 GeV;N_{b-jets};Number / event", 10, -0.5, 9.5)
#h_nBJets5    = ROOT.TH1F("nBJets5",    "Number of b-tagged jets, p_{T} > 30 GeV;N_{b-jets};Number / event", 10, -0.5, 9.5)
#h_nBJets6    = ROOT.TH1F("nBJets6",    "Number of b-tagged jets, p_{T} > 30 GeV;N_{b-jets};Number / event", 10, -0.5, 9.5)

h_nLepJets2  = ROOT.TH1F("nLepJets2",  "Number of jets, p_{T} > 30 GeV;N_{lep.side jets};Number / event",   10, -0.5, 9.5)
h_nLepJets3  = ROOT.TH1F("nLepJets3",  "Number of jets, p_{T} > 30 GeV;N_{lep.side jets};Number / event",   10, -0.5, 9.5)
h_nLepJets4  = ROOT.TH1F("nLepJets4",  "Number of jets, p_{T} > 30 GeV;N_{lep.side jets};Number / event",   10, -0.5, 9.5)
h_nLepJets5  = ROOT.TH1F("nLepJets5",  "Number of jets, p_{T} > 30 GeV;N_{lep.side jets};Number / event",   10, -0.5, 9.5)
h_nLepJets6  = ROOT.TH1F("nLepJets6",  "Number of jets, p_{T} > 30 GeV;N_{lep.side jets};Number / event",   10, -0.5, 9.5)

# lepton properties
if options.lepType == "muon":

    print "running on muons!"
    
    h_ptLep0  = ROOT.TH1F("ptLep0",  ";Muon p_{T} [GeV]; Muons / 5 GeV", 60, 0., 300.)
    h_ptLep1  = ROOT.TH1F("ptLep1",  ";Muon p_{T} [GeV]; Muons / 5 GeV", 60, 0., 300.)
    h_ptLep2  = ROOT.TH1F("ptLep2",  ";Muon p_{T} [GeV]; Muons / 5 GeV", 60, 0., 300.)
    h_ptLep3  = ROOT.TH1F("ptLep3",  ";Muon p_{T} [GeV]; Muons / 5 GeV", 60, 0., 300.)
    h_ptLep4  = ROOT.TH1F("ptLep4",  ";Muon p_{T} [GeV]; Muons / 5 GeV", 60, 0., 300.)
    h_ptLep5  = ROOT.TH1F("ptLep5",  ";Muon p_{T} [GeV]; Muons / 5 GeV", 60, 0., 300.)
    h_ptLep6  = ROOT.TH1F("ptLep6",  ";Muon p_{T} [GeV]; Muons / 5 GeV", 60, 0., 300.)
    h_ptLep7  = ROOT.TH1F("ptLep7",  ";Muon p_{T} [GeV]; Muons / 5 GeV", 60, 0., 300.)

    h_etaLep0 = ROOT.TH1F("etaLep0", ";Muon #eta; Muons / 0.1", 50, -2.5, 2.5)
    h_etaLep1 = ROOT.TH1F("etaLep1", ";Muon #eta; Muons / 0.1", 50, -2.5, 2.5)
    h_etaLep2 = ROOT.TH1F("etaLep2", ";Muon #eta; Muons / 0.1", 50, -2.5, 2.5)
    h_etaLep3 = ROOT.TH1F("etaLep3", ";Muon #eta; Muons / 0.1", 50, -2.5, 2.5)
    h_etaLep4 = ROOT.TH1F("etaLep4", ";Muon #eta; Muons / 0.1", 50, -2.5, 2.5)
    h_etaLep5 = ROOT.TH1F("etaLep5", ";Muon #eta; Muons / 0.1", 50, -2.5, 2.5)
    h_etaLep6 = ROOT.TH1F("etaLep6", ";Muon #eta; Muons / 0.1", 50, -2.5, 2.5)
    h_etaLep7 = ROOT.TH1F("etaLep7", ";Muon #eta; Muons / 0.1", 50, -2.5, 2.5)

    h_etaAbsLep0 = ROOT.TH1F("etaAbsLep0", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep1 = ROOT.TH1F("etaAbsLep1", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep2 = ROOT.TH1F("etaAbsLep2", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep3 = ROOT.TH1F("etaAbsLep3", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep4 = ROOT.TH1F("etaAbsLep4", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep4_low = ROOT.TH1F("etaAbsLep4Low", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep4_high = ROOT.TH1F("etaAbsLep4High", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep5 = ROOT.TH1F("etaAbsLep5", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep6 = ROOT.TH1F("etaAbsLep6", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep6_low = ROOT.TH1F("etaAbsLep6Low", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep6_high = ROOT.TH1F("etaAbsLep6High", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep7 = ROOT.TH1F("etaAbsLep7", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep7_low = ROOT.TH1F("etaAbsLep7Low", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)
    h_etaAbsLep7_high = ROOT.TH1F("etaAbsLep7High", ";Muon |#eta|; Muons / 0.05", 50, 0, 2.5)

    h_dRvspTPre  = ROOT.TH2F("dRvspTPre",  ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT0    = ROOT.TH2F("dRvspT0",    ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT1    = ROOT.TH2F("dRvspT1",    ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT2    = ROOT.TH2F("dRvspT2",    ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT3    = ROOT.TH2F("dRvspT3",    ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT4    = ROOT.TH2F("dRvspT4",    ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT5    = ROOT.TH2F("dRvspT5",    ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT6    = ROOT.TH2F("dRvspT6",    ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT7    = ROOT.TH2F("dRvspT7",    ";dR(muon, closest jet); p_{T}^{rel}(muon, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)

    h_pfIsoPre  = ROOT.TH1F("pfIsoPre",  ";PF-isolation/p_{T}; Muons / 0.01", 200, 0., 2.)
    h_pfIso0    = ROOT.TH1F("pfIso0",    ";PF-isolation/p_{T}; Muons / 0.01", 200, 0., 2.)
    h_pfIso1    = ROOT.TH1F("pfIso1",    ";PF-isolation/p_{T}; Muons / 0.01", 200, 0., 2.)
    h_pfIso2    = ROOT.TH1F("pfIso2",    ";PF-isolation/p_{T}; Muons / 0.01", 200, 0., 2.)
    h_pfIso3    = ROOT.TH1F("pfIso3",    ";PF-isolation/p_{T}; Muons / 0.01", 200, 0., 2.)
else:

    print "running on electrons!"
    
    h_ptLep0  = ROOT.TH1F("ptLep0",  ";Electron p_{T} [GeV]; Electrons / 5 GeV", 60, 0., 300.)
    h_ptLep1  = ROOT.TH1F("ptLep1",  ";Electron p_{T} [GeV]; Electrons / 5 GeV", 60, 0., 300.)
    h_ptLep2  = ROOT.TH1F("ptLep2",  ";Electron p_{T} [GeV]; Electrons / 5 GeV", 60, 0., 300.)
    h_ptLep3  = ROOT.TH1F("ptLep3",  ";Electron p_{T} [GeV]; Electrons / 5 GeV", 60, 0., 300.)
    h_ptLep4  = ROOT.TH1F("ptLep4",  ";Electron p_{T} [GeV]; Electrons / 5 GeV", 60, 0., 300.)
    h_ptLep5  = ROOT.TH1F("ptLep5",  ";Electron p_{T} [GeV]; Electrons / 5 GeV", 60, 0., 300.)
    h_ptLep6  = ROOT.TH1F("ptLep6",  ";Electron p_{T} [GeV]; Electrons / 5 GeV", 60, 0., 300.)
    h_ptLep7  = ROOT.TH1F("ptLep7",  ";Electron p_{T} [GeV]; Electrons / 5 GeV", 60, 0., 300.)

    h_etaLep0 = ROOT.TH1F("etaLep0", ";Electron #eta; Electrons / 0.1", 50, -2.5, 2.5)
    h_etaLep1 = ROOT.TH1F("etaLep1", ";Electron #eta; Electrons / 0.1", 50, -2.5, 2.5)
    h_etaLep2 = ROOT.TH1F("etaLep2", ";Electron #eta; Electrons / 0.1", 50, -2.5, 2.5)
    h_etaLep3 = ROOT.TH1F("etaLep3", ";Electron #eta; Electrons / 0.1", 50, -2.5, 2.5)
    h_etaLep4 = ROOT.TH1F("etaLep4", ";Electron #eta; Electrons / 0.1", 50, -2.5, 2.5)
    h_etaLep5 = ROOT.TH1F("etaLep5", ";Electron #eta; Electrons / 0.1", 50, -2.5, 2.5)
    h_etaLep6 = ROOT.TH1F("etaLep6", ";Electron #eta; Electrons / 0.1", 50, -2.5, 2.5)
    h_etaLep7 = ROOT.TH1F("etaLep7", ";Electron #eta; Electrons / 0.1", 50, -2.5, 2.5)
    
    h_etaAbsLep0 = ROOT.TH1F("etaAbsLep0", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep1 = ROOT.TH1F("etaAbsLep1", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep2 = ROOT.TH1F("etaAbsLep2", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep3 = ROOT.TH1F("etaAbsLep3", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep4 = ROOT.TH1F("etaAbsLep4", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep4_low = ROOT.TH1F("etaAbsLep4Low", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep4_high = ROOT.TH1F("etaAbsLep4High", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep5 = ROOT.TH1F("etaAbsLep5", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep6 = ROOT.TH1F("etaAbsLep6", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep6_low = ROOT.TH1F("etaAbsLep6Low", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep6_high = ROOT.TH1F("etaAbsLep6High", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep7 = ROOT.TH1F("etaAbsLep7", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep7_low = ROOT.TH1F("etaAbsLep7Low", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)
    h_etaAbsLep7_high = ROOT.TH1F("etaAbsLep7High", ";Electron |#eta|; Electrons / 0.05", 50, 0, 2.5)

    h_dRvspTPre  = ROOT.TH2F("dRvspTPre",  ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT0    = ROOT.TH2F("dRvspT0",    ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT1    = ROOT.TH2F("dRvspT1",    ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT2    = ROOT.TH2F("dRvspT2",    ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT3    = ROOT.TH2F("dRvspT3",    ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT4    = ROOT.TH2F("dRvspT4",    ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT5    = ROOT.TH2F("dRvspT5",    ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT6    = ROOT.TH2F("dRvspT6",    ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)
    h_dRvspT7    = ROOT.TH2F("dRvspT7",    ";dR(ele, closest jet); p_{T}^{rel}(ele, closest jet) [GeV]", 60, 0., 1.5, 50, 0., 100.)

    h_pfIsoPre  = ROOT.TH1F("pfIsoPre",  ";PF-isolation/p_{T}; Electrons / 0.01", 200, 0., 2.)
    h_pfIso0    = ROOT.TH1F("pfIso0",    ";PF-isolation/p_{T}; Electrons / 0.01", 200, 0., 2.)
    h_pfIso1    = ROOT.TH1F("pfIso1",    ";PF-isolation/p_{T}; Electrons / 0.01", 200, 0., 2.)
    h_pfIso2    = ROOT.TH1F("pfIso2",    ";PF-isolation/p_{T}; Electrons / 0.01", 200, 0., 2.)
    h_pfIso3    = ROOT.TH1F("pfIso3",    ";PF-isolation/p_{T}; Electrons / 0.01", 200, 0., 2.)


# leptonic W boson
h_wboson_pt0 = ROOT.TH1F("wboson_pt0", ";Leptonic W p_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_pt1 = ROOT.TH1F("wboson_pt1", ";Leptonic W p_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_pt2 = ROOT.TH1F("wboson_pt2", ";Leptonic W p_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_pt3 = ROOT.TH1F("wboson_pt3", ";Leptonic W p_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_pt4 = ROOT.TH1F("wboson_pt4", ";Leptonic W p_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_pt5 = ROOT.TH1F("wboson_pt5", ";Leptonic W p_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_pt6 = ROOT.TH1F("wboson_pt6", ";Leptonic W p_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_pt7 = ROOT.TH1F("wboson_pt7", ";Leptonic W p_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)

h_wboson_mt0 = ROOT.TH1F("wboson_mt0", ";Leptonic W m_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_mt1 = ROOT.TH1F("wboson_mt1", ";Leptonic W m_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_mt2 = ROOT.TH1F("wboson_mt2", ";Leptonic W m_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_mt3 = ROOT.TH1F("wboson_mt3", ";Leptonic W m_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_mt4 = ROOT.TH1F("wboson_mt4", ";Leptonic W m_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_mt5 = ROOT.TH1F("wboson_mt5", ";Leptonic W m_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_mt6 = ROOT.TH1F("wboson_mt6", ";Leptonic W m_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)
h_wboson_mt7 = ROOT.TH1F("wboson_mt7", ";Leptonic W m_{T} [GeV]; Events / 10 GeV", 75, 0., 750.)


# jet properties
#h_pt1Jet0 = ROOT.TH1F("pt1Jet0", ";Leading jet p_{T} [GeV]; Jets / 5 GeV",     60, 0., 300.)
#h_pt1Jet1 = ROOT.TH1F("pt1Jet1", ";Leading jet p_{T} [GeV]; Jets / 5 GeV",     60, 0., 300.)
#h_pt2Jet0 = ROOT.TH1F("pt2Jet0", ";2nd leading jet p_{T} [GeV]; Jets / 5 GeV", 40, 0., 200.)
#h_pt2Jet1 = ROOT.TH1F("pt2Jet1", ";2nd leading jet p_{T} [GeV]; Jets / 5 GeV", 40, 0., 200.)
#h_pt3Jet0 = ROOT.TH1F("pt3Jet0", ";3rd leading jet p_{T} [GeV]; Jets / 5 GeV", 40, 0., 200.)
#h_pt3Jet1 = ROOT.TH1F("pt3Jet1", ";3rd leading jet p_{T} [GeV]; Jets / 5 GeV", 40, 0., 200.)
#h_pt4Jet0 = ROOT.TH1F("pt4Jet0", ";4th leading jet p_{T} [GeV]; Jets / 5 GeV", 40, 0., 200.)
#h_pt4Jet1 = ROOT.TH1F("pt4Jet1", ";4th leading jet p_{T} [GeV]; Jets / 5 GeV", 40, 0., 200.)

#h_eta1Jet0 = ROOT.TH1F("eta1Jet0", ";Leading jet #eta; Jets / 0.1",     50, -2.5, 2.5)
#h_eta1Jet1 = ROOT.TH1F("eta1Jet1", ";Leading jet #eta; Jets / 0.1",     50, -2.5, 2.5)
#h_eta2Jet0 = ROOT.TH1F("eta2Jet0", ";2nd leading jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta2Jet1 = ROOT.TH1F("eta2Jet1", ";2nd leading jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta3Jet0 = ROOT.TH1F("eta3Jet0", ";3rd leading jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta3Jet1 = ROOT.TH1F("eta3Jet1", ";3rd leading jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta4Jet0 = ROOT.TH1F("eta4Jet0", ";4th leading jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta4Jet1 = ROOT.TH1F("eta4Jet1", ";4th leading jet #eta; Jets / 0.1", 50, -2.5, 2.5)

#h_csv1Jet0 = ROOT.TH1F("csv1Jet0", ";Leading jet CSV; Events / 0.02",     60, 0., 1.2)
#h_csv1Jet1 = ROOT.TH1F("csv1Jet1", ";Leading jet CSV; Events / 0.02",     60, 0., 1.2)
#h_csv2Jet0 = ROOT.TH1F("csv2Jet0", ";2nd leading jet CSV; Events / 0.02", 60, 0., 1.2)
#h_csv2Jet1 = ROOT.TH1F("csv2Jet1", ";2nd leading jet CSV; Events / 0.02", 60, 0., 1.2)
#h_csv3Jet0 = ROOT.TH1F("csv3Jet0", ";3rd leading jet CSV; Events / 0.02", 60, 0., 1.2)
#h_csv3Jet1 = ROOT.TH1F("csv3Jet1", ";3rd leading jet CSV; Events / 0.02", 60, 0., 1.2)
#h_csv4Jet0 = ROOT.TH1F("csv4Jet0", ";4th leading jet CSV; Events / 0.02", 60, 0., 1.2)
#h_csv4Jet1 = ROOT.TH1F("csv4Jet1", ";4th leading jet CSV; Events / 0.02", 60, 0., 1.2)

#h_vtxMass1Jet0 = ROOT.TH1F("vtxMass1Jet0", ";Leading jet vertex mass [GeV]; Events / 0.1 GeV",     70, 0., 7.)
#h_vtxMass1Jet1 = ROOT.TH1F("vtxMass1Jet1", ";Leading jet vertex mass [GeV]; Events / 0.1 GeV",     70, 0., 7.)
#h_vtxMass2Jet0 = ROOT.TH1F("vtxMass2Jet0", ";2nd leading jet vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
#h_vtxMass2Jet1 = ROOT.TH1F("vtxMass2Jet1", ";2nd leading jet vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
#h_vtxMass3Jet0 = ROOT.TH1F("vtxMass3Jet0", ";3rd leading jet vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
#h_vtxMass3Jet1 = ROOT.TH1F("vtxMass3Jet1", ";3rd leading jet vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
#h_vtxMass4Jet0 = ROOT.TH1F("vtxMass4Jet0", ";4th leading jet vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
#h_vtxMass4Jet1 = ROOT.TH1F("vtxMass4Jet1", ";4th leading jet vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)

#h_pt1LepJet2 = ROOT.TH1F("pt1LepJet2", ";Leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 100, 0., 500.)
#h_pt1LepJet3 = ROOT.TH1F("pt1LepJet3", ";Leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 100, 0., 500.)
#h_pt1LepJet4 = ROOT.TH1F("pt1LepJet4", ";Leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 100, 0., 500.)
#h_pt1LepJet5 = ROOT.TH1F("pt1LepJet5", ";Leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 100, 0., 500.)
#h_pt1LepJet6 = ROOT.TH1F("pt1LepJet6", ";Leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 100, 0., 500.)
#h_pt1LepJet7 = ROOT.TH1F("pt1LepJet7", ";Leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 100, 0., 500.)

#h_pt2LepJet2 = ROOT.TH1F("pt2LepJet2", ";2nd leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 50, 0., 250.)
#h_pt2LepJet3 = ROOT.TH1F("pt2LepJet3", ";2nd leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 50, 0., 250.)
#h_pt2LepJet4 = ROOT.TH1F("pt2LepJet4", ";2nd leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 50, 0., 250.)
#h_pt2LepJet5 = ROOT.TH1F("pt2LepJet5", ";2nd leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 50, 0., 250.)
#h_pt2LepJet6 = ROOT.TH1F("pt2LepJet6", ";2nd leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 50, 0., 250.)
#h_pt2LepJet7 = ROOT.TH1F("pt2LepJet7", ";2nd leading lep.side jet p_{T} [GeV]; Jets / 5 GeV", 50, 0., 250.)

#h_eta1LepJet2 = ROOT.TH1F("eta1LepJet2", ";Leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta1LepJet3 = ROOT.TH1F("eta1LepJet3", ";Leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta1LepJet4 = ROOT.TH1F("eta1LepJet4", ";Leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta1LepJet5 = ROOT.TH1F("eta1LepJet5", ";Leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta1LepJet6 = ROOT.TH1F("eta1LepJet6", ";Leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta1LepJet7 = ROOT.TH1F("eta1LepJet7", ";Leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)

#h_eta2LepJet2 = ROOT.TH1F("eta2LepJet2", ";2nd leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta2LepJet3 = ROOT.TH1F("eta2LepJet3", ";2nd leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta2LepJet4 = ROOT.TH1F("eta2LepJet4", ";2nd leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta2LepJet5 = ROOT.TH1F("eta2LepJet5", ";2nd leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta2LepJet6 = ROOT.TH1F("eta2LepJet6", ";2nd leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)
#h_eta2LepJet7 = ROOT.TH1F("eta2LepJet7", ";2nd leading lep.side jet #eta; Jets / 0.1", 50, -2.5, 2.5)

#h_csv1LepJet2 = ROOT.TH1F("csv1LepJet2", ";Leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv1LepJet3 = ROOT.TH1F("csv1LepJet3", ";Leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv1LepJet4 = ROOT.TH1F("csv1LepJet4", ";Leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv1LepJet5 = ROOT.TH1F("csv1LepJet5", ";Leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv1LepJet6 = ROOT.TH1F("csv1LepJet6", ";Leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv1LepJet7 = ROOT.TH1F("csv1LepJet7", ";Leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)

#h_csv2LepJet2 = ROOT.TH1F("csv2LepJet2", ";2nd leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv2LepJet3 = ROOT.TH1F("csv2LepJet3", ";2nd leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv2LepJet4 = ROOT.TH1F("csv2LepJet4", ";2nd leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv2LepJet5 = ROOT.TH1F("csv2LepJet5", ";2nd leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv2LepJet6 = ROOT.TH1F("csv2LepJet6", ";2nd leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)
#h_csv2LepJet7 = ROOT.TH1F("csv2LepJet7", ";2nd leading lep.side jet CSV; Jets / 0.02", 60, 0., 1.2)

#h_vtxMass1LepJet2 = ROOT.TH1F("vtxMass1LepJet2", ";Leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass1LepJet3 = ROOT.TH1F("vtxMass1LepJet3", ";Leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass1LepJet4 = ROOT.TH1F("vtxMass1LepJet4", ";Leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass1LepJet5 = ROOT.TH1F("vtxMass1LepJet5", ";Leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass1LepJet6 = ROOT.TH1F("vtxMass1LepJet6", ";Leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass1LepJet7 = ROOT.TH1F("vtxMass1LepJet7", ";Leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)

#h_vtxMass2LepJet2 = ROOT.TH1F("vtxMass2LepJet2", ";2nd leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass2LepJet3 = ROOT.TH1F("vtxMass2LepJet3", ";2nd leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass2LepJet4 = ROOT.TH1F("vtxMass2LepJet4", ";2nd leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass2LepJet5 = ROOT.TH1F("vtxMass2LepJet5", ";2nd leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass2LepJet6 = ROOT.TH1F("vtxMass2LepJet6", ";2nd leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)
#h_vtxMass2LepJet7 = ROOT.TH1F("vtxMass2LepJet7", ";2nd leading lep.side jet vertex mass [GeV]; Jets / 0.1 GeV", 70, 0., 7.)


# b-jet quantities
h_ptBJet7       = ROOT.TH1F("ptBJet7",      ";b-tagged jet p_{T} [GeV]; b-jets / 10 GeV", 50, 0., 500.)
h_etaBJet7      = ROOT.TH1F("etaBJet7",     ";b-tagged jet #eta; b-jets / 0.1", 50, -2.5, 2.5)
h_flavorBJet7   = ROOT.TH1F("flavorBJet7",     ";b-tagged jet true flavor; b-jets", 5, 0.5, 5.5)

h_vtxMass3 = ROOT.TH1F("vtxMass3", ";Leptonic-side secondary vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
h_vtxMass4 = ROOT.TH1F("vtxMass4", ";Leptonic-side secondary vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
h_vtxMass5 = ROOT.TH1F("vtxMass5", ";Leptonic-side secondary vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
h_vtxMass6 = ROOT.TH1F("vtxMass6", ";Leptonic-side secondary vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
h_vtxMass7 = ROOT.TH1F("vtxMass7", ";Leptonic-side secondary vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
h_vtxMass7_low = ROOT.TH1F("vtxMass7Low", ";Leptonic-side secondary vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)
h_vtxMass7_high = ROOT.TH1F("vtxMass7High", ";Leptonic-side secondary vertex mass [GeV]; Events / 0.1 GeV", 70, 0., 7.)


# event-level quantities
h_ptMET0 = ROOT.TH1F("ptMET0", ";MET [GeV]; Events / 2 GeV", 200, 0., 400.)
h_ptMET1 = ROOT.TH1F("ptMET1", ";MET [GeV]; Events / 2 GeV", 200, 0., 400.)
h_ptMET2 = ROOT.TH1F("ptMET2", ";MET [GeV]; Events / 2 GeV", 200, 0., 400.)
h_ptMET3 = ROOT.TH1F("ptMET3", ";MET [GeV]; Events / 2 GeV", 200, 0., 400.)
h_ptMET4 = ROOT.TH1F("ptMET4", ";MET [GeV]; Events / 2 GeV", 200, 0., 400.)
h_ptMET5 = ROOT.TH1F("ptMET5", ";MET [GeV]; Events / 2 GeV", 200, 0., 400.)
h_ptMET6 = ROOT.TH1F("ptMET6", ";MET [GeV]; Events / 2 GeV", 200, 0., 400.)
h_ptMET7 = ROOT.TH1F("ptMET7", ";MET [GeV]; Events / 2 GeV", 200, 0., 400.)

h_phiMET0 = ROOT.TH1F("phiMET0", ";#phi(MET); Events / 0.05", 140, -3.5, 3.5)
h_phiMET1 = ROOT.TH1F("phiMET1", ";#phi(MET); Events / 0.05", 140, -3.5, 3.5)
h_phiMET2 = ROOT.TH1F("phiMET2", ";#phi(MET); Events / 0.05", 140, -3.5, 3.5)
h_phiMET3 = ROOT.TH1F("phiMET3", ";#phi(MET); Events / 0.05", 140, -3.5, 3.5)
h_phiMET4 = ROOT.TH1F("phiMET4", ";#phi(MET); Events / 0.05", 140, -3.5, 3.5)
h_phiMET5 = ROOT.TH1F("phiMET5", ";#phi(MET); Events / 0.05", 140, -3.5, 3.5)
h_phiMET6 = ROOT.TH1F("phiMET6", ";#phi(MET); Events / 0.05", 140, -3.5, 3.5)
h_phiMET7 = ROOT.TH1F("phiMET7", ";#phi(MET); Events / 0.05", 140, -3.5, 3.5)

h_htLep0 = ROOT.TH1F("htLep0", ";H_{T}^{lep} [GeV]; Events / 5 GeV", 200, 0., 1000.)
h_htLep1 = ROOT.TH1F("htLep1", ";H_{T}^{lep} [GeV]; Events / 5 GeV", 200, 0., 1000.)
h_htLep2 = ROOT.TH1F("htLep2", ";H_{T}^{lep} [GeV]; Events / 5 GeV", 200, 0., 1000.)
h_htLep3 = ROOT.TH1F("htLep3", ";H_{T}^{lep} [GeV]; Events / 5 GeV", 200, 0., 1000.)
h_htLep4 = ROOT.TH1F("htLep4", ";H_{T}^{lep} [GeV]; Events / 5 GeV", 200, 0., 1000.)
h_htLep5 = ROOT.TH1F("htLep5", ";H_{T}^{lep} [GeV]; Events / 5 GeV", 200, 0., 1000.)
h_htLep6 = ROOT.TH1F("htLep6", ";H_{T}^{lep} [GeV]; Events / 5 GeV", 200, 0., 1000.)
h_htLep7 = ROOT.TH1F("htLep7", ";H_{T}^{lep} [GeV]; Events / 5 GeV", 200, 0., 1000.)

h_ht0 = ROOT.TH1F("ht0", ";H_{T} [GeV]; Events / 10 GeV", 300, 0., 3000.)
h_ht1 = ROOT.TH1F("ht1", ";H_{T} [GeV]; Events / 10 GeV", 300, 0., 3000.)
h_ht2 = ROOT.TH1F("ht2", ";H_{T} [GeV]; Events / 10 GeV", 300, 0., 3000.)
h_ht3 = ROOT.TH1F("ht3", ";H_{T} [GeV]; Events / 10 GeV", 300, 0., 3000.)
h_ht4 = ROOT.TH1F("ht4", ";H_{T} [GeV]; Events / 10 GeV", 300, 0., 3000.)
h_ht5 = ROOT.TH1F("ht5", ";H_{T} [GeV]; Events / 10 GeV", 300, 0., 3000.)
h_ht6 = ROOT.TH1F("ht6", ";H_{T} [GeV]; Events / 10 GeV", 300, 0., 3000.)
h_ht7 = ROOT.TH1F("ht7", ";H_{T} [GeV]; Events / 10 GeV", 300, 0., 3000.)

# leptonic top variables
h_leptop_pt3 = ROOT.TH1F("leptop_pt3", ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)
h_leptop_pt4 = ROOT.TH1F("leptop_pt4", ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)
h_leptop_pt5 = ROOT.TH1F("leptop_pt5", ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)
h_leptop_pt6 = ROOT.TH1F("leptop_pt6", ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)
h_leptop_pt7 = ROOT.TH1F("leptop_pt7", ";p_{T}(leptonic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)

h_leptop_mass3 = ROOT.TH1F("leptop_mass3", ";m(leptonic top) [GeV]; Events / 5 GeV", 100, 0., 500.)
h_leptop_mass4 = ROOT.TH1F("leptop_mass4", ";m(leptonic top) [GeV]; Events / 5 GeV", 100, 0., 500.)
h_leptop_mass5 = ROOT.TH1F("leptop_mass5", ";m(leptonic top) [GeV]; Events / 5 GeV", 100, 0., 500.)
h_leptop_mass6 = ROOT.TH1F("leptop_mass6", ";m(leptonic top) [GeV]; Events / 5 GeV", 100, 0., 500.)
h_leptop_mass7 = ROOT.TH1F("leptop_mass7", ";m(leptonic top) [GeV]; Events / 5 GeV", 100, 0., 500.)

h_leptop_y3 = ROOT.TH1F("leptop_y3", ";y(leptonic top); Events / 0.1", 100, -5, 5.)
h_leptop_y4 = ROOT.TH1F("leptop_y4", ";y(leptonic top); Events / 0.1", 100, -5, 5.)
h_leptop_y5 = ROOT.TH1F("leptop_y5", ";y(leptonic top); Events / 0.1", 100, -5, 5.)
h_leptop_y6 = ROOT.TH1F("leptop_y6", ";y(leptonic top); Events / 0.1", 100, -5, 5.)
h_leptop_y7 = ROOT.TH1F("leptop_y7", ";y(leptonic top); Events / 0.1", 100, -5, 5.)

h_lepVShad_pt3 = ROOT.TH2F("lepVShad_pt3", ";p_{T}(hadronic top) [GeV]; p_{T}(leptonic top) [GeV]", 150, 0., 1500., 150, 0., 1500.)

# hadronic top variables
h_hadtop_pt3 = ROOT.TH1F("hadtop_pt3", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)
h_hadtop_pt4 = ROOT.TH1F("hadtop_pt4", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)
h_hadtop_pt5 = ROOT.TH1F("hadtop_pt5", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)

h_hadtop_pt_pt      = ROOT.TH1F("hadtop_pt_pt",      ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)  # pass pt > 200 GeV
h_hadtop_pt_nsub    = ROOT.TH1F("hadtop_pt_nsub",    ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)  # + pass nsub >= 3
h_hadtop_pt_minmass = ROOT.TH1F("hadtop_pt_minmass", ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)  # + pass minmass > 50 GeV
h_hadtop_pt6        = ROOT.TH1F("hadtop_pt6",        ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)  # + pass 140 < mass < 250 GeV *** FINAL SELECTION ***
h_hadtop_pt_tau32   = ROOT.TH1F("hadtop_pt_tau32",   ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)  # + pass tau32 cut (beyond current selection!)
h_hadtop_pt_csv     = ROOT.TH1F("hadtop_pt_csv",     ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)  # + pass subjet b-tag cut (beyond current selection!)
h_hadtop_pt7        = ROOT.TH1F("hadtop_pt7",        ";p_{T}(hadronic top) [GeV]; Events / 5 GeV", 300, 0., 1500.)  # + pass pt > 400 GeV

h_hadtop_mass3 = ROOT.TH1F("hadtop_mass3", ";m(hadronic top) [GeV]; Events / 5 GeV", 100, 0., 500.)
h_hadtop_mass4 = ROOT.TH1F("hadtop_mass4", ";m(hadronic top) [GeV]; Events / 5 GeV", 100, 0., 500.)
h_hadtop_mass5 = ROOT.TH1F("hadtop_mass5", ";m(hadronic top) [GeV]; Events / 5 GeV", 100, 0., 500.)
h_hadtop_mass6 = ROOT.TH1F("hadtop_mass6", ";m(hadronic top) [GeV]; Events / 5 GeV", 100, 0., 500.)
h_hadtop_mass7 = ROOT.TH1F("hadtop_mass7", ";m(hadronic top) [GeV]; Events / 5 GeV", 100, 0., 500.)

h_hadtop_y3 = ROOT.TH1F("hadtop_y3", ";y(hadronic top); Events / 0.1", 100, -5, 5.)
h_hadtop_y4 = ROOT.TH1F("hadtop_y4", ";y(hadronic top); Events / 0.1", 100, -5, 5.)
h_hadtop_y5 = ROOT.TH1F("hadtop_y5", ";y(hadronic top); Events / 0.1", 100, -5, 5.)
h_hadtop_y6 = ROOT.TH1F("hadtop_y6", ";y(hadronic top); Events / 0.1", 100, -5, 5.)
h_hadtop_y7 = ROOT.TH1F("hadtop_y7", ";y(hadronic top); Events / 0.1", 100, -5, 5.)

h_ttbar_mass3 = ROOT.TH1F("ttbar_mass3", ";m(t#bar{t}) [GeV]; Events / 10 GeV", 200, 0., 2000.)
h_ttbar_mass4 = ROOT.TH1F("ttbar_mass4", ";m(t#bar{t}) [GeV]; Events / 10 GeV", 200, 0., 2000.)
h_ttbar_mass5 = ROOT.TH1F("ttbar_mass5", ";m(t#bar{t}) [GeV]; Events / 10 GeV", 200, 0., 2000.)
h_ttbar_mass6 = ROOT.TH1F("ttbar_mass6", ";m(t#bar{t}) [GeV]; Events / 10 GeV", 200, 0., 2000.)
h_ttbar_mass7 = ROOT.TH1F("ttbar_mass7", ";m(t#bar{t}) [GeV]; Events / 10 GeV", 200, 0., 2000.)

h_hadtop_eta4 = ROOT.TH1F("hadtop_eta4", ";top-tagged jet #eta; Events / 0.1", 50, -2.5, 2.5)
h_hadtop_eta6 = ROOT.TH1F("hadtop_eta6", ";top-tagged jet #eta; Events / 0.1", 50, -2.5, 2.5)
h_hadtop_eta7 = ROOT.TH1F("hadtop_eta7", ";top-tagged jet #eta; Events / 0.1", 50, -2.5, 2.5)

# plot various top-tagging variables, plot *before* cutting on the given variable
h_hadtop_precut_nsub    = ROOT.TH1F("hadtop_precut_nsub",    ";Number of subjets; Events / 1.0",                11, -0.5, 10.5)
h_hadtop_precut_minmass = ROOT.TH1F("hadtop_precut_minmass", ";Min pairwise mass [GeV]; Events / 1 GeV",        150, 0., 150.)
h_hadtop_precut_mass    = ROOT.TH1F("hadtop_precut_mass",    ";m(hadronic top) [GeV]; Events / 5 GeV",          100, 0., 500.)
h_hadtop_precut_tau32   = ROOT.TH1F("hadtop_precut_tau32",   ";#tau_{32}(hadronic top); Events / 0.02",          70, 0., 1.4)
h_hadtop_precut_csv     = ROOT.TH1F("hadtop_precut_csv",     ";CSV discriminator(hadronic top); Events / 0.01", 110, 0., 1.1)

h_hadtop_precut_nvtx_nsub    = ROOT.TH2F("hadtop_precut_nvtx_nsub",    ";Number of PV; Number of subjets",               40, 0, 80, 11, -0.5, 10.5)
h_hadtop_precut_nvtx_minmass = ROOT.TH2F("hadtop_precut_nvtx_minmass", ";Number of PV; Min pairwise mass [GeV]",         40, 0, 80, 150, 0., 150.)
h_hadtop_precut_nvtx_mass    = ROOT.TH2F("hadtop_precut_nvtx_mass",    ";Number of PV; m(hadronic top) [GeV]",           40, 0, 80, 100, 0., 500.)
h_hadtop_precut_nvtx_tau32   = ROOT.TH2F("hadtop_precut_nvtx_tau32",   ";Number of PV; #tau_{32}(hadronic top)",         40, 0, 80, 70, 0., 1.4)
h_hadtop_precut_nvtx_csv     = ROOT.TH2F("hadtop_precut_nvtx_csv",     ";Number of PV; CSV discriminator(hadronic top)", 40, 0, 80, 110, 0., 1.1)

h_muonSF   = ROOT.TH1F("muonSF",   ";; Average muon trigger+ID SF", 1,0.5,1.5)
h_btagSF   = ROOT.TH1F("btagSF",   ";; Average b-tagging SF", 1,0.5,1.5)
h_toptagSF = ROOT.TH1F("toptagSF", ";; Average top-tagging SF", 1,0.5,1.5)



############################################################################################################
# UNFOLDING 
############################################################################################################

# dummy histogram used only to specify dimensions for reponse matrix
ptbins = array('d',[0.0,200.0,400.0,500.0,600.0,700.0,800.0,1200.0,2000.0])
h_bins = ROOT.TH1F("bins",       ";;", len(ptbins)-1,       ptbins)

if options.makeResponse == True : 

    ## --------------------------------------------------------------------------------------------------
    ## ONE-STEP UNFOLDING
    ## --------------------------------------------------------------------------------------------------
    
    response = ROOT.RooUnfoldResponse(h_bins, h_bins)
    response.SetName('response_pt')
    response_nobtag = ROOT.RooUnfoldResponse(h_bins, h_bins)
    response_nobtag.SetName('response_pt_nobtag')
    h_ptGenTop          = ROOT.TH1F("ptGenTop",          ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
    h_ptGenTop_noweight = ROOT.TH1F("ptGenTop_noweight", ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)

    ## --------------------------------------------------------------------------------------------------
    ## TWO-STEP UNFOLDING
    ## --------------------------------------------------------------------------------------------------

    response_pp = ROOT.RooUnfoldResponse(h_bins, h_bins)
    response_pp.SetName('response_pt_pp')
    response_rp = ROOT.RooUnfoldResponse(h_bins, h_bins)
    response_rp.SetName('response_pt_rp')
    response_nobtag_rp = ROOT.RooUnfoldResponse(h_bins, h_bins)
    response_nobtag_rp.SetName('response_pt_nobtag_rp')
    h_ptPartTop          = ROOT.TH1F("ptPartTop",          ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
    h_ptPartTop_noweight = ROOT.TH1F("ptPartTop_noweight", ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)


    ### for acceptance correction / efficiency, all these are for semileptonic decays only 
    # passParton = pt(hadronic, gen-level top quark) > 400 GeV
    # passParticle = pass particle-level selection (includes pt(particle-level top jet) > 400 GeV cut)
    # passReco = pass full event selection
    # passRecoNoBtag = pass full event selection MINUS b-tagging
    h_ptRecoTop_passReco         = ROOT.TH1F("ptRecoTop_passReco",         ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptRecoTop_passRecoParton   = ROOT.TH1F("ptRecoTop_passRecoParton",   ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptRecoTop_passRecoParticle = ROOT.TH1F("ptRecoTop_passRecoParticle", ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptRecoTop_passRecoParticleParton = ROOT.TH1F("ptRecoTop_passRecoParticleParton", ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptRecoTop_passRecoParticleLoose  = ROOT.TH1F("ptRecoTop_passRecoParticleLoose",  ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)

    h_ptRecoTop_passRecoNoBtag         = ROOT.TH1F("ptRecoTop_passRecoNoBtag",         ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptRecoTop_passRecoNoBtagParton   = ROOT.TH1F("ptRecoTop_passRecoNoBtagParton",   ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptRecoTop_passRecoNoBtagParticle = ROOT.TH1F("ptRecoTop_passRecoNoBtagParticle", ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptRecoTop_passRecoNoBtagParticleParton = ROOT.TH1F("ptRecoTop_passRecoNoBtagParticleParton", ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptRecoTop_passRecoNoBtagParticleLoose  = ROOT.TH1F("ptRecoTop_passRecoNoBtagParticleLoose",  ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)

    h_ptPartTop_passParticle           = ROOT.TH1F("ptPartTop_passParticle",           ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptPartTop_passRecoParticle       = ROOT.TH1F("ptPartTop_passRecoParticle",       ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptPartTop_passRecoNoBtagParticle = ROOT.TH1F("ptPartTop_passRecoNoBtagParticle", ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptPartTop_passParticleParton     = ROOT.TH1F("ptPartTop_passParticleParton",     ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptPartTop_passRecoParticleParton       = ROOT.TH1F("ptPartTop_passRecoParticleParton",       ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    h_ptPartTop_passRecoNoBtagParticleParton = ROOT.TH1F("ptPartTop_passRecoNoBtagParticleParton", ";p_{T}(particle-level top) [GeV]; Events / 10 GeV", len(ptbins)-1,  ptbins)
    
    h_ptGenTop_passParton           = ROOT.TH1F("ptGenTop_passParton",           ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
    h_ptGenTop_passRecoParton       = ROOT.TH1F("ptGenTop_passRecoParton",       ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
    h_ptGenTop_passRecoNoBtagParton = ROOT.TH1F("ptGenTop_passRecoNoBtagParton", ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
    h_ptGenTop_passParticleParton   = ROOT.TH1F("ptGenTop_passParticleParton",   ";p_{T}(generated top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)



h_ptRecoTop        = ROOT.TH1F("ptRecoTop",        ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_ptRecoTop_nobtag = ROOT.TH1F("ptRecoTop_nobtag", ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_ptRecoTop_2step        = ROOT.TH1F("ptRecoTop_2step",        ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)
h_ptRecoTop_2step_nobtag = ROOT.TH1F("ptRecoTop_2step_nobtag", ";p_{T}(reconstructed top) [GeV]; Events / 10 GeV", len(ptbins)-1, ptbins)



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

metHandle    = Handle("std::vector<float>")
metLabel     = ("pfShyftTupleMET" + postfix, "pt")
metphiHandle = Handle("std::vector<float>")
metphiLabel  = ("pfShyftTupleMET" + postfix, "phi")

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
ak5JetFlavorHandle = Handle( "std::vector<float>" )
ak5JetFlavorLabel  = ("pfShyftTupleJets" + postfix + "AK5", "flavor")

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
topTagJetAreaHandle  = Handle( "std::vector<float>" )
topTagJetAreaLabel   = ("pfShyftTupleJetsLooseTopTag", "jetArea")

# CA8 subjets collection
nsubCA8Handle = Handle("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > >")
nsubCA8Label  = ("nsub", "CA8P4")

# top tagged tau2 / tau 3 variables
TopTau2Handle = Handle("std::vector<double>")
TopTau2Label  = ("nsub", "Tau2")
TopTau3Handle = Handle("std::vector<double>")
TopTau3Label  = ("nsub", "Tau3")

# top-tagged subjets variables
topTagsj0csvHandle = Handle("std::vector<float>")
topTagsj0csvLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj0csv")
topTagsj1csvHandle = Handle("std::vector<float>")
topTagsj1csvLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj1csv")
topTagsj2csvHandle = Handle("std::vector<float>")
topTagsj2csvLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj2csv")
topTagsj3csvHandle = Handle("std::vector<float>")
topTagsj3csvLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj3csv")

topTagsj0ptHandle = Handle("std::vector<float>")
topTagsj0ptLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj0pt")
topTagsj1ptHandle = Handle("std::vector<float>")
topTagsj1ptLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj1pt")
topTagsj2ptHandle = Handle("std::vector<float>")
topTagsj2ptLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj2pt")
topTagsj3ptHandle = Handle("std::vector<float>")
topTagsj3ptLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj3pt")

topTagsj0etaHandle = Handle("std::vector<float>")
topTagsj0etaLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj0eta")
topTagsj1etaHandle = Handle("std::vector<float>")
topTagsj1etaLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj1eta")
topTagsj2etaHandle = Handle("std::vector<float>")
topTagsj2etaLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj2eta")
topTagsj3etaHandle = Handle("std::vector<float>")
topTagsj3etaLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj3eta")

topTagsj0phiHandle = Handle("std::vector<float>")
topTagsj0phiLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj0phi")
topTagsj1phiHandle = Handle("std::vector<float>")
topTagsj1phiLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj1phi")
topTagsj2phiHandle = Handle("std::vector<float>")
topTagsj2phiLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj2phi")
topTagsj3phiHandle = Handle("std::vector<float>")
topTagsj3phiLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj3phi")

topTagsj0massHandle = Handle("std::vector<float>")
topTagsj0massLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj0mass")
topTagsj1massHandle = Handle("std::vector<float>")
topTagsj1massLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj1mass")
topTagsj2massHandle = Handle("std::vector<float>")
topTagsj2massLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj2mass")
topTagsj3massHandle = Handle("std::vector<float>")
topTagsj3massLabel  = ("pfShyftTupleJetsLooseTopTag", "topsj3mass")


# variables for PDF systematics (three different PDF sets)
if options.pdfSys != 0.0 or options.pdfSet != 0.0: 
    pdfWeightCT10Handle  = Handle("std::vector<double>")
    pdfWeightCT10Label   = ("pdfWeights", "ct10weights")
    
    pdfWeightMSTWHandle  = Handle("std::vector<double>")
    pdfWeightMSTWLabel   = ("pdfWeights", "mstwweights")

    pdfWeightNNPDFHandle = Handle("std::vector<double>")
    pdfWeightNNPDFLabel  = ("pdfWeights", "nnpdfweights")


# if making response matrix, need generated particles (truth-level)
if options.makeResponse == True or options.mttGenMax is not None or options.semilep is not None: 
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

if options.WjetsHF != None:
    genParticlesPtHandle     = Handle("std::vector<float>")
    genParticlesPtLabel      = ("pfShyftTupleGenParticles", "pt")
    genParticlesPdgIdHandle  = Handle("std::vector<float>")
    genParticlesPdgIdLabel   = ("pfShyftTupleGenParticles", "pdgId")
    genParticlesStatusHandle = Handle("std::vector<float>")
    genParticlesStatusLabel  = ("pfShyftTupleGenParticles", "status")


# if doing JER corrections, need the gen jets (for AK5 and CA8 jets)
# also need the gen jets when doing particle-level unfolding
if options.jerSys != None or options.makeResponse == True:
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
# read MC weights if doing top pt reweighting
# -------------------------------------------------------------------------------------

if options.set == 'mcatnlo':
	print "Using MC@NLO weights"
	weightFile = ROOT.TFile("ptlepNewSelmcatnlo_weight.root")
elif options.set == 'powheg':
	print "Using Powheg weights"
	weightFile = ROOT.TFile("ptlepNewSelpowheg_weight.root")
else:
	print "Using MadGraph weights"
	weightFile = ROOT.TFile("ptlepNewSel_weight.root")

weightPlot = weightFile.Get("lepptweight")
if options.ptWeight == False :
	print "Turning top pt reweighting off"


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
if "TT_max700" in options.outname and "scaleup" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2up * e_TT_Mtt_0_700_Q2up * lum / float(Nmc_ttbar_Q2up)
elif "TT_max700" in options.outname and "scaledown" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2dn * e_TT_Mtt_0_700_Q2dn * lum / float(Nmc_ttbar_Q2dn)
elif "TT_max700" in options.outname :
    weight_response = sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar)
## 700 < m < 100 GeV 
elif "TT_Mtt-700to1000" in options.outname and "scaleup" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2up * e_TT_Mtt_700_1000_Q2up * lum / float(Nmc_TT_Mtt_700_1000_Q2up)
elif "TT_Mtt-700to1000" in options.outname and "scaledown" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2dn * e_TT_Mtt_700_1000_Q2dn * lum / float(Nmc_TT_Mtt_700_1000_Q2dn)
elif "TT_Mtt-700to1000" in options.outname :
    weight_response = sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000)
## 1000 < m < inf GeV
elif "TT_Mtt-1000toInf" in options.outname and "scaleup" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2up * e_TT_Mtt_1000_Inf_Q2up * lum / float(Nmc_TT_Mtt_1000_Inf_Q2up)
elif "TT_Mtt-1000toInf" in options.outname and "scaledown" in options.outname :
    weight_response = sigma_ttbar_NNLO_Q2dn * e_TT_Mtt_1000_Inf_Q2dn * lum / float(Nmc_TT_Mtt_1000_Inf_Q2dn)
elif "TT_Mtt-1000toInf" in options.outname:
    weight_response = sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf)
    

# -------------------------------------------------------------------------------------
# reset various counters
# -------------------------------------------------------------------------------------

ntotal = 0       # total number of events
npassed = 0      # number of events passing selection
goodEvents = []  # vector for storing events passing full selection


# -------------------------------------------------------------------------------------
# start looping over events
# -------------------------------------------------------------------------------------

print "Start looping over events!"

for event in events :
    
    weight = 1.0 #event weight

    mttbarGen = -1.0

    ## various pass/fail for unfolding 
    passParton = False         ## this means pt(gen-level hadronic top) > 400 GeV
    passParticle = False       ## this means "loose particle-level selection" PLUS pt(particle-level top jet) > 400 GeV 
    passReco = False           ## this means passing full event selection
    passRecoNoBtag = False     ## this means passing full event selection MINUS b-tagging cut (i.e. merging both top-tag categories) 
    passParticleLoose = False  ## this means "loose particle-level selection"
    
    if ntotal % 10000 == 0 or options.debug :
      print  '--------- Processing Event ' + str(ntotal)
    ntotal += 1

    if options.oddeven != 'none':
        # odd only
        if options.oddeven == 1 and event.object().id().event()%2 == 1 :
            continue
        # event only
        if options.oddeven == 2 and event.object().id().event()%2 == 0 :
            continue
        

    # -------------------------------------------------------------------------------------
    # read PU information & do PU reweighting
    # -------------------------------------------------------------------------------------

    if options.pileup != 'none':   
    	event.getByLabel (puLabel, puHandle)
    	PileUp = puHandle.product()
    	bin1 = PilePlot.FindBin(PileUp[0]) 
    	weight *= PilePlot.GetBinContent(bin1)
        if options.debug : 
            print "PU weight is " + str(weight)

    event.getByLabel (npvLabel, npvHandle)
    numvert = npvHandle.product()
    nvtx = float(numvert[0])

    h_nvtx_pre.Fill(nvtx)
    h_nvtx_post.Fill(nvtx, weight)
    
    
    # -------------------------------------------------------------------------------------
    # If doing PDF systematatics:
    # Get the envelopes of the various PDF sets for this event.
    # Use the max and min values of all of the eigenvectors as the envelope. 
    # -------------------------------------------------------------------------------------

    if options.pdfSys != 0.0 or options.pdfSet != 0.0:

        if options.pdfSet == 1.0 :
            event.getByLabel( pdfWeightMSTWLabel, pdfWeightMSTWHandle )
            pdfWeight  = pdfWeightMSTWHandle.product()
        elif options.pdfSet == 2.0 :
            event.getByLabel( pdfWeightNNPDFLabel, pdfWeightNNPDFHandle )
            pdfWeight = pdfWeightNNPDFHandle.product()
        else :
            event.getByLabel( pdfWeightCT10Label, pdfWeightCT10Handle )
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
                    tmpweight = pdfWeight[1+2*iw] - 1.0
                if (pdfWeight[2+2*iw] - 1.0) > tmpweight :
                    tmpweight = pdfWeight[2+2*iw] - 1.0
                upweight += tmpweight*tmpweight
            upweight = 1.0 + math.sqrt(upweight)
            weight *= upweight
            this_pdfweight = upweight
        else :   # downward PDF uncertainty
            dnweight = 0.0
            for iw in range(0,nEigenVec) :
                tmpweight = 0.0
                if (1.0 - pdfWeight[1+2*iw]) > tmpweight :
                    tmpweight = 1.0 - pdfWeight[1+2*iw]
                if (1.0 - pdfWeight[2+2*iw]) > tmpweight :
                    tmpweight = 1.0 - pdfWeight[2+2*iw]
                dnweight += tmpweight*tmpweight
            dnweight = 1.0 - math.sqrt(dnweight)
            weight *= dnweight
            this_pdfweight = dnweight

        ## ignore potential events with crazy pdf weight (one CT10 pdf up weight...)
        if (this_pdfweight > 100.0):
            print "WARNING!! really large PDF weight for pdfset # " + str(options.pdfSet) + " syst # " + str(options.pdfSys) + ", weight = " + str(this_pdfweight) + " -- i'm ignoring this event!!"
            continue

        if options.debug : 
            print "PPDF weight is " + str(this_pdfweight)

        
    
    #endof if doing pdfSys
  

    
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
    genElectrons = []
    hadTop = None
    lepTop = None
    isSemiLeptonicGen = True
    isMuon = False
    isElectron = False
    
    if options.makeResponse == True or options.mttGenMax is not None or options.semilep is not None:
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

            if (abs(genParticlesPdgId[igen]) == 11) :
                isElectron = True
                p4Electron = ROOT.TLorentzVector()
                p4Electron.SetPtEtaPhiM( genParticlesPt[igen], genParticlesEta[igen], genParticlesPhi[igen], genParticlesMass[igen] )
                genElectrons.append(p4Electron)

        topQuarks.append( GenTopQuark( 6, p4Top, topDecay) )
        topQuarks.append( GenTopQuark( -6, p4Antitop, antitopDecay) )
        
        if (topDecay + antitopDecay == 1) and (isMuon == True) and (isElectron == False) and (options.lepType == "muon"):
            isSemiLeptonicGen = True
            if options.debug:
                print "semileptonic ttbar decay to muon channel!"
        elif (topDecay + antitopDecay == 1) and (isMuon == False) and (isElectron == True) and (options.lepType == "ele"):
            isSemiLeptonicGen = True
            if options.debug:
                print "semileptonic ttbar decay to electron channel!"
        else :
            isSemiLeptonicGen = False
            if options.debug:
                print "NON-semileptonic ttbar decay!"

        # If we are filling the response matrix, don't
        # consider "volunteer" events that pass the selection
        # even though they aren't really semileptonic events. 

        if options.makeResponse == True and not (options.semilep < 0) and isSemiLeptonicGen == False :
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

        h_mttbarGen0.Fill(mttbarGen, weight)

        if options.makeResponse == True:
            h_ptGenTop.Fill( hadTop.p4.Perp(), weight )
            h_ptGenTop_noweight.Fill( hadTop.p4.Perp() )
            
            if hadTop.p4.Perp() > 400.0:
                passParton = True
                h_ptGenTop_passParton.Fill(hadTop.p4.Perp(), weight)
                                
        # endif (making response matrix)


    ## if not doing response matrix stuff for ttbar, don't require parton-level cut either!
    if options.makeResponse != True:
        passParton = True

    if options.WjetsHF is not None:
        event.getByLabel( genParticlesPtLabel, genParticlesPtHandle )
        event.getByLabel( genParticlesPdgIdLabel, genParticlesPdgIdHandle )
        event.getByLabel( genParticlesStatusLabel, genParticlesStatusHandle )

        genParticlesPt  = genParticlesPtHandle.product()
        genParticlesPdgId  = genParticlesPdgIdHandle.product()
        genParticlesStatus = genParticlesStatusHandle.product()

        Wccjets = False
        Wbbjets = False
        Wcjets = False
        Wlightjets = False

        cCount = 0
        bCount = 0

        particleID = []
        
        for iparticle in xrange (len(genParticlesStatus)):
            if genParticlesStatus[iparticle] == 3:
                particleID.append( abs(genParticlesPdgId[iparticle]) )

        for iparticle in xrange (len(particleID)):
            if particleID[iparticle] == 4:
                cCount += 1
            elif particleID[iparticle] == 5:
                bCount += 1
                

        if bCount > 1:
            Wbbjets = True
        elif cCount > 1:
            Wccjets = True
        elif cCount == 1:
            Wcjets = True
        else :
            Wlightjets = True


        ## select Wbb final states
        if options.WjetsHF == "wbb" and Wbbjets == False:
            continue
        ## select Wcc final states
        if options.WjetsHF == "wcc" and Wccjets == False:
            continue
        ## select Wc final states
        if options.WjetsHF == "wc" and Wcjets == False:
            continue
        ## select W+light final states
        if options.WjetsHF == "wl" and Wlightjets == False:
            continue


             
    # -------------------------------------------------------------------------------------
    # read gen jets if doing JER systematics or 2-step unfolding
    # -------------------------------------------------------------------------------------

    ak5GenJets = []
    ca8GenJets = []
    
    if options.makeResponse == True or options.jerSys != None:
        event.getByLabel( ak5GenJetPtLabel, ak5GenJetPtHandle )
        if ak5GenJetPtHandle.isValid() == False :
            if options.makeResponse == True:
                response.Miss( hadTop.p4.Perp(), weight*weight_response )
                response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
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
            if options.makeResponse == True:
                response.Miss( hadTop.p4.Perp(), weight*weight_response )
                response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
                response_pp.Miss( hadTop.p4.Perp(), weight*weight_response )
            continue

        # loop over AK5 gen jets
        for iak5 in xrange( len(ak5GenJetPt) ) :
            p4 = ROOT.TLorentzVector()
            p4.SetPtEtaPhiM( ak5GenJetPt[iak5], ak5GenJetEta[iak5], ak5GenJetPhi[iak5], ak5GenJetMass[iak5] )
            ak5GenJets.append(p4)
            if options.debug :
                print 'AK5Gen {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f})'.format( iak5, ak5GenJetPt[iak5], ak5GenJetEta[iak5], ak5GenJetPhi[iak5], ak5GenJetMass[iak5] )

        event.getByLabel( ca8GenJetPtLabel, ca8GenJetPtHandle )
        if ca8GenJetPtHandle.isValid() == False :
            if options.makeResponse == True:
                response.Miss( hadTop.p4.Perp(), weight*weight_response )
                response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
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
            if options.makeResponse == True:
                response.Miss( hadTop.p4.Perp(), weight*weight_response )
                response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
                response_pp.Miss( hadTop.p4.Perp(), weight*weight_response )
            continue

        # loop over CA8 gen jets
        for ica8 in xrange( len(ca8GenJetPt) ) :
            p4 = ROOT.TLorentzVector()
            p4.SetPtEtaPhiM( ca8GenJetPt[ica8], ca8GenJetEta[ica8], ca8GenJetPhi[ica8], ca8GenJetMass[ica8] )
            ca8GenJets.append(p4)
            if options.debug :
                print 'CA8Gen {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f})'.format( ica8, ca8GenJetPt[ica8], ca8GenJetEta[ica8], ca8GenJetPhi[ica8], ca8GenJetMass[ica8] )



    # -------------------------------------------------------------------------------------
    # implement particle-level selection
    # -------------------------------------------------------------------------------------

    if options.makeResponse == True:
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


        ## loose particle-level selection w/o 400 cut
        if passParticleLoose == False:
            response_pp.Miss( hadTop.p4.Perp(), weight*weight_response )
        else:           
            h_ptPartTop.Fill( genTops[0].Perp(), weight )
            h_ptPartTop_noweight.Fill( genTops[0].Perp() )
            response_pp.Fill(genTops[0].Perp(), hadTop.p4.Perp(), weight*weight_response)

        ## particle-level selection *with* 400 cut
        if passParticle:
            h_ptPartTop_passParticle.Fill(genTops[0].Perp(), weight) 
            if passParton: 
                h_ptPartTop_passParticleParton.Fill(genTops[0].Perp(), weight) 
                h_ptGenTop_passParticleParton.Fill(hadTop.p4.Perp(), weight)
        
    else :
        passParticleLoose = True
        passParticle = True
    ## end particle-level selection
    

    # -------------------------------------------------------------------------------------
    # read AK5 jet information
    # -------------------------------------------------------------------------------------

    event.getByLabel (ak5JetPtLabel, ak5JetPtHandle)
    if ak5JetPtHandle.isValid() == False : 
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
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
        if ak5JetPts[ijet] > 25. :
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
                        
                if options.lepType == "ele":
                    h_dRvspTPre.Fill( electron.p4().DeltaR(eleJet), electron.p4().Perp(eleJet.Vect()), weight )
                    h_pfIsoPre.Fill(electron.getIsoPU(), weight)
            
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

                if options.lepType == "muon":
                    h_dRvspTPre.Fill( muon.p4().DeltaR(muJet), muon.p4().Perp(muJet.Vect()), weight )
                    h_pfIsoPre.Fill(muon.getIsoPU(), weight)

            muons.append(muon)


                    
    # -------------------------------------------------------------------------------------
    # muon channel
    # -------------------------------------------------------------------------------------

    cut1 = nMuons == 1 and nElectronsForVeto <= 0
    if options.debug == True and cut1 == True :
        print '----- event good for muons ----'

    # -------------------------------------------------------------------------------------
    # electron channel
    # -------------------------------------------------------------------------------------

    cut2 = nElectrons == 1 and nMuonsForVeto <= 0
    if options.debug == True and cut2 == True :
        print '----- event good for electrons ----'

    
    # -------------------------------------------------------------------------------------
    # fill nbr of leptons plots & require exactly one lepton
    # -------------------------------------------------------------------------------------
    cut = None
    muonSF = 1.0
    if options.lepType == "muon":
        cut = cut1
        if options.debug == True and cut == True :
            print '----- Counting as muon event -----'
        if nMuons == 1 and options.isData == False :
            muEta = muons[igoodMu].p4().Eta()
            muonSF = getMuonSF(muEta)
            weight = weight*muonSF
    else :
        cut = cut2
        if options.debug == True and cut == True :
            print '----- Counting as electron event -----'    
        if nElectrons == 1 and options.isData == False :
            elEta = electrons[igoodEle].p4().Eta()
            elPt = electrons[igoodEle].p4().Pt()
            electronSF = getElectronSF(elEta, elPt)
            weight = weight*electronSF
    
    leptons = muons + electrons
    #h_nMuons.Fill( nMuons, weight )
    #h_nElectrons.Fill( nElectrons, weight )
        
    if cut == False or cut == None: 
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue


    # -------------------------------------------------------------------------------------
    # Now look at the rest of the lepton information.
    # We will classify jets based on hemispheres, defined by the lepton.
    # -------------------------------------------------------------------------------------

    if options.lepType == "ele" :
        lepton = electrons[igoodEle]
    else :
        lepton = muons[igoodMu]

    closestFor2D = findClosestInList( lepton.p4(), jetsFor2D )

    if options.debug :
        print lepton
    

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
    # loop over AK5 jets
    # -------------------------------------------------------------------------------------

    ak5Jets = [] #list of smeared/corrected jets
    ht = 0.0

    if options.debug :
        print '---------- AK5 jets ------------'
    
    for ijet in xrange( len(ak5JetPts) ) :

        if options.debug :
            print 'Orig   {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f})'.format( ijet, ak5JetPts[ijet], ak5JetEtas[ijet], ak5JetPhis[ijet], ak5JetMasss[ijet] )
            
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
        
        # then apply any jet corrections uncertainty variations
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

        # calculate HT
        ht += thisJet.Perp()
            
        if options.debug :
            print 'Corr   {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f})'.format( ijet, ak5Jets[ijet].Perp(), ak5Jets[ijet].Eta(), ak5Jets[ijet].Phi(), ak5Jets[ijet].M() )

    

    # -------------------------------------------------------------------------------------
    # STEP (0): require a good lepton
    # -------------------------------------------------------------------------------------

    # HT = scalar sum of jet pt
    # HT_lep = scalar sum of jet pt (HT) & lepton pt
    
    met = math.sqrt(met_px*met_px + met_py*met_py)
    metv = ROOT.TLorentzVector()
    metv.SetPtEtaPhiM( met, 0.0, metphi, 0.0)

    htLep = lepton.p4().Perp() + met


    # -------------------------------------------------------------------------------------
    ## additional triangular cut for electron channel to reject QCD

    passTriangular = True
    
    if options.lepType == "ele" and options.useTriangular:
        dphi_emet = abs(metphi - lepton.p4().Phi())
        while dphi_emet > 3.14159 : 
            dphi_emet = abs(2*3.14159 - dphi_emet)
        dphi_jetmet = abs(metphi - ak5Jets[0].Phi())
        while dphi_jetmet > 3.14159 : 
            dphi_jetmet = abs(2*3.14159 - dphi_jetmet)
        
        if not options.doQCD:
            if ( abs(dphi_emet-1.5) > 1.5*met/75.0 or abs(dphi_jetmet-1.5) > 1.5*met/75.0 ):
                passTriangular = False
        else: 
            if ( abs(dphi_emet-1.5) < 1.5*met/75.0 and abs(dphi_jetmet-1.5) < 1.5*met/75.0 ):
                passTriangular = False

    if passTriangular == False:
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue
    # -------------------------------------------------------------------------------------

    
    if options.debug :
        print 'Passed stage0'
    cutflow['Stage 0: '] += 1
    
    h_ht0.Fill(ht, weight)
    h_htLep0.Fill(htLep, weight)
    h_ptMET0.Fill(met, weight)
    h_phiMET0.Fill(metphi, weight)
    h_pfIso0.Fill(lepton.getIsoPU(), weight)
    h_dRvspT0.Fill(lepton.p4().DeltaR(closestFor2D), lepton.p4().Perp(closestFor2D.Vect()), weight)
    h_ptLep0.Fill(lepton.p4().Perp(), weight)
    h_etaLep0.Fill(lepton.p4().Eta(), weight)
    h_etaAbsLep0.Fill(abs(lepton.p4().Eta()), weight)

    h_nvtx0_pre.Fill(nvtx)
    h_nvtx0_post.Fill(nvtx, weight)

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
    nBJets = 0.0
    i_goodjets = []
    for ijet in range(0,len(ak5Jets)) :
        if ak5Jets[ijet].Perp() > MIN_JET_PT and abs(ak5Jets[ijet].Eta()) < MAX_JET_ETA:
            nJets += 1.0
            i_goodjets.append(ijet)
            if ak5JetCSVs[ijet] > options.bDiscCut :
                nBJets += 1.0

    #h_nJets0.Fill(nJets, weight)
    #h_nBJets0.Fill(nBJets, weight)

    #if nJets >= 1 :
    #    ij = i_goodjets[0]
    #    h_pt1Jet0.Fill(ak5Jets[ij].Perp(), weight)
    #    h_eta1Jet0.Fill(ak5Jets[ij].Eta(), weight)
    #    h_csv1Jet0.Fill(ak5JetCSVs[ij], weight)
    #    h_vtxMass1Jet0.Fill(ak5JetSecvtxMasses[ij], weight)
    #if nJets >= 2 :
    #    ij = i_goodjets[1]
    #    h_pt2Jet0.Fill(ak5Jets[ij].Perp(), weight)
    #    h_eta2Jet0.Fill(ak5Jets[ij].Eta(), weight)
    #    h_csv2Jet0.Fill(ak5JetCSVs[ij], weight)
    #    h_vtxMass2Jet0.Fill(ak5JetSecvtxMasses[ij], weight)
    #if nJets >= 3 :
    #    ij = i_goodjets[2]
    #    h_pt3Jet0.Fill(ak5Jets[ij].Perp(), weight)
    #    h_eta3Jet0.Fill(ak5Jets[ij].Eta(), weight)
    #    h_csv3Jet0.Fill(ak5JetCSVs[ij], weight)
    #    h_vtxMass3Jet0.Fill(ak5JetSecvtxMasses[ij], weight)
    #if nJets >= 4 :
    #    ij = i_goodjets[3]
    #    h_pt4Jet0.Fill(ak5Jets[ij].Perp(), weight)
    #    h_eta4Jet0.Fill(ak5Jets[ij].Eta(), weight)
    #    h_csv4Jet0.Fill(ak5JetCSVs[ij], weight)
    #    h_vtxMass4Jet0.Fill(ak5JetSecvtxMasses[ij], weight)
        
    
    # -------------------------------------------------------------------------------------
    # define W boson from MET and lepton
    # -------------------------------------------------------------------------------------

    v_wboson = metv + lepton.p4()
    wboson_mt = v_wboson.Mt()
    wboson_pt = v_wboson.Perp()

    h_wboson_pt0.Fill(wboson_pt, weight)
    h_wboson_mt0.Fill(wboson_mt, weight)


    
    # -------------------------------------------------------------------------------------
    # STEP (1): require >= 2 AK5 jets above 30 GeV
    # -------------------------------------------------------------------------------------

    if nJets < 2 :
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue
    if options.debug :
        print 'Passed stage1'
    cutflow['Stage 1: '] += 1

    h_mttbarGen1.Fill(mttbarGen, weight)
    h_ht1.Fill(ht, weight)
    h_htLep1.Fill(htLep, weight)
    h_ptMET1.Fill(met, weight)
    h_phiMET1.Fill(metphi, weight)
    h_pfIso1.Fill(lepton.getIsoPU(), weight)
    h_dRvspT1.Fill(lepton.p4().DeltaR(closestFor2D), lepton.p4().Perp(closestFor2D.Vect()), weight)
    h_ptLep1.Fill(lepton.p4().Perp(), weight)
    h_etaLep1.Fill(lepton.p4().Eta(), weight)
    h_etaAbsLep1.Fill(abs(lepton.p4().Eta()), weight)
    #h_nJets1.Fill(nJets, weight)
    #h_nBJets1.Fill(nBJets, weight)

    h_wboson_pt1.Fill(wboson_pt, weight)
    h_wboson_mt1.Fill(wboson_mt, weight)

    #if nJets >= 1 :
    #    ij = i_goodjets[0]
    #    h_pt1Jet1.Fill(ak5Jets[ij].Perp(), weight)
    #    h_eta1Jet1.Fill(ak5Jets[ij].Eta(), weight)
    #    h_csv1Jet1.Fill(ak5JetCSVs[ij], weight)
    #    h_vtxMass1Jet1.Fill(ak5JetSecvtxMasses[ij], weight)
    #if nJets >= 2 :
    #    ij = i_goodjets[1]
    #    h_pt2Jet1.Fill(ak5Jets[ij].Perp(), weight)
    #    h_eta2Jet1.Fill(ak5Jets[ij].Eta(), weight)
    #    h_csv2Jet1.Fill(ak5JetCSVs[ij], weight)
    #    h_vtxMass2Jet1.Fill(ak5JetSecvtxMasses[ij], weight)
    #if nJets >= 3 :
    #    ij = i_goodjets[2]
    #    h_pt3Jet1.Fill(ak5Jets[ij].Perp(), weight)
    #    h_eta3Jet1.Fill(ak5Jets[ij].Eta(), weight)
    #    h_csv3Jet1.Fill(ak5JetCSVs[ij], weight)
    #    h_vtxMass3Jet1.Fill(ak5JetSecvtxMasses[ij], weight)
    #if nJets >= 4 :
    #    ij = i_goodjets[3]
    #    h_pt4Jet1.Fill(ak5Jets[ij].Perp(), weight)
    #    h_eta4Jet1.Fill(ak5Jets[ij].Eta(), weight)
    #    h_csv4Jet1.Fill(ak5JetCSVs[ij], weight)
    #    h_vtxMass4Jet1.Fill(ak5JetSecvtxMasses[ij], weight)

        
    # -------------------------------------------------------------------------------------
    # STEP (2): cut on MET?
    # -------------------------------------------------------------------------------------

    if options.metCut is not None and met < options.metCut :
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue

    if options.debug :
        print 'Passed stage2'
    cutflow['Stage 2: '] += 1

    h_mttbarGen2.Fill(mttbarGen, weight)
    h_ht2.Fill(ht, weight)
    h_htLep2.Fill(htLep, weight)
    h_ptMET2.Fill(met, weight)
    h_phiMET2.Fill(metphi, weight)
    h_pfIso2.Fill(lepton.getIsoPU(), weight)
    h_dRvspT2.Fill(lepton.p4().DeltaR(closestFor2D), lepton.p4().Perp(closestFor2D.Vect()), weight)
    h_ptLep2.Fill(lepton.p4().Perp(), weight)
    h_etaLep2.Fill(lepton.p4().Eta(), weight)
    h_etaAbsLep2.Fill(abs(lepton.p4().Eta()), weight)
    #h_nJets2.Fill(nJets, weight)
    #h_nBJets2.Fill(nBJets, weight)

    h_wboson_pt2.Fill(wboson_pt, weight)
    h_wboson_mt2.Fill(wboson_mt, weight)

        
    # -------------------------------------------------------------------------------------
    # read variables for CA8 jets
    # -------------------------------------------------------------------------------------

    event.getByLabel (topTagPtLabel, topTagPtHandle)
    if topTagPtHandle.isValid() == False :
        if options.debug :
            print 'No CA8 top tag jets in this event'
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
    event.getByLabel (topTagJetAreaLabel, topTagJetAreaHandle)
    topTagJetArea = topTagJetAreaHandle.product()


    ca8Jets = []  #list of smeared & corrected CA8 jets
    
    if options.debug :
        print '---------- CA8 jets ------------'

    # loop over top-tagged jets
    for ijet in xrange( len(topTagPt) ) :
        
        if options.debug :
            print 'Orig   {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f})'.format( ijet, topTagPt[ijet], topTagEta[ijet], topTagPhi[ijet], topTagMass[ijet] )

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

        # apply nominal jet energy corrections (for both data & MC)! what's stored now is the uncorrected jet variables! 
        jecNomAK7.setJetEta( thisJet.Eta() )
        jecNomAK7.setJetPt( thisJet.Perp() )
        jecNomAK7.setJetE( thisJet.E() )
        jecNomAK7.setNPV( len(npvHandle.product()) )
        jecNomAK7.setJetA( topTagJetArea[ijet] );
        jecNomAK7.setRho( rho[0] )
        corr = jecNomAK7.getCorrection()
        
        thisJet = thisJet * corr
                
        # next smear the jets (for CA8 jets, used the flat JER of 0.10, or 0.0/0.2 for down/up)
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
            jecUncAK7.setJetEta( thisJet.Eta() )
            jecUncAK7.setJetPt( thisJet.Perp() )                    
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
        
        if options.debug :
            print 'Corr   {0:4.0f} : ({1:6.2f} {2:6.2f} {3:6.2f} {4:6.2f})'.format( ijet, thisJet.Perp(), thisJet.Eta(), thisJet.Phi(), thisJet.M() )
               


    # -------------------------------------------------------------------------------------
    # define hadronic (CA8) / leptonic (AK5) side jet, apply b-tagging, etc. 
    # -------------------------------------------------------------------------------------

    hadJets = []      # CA8 jets with dR(jet,lepton) > pi/2
    hadJetsIndex = [] # identifier in full CA8 jet collection for CA8 jets with dR(jet,lepton) > pi/2
    lepJets = []      # AK5 jets with dR(jet,lepton) < pi/2
    lepcsvs = []      # CSV values of AK5 jets with dR(jet,lepton) < pi/2
    lepVtxMass = []   # secondary vertex mass of AK5 jets with dR(jet,lepton) < pi/2
    lepflavors = []   # True jet flavors of AK5 jets with dR(jet,lepton) < pi/2

    ## use closest jet for b-tagging (default)
    bjet_dR = 5.0      
    bjet_pt = -1.      
    bjet_eta = -99.    
    bjet_csv = -99.    
    bjet_vtxmass = -1. 
    bjet_flavor = -99  

    ## use leading-pt, leptonic-side jet for b-tagging (cross-check)
    bjet_lead_pt = -1.      
    bjet_lead_eta = -99.    
    bjet_lead_csv = -99.    
    bjet_lead_vtxmass = -1. 
    bjet_lead_flavor = -99  

    
    # loop over AK5 jets (leptonic side)
    for ijet in range(0,len(ak5Jets)) :
        if ak5Jets[ijet].Perp() > MIN_JET_PT and abs(ak5Jets[ijet].Eta()) < MAX_JET_ETA:
            jet = ak5Jets[ijet]
            this_dR = jet.DeltaR(lepton.p4())
            if this_dR < ROOT.TMath.Pi() / 2.0 :
                lepJets.append(jet)
                lepcsvs.append(ak5JetCSVs[ijet])
                lepVtxMass.append(ak5JetSecvtxMasses[ijet])
                lepflavors.append(ak5JetFlavors[ijet])
                
                this_pt = ak5Jets[ijet].Perp()

                this_flavor = 1
                if abs(ak5JetFlavors[ijet]) == 5:
                    this_flavor = 5
                elif abs(ak5JetFlavors[ijet]) == 4:
                    this_flavor = 4

                ## closest AK5 jet in dR to lepton -- this will be the one to use for b-tagging!
                if this_dR < bjet_dR: 
                    bjet_dR = this_dR
                    bjet_pt = ak5Jets[ijet].Perp()
                    bjet_eta = ak5Jets[ijet].Eta()
                    bjet_csv = ak5JetCSVs[ijet]
                    bjet_vtxmass = ak5JetSecvtxMasses[ijet]
                    bjet_flavor = this_flavor

                ## highest pt, leptonic-side AK5 jet -- cross-check for b-tagging!
                if this_pt > bjet_lead_pt: 
                    bjet_lead_pt = this_pt
                    bjet_lead_eta = ak5Jets[ijet].Eta()
                    bjet_lead_csv = ak5JetCSVs[ijet]
                    bjet_lead_vtxmass = ak5JetSecvtxMasses[ijet]
                    bjet_lead_flavor = this_flavor

                    
    # loop over CA8 jets (hadronic side)
    for ijet in range(0,len(ca8Jets)) :
        if ca8Jets[ijet].Perp() > MIN_JET_PT and abs(ca8Jets[ijet].Eta()) < MAX_JET_ETA:
            jet = ca8Jets[ijet]
            if jet.DeltaR( lepton.p4() ) > ROOT.TMath.Pi() / 2.0 :
                hadJets.append( jet )
                hadJetsIndex.append( ijet )


    h_nLepJets2.Fill(len(lepJets), weight)

    #if len(lepJets) > 0:
    #    h_pt1LepJet2.Fill(lepJets[0].Perp(), weight)
    #    h_eta1LepJet2.Fill(lepJets[0].Eta(), weight)
    #    h_csv1LepJet2.Fill(lepcsvs[0], weight)
    #    h_vtxMass1LepJet2.Fill(lepVtxMass[0], weight)
    #if len(lepJets) > 1:
    #    h_pt2LepJet2.Fill(lepJets[1].Perp(), weight)
    #    h_eta2LepJet2.Fill(lepJets[1].Eta(), weight)
    #    h_csv2LepJet2.Fill(lepcsvs[1], weight)
    #    h_vtxMass2LepJet2.Fill(lepVtxMass[1], weight)

    
    # -------------------------------------------------------------------------------------
    # STEP (3): require >=1 leptonic-side AK5 jet, >=1 hadronic-side CA8 jet with pt > jetPtCut
    # -------------------------------------------------------------------------------------

    if len(lepJets) < 1 or len(hadJets) < 1 or hadJets[0].Perp() < options.jetPtCut :
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue

    if options.debug :
        print 'Passed stage3'
    cutflow['Stage 3: '] += 1

    h_mttbarGen3.Fill(mttbarGen, weight)
    h_ht3.Fill(ht, weight)
    h_htLep3.Fill(htLep, weight)
    h_vtxMass3.Fill(bjet_vtxmass, weight)
    h_ptMET3.Fill(met, weight)
    h_phiMET3.Fill(metphi, weight)
    h_pfIso3.Fill(lepton.getIsoPU(), weight)
    h_dRvspT3.Fill(lepton.p4().DeltaR(closestFor2D), lepton.p4().Perp(closestFor2D.Vect()), weight)
    h_ptLep3.Fill(lepton.p4().Perp(), weight)
    h_etaLep3.Fill(lepton.p4().Eta(), weight)
    h_etaAbsLep3.Fill(abs(lepton.p4().Eta()), weight)
    #h_nJets3.Fill(nJets, weight)
    #h_nBJets3.Fill(nBJets, weight)
    h_nLepJets3.Fill(len(lepJets), weight)

    #if len(lepJets) > 0:
    #    h_pt1LepJet3.Fill(lepJets[0].Perp(), weight)
    #    h_eta1LepJet3.Fill(lepJets[0].Eta(), weight)
    #    h_csv1LepJet3.Fill(lepcsvs[0], weight)
    #    h_vtxMass1LepJet3.Fill(lepVtxMass[0], weight)
    #if len(lepJets) > 1:
    #    h_pt2LepJet3.Fill(lepJets[1].Perp(), weight)
    #    h_eta2LepJet3.Fill(lepJets[1].Eta(), weight)
    #    h_csv2LepJet3.Fill(lepcsvs[1], weight)
    #    h_vtxMass2LepJet3.Fill(lepVtxMass[1], weight)

    h_wboson_pt3.Fill(wboson_pt, weight)
    h_wboson_mt3.Fill(wboson_mt, weight)


    # define leptonic top & find weight for possibly applying top pt reweighting
    v_leptop = (metv+lepJets[0]+lepton.p4())
    leptop_pt   = v_leptop.Perp()
    leptop_y    = v_leptop.Rapidity()
    leptop_mass = v_leptop.M()
    
    if options.ptWeight == True :
        Bin = weightPlot.FindBin(leptop_pt)
        leptop_weight = weightPlot.GetBinContent(Bin)
        top_weight=weight*leptop_weight
    else:
        top_weight=weight

    h_leptop_pt3.Fill(leptop_pt, top_weight)
    h_leptop_y3.Fill(leptop_y, top_weight)
    h_leptop_mass3.Fill(leptop_mass, top_weight)

    # preliminary hadronic top (i.e. before top-tagged selection)
    h_hadtop_pt3.Fill(hadJets[0].Perp(), top_weight)
    h_hadtop_y3.Fill(hadJets[0].Rapidity(), top_weight)
    h_hadtop_mass3.Fill(hadJets[0].M(), top_weight)

    v_ttbar = hadJets[0] + v_leptop
    ttbar_mass = v_ttbar.M()

    h_ttbar_mass3.Fill(ttbar_mass, top_weight)
    

    # -------------------------------------------------------------------------------------
    # STEP (4): require CA8 jet > 400 GeV
    # -------------------------------------------------------------------------------------

    if hadJets[0].Perp() < 400.0 :
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue

    if options.debug :
        print 'Passed stage4'
    cutflow['Stage 4: '] += 1

    h_mttbarGen4.Fill(mttbarGen, weight)
    h_ht4.Fill(ht, weight)
    h_htLep4.Fill(htLep, weight)
    h_ptMET4.Fill(met, weight)
    h_phiMET4.Fill(metphi, weight)
    h_vtxMass4.Fill(bjet_vtxmass, weight)
    h_ptLep4.Fill(lepton.p4().Perp(), weight)
    h_etaLep4.Fill(lepton.p4().Eta(), weight)
    h_etaAbsLep4.Fill(abs(lepton.p4().Eta()), weight)
    if (hadJets[0].Perp() < 600.) :
        h_etaAbsLep4_low.Fill(abs(lepton.p4().Eta()), weight)
    if (hadJets[0].Perp() > 600.) :
        h_etaAbsLep4_high.Fill(abs(lepton.p4().Eta()), weight)
    #h_nJets4.Fill(nJets, weight)
    #h_nBJets4.Fill(nBJets, weight)
    h_nLepJets4.Fill(len(lepJets), weight)
    h_dRvspT4.Fill(lepton.p4().DeltaR(closestFor2D), lepton.p4().Perp(closestFor2D.Vect()), weight)

    #if len(lepJets) > 0:
    #    h_pt1LepJet4.Fill(lepJets[0].Perp(), weight)
    #    h_eta1LepJet4.Fill(lepJets[0].Eta(), weight)
    #    h_csv1LepJet4.Fill(lepcsvs[0], weight)
    #    h_vtxMass1LepJet4.Fill(lepVtxMass[0], weight)
    #if len(lepJets) > 1:
    #    h_pt2LepJet4.Fill(lepJets[1].Perp(), weight)
    #    h_eta2LepJet4.Fill(lepJets[1].Eta(), weight)
    #    h_csv2LepJet4.Fill(lepcsvs[1], weight)
    #    h_vtxMass2LepJet4.Fill(lepVtxMass[1], weight)

    h_wboson_pt4.Fill(wboson_pt, weight)
    h_wboson_mt4.Fill(wboson_mt, weight)

    h_leptop_pt4.Fill(leptop_pt, top_weight)
    h_leptop_y4.Fill(leptop_y, top_weight)
    h_leptop_mass4.Fill(leptop_mass, top_weight)

    h_hadtop_pt4.Fill(hadJets[0].Perp(), top_weight)
    h_hadtop_y4.Fill(hadJets[0].Rapidity(), top_weight)
    h_hadtop_mass4.Fill(hadJets[0].M(), top_weight)
    h_hadtop_eta4.Fill(hadJets[0].Eta(), top_weight)

    h_ttbar_mass4.Fill(ttbar_mass, top_weight)

    
    # -------------------------------------------------------------------------------------
    # STEP (5): cut on HT or leptonic HT?
    # -------------------------------------------------------------------------------------
    
    if options.htLepCut is not None and htLep < options.htLepCut :
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue

    if options.htCut is not None and ht < options.htCut :
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue

    if options.debug :
        print 'Passed stage5'
    cutflow['Stage 5: '] += 1


    h_mttbarGen5.Fill(mttbarGen, weight)
    h_ht5.Fill(ht, weight)
    h_htLep5.Fill(htLep, weight)
    h_vtxMass5.Fill(bjet_vtxmass, weight)
    h_ptLep5.Fill(lepton.p4().Perp(), weight)
    h_etaLep5.Fill(lepton.p4().Eta(), weight)
    h_etaAbsLep5.Fill(abs(lepton.p4().Eta()), weight)
    h_ptMET5.Fill(met, weight)
    h_phiMET5.Fill(metphi, weight)
    #h_nJets5.Fill(nJets, weight)
    #h_nBJets5.Fill(nBJets, weight)
    h_nLepJets5.Fill(len(lepJets), weight)
    h_dRvspT5.Fill(lepton.p4().DeltaR(closestFor2D), lepton.p4().Perp(closestFor2D.Vect()), weight)

    #if len(lepJets) > 0:
    #    h_pt1LepJet5.Fill(lepJets[0].Perp(), weight)
    #    h_eta1LepJet5.Fill(lepJets[0].Eta(), weight)
    #    h_csv1LepJet5.Fill(lepcsvs[0], weight)
    #    h_vtxMass1LepJet5.Fill(lepVtxMass[0], weight)
    #if len(lepJets) > 1:
    #    h_pt2LepJet5.Fill(lepJets[1].Perp(), weight)
    #    h_eta2LepJet5.Fill(lepJets[1].Eta(), weight)
    #    h_csv2LepJet5.Fill(lepcsvs[1], weight)
    #    h_vtxMass2LepJet5.Fill(lepVtxMass[1], weight)

    h_wboson_pt5.Fill(wboson_pt, weight)
    h_wboson_mt5.Fill(wboson_mt, weight)

    h_leptop_pt5.Fill(leptop_pt, top_weight)
    h_leptop_y5.Fill(leptop_y, top_weight)
    h_leptop_mass5.Fill(leptop_mass, top_weight)

    h_hadtop_pt5.Fill(hadJets[0].Perp(), top_weight)
    h_hadtop_y5.Fill(hadJets[0].Rapidity(), top_weight)
    h_hadtop_mass5.Fill(hadJets[0].M(), top_weight)

    h_ttbar_mass5.Fill(ttbar_mass, top_weight)

    
    # -------------------------------------------------------------------------------------
    # get variables for subjets of top-tagged jet 
    # -------------------------------------------------------------------------------------

    # top subjet information
    event.getByLabel (topTagsj0ptLabel, topTagsj0ptHandle)
    Topsj0pt = topTagsj0ptHandle.product() 
    event.getByLabel (topTagsj0etaLabel, topTagsj0etaHandle)
    Topsj0eta = topTagsj0etaHandle.product() 
    event.getByLabel (topTagsj0phiLabel, topTagsj0phiHandle)
    Topsj0phi = topTagsj0phiHandle.product() 
    event.getByLabel (topTagsj0massLabel, topTagsj0massHandle)
    Topsj0mass = topTagsj0massHandle.product() 

    # lists of variables for all subjets 
    sjmass = []
    sjeta = []
    sjphi = []
    sjpt = []

    sjmass.append(Topsj0mass[0])
    sjeta.append(Topsj0eta[0])
    sjphi.append(Topsj0phi[0])
    sjpt.append(Topsj0pt[0])
    
    if topTagNSub[0] > 1:
    	event.getByLabel (topTagsj1ptLabel, topTagsj1ptHandle)
    	Topsj1pt = topTagsj1ptHandle.product() 
    	event.getByLabel (topTagsj1etaLabel, topTagsj1etaHandle)
    	Topsj1eta = topTagsj1etaHandle.product() 
    	event.getByLabel (topTagsj1phiLabel, topTagsj1phiHandle)
    	Topsj1phi = topTagsj1phiHandle.product() 
    	event.getByLabel (topTagsj1massLabel, topTagsj1massHandle)
    	Topsj1mass = topTagsj1massHandle.product() 

    	sjmass.append(Topsj1mass[0])
    	sjeta.append(Topsj1eta[0])
    	sjphi.append(Topsj1phi[0])
    	sjpt.append(Topsj1pt[0])
        
    if topTagNSub[0] > 2:
    	event.getByLabel (topTagsj2ptLabel, topTagsj2ptHandle)
    	Topsj2pt = topTagsj2ptHandle.product() 
    	event.getByLabel (topTagsj2etaLabel, topTagsj2etaHandle)
    	Topsj2eta = topTagsj2etaHandle.product() 
    	event.getByLabel (topTagsj2phiLabel, topTagsj2phiHandle)
    	Topsj2phi = topTagsj2phiHandle.product()
    	event.getByLabel (topTagsj2massLabel, topTagsj2massHandle)
    	Topsj2mass = topTagsj2massHandle.product() 

    	sjmass.append(Topsj2mass[0])
    	sjeta.append(Topsj2eta[0])
    	sjphi.append(Topsj2phi[0])
    	sjpt.append(Topsj2pt[0])

    if topTagNSub[0] > 3:
    	event.getByLabel (topTagsj3ptLabel, topTagsj3ptHandle)
    	Topsj3pt = topTagsj3ptHandle.product()
    	event.getByLabel (topTagsj3etaLabel, topTagsj3etaHandle)
    	Topsj3eta = topTagsj3etaHandle.product()
    	event.getByLabel (topTagsj3phiLabel, topTagsj3phiHandle)
    	Topsj3phi = topTagsj3phiHandle.product() 
    	event.getByLabel (topTagsj3massLabel, topTagsj3massHandle)
    	Topsj3mass = topTagsj3massHandle.product()

    	sjmass.append(Topsj3mass[0])
    	sjeta.append(Topsj3eta[0])
    	sjphi.append(Topsj3phi[0])
    	sjpt.append(Topsj3pt[0])


    # create lorentzvector for subjets
    sj = ROOT.TLorentzVector()
    sjets = []
    sjets.append(ROOT.TLorentzVector())
    sjets[0].SetPtEtaPhiM( sjpt[0], sjeta[0], sjphi[0], sjmass[0] )
    topcomp = ROOT.TLorentzVector()
    topcomp.SetPtEtaPhiM( sjpt[0], sjeta[0], sjphi[0], sjmass[0] )
    
    for isub in range(1,int(topTagNSub[0])):
        sj.SetPtEtaPhiM( sjpt[isub], sjeta[isub], sjphi[isub], sjmass[isub] )
        sjets.append(ROOT.TLorentzVector())	
        sjets[isub].SetPtEtaPhiM( sjpt[isub], sjeta[isub], sjphi[isub], sjmass[isub] )
        topcomp+=sj

    

    # -------------------------------------------------------------------------------------
    # loop over the top-tagged jets in opposite hemisphere from lepton and
    # apply selection for "good" top-tagged jet 
    # -------------------------------------------------------------------------------------

    itop_pt = -1       # identifier for leading-pt had-top passing pt cut
    itop_nsub = -1     #          .....                    passing nsubjet cut
    itop_minmass = -1  #          .....                    passing minmass cut
    itop_mass = -1     #          .....                    passing mass cut, i.e. final selection
    
    
    for ijet in range(0,len(hadJets)) :
        topjet = hadJets[ijet]
        itop = hadJetsIndex[ijet]

        # top-tagged jet pt > 400 GeV
        if topjet.Perp() < 400.: 
            continue
        if itop_pt < 0: 
            itop_pt = ijet
                
        # nsubjets >= 3
        if topTagNSub[itop] < 3: 
            continue
        if itop_nsub < 0: 
            itop_nsub = ijet

        # min pairwise subjet mass > 50 GeV 
        if topTagMinMass[itop] < 50.: 
            continue
        if itop_minmass < 0: 
            itop_minmass = ijet
        
        # top-tagged jet mass [140, 250] GeV 
        if topjet.M() < 140. or topjet.M() > 250.: 
            continue
        if itop_mass < 0: 
            itop_mass = ijet

    
    # now we have identified top jets passing the different selection criteria, fill histograms! 
    passSelection = False
    
    if itop_pt >= 0:
        h_hadtop_pt_pt.Fill(hadJets[itop_pt].Perp(), top_weight)
        h_hadtop_precut_nsub.Fill(topTagNSub[hadJetsIndex[itop_pt]], top_weight) 
        h_hadtop_precut_nvtx_nsub.Fill(nvtx, topTagNSub[hadJetsIndex[itop_pt]], top_weight)

    if itop_nsub >= 0:
        h_hadtop_pt_nsub.Fill(hadJets[itop_nsub].Perp(), top_weight)
        h_hadtop_precut_minmass.Fill(topTagMinMass[hadJetsIndex[itop_nsub]], top_weight)
        h_hadtop_precut_nvtx_minmass.Fill(nvtx, topTagMinMass[hadJetsIndex[itop_nsub]], top_weight)

    if itop_minmass >= 0:
        h_hadtop_pt_minmass.Fill(hadJets[itop_minmass].Perp(), top_weight)
        h_hadtop_precut_mass.Fill(hadJets[itop_minmass].M(), top_weight)
        h_hadtop_precut_nvtx_mass.Fill(nvtx, hadJets[itop_minmass].M(), top_weight)

    if itop_mass >= 0:
        passSelection = True


    # -------------------------------------------------------------------------------------
    # STEP (6): we now have an event with top-tagged jet passing full selection (minus b-tagging!)
    # -------------------------------------------------------------------------------------

    if not passSelection:
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            response_nobtag.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
                response_nobtag_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue
    if options.debug :
        print 'Passed stage6'
    cutflow['Stage 6: '] += 1

    goodtop = hadJets[itop_mass]
    igoodtop = hadJetsIndex[itop_mass]

    ## apply top-tagging systematic variation up/down
    toptagSF = 1.0
    if options.isData == False :
        topEta = goodtop.Eta()
        isElec = True
        if options.lepType == "muon":
            isElec = False
        toptagSF = getToptagSF(topEta, options.pdfSet, options.pdfSys, isElec)
        if options.toptagSys != None :
            toptagSF *= (1.0 + options.toptagSys) ## scale up/down by 25%
		
        #if options.toptagSys != None :
        #toptagSFerr = getToptagSFerror(topEta)
        #if options.toptagSys > 0 :
        #toptagSF += toptagSFerr
        #else :
        #toptagSF -= toptagSFerr
        weight *= toptagSF
        top_weight *= toptagSF


    h_hadtop_pt6.Fill(goodtop.Perp(), top_weight)
    h_hadtop_mass6.Fill(goodtop.M(), top_weight)
    h_hadtop_y6.Fill(goodtop.Rapidity(), top_weight)
    h_hadtop_eta6.Fill(goodtop.Eta(), top_weight)

    h_mttbarGen6.Fill(mttbarGen, weight)
    h_ht6.Fill(ht, weight)
    h_htLep6.Fill(htLep, weight)
    h_vtxMass6.Fill(bjet_vtxmass, weight)
    h_ptMET6.Fill(met, weight)
    h_phiMET6.Fill(metphi, weight)
    h_ptLep6.Fill(lepton.p4().Perp(), weight)
    h_etaLep6.Fill(lepton.p4().Eta(), weight)
    h_etaAbsLep6.Fill(abs(lepton.p4().Eta()), weight)
    if (goodtop.Perp() < 600.) :
        h_etaAbsLep6_low.Fill(abs(lepton.p4().Eta()), weight)
    if (goodtop.Perp() > 600.) :
        h_etaAbsLep6_high.Fill(abs(lepton.p4().Eta()), weight)
    #h_nJets6.Fill(nJets, weight)
    #h_nBJets6.Fill(nBJets, weight)
    h_nLepJets6.Fill(len(lepJets), weight)
    h_dRvspT6.Fill(lepton.p4().DeltaR(closestFor2D), lepton.p4().Perp(closestFor2D.Vect()), weight)
    
    #if len(lepJets) > 0:
    #    h_pt1LepJet6.Fill(lepJets[0].Perp(), weight)
    #    h_eta1LepJet6.Fill(lepJets[0].Eta(), weight)
    #    h_csv1LepJet6.Fill(lepcsvs[0], weight)
    #    h_vtxMass1LepJet6.Fill(lepVtxMass[0], weight)
    #if len(lepJets) > 1:
    #    h_pt2LepJet6.Fill(lepJets[1].Perp(), weight)
    #    h_eta2LepJet6.Fill(lepJets[1].Eta(), weight)
    #    h_csv2LepJet6.Fill(lepcsvs[1], weight)
    #    h_vtxMass2LepJet6.Fill(lepVtxMass[1], weight)
    
    h_wboson_pt6.Fill(wboson_pt, weight)
    h_wboson_mt6.Fill(wboson_mt, weight)
    
    h_leptop_pt6.Fill(leptop_pt, top_weight)
    h_leptop_y6.Fill(leptop_y, top_weight)
    h_leptop_mass6.Fill(leptop_mass, top_weight)
    
    v2_ttbar = goodtop + v_leptop
    ttbar_mass = v2_ttbar.M()

    h_ttbar_mass6.Fill(ttbar_mass, top_weight)


    ### ------------------------------------------------------------------------------------------------
    ### for unfolding using both top-tagged categories, fill those histograms / response matrix here !!!
    ### ------------------------------------------------------------------------------------------------

    h_ptRecoTop_nobtag.Fill( goodtop.Perp(), top_weight )
    h_ptRecoTop_2step_nobtag.Fill( goodtop.Perp(), top_weight )
    
    if options.makeResponse == True :		
        h_ptRecoTop_passRecoNoBtag.Fill( goodtop.Perp(), top_weight )

        if passParticleLoose:
            h_ptRecoTop_passRecoNoBtagParticleLoose.Fill( goodtop.Perp(), top_weight )
        if passParton:
            h_ptRecoTop_passRecoNoBtagParton.Fill( goodtop.Perp(), top_weight )
            h_ptGenTop_passRecoNoBtagParton.Fill(hadTop.p4.Perp(), top_weight)
        if passParticle:
            h_ptRecoTop_passRecoNoBtagParticle.Fill(goodtop.Perp(), top_weight)
            h_ptPartTop_passRecoNoBtagParticle.Fill(genTops[0].Perp(), top_weight)
        if passParton and passParticle:
            h_ptRecoTop_passRecoNoBtagParticleParton.Fill(goodtop.Perp(), top_weight)
            h_ptPartTop_passRecoNoBtagParticleParton.Fill(genTops[0].Perp(), top_weight)
            
        response_nobtag.Fill(hadJets[itop_mass].Perp(), hadTop.p4.Perp(), top_weight*weight_response)
        if passParticleLoose:
            response_nobtag_rp.Fill(hadJets[itop_mass].Perp(), genTops[0].Perp(), top_weight*weight_response)
        else:
            response_nobtag_rp.Fake(hadJets[itop_mass].Perp(), top_weight*weight_response)
    ### ------------------------------------------------------------------------------------------------

    
    # look at more variables for top-tagged subjets, even though we're not cutting on them at the moment
    event.getByLabel (nsubCA8Label, nsubCA8Handle)
    nsubCA8Jets = nsubCA8Handle.product() 
    event.getByLabel (topTagsj0csvLabel, topTagsj0csvHandle)
    Topsj0BDiscCSV = topTagsj0csvHandle.product() 
    event.getByLabel (topTagsj1csvLabel, topTagsj1csvHandle)
    Topsj1BDiscCSV = topTagsj1csvHandle.product() 
    event.getByLabel (topTagsj2csvLabel, topTagsj2csvHandle)
    Topsj2BDiscCSV = topTagsj2csvHandle.product() 
    event.getByLabel (TopTau2Label, TopTau2Handle)
    Tau2 = TopTau2Handle.product() 
    event.getByLabel (TopTau3Label, TopTau3Handle)
    Tau3 = TopTau3Handle.product() 
    
    # loop over CA8 subjets
    index = -1
    for iCAjet in range(0,len(nsubCA8Jets)):
        CAjetTLV = ROOT.TLorentzVector()
        CAjetTLV.SetPtEtaPhiM( nsubCA8Jets[iCAjet].pt(), nsubCA8Jets[iCAjet].eta(), nsubCA8Jets[iCAjet].phi(), nsubCA8Jets[iCAjet].mass() )
        if (abs(goodtop.DeltaR(CAjetTLV))<0.5):
            index = iCAjet
            break
            
    tau32 = Tau3[index]/Tau2[index]
    
    h_hadtop_precut_tau32.Fill(tau32, top_weight)
    h_hadtop_precut_nvtx_tau32.Fill(nvtx, tau32, top_weight)

    # this is selection beyond our standard selection, only as a check!!
    if tau32 < 0.6:
        subjet_csv = max(Topsj0BDiscCSV[igoodtop],Topsj1BDiscCSV[igoodtop],Topsj2BDiscCSV[igoodtop])
        h_hadtop_precut_csv.Fill(subjet_csv, top_weight)
        h_hadtop_precut_nvtx_csv.Fill(nvtx, subjet_csv, top_weight)
        h_hadtop_pt_tau32.Fill(goodtop.Perp(), top_weight) 
        
        if subjet_csv > options.bDiscCut:
            h_hadtop_pt_csv.Fill(goodtop.Perp(), top_weight) 
    


    # -------------------------------------------------------------------------------------
    # STEP (7): require b-tagging!
    # -------------------------------------------------------------------------------------
    
    
    # -------------------------------------------------------------------------------------
    # check if closest dR jet fulfills b-tagging
    # -------------------------------------------------------------------------------------

    passBtag = False
    btagSF = 1.0

    if bjet_csv > options.bDiscCut and bjet_vtxmass > 0.0:

        passBtag = True
        
        # b-tagging SF 
        if options.isData == False :
            
            ### SF for b-jets and c-jets
            if (abs(bjet_flavor)==5 or abs(bjet_flavor)==4): 
                btagSF = getBtagSF(bjet_pt)
                if options.btagSys != None :
                    btagSFerr = getBtagSFerror(bjet_pt)
                    if (abs(bjet_flavor)==4):
                        btagSFerr *= 2.0 ##for c-jets, use twice the uncertainty
                    if options.btagSys > 0 :
                        btagSF += btagSFerr
                    else :
                        btagSF -= btagSFerr
            ### SF for light-jets
            else:
                if options.btagSys == None :
                    btagSF = getBtagSF_light(bjet_pt,bjet_eta,0)
                else : 
                    btagSF = getBtagSF_light(bjet_pt,bjet_eta,options.btagSys)
    # -------------------------------------------------------------------------------------

    
    # -------------------------------------------------------------------------------------
    # check if leading-pt, leptonic-side jet fulfills b-tagging
    # -------------------------------------------------------------------------------------
    #
    #passBtag_lead = False
    #btagSF_lead = 1.0
    #
    #if bjet_lead_csv > options.bDiscCut and bjet_lead_vtxmass > 0.0:
    #
    #    passBtag_lead = True
    #    
    #    # b-tagging SF 
    #    if options.isData == False :
    #        
    #        ### SF for b-jets and c-jets
    #        if (abs(bjet_lead_flavor)==5 or abs(bjet_lead_flavor)==4): 
    #            btagSF_lead = getBtagSF(bjet_lead_pt)
    #            if options.btagSys != None :
    #                btagSFerr = getBtagSFerror(bjet_lead_pt)
    #                if (abs(bjet_lead_flavor)==4):
    #                    btagSFerr *= 2.0 ##for c-jets, use twice the uncertainty
    #                if options.btagSys > 0 :
    #                    btagSF_lead += btagSFerr
    #                else :
    #                    btagSF_lead -= btagSFerr
    #        ### SF for light-jets
    #        else:
    #            if options.btagSys == None :
    #                btagSF_lead = getBtagSF_light(bjet_lead_pt,bjet_lead_eta,0)
    #            else : 
    #                btagSF_lead = getBtagSF_light(bjet_lead_pt,bjet_lead_eta,options.btagSys)
    # -------------------------------------------------------------------------------------


    # -------------------------------------------------------------------------------------
    # check if any leptonic-side jet fulfills b-tagging
    # -------------------------------------------------------------------------------------
    #
    #passBtag_any = False
    #btagSF_any = 1.0
    #
    ## use any leptonic-side jet for b-tagging, if multiple passes, use leading-pt one (old default)
    #bjet_any_i = -1.      
    #bjet_any_pt = -1.      
    #bjet_any_eta = -99.    
    #bjet_any_flavor = -1.      
    #bjet_any_vtxmass = -1. 
    #
    #for ijet in range(0,len(lepcsvs)) :
    #    lepjet = lepJets[ijet]
    #    lep_csv = lepcsvs[ijet]
    #    lep_vtxmass = lepVtxMass[ijet]
    #    lep_flavor = lepflavors[ijet]
    #    if lep_csv > options.bDiscCut and lep_vtxmass > 0.0:
    #
    #        passBtag_any = True
    #        
    #        if (lepjet.Perp() > bjet_any_pt):
    #            bjet_any_pt = lepjet.Perp()
    #            bjet_any_eta = lepjet.Eta()
    #            bjet_any_vtxmass = lep_vtxmass
    #            bjet_any_i = ijet
    #            
    #            if abs(lep_flavor) == 5:
    #                bjet_any_flavor = 5
    #            elif abs(lep_flavor) == 4:
    #                bjet_any_flavor = 4
    #            else:
    #                bjet_any_flavor = 1
    #        
    #    # get jet's contribution to b-tagging SF 
    #    if options.isData == False :
    #
    #        jet_btagSF = 1.0
    #        
    #        ### SF for b-jets and c-jets
    #        if (abs(lep_flavor)==5 or abs(lep_flavor)==4): 
    #            jet_btagSF = getBtagSF(lepjet.Perp())
    #            if options.btagSys != None :
    #                jet_btagSFerr = getBtagSFerror(lepjet.Perp())
    #                if (abs(lep_flavor)==4):
    #                    jet_btagSFerr *= 2.0 ##for c-jets, use twice the uncertainty
    #                if options.btagSys > 0 :
    #                    jet_btagSF += jet_btagSFerr
    #                else :
    #                    jet_btagSF -= jet_btagSFerr
    #        ### SF for light-jets
    #        else:
    #            if options.btagSys == None :
    #                jet_btagSF = getBtagSF_light(lepjet.Perp(),lepjet.Eta(),0)
    #            else : 
    #                jet_btagSF = getBtagSF_light(lepjet.Perp(),lepjet.Eta(),options.btagSys)
    #
    #
    #        ### a tagged jets enters just through SF...
    #        if lep_csv > options.bDiscCut:
    #            btagSF_any *= jet_btagSF
    #        ### ...while a non-tagged jet need the MC tagging efficiency as well
    #        else: 
    #            effMC = getBtagEff(lepjet.Perp(), lepjet.Eta(), lep_flavor)
    #            btagSF_any *= ((1.0 - jet_btagSF*effMC)/(1.0 - effMC))
    # -------------------------------------------------------------------------------------


    
    # apply b-tagging SF
    weight *= btagSF
    top_weight *= btagSF

    
    # require a b-tagged jet (using closest jet as b-tag candidate!)
    if passBtag == False:
        if options.makeResponse == True:
            response.Miss( hadTop.p4.Perp(), weight*weight_response )
            if passParticleLoose:
                response_rp.Miss( genTops[0].Perp(), weight*weight_response )
        continue

    if options.debug :
        print 'Have a leptonic-side b-tagged AK5 jet'
    if options.debug :
        print 'Passed stage7'
    cutflow['Stage 7: '] += 1
    npassed += 1

    
    goodEvents.append( [ event.object().id().run(), event.object().id().luminosityBlock(), event.object().id().event() ] )

    
    h_mttbarGen7.Fill(mttbarGen, weight)
    h_wboson_pt7.Fill(wboson_pt, weight)
    h_wboson_mt7.Fill(wboson_mt, weight)
    
    #h_pt1LepJet7.Fill(lepJets[0].Perp(), weight)
    #h_eta1LepJet7.Fill(lepJets[0].Eta(), weight)
    #h_csv1LepJet7.Fill(lepcsvs[0], weight)
    #h_vtxMass1LepJet7.Fill(lepVtxMass[0], weight)
    h_ptLep7.Fill(lepton.p4().Perp(), weight)
    h_etaLep7.Fill(lepton.p4().Eta(), weight)
    h_etaAbsLep7.Fill(abs(lepton.p4().Eta()), weight)
    if (goodtop.Perp() < 600.) :
        h_etaAbsLep7_low.Fill(abs(lepton.p4().Eta()), weight)
    if (goodtop.Perp() > 600.) :
        h_etaAbsLep7_high.Fill(abs(lepton.p4().Eta()), weight)

    h_dRvspT7.Fill(lepton.p4().DeltaR(closestFor2D), lepton.p4().Perp(closestFor2D.Vect()), weight)
    
    #if len(lepJets) > 1:
    #    h_pt2LepJet7.Fill(lepJets[1].Perp(), weight)
    #    h_eta2LepJet7.Fill(lepJets[1].Eta(), weight)
    #    h_csv2LepJet7.Fill(lepcsvs[1], weight)
    #    h_vtxMass2LepJet7.Fill(lepVtxMass[1], weight)
        
    h_ptBJet7.Fill(bjet_pt, weight)
    h_etaBJet7.Fill(bjet_eta, weight)
    h_vtxMass7.Fill(bjet_vtxmass, weight)
    if (goodtop.Perp() < 600.) :
        h_vtxMass7_low.Fill(bjet_vtxmass, weight)
    if (goodtop.Perp() > 600.) :
        h_vtxMass7_high.Fill(bjet_vtxmass, weight)
    h_flavorBJet7.Fill(bjet_flavor, weight)
                
    h_ht7.Fill(ht, weight)
    h_htLep7.Fill(htLep, weight)
    h_ptMET7.Fill(met, weight)
    h_phiMET7.Fill(metphi, weight)
    
    h_leptop_pt7.Fill(leptop_pt, top_weight)
    h_leptop_y7.Fill(leptop_y, top_weight)
    h_leptop_mass7.Fill(leptop_mass, top_weight)
    
    h_hadtop_pt7.Fill(goodtop.Perp(), top_weight)
    h_hadtop_mass7.Fill(goodtop.M(), top_weight)
    h_hadtop_y7.Fill(goodtop.Rapidity(), top_weight)
    h_hadtop_eta7.Fill(goodtop.Eta(), top_weight)

    h_ttbar_mass7.Fill(ttbar_mass, top_weight)

        
    # -------------------------------------------------------------------------------------
    # fill histograms for average scale factors
    # -------------------------------------------------------------------------------------

    if options.isData == False :
        h_muonSF.Fill(1.0,muonSF*weight)
        h_btagSF.Fill(1.0,btagSF*weight)
        h_toptagSF.Fill(1.0,toptagSF*weight)

    
    # -------------------------------------------------------------------------------------
    # finally fill response matrix if doing unfolding
    # -------------------------------------------------------------------------------------

    h_ptRecoTop.Fill( goodtop.Perp(), top_weight )
    h_ptRecoTop_2step.Fill( goodtop.Perp(), top_weight )
    
    if options.makeResponse == True :		
        h_ptRecoTop_passReco.Fill( goodtop.Perp(), top_weight )

        if passParticleLoose:
            h_ptRecoTop_passRecoParticleLoose.Fill( goodtop.Perp(), top_weight )
        if passParton:
            h_ptRecoTop_passRecoParton.Fill( goodtop.Perp(), top_weight )
            h_ptGenTop_passRecoParton.Fill(hadTop.p4.Perp(), top_weight)
        if passParticle:
            h_ptRecoTop_passRecoParticle.Fill(goodtop.Perp(), top_weight)
            h_ptPartTop_passRecoParticle.Fill(genTops[0].Perp(), top_weight)
        if passParton and passParticle:
            h_ptRecoTop_passRecoParticleParton.Fill(goodtop.Perp(), top_weight)
            h_ptPartTop_passRecoParticleParton.Fill(genTops[0].Perp(), top_weight)
        
        response.Fill(hadJets[itop_mass].Perp(), hadTop.p4.Perp(), top_weight*weight_response)
        if passParticleLoose:
            response_rp.Fill(hadJets[itop_mass].Perp(), genTops[0].Perp(), top_weight*weight_response)
        else:
            response_rp.Fake(hadJets[itop_mass].Perp(), top_weight*weight_response)    


 
# -------------------------------------------------------------------------------------
# END OF LOOPING OVER EVENTS!!!
# -------------------------------------------------------------------------------------

for stage, count in sorted(cutflow.iteritems()) :
    print '{0} {1:15.0f}'.format( stage, count )

print  'Total Events: ' + str(ntotal)
print  'Passed      : ' + str(npassed)
f.cd()

if options.makeResponse == True :
    response.Write()
    response_nobtag.Write()

    response_pp.Write()
    response_rp.Write()
    response_nobtag_rp.Write()

f.Write()
f.Close()

# if printing to file all the events that pass selection
if options.printEvents :
    outtxt = open(name + "_events.txt", "w")
    sys.stdout = outtxt
    for goodEvent in goodEvents :
        print '{0:12.0f}:{1:12.0f}:{2:12.0f}'.format(goodEvent[0], goodEvent[1], goodEvent[2])


print "Total time = " + str( time.time() - start_time) + " seconds"


