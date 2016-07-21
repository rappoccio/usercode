#!/usr/bin/env python

import math

# -------------------------------------------------------------------------------------
# Script for doing RooUnfold on the ttbar differential cross secion
# -------------------------------------------------------------------------------------

from optparse import OptionParser
parser = OptionParser()


# -------------------------------------------------------------------------------------
# input options
# -------------------------------------------------------------------------------------

parser.add_option('--closureTest', metavar='F', action='store_true',
                  default=False,
                  dest='closureTest',
                  help='Run closure test')

parser.add_option('--whatClosure', metavar='F', type='string', action='store',
                  default='nom',
                  dest='whatClosure',
                  help='What type of closure test? Options: reverse, data, nom, full')

parser.add_option('--normalize', metavar='F', action='store_true',
                  default=False,
                  dest='normalize',
                  help='Do normalized differential cross section')

parser.add_option('--twoStep', metavar='F', action='store_true',
                  default=False,
                  dest='twoStep',
                  help='Do reco-particle and particle-parton unfolding')

parser.add_option('--systVariation', metavar='F', type='string', action='store',
                  default='nom',
                  dest='syst',
                  help='Run nominal or systematic variation?')

parser.add_option('--bkgSyst', metavar='F', type='string', action='store',
                  default='nom',
                  dest='bkgSyst',
                  help='Run nominal or systematic variation for backgrounds (nom or bkgup / bkgdn) ?')

parser.add_option('--ttbarPDF', metavar='F', type='string', action='store',
                  default='CT10_nom',
                  dest='pdf',
                  help='Which PDF set and nominal vs up/down? Or Q2 up/down?')

parser.add_option('--addNoBtag', metavar='F', action='store_true',
                  default=False,
                  dest='addNoBtag',
                  help='Unfold only using category \"1 top-tag, 1 b-tag\" (default) or adding \"1 top-tag, 0 b-tag\" (use --addNoBtag)')

parser.add_option('--lepType', metavar='F', type='string', action='store',
                  default='muon',
                  dest='lepType',
                  help='Lepton type (ele or muon)')

parser.add_option('--troubleshoot', metavar='F', action='store_true',
                  default=False,
                  dest='troubleshoot',
                  help='Make troubleshooting plots')

parser.add_option('--toUnfold', metavar='F', type='string', action='store',
                  default='pt',
                  dest='toUnfold',
                  help='Which distribution (pt or y) to unfold?')

parser.add_option('--useGenWeights', metavar='F', action='store_true',
                  default=True,
                  dest='useGenWeights',
                  help='Use generator weights for MC@NLO')



# -------------------------------------------------------------------------------------
# load options & set plot style
# -------------------------------------------------------------------------------------

(options, args) = parser.parse_args()
argv = []

import sys

nobtag = ""
if options.addNoBtag == True:
    nobtag = "_nobtag"

    
from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor
from array import array

gROOT.Macro("rootlogon.C")
gROOT.SetBatch(True)

gStyle.SetOptStat(000000)
gStyle.SetOptTitle(0);

gStyle.SetTitleFont(43)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")

gStyle.SetPadTopMargin(0.07);
gStyle.SetPadRightMargin(0.05);
gStyle.SetPadBottomMargin(0.16);
gStyle.SetPadLeftMargin(0.18);
  
#gSystem.Load("RooUnfold-1.1.1/libRooUnfold.so")
gSystem.Load("RooUnfold/libRooUnfold.so")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd

  
# -------------------------------------------------------------------------------------
# cross sections, efficiencies, total number of events
# -------------------------------------------------------------------------------------

# luminosity
lum = 19.7 #fb-1

# cross sections
sigma_ttbar = [ 
    [252.89*1000., 252.89*1000., 252.89*1000.],  # nominal (m<700, 700-1000, 1000-inf)
    [(252.89+6.39)*1000., (252.89+6.39)*1000., (252.89+6.39)*1000.],  # Q2 up
    [(252.89-8.64)*1000., (252.89-8.64)*1000., (252.89-8.64)*1000.]   # Q2 down
    ]
eff_ttbar = [ 
    [1.0, 0.074, 0.015],  # nominal
    [1.0, 0.074, 0.014],  # Q2 up
    [1.0, 0.081, 0.016]   # Q2 down
    ]
Nmc_ttbar = [
    [21675970., 3082812., 1249111.],  # nominal
    [14983686., 2243672., 1241650.],  # Q2 up
    [14545715*89./102., 2170074., 1308090.]    # Q2 down
    ]

if options.pdf == "scaleup" :
    ipdf = 1
elif options.pdf == "scaledown" :
    ipdf = 2
else:
    ipdf = 0


sigma_T_t = 56.4 * 1000.       # 
sigma_Tbar_t = 30.7 * 1000.    # All single-top approx NNLO cross sections from
sigma_T_s = 3.79 * 1000.       # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
sigma_Tbar_s = 1.76 * 1000.    # 
sigma_T_tW = 11.1 * 1000.      # 
sigma_Tbar_tW = 11.1 * 1000.   # 
sigma_WJets = 36703.2 * 1000.  # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
sigma_WJets_1jet = 5400*1.207*1000. #
sigma_WJets_2jet = 1750*1.207*1000. #
sigma_WJets_3jet = 519 *1.207*1000. #
sigma_WJets_4jet = 214 *1.207*1000. #

# MC event counts from B2G twiki here :
# https://twiki.cern.ch/twiki/bin/view/CMS/B2GTopLikeBSM53X#Backgrounds
Nmc_T_t = 3758227
Nmc_Tbar_t = 1935072
Nmc_T_s = 259961
Nmc_Tbar_s = 139974
Nmc_T_tW = 497658
Nmc_Tbar_tW = 493460
Nmc_WJets = 57709905
Nmc_WJets_1jet = 23141598
Nmc_WJets_2jet = 34044921
Nmc_WJets_3jet = 15539503
Nmc_WJets_4jet = 13382803


## hack to account for that when doing closure test (unfold 1/2 sample with other 1/2), the ttbar sample is split in two 
eff_closure = 1.0
if options.closureTest == True and options.whatClosure == "nom" and options.pdf != "MG" and options.pdf != "mcnlo":
    eff_closure = 2.0


# -------------------------------------------------------------------------------------
# Scaling of the various backgrounds from the theta fit
# *** these are using the combined fit result ***
# -------------------------------------------------------------------------------------

## background counts: 1toptag+1btag (nom, up, dn), 1toptag+>=0btag (nom, up, dn))
i_bkgnorm = 0
if nobtag == "" and options.bkgSyst == "bkgup": 
    i_bkgnorm = 1
elif nobtag == "" and options.bkgSyst == "bkgdn": 
    i_bkgnorm = 2
elif nobtag == "": 
    i_bkgnorm = 0
elif options.bkgSyst == "bkgup": 
    i_bkgnorm = 4
elif options.bkgSyst == "bkgdn": 
    i_bkgnorm = 5
else:
    i_bkgnorm = 3
    
    
## muon channel
if options.lepType == "muon" :   #unfold
    n_ttbarnonsemilep = [29.7176, 31.95, 27.4852, 74.4024, 79.9916, 68.8133]   #unfold
    n_wjets           = [3.90922, 4.17621, 3.64223, 157.76, 168.534, 146.985]   #unfold
    n_singletop       = [4.07011, 5.93787, 2.20234, 18.502, 26.9925, 10.0115]   #unfold
    n_qcd             = [7.61582, 11.1999, 4.0317, 21.0118, 30.9003, 11.1233]   #unfold
    
## electron channel
if options.lepType == "ele" :   #unfold
    n_ttbarnonsemilep = [30.1172, 32.3796, 27.8548, 69.9322, 75.1855, 64.6789]   #unfold
    n_wjets           = [2.74315, 2.9305, 2.5558, 132.34, 141.378, 123.301]   #unfold
    n_singletop       = [3.16264, 4.61396, 1.71131, 14.7989, 21.5902, 8.00773]   #unfold
    n_qcd             = [10.4814, 12.2568, 8.70593, 78.0737, 91.2986, 64.8488]   #unfold


## extract relevant background normalizations
fitted_qcd = n_qcd[i_bkgnorm]
fitted_singletop = n_singletop[i_bkgnorm]
fitted_wjets = n_wjets[i_bkgnorm]
fitted_ttbarnonsemilep = n_ttbarnonsemilep[i_bkgnorm]


# -------------------------------------------------------------------------------------
#  read histogram files
# -------------------------------------------------------------------------------------

DIR = ""
ttDIR = "2Dhists"
dataDIR = "2Dhist"
muOrEl = "mu"
if options.lepType=="ele":
    print ""
    print "UNFOLDING FOR ELECTRON CHANNEL !!!" 
    print ""
    DIR = "_el"
    ttDIR = "qcd_el"
    dataDIR = "qcd_el"
    muOrEl = "el"
else:
    print ""
    print "UNFOLDING FOR MUON CHANNEL !!!" 
    print ""
    
if options.lepType=="ele":
    f_data = TFile("histfiles/"+dataDIR+"/SingleEl_iheartNY_V1_el_Run2012_2Dcut_nom.root")
    f_QCD  = TFile("histfiles/"+dataDIR+"/SingleEl_iheartNY_V1_el_Run2012_2Dcut_qcd.root")
else:
    f_data = TFile("histfiles/"+dataDIR+"/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root")
    f_QCD  = TFile("histfiles/"+dataDIR+"/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root")


### use histograms which have the posterior top-tagging SF applied! 
usePost = True
postname = ""
if options.closureTest == True: 
    usePost = False
if usePost: 
    ttDIR = "postfit_combfit"
    postname = "postfit_"

# In the below, file named f_..._odd will be the one from which response matrix is extracted from (if closureTest == True) 

## reverse:  unfold Powheg ttbar sample using MadGraph response matrix as closure test
if options.pdf == "MG" and options.closureTest == True and options.whatClosure == "reverse":
    f_ttbar_max700    = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_700to1000 = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_1000toInf = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_max700_odd = TFile("histfiles_MG/TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
## unfold MadGraph ttbar sample using Powheg response matrix as closure test
elif options.pdf == "MG" and options.closureTest == True :
    f_ttbar_max700 = TFile("histfiles_MG/TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
    f_ttbar_max700_odd    = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_700to1000_odd = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_1000toInf_odd = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
## MadGraph
elif options.pdf == "MG":
    f_ttbar_max700 = TFile("histfiles_MG/TTJets_SemiLeptMGDecays_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
## reverse:  unfold Powheg ttbar sample using MC@NLO response matrix
elif options.pdf == "mcnlo" and options.closureTest == True and options.whatClosure == "reverse":
    f_ttbar_max700    = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_700to1000 = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_1000toInf = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    if options.useGenWeights:
        f_ttbar_max700_odd = TFile("histfiles_mcnlo_weight/TT_mcatnlo_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
    else:
        f_ttbar_max700_odd = TFile("histfiles_mcnlo/TT_mcatnlo_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
## unfold MC@NLO ttbar sample using Powheg response matrix
elif options.pdf == "mcnlo" and options.closureTest == True :
    if options.useGenWeights:
        f_ttbar_max700 = TFile("histfiles_mcnlo_weight/TT_mcatnlo_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
    else:
        f_ttbar_max700 = TFile("histfiles_mcnlo/TT_mcatnlo_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
    f_ttbar_max700_odd    = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_700to1000_odd = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_1000toInf_odd = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
## MC@NLO
elif options.pdf == "mcnlo":
    if options.useGenWeights:
        f_ttbar_max700 = TFile("histfiles_mcnlo_weight/TT_mcatnlo_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
    else:
        f_ttbar_max700 = TFile("histfiles_mcnlo/TT_mcatnlo_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
## regular closure test, unfolding 1/2 sample (even) using other 1/2 (odd)
elif options.closureTest == True and options.whatClosure == "nom" : 
    if options.lepType=="ele":
        ttDIR = "qcd_el"
    else :
        ttDIR = "2Dhists"
    f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_max700_odd    = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    f_ttbar_700to1000_odd = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    f_ttbar_1000toInf_odd = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
## unfold data using some ttbar variation
else :
    f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+postname+options.syst+".root")
    f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+postname+options.syst+".root")
    f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+postname+options.syst+".root")

if options.pdf == "MG" or options.pdf == "mcnlo":
    f_ttbar_nonsemilep_max700    = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_nonsemilep_700to1000 = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_nonsemilep_1000toInf = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
else:
    f_ttbar_nonsemilep_max700    = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+postname+options.syst+".root")
    f_ttbar_nonsemilep_700to1000 = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+postname+options.syst+".root")
    f_ttbar_nonsemilep_1000toInf = TFile("histfiles_"+options.pdf+"/"+ttDIR+"/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_"+options.pdf+"_2Dcut_"+postname+options.syst+".root")

f_T_t     = TFile("histfiles/"+dataDIR+"/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_t  = TFile("histfiles/"+dataDIR+"/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_T_s     = TFile("histfiles/"+dataDIR+"/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_s  = TFile("histfiles/"+dataDIR+"/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_T_tW    = TFile("histfiles/"+dataDIR+"/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_Tbar_tW = TFile("histfiles/"+dataDIR+"/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")

f_WJets_1jet   = TFile("histfiles/"+dataDIR+"/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_2jet   = TFile("histfiles/"+dataDIR+"/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_3jet   = TFile("histfiles/"+dataDIR+"/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")
f_WJets_4jet   = TFile("histfiles/"+dataDIR+"/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_"+muOrEl+"_2Dcut_nom.root")

# the response matrices are simply added here, but have been filled with the full event weights (taking sample size, efficiency, etx. into account)
if (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and options.whatClosure=="reverse": 
    ## reverse = unfold Powheg using MC@NLO/MadGraph response matrix
    response_ttbar_max700    = f_ttbar_max700_odd.Get("response_"+options.toUnfold+nobtag)
    response = response_ttbar_max700.Clone()
    response.SetName("response_"+options.toUnfold+"_"+options.syst)
elif options.closureTest == True and options.whatClosure=="nom":
    ## regular closure test, unfolding some distribution using Powheg as response mastrix 
    response_ttbar_max700    = f_ttbar_max700_odd.Get("response_"+options.toUnfold+nobtag)
    response_ttbar_700to1000 = f_ttbar_700to1000_odd.Get("response_"+options.toUnfold+nobtag)
    response_ttbar_1000toInf = f_ttbar_1000toInf_odd.Get("response_"+options.toUnfold+nobtag)
    response = response_ttbar_max700.Clone()
    response.SetName("response_"+options.toUnfold+options.syst)
    response.Add(response_ttbar_700to1000)
    response.Add(response_ttbar_1000toInf)

    if options.troubleshoot :
        response_ttbar_max700_even    = f_ttbar_max700.Get("response_"+options.toUnfold+nobtag)
        response_ttbar_700to1000_even = f_ttbar_700to1000.Get("response_"+options.toUnfold+nobtag)
        response_ttbar_1000toInf_even = f_ttbar_1000toInf.Get("response_"+options.toUnfold+nobtag)
        response_even = response_ttbar_max700_even.Clone()
        response_even.SetName("response_even_"+options.toUnfold+options.syst)
        response_even.Add(response_ttbar_700to1000_even)
        response_even.Add(response_ttbar_1000toInf_even)

elif (options.pdf == "MG" or options.pdf == "mcnlo") and (options.closureTest == False or options.whatClosure == "full"): 
    response_ttbar_max700 = f_ttbar_max700.Get("response_"+options.toUnfold+nobtag)
    response = response_ttbar_max700.Clone()
    response.SetName("response_"+options.toUnfold+"_"+options.syst)
else :
    response_ttbar_max700    = f_ttbar_max700.Get("response_"+options.toUnfold+nobtag)
    response_ttbar_700to1000 = f_ttbar_700to1000.Get("response_"+options.toUnfold+nobtag)
    response_ttbar_1000toInf = f_ttbar_1000toInf.Get("response_"+options.toUnfold+nobtag)
    response = response_ttbar_max700.Clone()
    response.SetName("response_"+options.toUnfold+"_"+options.syst)
    response.Add(response_ttbar_700to1000)
    response.Add(response_ttbar_1000toInf)


## response matrices for two-step unfolding
if options.twoStep == True :
    if (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and options.whatClosure=="reverse":
        response_ttbar_max700_rp = f_ttbar_max700_odd.Get("response_"+options.toUnfold+nobtag+"_rp")
        response_ttbar_max700_pp = f_ttbar_max700_odd.Get("response_"+options.toUnfold+"_pp")
        
        response_rp = response_ttbar_max700_rp.Clone()
        response_rp.SetName("response_"+options.toUnfold+"_"+options.syst+"_rp")
        response_pp = response_ttbar_max700_pp.Clone()
        response_pp.SetName("response_"+options.toUnfold+"_"+options.syst+"_pp")
    
    elif options.closureTest == True and options.whatClosure=="nom": 
        response_ttbar_max700_rp    = f_ttbar_max700_odd.Get("response_"+options.toUnfold+nobtag+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000_odd.Get("response_"+options.toUnfold+nobtag+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf_odd.Get("response_"+options.toUnfold+nobtag+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700_odd.Get("response_"+options.toUnfold+"_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000_odd.Get("response_"+options.toUnfold+"_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf_odd.Get("response_"+options.toUnfold+"_pp")

        response_rp = response_ttbar_max700_rp.Clone()
        response_rp.SetName("response_"+options.toUnfold+"_"+options.syst+"_rp")
        response_rp.Add(response_ttbar_700to1000_rp)
        response_rp.Add(response_ttbar_1000toInf_rp)
        response_pp = response_ttbar_max700_pp.Clone()
        response_pp.SetName("response_"+options.toUnfold+"_"+options.syst+"_pp")
        response_pp.Add(response_ttbar_700to1000_pp)
        response_pp.Add(response_ttbar_1000toInf_pp)

        if options.troubleshoot == True:
            response_ttbar_max700_rp_even    = f_ttbar_max700.Get("response_"+options.toUnfold+nobtag+"_rp")
            response_ttbar_700to1000_rp_even = f_ttbar_700to1000.Get("response_"+options.toUnfold+nobtag+"_rp")
            response_ttbar_1000toInf_rp_even = f_ttbar_1000toInf.Get("response_"+options.toUnfold+nobtag+"_rp")
            response_ttbar_max700_pp_even    = f_ttbar_max700.Get("response_"+options.toUnfold+"_pp")
            response_ttbar_700to1000_pp_even = f_ttbar_700to1000.Get("response_"+options.toUnfold+"_pp")
            response_ttbar_1000toInf_pp_even = f_ttbar_1000toInf.Get("response_"+options.toUnfold+"_pp")

            response_rp_even = response_ttbar_max700_rp_even.Clone()
            response_rp_even.SetName("response_"+options.toUnfold+"_"+options.syst+"_rp_even")
            response_rp_even.Add(response_ttbar_700to1000_rp_even)
            response_rp_even.Add(response_ttbar_1000toInf_rp_even)
            
            response_pp_even = response_ttbar_max700_pp_even.Clone()
            response_pp_even.SetName("response_"+options.toUnfold+"_"+options.syst+"_pp_even")
            response_pp_even.Add(response_ttbar_700to1000_pp_even)
            response_pp_even.Add(response_ttbar_1000toInf_pp_even)

    
    elif (options.pdf == "MG" or options.pdf == "mcnlo") and (options.closureTest == False or options.whatClosure=="full"):
        response_ttbar_max700_rp = f_ttbar_max700.Get("response_"+options.toUnfold+nobtag+"_rp")
        response_ttbar_max700_pp = f_ttbar_max700.Get("response_"+options.toUnfold+"_pp")
        
        response_rp = response_ttbar_max700_rp.Clone()
        response_rp.SetName("response_"+options.toUnfold+"_"+options.syst+"_rp")
        response_pp = response_ttbar_max700_pp.Clone()
        response_pp.SetName("response_"+options.toUnfold+"_"+options.syst+"_pp")
    
    else:
        response_ttbar_max700_rp    = f_ttbar_max700.Get("response_"+options.toUnfold+nobtag+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000.Get("response_"+options.toUnfold+nobtag+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf.Get("response_"+options.toUnfold+nobtag+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700.Get("response_"+options.toUnfold+"_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000.Get("response_"+options.toUnfold+"_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf.Get("response_"+options.toUnfold+"_pp")

        response_rp = response_ttbar_max700_rp.Clone()
        response_rp.SetName("response_"+options.toUnfold+"_"+options.syst+"_rp")
        response_rp.Add(response_ttbar_700to1000_rp)
        response_rp.Add(response_ttbar_1000toInf_rp)
        response_pp = response_ttbar_max700_pp.Clone()
        response_pp.SetName("response_"+options.toUnfold+"_"+options.syst+"_pp")
        response_pp.Add(response_ttbar_700to1000_pp)
        response_pp.Add(response_ttbar_1000toInf_pp)

TH1.AddDirectory(0)

# -------------------------------------------------------------------------------------
# output file for storing histograms to  
# -------------------------------------------------------------------------------------

bkgout = ""
if options.bkgSyst == "bkgup" or options.bkgSyst == "bkgdn":
    bkgout = "_"+options.bkgSyst
closureout = ""
if options.closureTest == True: 
    closureout = "_closure_" + options.whatClosure
norm_flag = ""
if options.normalize:
    norm_flag = "_norm"

append1 = "_"+options.toUnfold
if options.twoStep :
    append1 += "_2step"    

if options.twoStep :
    fout = TFile("UnfoldingPlots/unfold"+DIR+"_2step_"+options.toUnfold+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+closureout+norm_flag+".root","recreate");
else :
    fout = TFile("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+closureout+norm_flag+".root","recreate");


# -------------------------------------------------------------------------------------
# read actual histograms
# -------------------------------------------------------------------------------------

if (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and (options.whatClosure=="nom" or options.whatClosure=="full"):
    # use truth-level distributions (and reco-level) from MC@NLO/MadGraph
    hTrue_max700    = f_ttbar_max700.Get(options.toUnfold+"GenTop")  
    hTrue_max700.Sumw2()
    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get(options.toUnfold+"PartTop")
        hPart_max700.Sumw2()
elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == False:
    hTrue_max700    = f_ttbar_max700.Get(options.toUnfold+"GenTop")  
    hTrue_max700.Sumw2()
    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get(options.toUnfold+"PartTop")
        hPart_max700.Sumw2()
else :
    hTrue_max700    = f_ttbar_max700.Get(options.toUnfold+"GenTop")
    hTrue_700to1000 = f_ttbar_700to1000.Get(options.toUnfold+"GenTop")
    hTrue_1000toInf = f_ttbar_1000toInf.Get(options.toUnfold+"GenTop")
    hTrue_max700.Sumw2()
    hTrue_700to1000.Sumw2()
    hTrue_1000toInf.Sumw2()

    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get(options.toUnfold+"PartTop")
        hPart_700to1000 = f_ttbar_700to1000.Get(options.toUnfold+"PartTop")
        hPart_1000toInf = f_ttbar_1000toInf.Get(options.toUnfold+"PartTop")
        hPart_max700.Sumw2()
        hPart_700to1000.Sumw2()
        hPart_1000toInf.Sumw2()

    if options.troubleshoot and  options.closureTest == True and options.whatClosure=="nom":
        hTrue_max700_odd    = f_ttbar_max700_odd.Get(options.toUnfold+"GenTop")
        hTrue_700to1000_odd = f_ttbar_700to1000_odd.Get(options.toUnfold+"GenTop")
        hTrue_1000toInf_odd = f_ttbar_1000toInf_odd.Get(options.toUnfold+"GenTop")
        hTrue_max700_odd.Sumw2()
        hTrue_700to1000_odd.Sumw2()
        hTrue_1000toInf_odd.Sumw2()

        if options.twoStep :
            hPart_max700_odd    = f_ttbar_max700_odd.Get(options.toUnfold+"PartTop")
            hPart_700to1000_odd = f_ttbar_700to1000_odd.Get(options.toUnfold+"PartTop")
            hPart_1000toInf_odd = f_ttbar_1000toInf_odd.Get(options.toUnfold+"PartTop")
            hPart_max700_odd.Sumw2()
            hPart_700to1000_odd.Sumw2()
            hPart_1000toInf_odd.Sumw2()

isTwoStep = ""
if options.twoStep:
    isTwoStep = "_2step"

hRecoQCD = f_QCD.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag).Clone()
hRecoQCD.SetName("hRecoQCD")
hRecoQCD.Sumw2()
hRecoQCD.SetFillColor(TColor.kYellow)

if options.closureTest == False: 
    hMeas = f_data.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
elif options.closureTest == True and options.whatClosure == "data": 
    # data distribution
    hMeas = f_data.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    # ttbar prediction to scale data
    hMeas_max700    = f_ttbar_max700.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_700to1000 = f_ttbar_700to1000.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_1000toInf = f_ttbar_1000toInf.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_max700.Sumw2()
    hMeas_700to1000.Sumw2()
    hMeas_1000toInf.Sumw2()
elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and (options.whatClosure=="nom" or options.whatClosure=="full"):
    # use truth-level distributions (and reco-level) from MC@NLO/MadGraph
    hMeas_max700    = f_ttbar_max700.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_max700.Sumw2()
else :
    hMeas_max700    = f_ttbar_max700.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_700to1000 = f_ttbar_700to1000.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_1000toInf = f_ttbar_1000toInf.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_max700.Sumw2()
    hMeas_700to1000.Sumw2()
    hMeas_1000toInf.Sumw2()

if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
    hMeas_max700_odd    = f_ttbar_max700_odd.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_700to1000_odd = f_ttbar_700to1000_odd.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_1000toInf_odd = f_ttbar_1000toInf_odd.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
    hMeas_max700_odd.Sumw2()
    hMeas_700to1000_odd.Sumw2()
    hMeas_1000toInf_odd.Sumw2()

hMeas_T_t     = f_T_t.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_Tbar_t  = f_Tbar_t.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_T_s     = f_T_s.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_Tbar_s  = f_Tbar_s.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_T_tW    = f_T_tW.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_Tbar_tW = f_Tbar_tW.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_WJets_1jet   = f_WJets_1jet.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_WJets_2jet   = f_WJets_2jet.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_WJets_3jet   = f_WJets_3jet.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_WJets_4jet   = f_WJets_4jet.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_tt0_nonsemi = f_ttbar_nonsemilep_max700.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_tt700_nonsemi = f_ttbar_nonsemilep_700to1000.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)
hMeas_tt1000_nonsemi = f_ttbar_nonsemilep_1000toInf.Get(options.toUnfold+"RecoTop"+isTwoStep+nobtag)

hMeas_T_t.Sumw2()
hMeas_Tbar_t.Sumw2()
hMeas_T_s.Sumw2()
hMeas_Tbar_s.Sumw2()
hMeas_T_tW.Sumw2()
hMeas_Tbar_tW.Sumw2()
hMeas_WJets_1jet.Sumw2()
hMeas_WJets_2jet.Sumw2()
hMeas_WJets_3jet.Sumw2()
hMeas_WJets_4jet.Sumw2()
hMeas_tt0_nonsemi.Sumw2()
hMeas_tt700_nonsemi.Sumw2()
hMeas_tt1000_nonsemi.Sumw2()

# -------------------------------------------------------------------------------------
# Normalize histograms
# -------------------------------------------------------------------------------------

### normalize measured "data" for closure tests
# MC@NLO/MadGraph
if options.pdf == "MG" and options.closureTest == True and (options.whatClosure=="nom" or options.whatClosure=="full"):
    hMeas_max700.Scale(252.89*1000.0*19.7/25424818.*0.438)
    hMeas = hMeas_max700.Clone()
    hMeas.SetName(options.toUnfold+"RecoTop_measured")
elif options.pdf == "mcnlo" and options.closureTest == True and (options.whatClosure=="nom" or options.whatClosure=="full"):
    if options.useGenWeights:
        hMeas_max700.Scale(252.89*1000.0*19.7/(32852589.*16777215./32575024.))
    else:
        hMeas_max700.Scale(252.89*1000.0*19.7/32852589)
    hMeas = hMeas_max700.Clone()
    hMeas.SetName(options.toUnfold+"RecoTop_measured")
# ttbar nominal as "measured" distribution
elif options.closureTest == True and options.whatClosure != "data": 
    hMeas_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hMeas_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hMeas_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hMeas = hMeas_max700.Clone()
    hMeas.SetName(options.toUnfold+"RecoTop_measured")
    hMeas.Add(hMeas_700to1000)
    hMeas.Add(hMeas_1000toInf)    

    if options.troubleshoot and options.whatClosure == "nom":
        hMeas_max700_odd.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
        hMeas_700to1000_odd.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
        hMeas_1000toInf_odd.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
        hMeas_odd = hMeas_max700_odd.Clone()
        hMeas_odd.SetName(options.toUnfold+"RecoTop_measured_odd")
        hMeas_odd.Add(hMeas_700to1000_odd)
        hMeas_odd.Add(hMeas_1000toInf_odd)    

# for closure test of data, need ttbar
elif options.closureTest == True and options.whatClosure == "data": 
    hMeas_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hMeas_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hMeas_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hMeasTT = hMeas_max700.Clone()
    hMeasTT.SetName(options.toUnfold+"RecoTop_TT")
    hMeasTT.Add(hMeas_700to1000)
    hMeasTT.Add(hMeas_1000toInf)
        
    
if options.pdf == "MG" and ((options.closureTest == True and (options.whatClosure=="nom" or options.whatClosure=="full")) or options.closureTest == False): 
    hTrue_max700.Scale(252.89*1000.0*19.7/25424818.*0.438)
    hTrue = hTrue_max700.Clone()
    hTrue.SetName(options.toUnfold+"_genTop")
elif options.pdf == "mcnlo" and ((options.closureTest == True and (options.whatClosure=="nom" or options.whatClosure=="full")) or options.closureTest == False): 
    if options.useGenWeights:
        hTrue_max700.Scale(252.89*1000.0*19.7/(32852589.*16777215./32575024.))
    else:
        hTrue_max700.Scale(252.89*1000.0*19.7/32852589)
    hTrue = hTrue_max700.Clone()
    hTrue.SetName(options.toUnfold+"_genTop")
else :
    hTrue_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hTrue_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hTrue_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hTrue = hTrue_max700.Clone()
    hTrue.SetName(options.toUnfold+"_genTop")
    hTrue.Add(hTrue_700to1000)
    hTrue.Add(hTrue_1000toInf)

if options.troubleshoot and options.closureTest and options.whatClosure == "nom" :
    hTrue_max700_odd.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hTrue_700to1000_odd.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hTrue_1000toInf_odd.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hTrue_odd = hTrue_max700_odd.Clone()
    hTrue_odd.SetName(options.toUnfold+"_genTop_odd")
    hTrue_odd.Add(hTrue_700to1000_odd)
    hTrue_odd.Add(hTrue_1000toInf_odd)

if options.twoStep :
    if options.pdf == "MG" and ((options.closureTest == True and (options.whatClosure=="nom" or options.whatClosure=="full")) or options.closureTest == False):
        hPart_max700.Scale(252.89*1000.0*19.7/25424818.*0.438)
        hPart = hPart_max700.Clone()
        hPart.SetName(options.toUnfold+"_partTop")
    elif options.pdf == "mcnlo" and ((options.closureTest == True and (options.whatClosure=="nom" or options.whatClosure=="full")) or options.closureTest == False): 
        if options.useGenWeights:
            hPart_max700.Scale(252.89*1000.0*19.7/(32852589.*16777215./32575024.))
        else:
            hPart_max700.Scale(252.89*1000.0*19.7/32852589)
        hPart = hPart_max700.Clone()
        hPart.SetName(options.toUnfold+"_partTop")
    else :
        hPart_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
        hPart_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
        hPart_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
        hPart = hPart_max700.Clone()
        hPart.SetName(options.toUnfold+"_partTop")
        hPart.Add(hPart_700to1000)
        hPart.Add(hPart_1000toInf)

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom" :
        hPart_max700_odd.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
        hPart_700to1000_odd.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
        hPart_1000toInf_odd.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
        hPart_odd = hPart_max700_odd.Clone()
        hPart_odd.SetName(options.toUnfold+"_partTop_odd")
        hPart_odd.Add(hPart_700to1000_odd)
        hPart_odd.Add(hPart_1000toInf_odd)

hMeas_T_t.Scale( sigma_T_t * lum / float(Nmc_T_t) )
hMeas_Tbar_t.Scale( sigma_Tbar_t * lum / float(Nmc_Tbar_t) )
hMeas_T_s.Scale( sigma_T_s * lum / float(Nmc_T_s) )
hMeas_Tbar_s.Scale( sigma_Tbar_s * lum / float(Nmc_Tbar_s) )
hMeas_T_tW.Scale( sigma_T_tW * lum / float(Nmc_T_tW) )
hMeas_Tbar_tW.Scale( sigma_Tbar_tW * lum / float(Nmc_Tbar_tW) )

hMeas_WJets_1jet.Scale( sigma_WJets_1jet * lum / float(Nmc_WJets_1jet) )
hMeas_WJets_2jet.Scale( sigma_WJets_2jet * lum / float(Nmc_WJets_2jet) )
hMeas_WJets_3jet.Scale( sigma_WJets_3jet * lum / float(Nmc_WJets_3jet) )
hMeas_WJets_4jet.Scale( sigma_WJets_4jet * lum / float(Nmc_WJets_4jet) )


hMeas_SingleTop = hMeas_T_t.Clone()
hMeas_SingleTop.SetName(options.toUnfold+"RecoTop_SingleTop")

hMeas_WJets = hMeas_WJets_1jet.Clone()
hMeas_WJets.SetName(options.toUnfold+"RecoTop_WJets")

for hist in [hMeas_Tbar_t, hMeas_T_s, hMeas_Tbar_s, hMeas_T_tW, hMeas_Tbar_tW] :
    hMeas_SingleTop.Add( hist )
for hist in [hMeas_WJets_2jet,hMeas_WJets_3jet,hMeas_WJets_4jet] :
    hMeas_WJets.Add( hist )

hMeas_tt0_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
hMeas_tt700_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
hMeas_tt1000_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))

hMeas_TTNonSemi = hMeas_tt0_nonsemi.Clone()
hMeas_TTNonSemi.SetName(options.toUnfold+"RecoTop_TTNonSemilep")
hMeas_TTNonSemi.Add( hMeas_tt700_nonsemi )
hMeas_TTNonSemi.Add( hMeas_tt1000_nonsemi )


# -------------------------------------------------------------------------------------
# Scale each sample to that fitted by theta
# -------------------------------------------------------------------------------------

hRecoQCD.Scale( fitted_qcd / hRecoQCD.Integral() )
hMeas_SingleTop.Scale( fitted_singletop / hMeas_SingleTop.Integral() )
hMeas_WJets.Scale( fitted_wjets / hMeas_WJets.Integral() )
hMeas_TTNonSemi.Scale( fitted_ttbarnonsemilep / hMeas_TTNonSemi.Integral() )


# -------------------------------------------------------------------------------------
# subtract backgrounds from the data distribution, but not for closure test!!! 
# -------------------------------------------------------------------------------------

# Plot comparison of data and MC (pre reweighting) if doing 'data' closure test
if options.closureTest and options.whatClosure == "data" and options.troubleshoot:
    ctA = TCanvas("ctA", "", 800, 600)

    if options.toUnfold == "pt":
        ltA = TLegend(0.4, 0.65, 0.7, 0.9)
        ltA.SetFillStyle(0)
        ltA.SetTextFont(42)
        ltA.SetTextSize(0.045)
        ltA.SetBorderSize(0)
    if options.toUnfold == "y":
        ltA = TLegend(0.4, 0.6, 0.7, 0.8)
        ltA.SetFillStyle(0)
        ltA.SetTextFont(42)
        ltA.SetTextSize(0.035)
        ltA.SetBorderSize(0)
    
    hMeas.SetMarkerColor(1)
    hMeasTT.SetMarkerColor(4)
    hMeas.Draw()
    hMeasTT.Draw("same")
    ltA.AddEntry(hMeas, "Data distribution, pre-reweighting","l")
    ltA.AddEntry(hMeasTT, "MC distribution","l")
    ltA.Draw()
    ctA.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hMeas_dataVSmc"+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf")

if options.closureTest == False or options.whatClosure == "data": 
    for hist in [hMeas_SingleTop, hMeas_WJets, hRecoQCD, hMeas_TTNonSemi] :
        hMeas.Add(hist, -1.)

    for ibin in xrange( hMeas.GetNbinsX() ) :
        if ( hMeas.GetBinContent( ibin ) < 0.0 ) :
            hMeas.SetBinContent( ibin, 0.0 )

    if options.whatClosure == "data": 
        for ibin in range(1, hMeas.GetXaxis().GetNbins()+1) :
        
            bin_data = hMeas.GetBinContent(ibin)
            bin_TT = hMeasTT.GetBinContent(ibin)
            ebin_data = hMeas.GetBinError(ibin)
            
            if (bin_data > 0):
                scale = bin_TT/bin_data
            else:
                scale = 0.0

            hMeas.SetBinContent(ibin, hMeas.GetBinContent(ibin)*scale)
            hMeas.SetBinError(ibin, hMeas.GetBinError(ibin)*scale)
        


# -------------------------------------------------------------------------------------
# draw background-subtracted data distribution 
# -------------------------------------------------------------------------------------

if options.closureTest and options.troubleshoot and options.whatClosure == "nom":
    ct1 = TCanvas("ct1", "", 800, 600)

    if options.toUnfold == "pt":
        lt1 = TLegend(0.4, 0.65, 0.7, 0.9)
        lt1.SetFillStyle(0)
        lt1.SetTextFont(42)
        lt1.SetTextSize(0.045)
        lt1.SetBorderSize(0)
    if options.toUnfold == "y":
        lt1 = TLegend(0.4, 0.6, 0.7, 0.8)
        lt1.SetFillStyle(0)
        lt1.SetTextFont(42)
        lt1.SetTextSize(0.035)
        lt1.SetBorderSize(0)
    
    hMeas.SetLineColor(2)
    hMeas.SetLineWidth(2)
    hMeas_odd.SetLineColor(4)
    hMeas_odd.SetLineWidth(2)
    hMeas.Draw()
    hMeas_odd.Draw("same")
    lt1.AddEntry(hMeas, "Unfolding input, even","l")
    lt1.AddEntry(hMeas_odd, "Unfolding input, odd","l")
    lt1.Draw()
    ct1.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hMeas_evenVsOdd"+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf")

    if options.twoStep :
        ct2 = TCanvas("ct2", "", 800, 600)
        
        if options.toUnfold == "pt":
            lt2 = TLegend(0.4, 0.65, 0.7, 0.9)
            lt2.SetFillStyle(0)
            lt2.SetTextFont(42)
            lt2.SetTextSize(0.045)
            lt2.SetBorderSize(0)
        if options.toUnfold == "y":
            lt2 = TLegend(0.4, 0.6, 0.7, 0.8)
            lt2.SetFillStyle(0)
            lt2.SetTextFont(42)
            lt2.SetTextSize(0.035)
            lt2.SetBorderSize(0)
    
        hPart_odd.SetLineColor(2)
        hPart_odd.SetLineWidth(2)
        hPart.SetLineColor(4)
        hPart.SetLineWidth(2)
        hPart_odd.Draw()
        hPart.Draw("same")
        lt2.AddEntry(hPart, "Particle-level truth, even","l")
        lt2.AddEntry(hPart_odd, "Particle-level truth, odd","l")
        lt2.Draw()
        ct2.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hPart_evenVsOdd"+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf")

    ct3 = TCanvas("ct3", "", 800, 600)
    
    if options.toUnfold == "pt":
        lt3 = TLegend(0.4, 0.65, 0.7, 0.9)
        lt3.SetFillStyle(0)
        lt3.SetTextFont(42)
        lt3.SetTextSize(0.045)
        lt3.SetBorderSize(0)
    if options.toUnfold == "y":
        lt3 = TLegend(0.4, 0.6, 0.7, 0.8)
        lt3.SetFillStyle(0)
        lt3.SetTextFont(42)
        lt3.SetTextSize(0.035)
        lt3.SetBorderSize(0)
    
    hTrue_odd.SetLineColor(2)
    hTrue_odd.SetLineWidth(2)
    hTrue.SetLineColor(4)
    hTrue.SetLineWidth(2)
    hTrue_odd.Draw()
    hTrue.Draw("same")
    lt3.AddEntry(hTrue, "Parton-level truth, even","l")
    lt3.AddEntry(hTrue_odd, "Parton-level truth, odd","l")
    lt3.Draw()
    ct3.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hTrue_evenVsOdd"+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf")


    
# -------------------------------------------------------------------------------------
# do the actual unfolding
# -------------------------------------------------------------------------------------

## FOR CHECKING aNNNLO UNFOLDING CLOSURE TEST
#
#SF = [ 1.0, 1.0, 11.9236298085/11.8437366486, 3.58917547755/3.22087001801, 1.19792962383/0.97037011385, 0.429050592794/0.329721450806, 0.0648451839752/0.0464682132006, 1.0]
#
#for ibin in range(1, hTrue.GetXaxis().GetNbins()+1 ) :
#    print "SF = " + str(SF[ibin-1])
#    bc = hMeas.GetBinContent(ibin)
#    be = hMeas.GetBinError(ibin)
#    hMeas.SetBinContent(ibin, bc*SF[ibin-1])
#    hMeas.SetBinError(ibin, be*SF[ibin-1])
#    bc = hTrue.GetBinContent(ibin)
#    be = hTrue.GetBinError(ibin)
#    hTrue.SetBinContent(ibin, bc*SF[ibin-1])
#    hTrue.SetBinError(ibin, be*SF[ibin-1])


# -------------------------------------------------------------------------------------
# one-step unfolding
if options.twoStep == False:                
    
    print "------------ UNFOLDING (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold = RooUnfoldBayes(response, hMeas, 4);
    unfold = RooUnfoldSvd(response, hMeas, 2);
    #unfold = RooUnfoldTUnfold(response, hMeas);
    
    # get the unfolded distribution
    hReco = unfold.Hreco()

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        unfold_even = RooUnfoldSvd(response_even, hMeas_odd, 2);
        hReco_odd = unfold_even.Hreco()


# -------------------------------------------------------------------------------------
# two-step unfolding
else :    
    
    print "------------ UNFOLD TO PARTICLE-LEVEL (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold_rp = RooUnfoldBayes(response_rp, hMeas, 4);
    unfold_rp = RooUnfoldSvd(response_rp, hMeas, 2);
    #unfold_rp = RooUnfoldTUnfold(response_rp, hMeas);

    # get the distribution unfolded to particle-level
    hReco_rp = unfold_rp.Hreco()
        
    print "------------ UNFOLD TO PARTON-LEVEL (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold = RooUnfoldBayes(response_pp, hReco_rp, 4);
    unfold = RooUnfoldSvd(response_pp, hReco_rp, 2);
    #unfold = RooUnfoldTUnfold(response_pp, hReco_rp);

    # get the distribution unfolded to parton-level
    hReco = unfold.Hreco()

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        unfold_rp_even = RooUnfoldSvd(response_rp_even, hMeas_odd, 2);
        hReco_rp_odd = unfold_rp_even.Hreco()
        unfold_even = RooUnfoldSvd(response_pp_even, hReco_rp_odd, 2);
        hReco_odd = unfold_even.Hreco()


# -------------------------------------------------------------------------------------
# Translate to cross section (not events) in bins of pt N/L/BR)
# -------------------------------------------------------------------------------------

hTrue.Scale(1.0/(lum*0.438/3.)) # true @ parton level
hMeas.Scale(1.0/(lum*0.438/3.)) # measured @ reco level
hReco.Scale(1.0/(lum*0.438/3.)) # unfolded to parton level
if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
    hTrue_odd.Scale(1.0/(lum*0.438/3.)) # true @ parton level
    hMeas_odd.Scale(1.0/(lum*0.438/3.)) # measured @ reco level
    hReco_odd.Scale(1.0/(lum*0.438/3.)) # unfolded to parton level
if options.twoStep:
    hPart.Scale(1.0/(lum*0.438/3.))    # true @ parton level
    hReco_rp.Scale(1.0/(lum*0.438/3.)) # unfolded to particle level
    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        hPart_odd.Scale(1.0/(lum*0.438/3.))    # true @ parton level
        hReco_rp_odd.Scale(1.0/(lum*0.438/3.)) # unfolded to particle level


# -------------------------------------------------------------------------------------
# Adjust for bin width
# -------------------------------------------------------------------------------------

sumReco = 0
sumTrue = 0
sumMeas = 0
sumReco_rp = 0
sumPart = 0
sumReco_odd = 0
sumTrue_odd = 0
sumMeas_odd = 0
sumReco_rp_odd = 0
sumPart_odd = 0

lowedge = 399.
highedge = 1199.
if options.toUnfold == "y":
    lowedge = -2.5
    highedge = 2.5

for ibin in range(1, hTrue.GetXaxis().GetNbins()+1 ) :
        
    # total cross section for pt > 400 GeV
    if hTrue.GetBinLowEdge(ibin) > lowedge :
        sumTrue += hTrue.GetBinContent(ibin)
    if hReco.GetBinLowEdge(ibin) > lowedge :
        sumReco += hReco.GetBinContent(ibin)
    if hMeas.GetBinLowEdge(ibin) > lowedge :
        sumMeas += hMeas.GetBinContent(ibin)
    if options.twoStep:
        if hReco_rp.GetBinLowEdge(ibin) > lowedge :
            sumReco_rp += hReco_rp.GetBinContent(ibin)
        if hPart.GetBinLowEdge(ibin) > lowedge :
            sumPart += hPart.GetBinContent(ibin)

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        if hTrue_odd.GetBinLowEdge(ibin) > lowedge :
            sumTrue_odd += hTrue_odd.GetBinContent(ibin)
        if hReco_odd.GetBinLowEdge(ibin) > lowedge :
            sumReco_odd += hReco_odd.GetBinContent(ibin)
        if hMeas_odd.GetBinLowEdge(ibin) > lowedge :
            sumMeas_odd += hMeas_odd.GetBinContent(ibin)
        if options.twoStep:
            if hReco_rp_odd.GetBinLowEdge(ibin) > lowedge :
                sumReco_rp_odd += hReco_rp_odd.GetBinContent(ibin)
            if hPart_odd.GetBinLowEdge(ibin) > lowedge :
                sumPart_odd += hPart_odd.GetBinContent(ibin)

    width = hTrue.GetBinWidth(ibin)

    hTrue.SetBinContent(ibin, hTrue.GetBinContent(ibin) / width )
    hTrue.SetBinError(ibin, hTrue.GetBinError(ibin) / width )

    hMeas.SetBinContent(ibin,  hMeas.GetBinContent(ibin) / width )
    hMeas.SetBinError(ibin,  hMeas.GetBinError(ibin) / width )
        
    hReco.SetBinContent(ibin, hReco.GetBinContent(ibin) / width )
    hReco.SetBinError(ibin, hReco.GetBinError(ibin) / width )

    if options.twoStep:
        hReco_rp.SetBinContent(ibin, hReco_rp.GetBinContent(ibin) / width )
        hReco_rp.SetBinError(ibin, hReco_rp.GetBinError(ibin) / width )

        hPart.SetBinContent(ibin, hPart.GetBinContent(ibin) / width )
        hPart.SetBinError(ibin, hPart.GetBinError(ibin) / width )            

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        hTrue_odd.SetBinContent(ibin, hTrue_odd.GetBinContent(ibin) / width )
        hTrue_odd.SetBinError(ibin, hTrue_odd.GetBinError(ibin) / width )

        hMeas_odd.SetBinContent(ibin,  hMeas_odd.GetBinContent(ibin) / width )
        hMeas_odd.SetBinError(ibin,  hMeas_odd.GetBinError(ibin) / width )
        
        hReco_odd.SetBinContent(ibin, hReco_odd.GetBinContent(ibin) / width )
        hReco_odd.SetBinError(ibin, hReco_odd.GetBinError(ibin) / width )

        if options.twoStep:
            hReco_rp_odd.SetBinContent(ibin, hReco_rp_odd.GetBinContent(ibin) / width )
            hReco_rp_odd.SetBinError(ibin, hReco_rp_odd.GetBinError(ibin) / width )

            hPart_odd.SetBinContent(ibin, hPart_odd.GetBinContent(ibin) / width )
            hPart_odd.SetBinError(ibin, hPart_odd.GetBinError(ibin) / width )            


# -------------------------------------------------------------------------------------
# do NORMALIZED differential cross section instead??
# -------------------------------------------------------------------------------------

if options.normalize: 
    hTrue.Scale(1.0/sumTrue)
    hReco.Scale(1.0/sumReco)
    hMeas.Scale(1.0/sumMeas)
    if options.twoStep:
        hReco_rp.Scale(1.0/sumReco_rp)
        hPart.Scale(1.0/sumPart)
    
        
# -------------------------------------------------------------------------------------
# print & draw
# -------------------------------------------------------------------------------------

## ratio of unfolded data to generator-level 
hFrac = hReco.Clone()
hFrac.SetName("hFrac")
if options.toUnfold == "pt":
    hFrac.SetTitle(";Top quark p_{T} (GeV);Data/MC")
elif options.toUnfold == "y":
    hFrac.SetTitle(";Top quark rapidity;Data/MC")
hFrac.Divide(hTrue)

if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
    hFrac_odd = hReco_odd.Clone()
    hFrac_odd.SetName("hFrac_odd")
    if options.toUnfold == "pt":
        hFrac_odd.SetTitle(";Top quark p_{T} (GeV);Data/MC")
    elif options.toUnfold == "y":
        hFrac_odd.SetTitle(";Top quark rapidity;Data/MC")
    hFrac_odd.Divide(hTrue_odd)

## ratio of unfolded data to particle-level 
if options.twoStep:
    hFrac_rp = hReco_rp.Clone()
    hFrac_rp.SetName("hFrac_rp")
    if options.toUnfold == "pt" :
        hFrac_rp.SetTitle(";Particle-level t jet p_{T} (GeV);Data/MC")
    elif options.toUnfold == "y" :
        hFrac_rp.SetTitle(";Particle-level t jet y;Data/MC")
    hFrac_rp.Divide(hPart)

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        hFrac_rp_odd = hReco_rp_odd.Clone()
        hFrac_rp_odd.SetName("hFrac_rp_odd")
        if options.toUnfold == "pt" :
            hFrac_rp_odd.SetTitle(";Particle-level t jet p_{T} (GeV);Data/MC")
        elif options.toUnfold == "y" :
            hFrac_rp_odd.SetTitle(";Particle-level t jet y;Data/MC")
        hFrac_rp_odd.Divide(hPart_odd)

#if options.closureTest and options.whatClosure == "reverse":
if options.closureTest:
    print ''
    print '-------------------------------------------------------------------------------------'
    print 'uncertainty from closure test for ' + options.pdf + ' ' + options.whatClosure + ' (' + options.lepType + ')'
    print '-------------------------------------------------------------------------------------'
    print 'parton-level'
    for ibin in range(1, hFrac.GetXaxis().GetNbins()+1 ) :
        if hFrac.GetBinLowEdge(ibin) > lowedge and hFrac.GetBinLowEdge(ibin) < highedge:
            print '[' + str(hFrac.GetBinLowEdge(ibin)) + ',' + str(hFrac.GetBinLowEdge(ibin+1)) + '] = ' + str((hFrac.GetBinContent(ibin)-1.0)*100.0) + ' %'            
    if options.twoStep:
        print ''
        print 'particle-level'
        for ibin in range(1, hFrac_rp.GetXaxis().GetNbins()+1 ) :
            
            if hFrac_rp.GetBinLowEdge(ibin) > lowedge and hFrac_rp.GetBinLowEdge(ibin) < highedge:
                print '[' + str(hFrac_rp.GetBinLowEdge(ibin)) + ',' + str(hFrac_rp.GetBinLowEdge(ibin+1)) + '] = ' + str((hFrac_rp.GetBinContent(ibin)-1.0)*100.0) + ' %' 
    

    if options.toUnfold == "y":
        print ''
        print 'averaged in rapidity bins PARTON'
        print '[-2.4,-1.2] = ' + str( ( abs(hFrac.GetBinContent(1)-1.0)*100.0 + abs(hFrac.GetBinContent(6)-1.0)*100.0 )/2 ) + ' %'            
        print '[-1.2,-0.6] = ' + str( ( abs(hFrac.GetBinContent(2)-1.0)*100.0 + abs(hFrac.GetBinContent(5)-1.0)*100.0 )/2 ) + ' %'            
        print '[-0.6, 0.0] = ' + str( ( abs(hFrac.GetBinContent(3)-1.0)*100.0 + abs(hFrac.GetBinContent(4)-1.0)*100.0 )/2 ) + ' %'            
        print '[ 0.0, 0.6] = ' + str( ( abs(hFrac.GetBinContent(3)-1.0)*100.0 + abs(hFrac.GetBinContent(4)-1.0)*100.0 )/2 ) + ' %'            
        print '[ 0.6, 1.2] = ' + str( ( abs(hFrac.GetBinContent(2)-1.0)*100.0 + abs(hFrac.GetBinContent(5)-1.0)*100.0 )/2 ) + ' %'            
        print '[ 1.2, 2.4] = ' + str( ( abs(hFrac.GetBinContent(1)-1.0)*100.0 + abs(hFrac.GetBinContent(6)-1.0)*100.0 )/2 ) + ' %'            
        if options.twoStep:
            print ''
            print 'averaged in rapidity bins PARTICLE'
            print '[-2.4,-1.2] = ' + str( ( abs(hFrac_rp.GetBinContent(1)-1.0)*100.0 + abs(hFrac_rp.GetBinContent(6)-1.0)*100.0 )/2 ) + ' %'            
            print '[-1.2,-0.6] = ' + str( ( abs(hFrac_rp.GetBinContent(2)-1.0)*100.0 + abs(hFrac_rp.GetBinContent(5)-1.0)*100.0 )/2 ) + ' %'            
            print '[-0.6, 0.0] = ' + str( ( abs(hFrac_rp.GetBinContent(3)-1.0)*100.0 + abs(hFrac_rp.GetBinContent(4)-1.0)*100.0 )/2 ) + ' %'            
            print '[ 0.0, 0.6] = ' + str( ( abs(hFrac_rp.GetBinContent(3)-1.0)*100.0 + abs(hFrac_rp.GetBinContent(4)-1.0)*100.0 )/2 ) + ' %'            
            print '[ 0.6, 1.2] = ' + str( ( abs(hFrac_rp.GetBinContent(2)-1.0)*100.0 + abs(hFrac_rp.GetBinContent(5)-1.0)*100.0 )/2 ) + ' %'            
            print '[ 1.2, 2.4] = ' + str( ( abs(hFrac_rp.GetBinContent(1)-1.0)*100.0 + abs(hFrac_rp.GetBinContent(6)-1.0)*100.0 )/2 ) + ' %'            
        

print ''
print '-------------------------------------------------------------------------------------'
print 'sigma (raw data) = ' + str(int(sumMeas)) + ' fb'
print 'true sigma @ parton-level (pt > 400 GeV)      = ' + str(int(sumTrue)) + ' fb'
print 'measured sigma (unfolded data) @ parton-level = ' + str(int(sumReco)) + ' fb'
if options.twoStep:
    print 'true sigma @ particle-level                     = ' + str(int(sumPart)) + ' fb'
    print 'measured sigma (unfolded data) @ particle-level = ' + str(int(sumReco_rp)) + ' fb'
print '-------------------------------------------------------------------------------------'
print ''


# -------------------------------------------------------------------------------------
# draw parton-level unfolding
# -------------------------------------------------------------------------------------

c1 = TCanvas("c", "c", 700, 700)
pad1 =  TPad("pad1","pad1",0,0.3,1,1)
pad1.SetBottomMargin(0.05);
pad1.Draw();
pad1.cd();

#unfold.PrintTable (cout, hTrue);
hReco.SetMarkerStyle(21)
hMeas.SetMarkerStyle(25);

if options.toUnfold == "pt":
    hReco.GetXaxis().SetRangeUser(400.,1200.)
    hTrue.GetXaxis().SetRangeUser(400.,1200.)
    hMeas.GetXaxis().SetRangeUser(400.,1200.)

xsec_title = ";;d#sigma/dp_{T} [fb/GeV]"
if options.toUnfold == "y":
    xsec_title = ";;d#sigma/dy [fb]"
if options.normalize:    
    xsec_title = ";;1/#sigma d#sigma/dp_{T} [1/GeV]"
    if options.toUnfold == "y":
        xsec_title = ";;1/#sigma d#sigma/dy"

hReco.SetTitle(xsec_title)
hReco.GetYaxis().SetTitleOffset(1.2)
hReco.SetMinimum(0.0)
max = hTrue.GetMaximum()
max2 = hReco.GetMaximum()
if max2 > max:
	max = max2
hReco.SetAxisRange(0,max*1.15,"Y")
if options.toUnfold == "y":
    hReco.SetAxisRange(0,max*1.5,"Y")
hReco.Draw()
hTrue.Draw('hist same')
hMeas.Draw('same')
hTrue.UseCurrentStyle()
hTrue.SetLineColor(4);
hTrue.GetYaxis().SetTitleSize(25)
hTrue.GetXaxis().SetLabelSize(0)


if options.toUnfold == "pt":
    leg = TLegend(0.5, 0.55, 0.9, 0.75)
elif options.toUnfold == "y":
    leg = TLegend(0.2, 0.7, 0.5, 0.9)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)
leg.SetBorderSize(0)

tt = TLatex()
tt.SetNDC()
tt.SetTextFont(42)

if options.closureTest == False : 
    leg.AddEntry( hReco, 'Unfolded data', 'p')
    leg.AddEntry( hTrue, 'Generated (Powheg)', 'l')
    leg.AddEntry( hMeas, 'Raw data', 'p')
elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and options.whatClosure == "reverse":
    leg.AddEntry( hReco, 'Powheg (unfolded)', 'p')
    leg.AddEntry( hTrue, 'Powheg (generated)', 'l')
    leg.AddEntry( hMeas, 'Powheg (reco-level)', 'p')
    if (options.toUnfold == "pt"):
        tt.DrawLatex(0.55,0.45, "Closure test, response")
        if options.pdf == "MG":
            tt.DrawLatex(0.55,0.40, "matrix from MadGraph")
        else: 
            tt.DrawLatex(0.55,0.40, "matrix from MC@NLO")
    elif (options.toUnfold == "y"):
        tt.SetTextSize(0.042)
        tt.DrawLatex(0.22,0.62, "Closure test,")
        tt.DrawLatex(0.22,0.57, "response matrix")
        if options.pdf == "MG":
            tt.DrawLatex(0.22,0.52, "from MadGraph")
        else: 
            tt.DrawLatex(0.22,0.52, "from MC@NLO")
elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True:
    if options.pdf == "MG":
        leg.AddEntry( hReco, 'MadGraph (unfolded)', 'p')
        leg.AddEntry( hTrue, 'MadGraph (generated)', 'l')
        leg.AddEntry( hMeas, 'MadGraph (reco-level)', 'p')
    else :
        leg.AddEntry( hReco, 'MC@NLO (unfolded)', 'p')
        leg.AddEntry( hTrue, 'MC@NLO (generated)', 'l')
        leg.AddEntry( hMeas, 'MC@NLO (reco-level)', 'p')
    if (options.whatClosure == "full") == False:
        tt.DrawLatex(0.55,0.45, "Closure test, response")
        tt.DrawLatex(0.55,0.40, "matrix from Powheg")
else : 
    leg.AddEntry( hReco, 'Unfolded MC (Powheg)', 'p')
    leg.AddEntry( hTrue, 'Generated (Powheg)', 'l')
    leg.AddEntry( hMeas, 'Reco-level (Powheg)', 'p')
    if options.toUnfold == "pt":
        tt.DrawLatex(0.55,0.45, "MC closure test")
    if options.toUnfold == "y":
        tt.DrawLatex(0.22,0.62, "MC closure test")
    
leg.Draw()


# write histograms to file
if options.closureTest:
    hReco.SetName("UnfoldedMC")
else:
    hReco.SetName("UnfoldedData")

hReco.Write()
hTrue.Write()
hMeas.Write()


text1 = TLatex()
text1.SetNDC()
text1.SetTextFont(42)
if options.toUnfold == "pt":
    text1.DrawLatex(0.55,0.8, "#scale[1.0]{L = 19.7 fb^{-1}, #sqrt{s} = 8 TeV}")
if options.toUnfold == "y":    
    text1.DrawLatex(0.72,0.82, "#scale[1.0]{L = 19.7 fb^{-1}}")
    text1.DrawLatex(0.72,0.75, "#scale[1.0]{#sqrt{s} = 8 TeV}")


c1.cd();
pad2 =  TPad("pad2","pad2",0,0.0,1,0.28)
pad2.SetTopMargin(0.05);
pad2.SetBottomMargin(0.4);
pad2.Draw();
pad2.cd();
pad2.SetGridy()
hFrac.SetMaximum(1.4)
hFrac.SetMinimum(0.6)
if options.normalize == False and options.closureTest == False: 
    hFrac.SetMaximum(1.2)
    hFrac.SetMinimum(0.4)    
hFrac.UseCurrentStyle()
hFrac.GetYaxis().SetTitleSize(25)
hFrac.GetYaxis().SetTitleOffset(2.0)
hFrac.GetXaxis().SetTitleOffset(4.0)
hFrac.GetXaxis().SetLabelSize(25)
hFrac.GetYaxis().SetNdivisions(4,4,0,False)

hFrac.Draw("e")
hFrac.GetXaxis().SetRangeUser(400., 1200.)

c1.Update()

if options.syst=="nom" and options.bkgSyst=="nom":
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf", "pdf")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".png", "png")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".eps", "eps")

if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
    pad1.cd()

    hReco_odd.SetMarkerStyle(21)
    hMeas_odd.SetMarkerStyle(25);

    if options.toUnfold == "pt":
        hReco_odd.GetXaxis().SetRangeUser(400.,1200.)
        hTrue_odd.GetXaxis().SetRangeUser(400.,1200.)
        hMeas_odd.GetXaxis().SetRangeUser(400.,1200.)

    hReco_odd.SetTitle(xsec_title)
    hReco_odd.GetYaxis().SetTitleOffset(1.2)
    hReco_odd.SetMinimum(0.0)
    max = hTrue_odd.GetMaximum()
    max2 = hReco_odd.GetMaximum()
    if max2 > max:
	max = max2
    hReco_odd.SetAxisRange(0,max*1.15,"Y")
    if options.toUnfold == "y":
        hReco_odd.SetAxisRange(0,max*1.5,"Y")
    hReco_odd.Draw()
    hTrue_odd.Draw('hist same')
    hMeas_odd.Draw('same')
    hTrue_odd.UseCurrentStyle()
    hTrue_odd.SetLineColor(4);
    hTrue_odd.GetYaxis().SetTitleSize(25)
    hTrue_odd.GetXaxis().SetLabelSize(0)

    if options.toUnfold == "pt":
        legA = TLegend(0.45, 0.55, 0.85, 0.75)
    if options.toUnfold == "y":
        legA = TLegend(0.37, 0.25, 0.65, 0.45)
    legA.SetTextSize(0.045)
    legA.SetFillStyle(0)
    legA.SetTextFont(42)
    legA.SetBorderSize(0)
 
    legA.AddEntry( hReco_odd, 'Unfolded MC (Powheg)', 'p')
    legA.AddEntry( hTrue_odd, 'Generated (Powheg)', 'l')
    legA.AddEntry( hMeas_odd, 'Reco-level (Powheg)', 'p')
    if options.toUnfold == "pt":
        tt.DrawLatex(0.5,0.45, "MC closure test")
    if options.toUnfold == "y":
        tt.DrawLatex(0.45,0.45, "MC closure test")
    
    legA.Draw()

    pad2.cd();
    hFrac_odd.SetMaximum(1.4)
    hFrac_odd.SetMinimum(0.6)
    hFrac_odd.UseCurrentStyle()
    hFrac_odd.GetYaxis().SetTitleSize(25)
    hFrac_odd.GetYaxis().SetTitleOffset(2.0)
    hFrac_odd.GetXaxis().SetTitleOffset(4.0)
    hFrac_odd.GetXaxis().SetLabelSize(25)
    hFrac_odd.GetYaxis().SetNdivisions(4,4,0,False)

    hFrac_odd.Draw("e")
    if options.toUnfold == "pt":
        hFrac_odd.GetXaxis().SetRangeUser(400., 1200.)

    c1.Update()

    c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_unfoldOdd"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf", "pdf")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_unfoldOdd"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".png", "png")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_unfoldOdd"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".eps", "eps")


# -------------------------------------------------------------------------------------
# draw particle-level unfolding
# -------------------------------------------------------------------------------------

if options.twoStep:
    pad1.cd();

    hReco_rp.SetMarkerStyle(21)
    hMeas.SetMarkerStyle(25);

    if options.toUnfold == "pt":
        hReco_rp.GetXaxis().SetRangeUser(400.,1200.)
        hPart.GetXaxis().SetRangeUser(400.,1200.)
        hMeas.GetXaxis().SetRangeUser(400.,1200.)

    hReco_rp.SetTitle(xsec_title)
    hReco_rp.GetYaxis().SetTitleOffset(1.2)
    hReco_rp.SetMinimum(0.0)
    max = hPart.GetMaximum()
    max2 = hReco_rp.GetMaximum()
    if max2 > max:
        max = max2
    hReco_rp.SetAxisRange(0,max*1.15,"Y")
    if options.toUnfold == "y":
        hReco_rp.SetAxisRange(0,max*1.5,"Y")
    hReco_rp.Draw()
    hPart.Draw('hist same')
    hMeas.Draw('same')
    hPart.UseCurrentStyle()
    hPart.SetLineColor(4);
    hPart.GetYaxis().SetTitleSize(25)
    hPart.GetXaxis().SetLabelSize(0)

        
    if options.toUnfold == "pt":
        leg2 = TLegend(0.5, 0.55, 0.9, 0.75)
    elif options.toUnfold == "y":
        leg2 = TLegend(0.2, 0.7, 0.5, 0.9)
    leg2.SetFillStyle(0)
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.045)
    leg2.SetBorderSize(0)

    if options.closureTest == False : 
        leg2.AddEntry( hReco, 'Unfolded data', 'p')
        leg2.AddEntry( hTrue, 'Generated (Powheg)', 'l')
        leg2.AddEntry( hMeas, 'Raw data', 'p')
    elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and options.whatClosure == "reverse":
        leg2.AddEntry( hReco, 'Powheg (unfolded)', 'p')
        leg2.AddEntry( hTrue, 'Powheg (generated)', 'l')
        leg2.AddEntry( hMeas, 'Powheg (reco-level)', 'p')
        if options.toUnfold == "pt":
            tt.DrawLatex(0.55,0.45, "Closure test, response")
            if options.pdf == "MG":
                tt.DrawLatex(0.55,0.40, "matrix from MadGraph")
            else: 
                tt.DrawLatex(0.55,0.40, "matrix from MC@NLO")
        elif options.toUnfold == "y":
            tt.SetTextSize(0.042)
            tt.DrawLatex(0.22,0.62, "Closure test,")
            tt.DrawLatex(0.22,0.57, "response matrix")
            if options.pdf == "MG":
                tt.DrawLatex(0.22,0.52, "from MadGraph")
            else: 
                tt.DrawLatex(0.22,0.52, "from MC@NLO")
    elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True:
        if options.pdf == "MG":
            leg2.AddEntry( hReco, 'MadGraph (unfolded)', 'p')
            leg2.AddEntry( hTrue, 'MadGraph (generated)', 'l')
            leg2.AddEntry( hMeas, 'MadGraph (reco-level)', 'p')
        else :
            leg2.AddEntry( hReco, 'MC@NLO (unfolded)', 'p')
            leg2.AddEntry( hTrue, 'MC@NLO (generated)', 'l')
            leg2.AddEntry( hMeas, 'MC@NLO (reco-level)', 'p')
        if (options.whatClosure == "full") == False:
            tt.DrawLatex(0.55,0.45, "Closure test, response")
            tt.DrawLatex(0.55,0.40, "matrix from Powheg")
    else : 
        leg2.AddEntry( hReco, 'Unfolded MC (Powheg)', 'p')
        leg2.AddEntry( hTrue, 'Generated (Powheg)', 'l')
        leg2.AddEntry( hMeas, 'Reco-level (Powheg)', 'p')
        if options.toUnfold == "pt":
            tt.DrawLatex(0.55,0.45, "MC closure test")
        if options.toUnfold == "y":
            tt.DrawLatex(0.22,0.62, "MC closure test")
    
    leg2.Draw()

    # write histograms to file
    if options.closureTest:
        hReco_rp.SetName("UnfoldedMC_rp")
    else:
        hReco_rp.SetName("UnfoldedData_rp")

    hReco_rp.Write()
    hPart.Write()
    hMeas.Write()

    if options.toUnfold == "pt":
        text1.DrawLatex(0.55,0.8, "#scale[1.0]{L = 19.7 fb^{-1}, #sqrt{s} = 8 TeV}")
    if options.toUnfold == "y":
        text1.DrawLatex(0.72,0.82, "#scale[1.0]{L = 19.7 fb^{-1}}")
        text1.DrawLatex(0.72,0.75, "#scale[1.0]{#sqrt{s} = 8 TeV}")

    pad2.cd()

    hFrac_rp.SetMaximum(1.4)
    hFrac_rp.SetMinimum(0.6)
    if options.normalize == False and options.closureTest == False: 
        hFrac_rp.SetMaximum(1.2)
        hFrac_rp.SetMinimum(0.4)
    hFrac_rp.UseCurrentStyle()
    hFrac_rp.GetYaxis().SetTitleSize(25)
    hFrac_rp.GetYaxis().SetTitleOffset(2.0)
    hFrac_rp.GetXaxis().SetTitleOffset(4.0)
    hFrac_rp.GetXaxis().SetLabelSize(25)
    hFrac_rp.GetYaxis().SetNdivisions(4,4,0,False)

    hFrac_rp.Draw("e")
    if options.toUnfold == "pt":
        hFrac_rp.GetXaxis().SetRangeUser(400., 1200.)

    c1.Update()

    if options.syst=="nom" and options.bkgSyst=="nom":
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_"+options.toUnfold+"_2step_particle"+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf", "pdf")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_"+options.toUnfold+"_2step_particle"+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".png", "png")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_"+options.toUnfold+"_2step_particle"+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".eps", "eps")

    if options.troubleshoot :
        pad1.cd()

        hReco_rp.SetMarkerStyle(25)
        hTrue.SetLineColor(1)
        hTrue.Draw('hist')
        hReco_rp.Draw('same')
        hPart.Draw('hist same')
        hReco.Draw('same')

        if options.toUnfold == "pt":
            leg2A = TLegend(0.45, 0.55, 0.85, 0.75)
        if options.toUnfold == "y":
            leg2A = TLegend(0.37, 0.25, 0.65, 0.45)
        leg2A.SetFillStyle(0)
        leg2A.SetTextFont(42)
        leg2A.SetTextSize(0.045)
        leg2A.SetBorderSize(0)

        tt = TLatex()
        tt.SetNDC()
        tt.SetTextFont(42)

        leg2A.AddEntry( hReco_rp, 'pp unfolding input', 'p')
        leg2A.AddEntry( hPart, 'MC (particle-level)','l')
        leg2A.AddEntry( hTrue, 'MC (parton-level)', 'l')
        leg2A.AddEntry( hReco, 'Unfolded (parton-level)', 'p')
    
        leg2A.Draw()

        pad2.cd();
        hFrac.Draw("e")

        c1.Update()

        c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_pp"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf", "pdf")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_pp"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".png", "png")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_pp"+DIR+append1+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".eps", "eps")


    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        pad1.cd();
        
        hReco_rp_odd.SetMarkerStyle(21)
        hMeas_odd.SetMarkerStyle(25);

        if options.toUnfold == "pt":
            hReco_rp_odd.GetXaxis().SetRangeUser(400.,1200.)
            hPart_odd.GetXaxis().SetRangeUser(400.,1200.)
            hMeas_odd.GetXaxis().SetRangeUser(400.,1200.)
        
        hReco_rp_odd.SetTitle(xsec_title)
        hReco_rp_odd.GetYaxis().SetTitleOffset(1.2)
        hReco_rp_odd.SetMinimum(0.0)
        max = hPart_odd.GetMaximum()
        max2 = hReco_rp_odd.GetMaximum()
        if max2 > max:
            max = max2
        hReco_rp_odd.SetAxisRange(0,max*1.15,"Y")
        if options.toUnfold == "y":
            hReco_rp_odd.SetAxisRange(0,max*1.5,"Y")
        hReco_rp_odd.Draw()
        hPart_odd.Draw('hist same')
        hMeas_odd.Draw('same')
        hPart_odd.UseCurrentStyle()
        hPart_odd.SetLineColor(4);
        hPart_odd.GetYaxis().SetTitleSize(25)
        hPart_odd.GetXaxis().SetLabelSize(0)

        if options.toUnfold == "pt":
            leg2B = TLegend(0.45, 0.55, 0.85, 0.75)
        if options.toUnfold == "y":
            leg2B = TLegend(0.37, 0.25, 0.65, 0.45)
        leg2B.SetFillStyle(0)
        leg2B.SetTextFont(42)
        leg2B.SetTextSize(0.045)
        leg2B.SetBorderSize(0)

        leg2B.AddEntry( hReco_odd, 'Unfolded MC (Powheg)', 'p')
        leg2B.AddEntry( hTrue_odd, 'Generated (Powheg)', 'l')
        leg2B.AddEntry( hMeas_odd, 'Reco-level (Powheg)', 'p')
        if options.toUnfold == "pt":
            tt.DrawLatex(0.5,0.45, "MC closure test")
        if options.toUnfold == "y":
            tt.DrawLatex(0.45,0.45, "MC closure test")
    
        leg2B.Draw()

        c1.cd()
        pad2.cd()

        hFrac_rp_odd.SetMaximum(1.4)
        hFrac_rp_odd.SetMinimum(0.6)
        hFrac_rp_odd.UseCurrentStyle()
        hFrac_rp_odd.GetYaxis().SetTitleSize(25)
        hFrac_rp_odd.GetYaxis().SetTitleOffset(2.0)
        hFrac_rp_odd.GetXaxis().SetTitleOffset(4.0)
        hFrac_rp_odd.GetXaxis().SetLabelSize(25)
        hFrac_rp_odd.GetYaxis().SetNdivisions(4,4,0,False)

        hFrac_rp_odd.Draw("e")
        if options.toUnfold == "pt":
            hFrac_rp_odd.GetXaxis().SetRangeUser(400., 1200.)

        c1.Update()

        c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_unfoldOdd"+DIR+"_"+options.toUnfold+"_2step_particle"+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".pdf", "pdf")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_unfoldOdd"+DIR+"_"+options.toUnfold+"_2step_particle"+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".png", "png")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs_troubleshoot_unfoldOdd"+DIR+"_"+optoins.toUnfold+"_2step_particle"+closureout+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+norm_flag+".eps", "eps")

# -------------------------------------------------------------------------------------
# plot response matrices 
# (do this in the end as the normalization otherwise will mess up the unfolding result!)
# -------------------------------------------------------------------------------------

#gStyle.SetPalette(1)

ncontours = 256
stops = [0.00, 1.00]
#red   = [0.99, 0.32]
#green = [0.99, 0.3]
#blue  = [0.99, 0.9]
red   = [0.99, 0.32]
green = [0.99, 0.42]
blue  = [0.99, 0.9]
s = array('d', stops)
r = array('d', red)
g = array('d', green)
b = array('d', blue)
npoints = len(s)
TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
gStyle.SetNumberContours(ncontours)

#GREEN:  new TColor(8, 0.35,0.83,0.33);
#BLUE:  new TColor(9, 0.35,0.33,0.85);
#GREY-BLUE:  new TColor(38,0.49,0.6,0.82);
# red - green - blue

# -------------------------------------------------------------------------------------
# one-step unfolding
# -------------------------------------------------------------------------------------

gStyle.SetPadRightMargin(0.12);
cr = TCanvas("c_response", "", 800, 600)

if options.twoStep == False:
    
    hEmpty2D = response.Hresponse().Clone()
    hEmpty2D.SetName("empty2D")
    hEmpty2D.Reset()
    if options.toUnfold == "pt":
        hEmpty2D.GetXaxis().SetTitle("Reconstructed top jet p_{T} (GeV)")
        hEmpty2D.GetYaxis().SetTitle("Top quark p_{T} (GeV)")
    elif options.toUnfold == "y":
        hEmpty2D.GetXaxis().SetTitle("Reconstructed top jet rapidity")
        hEmpty2D.GetYaxis().SetTitle("Top quark rapidity")        
    hEmpty2D.GetXaxis().SetLabelSize(0.045)
    hEmpty2D.GetYaxis().SetLabelSize(0.045)
    hEmpty2D.Draw()
    
    hResponse2D = response.Hresponse().Clone()
    hResponse2D.SetName("plottedResponse")

    gStyle.SetPaintTextFormat(".1f")
    hResponse2D.Draw("colz,same,text")
    hEmpty2D.Draw("axis,same")

    if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_full_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_full_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_full_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        hEmpty2D.Draw()
        hResponse2D.Draw("colz,same,text")
        hEmpty2D.Draw("axis,same")

        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+append1+closureout+"_responseMatrix_full_even_"+options.pdf+"_"+options.syst+nobtag+".pdf")

        hResponse2D_even = response_even.Hresponse().Clone()
        hResponse2D_even.SetName("plottedResponse_even")
        hEmpty2D.Draw()
        hResponse2D_even.Draw("colz,same,text")
        hEmpty2D.Draw("axis,same")

        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+append1+closureout+"_responseMatrix_full_odd_"+options.pdf+"_"+options.syst+nobtag+".pdf")

        hRatio2D = hResponse2D.Clone()
        hRatio2D.Divide(hResponse2D_even)

        hEmpty2D.Draw()
        hRatio2D.Draw("colz,same,text")
        hEmpty2D.Draw("axis,same")

        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+append1+closureout+"_responseMatrix_full_ratio_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    
    # normalize so that for each bin of true top quark pt(eta), the bins in measured top pt(eta) add up to 100%
    nbinsX = hResponse2D.GetNbinsX()
    nbinsY = hResponse2D.GetNbinsY()
    for iby in range(1,nbinsY+1) :
        rowIntegral = hResponse2D.Integral(1,nbinsX,iby,iby)
        #print "for y-bin " + str(iby) + " row integral = " + str(rowIntegral)
        for ibx in range(1,nbinsX+1) :
            binContent = hResponse2D.GetBinContent(ibx,iby)
            newContent = 0
            if rowIntegral > 0:
                newContent = binContent/rowIntegral*100.0
            #print "bin content x-bin " + str(ibx) + " y-bin " + str(iby) + " binContent " + str(binContent) + " newContent " + str(newContent)
            hResponse2D.SetBinContent(ibx,iby,newContent)

    hEmpty2D.Draw()
    hResponse2D.Draw("colz,same,text")
    hEmpty2D.Draw("axis,same")
    if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    if options.toUnfold == "pt":
        hEmpty2D.SetAxisRange(450,1150,"X")
        hEmpty2D.SetAxisRange(450,1150,"Y")
        hResponse2D.SetAxisRange(450,1150,"X")
        hResponse2D.SetAxisRange(450,1150,"Y")
        hEmpty2D.Draw()
        hResponse2D.Draw("colz,same,text")
        hEmpty2D.Draw("axis,same")

        if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+append1+closureout+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")
        
    response.Hresponse().SetName("responseMatrix_"+options.syst)
    response.Hresponse().Write()
    

# -------------------------------------------------------------------------------------
# two-step unfolding
# -------------------------------------------------------------------------------------

if options.twoStep:

    cr.SetTopMargin(0.08)

    # -------------------------------------------------------------------------------------
    ### reco to particle level
    hEmpty2D_rp = response_rp.Hresponse().Clone()
    hEmpty2D_rp.SetName("empty2D_rp")
    hEmpty2D_rp.Reset()
    if options.toUnfold == "pt":
        hEmpty2D_rp.GetXaxis().SetTitle("Reconstructed t jet p_{T} (GeV)")
        hEmpty2D_rp.GetYaxis().SetTitle("Particle-level t jet p_{T} (GeV)")
    elif options.toUnfold == "y":
        hEmpty2D_rp.GetXaxis().SetTitle("Reconstructed t jet y")
        hEmpty2D_rp.GetYaxis().SetTitle("Particle-level t jet y")
    hEmpty2D_rp.GetXaxis().SetLabelSize(0.05)
    hEmpty2D_rp.GetYaxis().SetLabelSize(0.05)
    hEmpty2D_rp.GetXaxis().SetTitleOffset(1.2)
    hEmpty2D_rp.GetYaxis().SetTitleOffset(1.2)
    hEmpty2D_rp.Draw()
    hResponse2D_rp = response_rp.Hresponse().Clone()
    hResponse2D_rp.SetName("plottedResponse_rp")

    hEmpty2D_rp.Draw()
    gStyle.SetPaintTextFormat(".1f")
    hResponse2D_rp.SetMarkerSize(1.2)
    hResponse2D_rp.Draw("colz,same,text")
    hEmpty2D_rp.Draw("axis,same")
    if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_full_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_full_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_full_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        hResponse2D_rp_even = response_rp_even.Hresponse().Clone()
        hResponse2D_rp_even.SetName("plottedResponse_rp_even")

        hEmpty2D_rp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp.Draw("colz,same,text")
        hEmpty2D_rp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_full_odd_"+options.pdf+"_"+options.syst+nobtag+".pdf")

        hEmpty2D_rp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp_even.Draw("colz,same,text")
        hEmpty2D_rp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_full_even_"+options.pdf+"_"+options.syst+nobtag+".pdf")

        hRatio2D_rp = hResponse2D_rp.Clone()
        hRatio2D_rp.Divide(hResponse2D_rp_even)

        hEmpty2D_rp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hRatio2D_rp.Draw("colz,same,text")
        hEmpty2D_rp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_full_ratio_"+options.pdf+"_"+options.syst+nobtag+".pdf")
    
    # normalize so that for each bin of particle-level top pt(eta), the bins in measured top pt(eta) add up to 100%
    nbinsX = hResponse2D_rp.GetNbinsX()
    nbinsY = hResponse2D_rp.GetNbinsY()
    for iby in range(1,nbinsY+1) :
        rowIntegral = hResponse2D_rp.Integral(1,nbinsX,iby,iby)
        #print "for y-bin " + str(iby) + " row integral = " + str(rowIntegral)
        for ibx in range(1,nbinsX+1) :
            binContent = hResponse2D_rp.GetBinContent(ibx,iby)
            newContent = 0
            if rowIntegral > 0:
                newContent = binContent/rowIntegral*100.0
            #print "bin content x-bin " + str(ibx) + " y-bin " + str(iby) + " binContent " + str(binContent) + " newContent " + str(newContent)
            hResponse2D_rp.SetBinContent(ibx,iby,newContent)

    hEmpty2D_rp.Draw()
    hResponse2D_rp.Draw("colz,same,text")
    hEmpty2D_rp.Draw("axis,same")

    cmsTextSize = 0.06
    extraOverCmsTextSize = 0.76
    extraTextSize = extraOverCmsTextSize*cmsTextSize
    
    t1 = TLatex()
    t1.SetNDC()
    t1.SetTextFont(61)
    t1.SetTextAngle(0)
    t1.SetTextColor(1)
    t1.SetTextSize(cmsTextSize)
    t1.DrawLatex(0.18,0.94, "CMS")
    
    t2 = TLatex()
    t2.SetNDC()
    t2.SetTextFont(52)
    t2.SetTextColor(1)
    t2.SetTextSize(extraTextSize)
    t2.DrawLatex(0.28,0.94, "Supplementary")
    
    t3 = TLatex()
    t3.SetNDC()
    t3.SetTextFont(42)
    t3.SetTextColor(1)
    t3.SetTextSize(extraTextSize)
    if (options.lepType == "ele"):
        t3.DrawLatex(0.52,0.94, "(e+jets)")
    else:
        t3.DrawLatex(0.52,0.94, "(#mu+jets)")
    t3.DrawLatex(0.67,0.94, "19.7 fb^{-1} (8 TeV)")    
    
    if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    if options.toUnfold == "pt":
        hEmpty2D_rp.SetAxisRange(450,1150,"X")
        hEmpty2D_rp.SetAxisRange(450,1150,"Y")
        hResponse2D_rp.SetAxisRange(450,1150,"X")
        hResponse2D_rp.SetAxisRange(450,1150,"Y")
        hEmpty2D_rp.Draw()
        hResponse2D_rp.Draw("colz,same,text")
        hEmpty2D_rp.Draw("axis,same")
                
        t1.DrawLatex(0.18,0.94, "CMS")
        t2.DrawLatex(0.28,0.94, "Supplementary")
        if (options.lepType == "ele"):
            t3.DrawLatex(0.52,0.94, "(e+jets)")
        else:
            t3.DrawLatex(0.52,0.94, "(#mu+jets)")
        t3.DrawLatex(0.67,0.94, "19.7 fb^{-1} (8 TeV)")    

        if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")


    response_rp.Hresponse().SetName("responseMatrix_rp_"+options.syst)
    response_rp.Hresponse().Write()
    
    
    # -------------------------------------------------------------------------------------
    ### particle level to parton level 
    hEmpty2D_pp = response_pp.Hresponse().Clone()
    hEmpty2D_pp.SetName("empty2D_pp")
    hEmpty2D_pp.Reset()
    if options.toUnfold == "pt":
        hEmpty2D_pp.GetXaxis().SetTitle("Particle-level t jet p_{T} (GeV)")
        hEmpty2D_pp.GetYaxis().SetTitle("Top quark p_{T} (GeV)")
    if options.toUnfold == "y":
        hEmpty2D_pp.GetXaxis().SetTitle("Particle-level t jet y")
        hEmpty2D_pp.GetYaxis().SetTitle("Top quark y")
    hEmpty2D_pp.GetXaxis().SetLabelSize(0.05)
    hEmpty2D_pp.GetYaxis().SetLabelSize(0.05)
    hEmpty2D_pp.GetXaxis().SetTitleOffset(1.2)
    hEmpty2D_pp.GetYaxis().SetTitleOffset(1.2)
    hEmpty2D_pp.Draw()
    hResponse2D_pp = response_pp.Hresponse().Clone()
    hResponse2D_pp.SetName("plottedResponse_pp")

    gStyle.SetPaintTextFormat(".1f")
    hResponse2D_pp.SetMarkerSize(1.2)
    hResponse2D_pp.Draw("colz,same,text")
    hEmpty2D_pp.Draw("axis,same")
    if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_full_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_full_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_full_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    if options.troubleshoot and options.closureTest and options.whatClosure == "nom":
        hResponse2D_pp_even = response_pp_even.Hresponse().Clone()
        hResponse2D_pp_even.SetName("plottedResponse_pp_even")

        hEmpty2D_pp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp.Draw("colz,same,text")
        hEmpty2D_pp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_full_odd_"+options.pdf+"_"+options.syst+nobtag+".pdf")

        hEmpty2D_pp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp_even.Draw("colz,same,text")
        hEmpty2D_pp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_full_even_"+options.pdf+"_"+options.syst+nobtag+".pdf")

        hRatio2D_pp = hResponse2D_pp.Clone()
        hRatio2D_pp.Divide(hResponse2D_pp_even)

        hEmpty2D_pp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hRatio2D_pp.Draw("colz,same,text")
        hEmpty2D_pp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_full_ratio_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    # normalize so that for each bin of particle-level top pt(eta), the bins in measured top pt(eta) add up to 100%
    nbinsX = hResponse2D_pp.GetNbinsX()
    nbinsY = hResponse2D_pp.GetNbinsY()
    for iby in range(1,nbinsY+1) :
        rowIntegral = hResponse2D_pp.Integral(1,nbinsX,iby,iby)
        #print "for y-bin " + str(iby) + " row integral = " + str(rowIntegral)
        for ibx in range(1,nbinsX+1) :
            binContent = hResponse2D_pp.GetBinContent(ibx,iby)
            newContent = 0
            if rowIntegral > 0:
                newContent = binContent/rowIntegral*100.0
            #print "bin content x-bin " + str(ibx) + " y-bin " + str(iby) + " binContent " + str(binContent) + " newContent " + str(newContent)
            hResponse2D_pp.SetBinContent(ibx,iby,newContent)

    hResponse2D_pp.Draw("colz,same,text")
    hEmpty2D_pp.Draw("axis,same")
    
    cmsTextSize = 0.06
    extraOverCmsTextSize = 0.76
    extraTextSize = extraOverCmsTextSize*cmsTextSize
    
    t1 = TLatex()
    t1.SetNDC()
    t1.SetTextFont(61)
    t1.SetTextAngle(0)
    t1.SetTextColor(1)
    t1.SetTextSize(cmsTextSize)
    t1.DrawLatex(0.18,0.94, "CMS")
    
    t2 = TLatex()
    t2.SetNDC()
    t2.SetTextFont(52)
    t2.SetTextColor(1)
    t2.SetTextSize(extraTextSize)
    t2.DrawLatex(0.28,0.94, "Supplementary")
    
    t3 = TLatex()
    t3.SetNDC()
    t3.SetTextFont(42)
    t3.SetTextColor(1)
    t3.SetTextSize(extraTextSize)
    if (options.lepType == "ele"):
        t3.DrawLatex(0.52,0.94, "(e+jets)")
    else:
        t3.DrawLatex(0.52,0.94, "(#mu+jets)")
    t3.DrawLatex(0.67,0.94, "19.7 fb^{-1} (8 TeV)")    

    if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    if options.toUnfold == "pt":
        hEmpty2D_pp.SetAxisRange(450,1150,"X")
        hEmpty2D_pp.SetAxisRange(450,1150,"Y")
        hResponse2D_pp.SetAxisRange(450,1150,"X")
        hResponse2D_pp.SetAxisRange(450,1150,"Y")
        hEmpty2D_pp.Draw()
        hResponse2D_pp.Draw("colz,same,text")
        hEmpty2D_pp.Draw("axis,same")
        
        t1.DrawLatex(0.18,0.94, "CMS")
        t2.DrawLatex(0.28,0.94, "Supplementary")
        if (options.lepType == "ele"):
            t3.DrawLatex(0.52,0.94, "(e+jets)")
        else:
            t3.DrawLatex(0.52,0.94, "(#mu+jets)")
        t3.DrawLatex(0.67,0.94, "19.7 fb^{-1} (8 TeV)")    
    
        if options.syst=="nom" and options.bkgSyst=="nom" and options.closureTest==False:
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
            cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_"+options.toUnfold+"_2step"+closureout+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    response_pp.Hresponse().SetName("responseMatrix_pp_"+options.syst)
    response_pp.Hresponse().Write()



fout.Close()
