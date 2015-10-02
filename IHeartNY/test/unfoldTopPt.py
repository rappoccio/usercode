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
                  help='What type of closure test?')

parser.add_option('--normalize', metavar='F', action='store_true',
                  default=False,
                  dest='normalize',
                  help='Do normalized differential cross section')

parser.add_option('--scale', metavar='F', action='store_true',
                  default=False,
                  dest='scale',
                  help='Scale total cross section to value from theta / MC ???')

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

gROOT.Macro("rootlogon.C")

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
  
gSystem.Load("RooUnfold-1.1.1/libRooUnfold.so")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd


# -------------------------------------------------------------------------------------
# scale unfolded cross section to value from theta / MC ??? 
# -------------------------------------------------------------------------------------

if options.pdf=="MG" and options.whatClosure != "reverse":
    tmp_xs_parton   =  [1844.47, 1846.56]
    tmp_xs_particle = [1491.67, 1513.0]
elif options.pdf=="mcnlo" and options.whatClosure != "reverse":
    tmp_xs_parton   = [1402.3, 1395.71]
    tmp_xs_particle = [1188.57, 1195.22]
else:
    tmp_xs_parton   = [1662.91, 1674.3]
    tmp_xs_particle = [1483.66, 1502.36]

tmp_xs_theta_parton   = [1662.91*0.86, 1674.3*0.86]
tmp_xs_theta_particle = [1483.66*0.86, 1502.36*0.86]

if options.lepType=="muon":
    xs_parton = tmp_xs_parton[0]    
    xs_particle = tmp_xs_particle[0]    
    xs_theta_parton = tmp_xs_theta_parton[0]    
    xs_theta_particle = tmp_xs_theta_particle[0]    
else :
    xs_parton = tmp_xs_parton[1]
    xs_particle = tmp_xs_particle[1]    
    xs_theta_parton = tmp_xs_theta_parton[1]    
    xs_theta_particle = tmp_xs_theta_particle[1] 

  
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
    f_ttbar_max700_odd = TFile("histfiles_mcnlo/TT_mcatnlo_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
## unfold MC@NLO ttbar sample using Powheg response matrix
elif options.pdf == "mcnlo" and options.closureTest == True :
    f_ttbar_max700 = TFile("histfiles_mcnlo/TT_mcatnlo_iheartNY_V1_"+muOrEl+"_2Dcut_"+postname+"nom.root")
    f_ttbar_max700_odd    = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_700to1000_odd = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
    f_ttbar_1000toInf_odd = TFile("histfiles_CT10_nom/"+ttDIR+"/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_"+muOrEl+"_CT10_nom_2Dcut_"+postname+options.syst+".root")
## MC@NLO
elif options.pdf == "mcnlo":
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
    response_ttbar_max700    = f_ttbar_max700_odd.Get("response_pt"+nobtag)
    response = response_ttbar_max700.Clone()
    response.SetName("response_pt_"+options.syst)
elif options.closureTest == True and options.whatClosure=="nom":
    ## regular closure test, unfolding some distribution using Powheg as response mastrix 
    response_ttbar_max700    = f_ttbar_max700_odd.Get("response_pt"+nobtag)
    response_ttbar_700to1000 = f_ttbar_700to1000_odd.Get("response_pt"+nobtag)
    response_ttbar_1000toInf = f_ttbar_1000toInf_odd.Get("response_pt"+nobtag)
    response = response_ttbar_max700.Clone()
    response.SetName("response_pt_"+options.syst)
    response.Add(response_ttbar_700to1000)
    response.Add(response_ttbar_1000toInf)
elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == False: 
    response_ttbar_max700 = f_ttbar_max700.Get("response_pt"+nobtag)
    response = response_ttbar_max700.Clone()
    response.SetName("response_pt_"+options.syst)
else :
    response_ttbar_max700    = f_ttbar_max700.Get("response_pt"+nobtag)
    response_ttbar_700to1000 = f_ttbar_700to1000.Get("response_pt"+nobtag)
    response_ttbar_1000toInf = f_ttbar_1000toInf.Get("response_pt"+nobtag)
    response = response_ttbar_max700.Clone()
    response.SetName("response_pt_"+options.syst)
    response.Add(response_ttbar_700to1000)
    response.Add(response_ttbar_1000toInf)


## response matrices for two-step unfolding
if options.twoStep == True :
    if (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and options.whatClosure=="reverse":
        response_ttbar_max700_rp = f_ttbar_max700_odd.Get("response_pt"+nobtag+"_rp")
        response_ttbar_max700_pp = f_ttbar_max700_odd.Get("response_pt_pp")
        
        response_rp = response_ttbar_max700_rp.Clone()
        response_rp.SetName("response_pt_"+options.syst+"_rp")
        response_pp = response_ttbar_max700_pp.Clone()
        response_pp.SetName("response_pt_"+options.syst+"_pp")
    
    elif options.closureTest == True and options.whatClosure=="nom": 
        response_ttbar_max700_rp    = f_ttbar_max700_odd.Get("response_pt"+nobtag+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000_odd.Get("response_pt"+nobtag+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf_odd.Get("response_pt"+nobtag+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700_odd.Get("response_pt_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000_odd.Get("response_pt_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf_odd.Get("response_pt_pp")

        response_rp = response_ttbar_max700_rp.Clone()
        response_rp.SetName("response_pt_"+options.syst+"_rp")
        response_rp.Add(response_ttbar_700to1000_rp)
        response_rp.Add(response_ttbar_1000toInf_rp)
        response_pp = response_ttbar_max700_pp.Clone()
        response_pp.SetName("response_pt_"+options.syst+"_pp")
        response_pp.Add(response_ttbar_700to1000_pp)
        response_pp.Add(response_ttbar_1000toInf_pp)

        if options.troubleshoot == True:
            response_ttbar_max700_rp_even    = f_ttbar_max700.Get("response_pt"+nobtag+"_rp")
            response_ttbar_700to1000_rp_even = f_ttbar_700to1000.Get("response_pt"+nobtag+"_rp")
            response_ttbar_1000toInf_rp_even = f_ttbar_1000toInf.Get("response_pt"+nobtag+"_rp")
            response_ttbar_max700_pp_even    = f_ttbar_max700.Get("response_pt_pp")
            response_ttbar_700to1000_pp_even = f_ttbar_700to1000.Get("response_pt_pp")
            response_ttbar_1000toInf_pp_even = f_ttbar_1000toInf.Get("response_pt_pp")
    
    elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == False:
        response_ttbar_max700_rp = f_ttbar_max700.Get("response_pt"+nobtag+"_rp")
        response_ttbar_max700_pp = f_ttbar_max700.Get("response_pt_pp")
        
        response_rp = response_ttbar_max700_rp.Clone()
        response_rp.SetName("response_pt_"+options.syst+"_rp")
        response_pp = response_ttbar_max700_pp.Clone()
        response_pp.SetName("response_pt_"+options.syst+"_pp")
    
    else:
        response_ttbar_max700_rp    = f_ttbar_max700.Get("response_pt"+nobtag+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000.Get("response_pt"+nobtag+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf.Get("response_pt"+nobtag+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700.Get("response_pt_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000.Get("response_pt_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf.Get("response_pt_pp")

        response_rp = response_ttbar_max700_rp.Clone()
        response_rp.SetName("response_pt_"+options.syst+"_rp")
        response_rp.Add(response_ttbar_700to1000_rp)
        response_rp.Add(response_ttbar_1000toInf_rp)
        response_pp = response_ttbar_max700_pp.Clone()
        response_pp.SetName("response_pt_"+options.syst+"_pp")
        response_pp.Add(response_ttbar_700to1000_pp)
        response_pp.Add(response_ttbar_1000toInf_pp)

    if options.troubleshoot and options.closureTest == True and options.whatClosure=="nom":
        response_rp_even = response_ttbar_max700_rp_even.Clone()
        response_rp_even.SetName("response_pt_"+options.syst+"_rp_even")
        response_rp_even.Add(response_ttbar_700to1000_rp_even)
        response_rp_even.Add(response_ttbar_1000toInf_rp_even)
        
        response_pp_even = response_ttbar_max700_pp_even.Clone()
        response_pp_even.SetName("response_pt_"+options.syst+"_pp_even")
        response_pp_even.Add(response_ttbar_700to1000_pp_even)
        response_pp_even.Add(response_ttbar_1000toInf_pp_even)


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
if options.twoStep :
    fout = TFile("UnfoldingPlots/unfold"+DIR+"_2step_"+options.pdf+"_"+options.syst+bkgout+nobtag+closureout+".root","recreate");
else :
    fout = TFile("UnfoldingPlots/unfold"+DIR+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+closureout+".root","recreate");


# -------------------------------------------------------------------------------------
# read actual histograms
# -------------------------------------------------------------------------------------

if (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and options.whatClosure=="nom":
    # use truth-level distributions (and reco-level) from MC@NLO/MadGraph
    hTrue_max700    = f_ttbar_max700.Get("ptGenTop")  
    hTrue_max700.Sumw2()
    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get("ptPartTop")
        hPart_max700.Sumw2()
elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == False:
    hTrue_max700    = f_ttbar_max700.Get("ptGenTop")  
    hTrue_max700.Sumw2()
    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get("ptPartTop")
        hPart_max700.Sumw2()
else :
    hTrue_max700    = f_ttbar_max700.Get("ptGenTop")
    hTrue_700to1000 = f_ttbar_700to1000.Get("ptGenTop")
    hTrue_1000toInf = f_ttbar_1000toInf.Get("ptGenTop")
    hTrue_max700.Sumw2()
    hTrue_700to1000.Sumw2()
    hTrue_1000toInf.Sumw2()

    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get("ptPartTop")
        hPart_700to1000 = f_ttbar_700to1000.Get("ptPartTop")
        hPart_1000toInf = f_ttbar_1000toInf.Get("ptPartTop")
        hPart_max700.Sumw2()
        hPart_700to1000.Sumw2()
        hPart_1000toInf.Sumw2()

        if options.troubleshoot and  options.closureTest == True and options.whatClosure=="nom":
            hTrue_max700_even    = f_ttbar_max700_odd.Get("ptGenTop")
            hTrue_700to1000_even = f_ttbar_700to1000_odd.Get("ptGenTop")
            hTrue_1000toInf_even = f_ttbar_1000toInf_odd.Get("ptGenTop")
            hPart_max700_even    = f_ttbar_max700_odd.Get("ptPartTop")
            hPart_700to1000_even = f_ttbar_700to1000_odd.Get("ptPartTop")
            hPart_1000toInf_even = f_ttbar_1000toInf_odd.Get("ptPartTop")
            hTrue_max700_even.Sumw2()
            hTrue_700to1000_even.Sumw2()
            hTrue_1000toInf_even.Sumw2()
            hPart_max700_even.Sumw2()
            hPart_700to1000_even.Sumw2()
            hPart_1000toInf_even.Sumw2()

isTwoStep = ""
if options.twoStep:
    isTwoStep = "_2step"
   

hRecoData = f_data.Get("ptRecoTop"+isTwoStep+nobtag).Clone()
hRecoData.SetName("hRecoData")

hRecoQCD = f_QCD.Get("ptRecoTop"+isTwoStep+nobtag).Clone()
hRecoQCD.SetName("hRecoQCD")
hRecoQCD.Sumw2()
hRecoQCD.SetFillColor(TColor.kYellow)

if options.closureTest == False: 
    hMeas = f_data.Get("ptRecoTop"+isTwoStep+nobtag)
elif options.closureTest == True and options.whatClosure == "data": 
    # data distribution
    hMeas = f_data.Get("ptRecoTop"+isTwoStep+nobtag)
    # ttbar prediction to scale data
    hMeas_max700    = f_ttbar_max700.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_700to1000 = f_ttbar_700to1000.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_max700.Sumw2()
    hMeas_700to1000.Sumw2()
    hMeas_1000toInf.Sumw2()
elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True and options.whatClosure=="nom":
    # use truth-level distributions (and reco-level) from MC@NLO/MadGraph
    hMeas_max700    = f_ttbar_max700.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_max700.Sumw2()
else :
    hMeas_max700    = f_ttbar_max700.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_700to1000 = f_ttbar_700to1000.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag)
    hMeas_max700.Sumw2()
    hMeas_700to1000.Sumw2()
    hMeas_1000toInf.Sumw2()

    if options.troubleshoot :
        hMeas_max700_odd    = f_ttbar_max700_odd.Get("ptRecoTop"+isTwoStep+nobtag)
        hMeas_700to1000_odd = f_ttbar_700to1000_odd.Get("ptRecoTop"+isTwoStep+nobtag)
        hMeas_1000toInf_odd = f_ttbar_1000toInf_odd.Get("ptRecoTop"+isTwoStep+nobtag)
        hMeas_max700_odd.Sumw2()
        hMeas_700to1000_odd.Sumw2()
        hMeas_1000toInf_odd.Sumw2()
    

hMeas_T_t     = f_T_t.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_Tbar_t  = f_Tbar_t.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_T_s     = f_T_s.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_Tbar_s  = f_Tbar_s.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_T_tW    = f_T_tW.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_Tbar_tW = f_Tbar_tW.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_WJets_1jet   = f_WJets_1jet.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_WJets_2jet   = f_WJets_2jet.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_WJets_3jet   = f_WJets_3jet.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_WJets_4jet   = f_WJets_4jet.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_tt0_nonsemi = f_ttbar_nonsemilep_max700.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_tt700_nonsemi = f_ttbar_nonsemilep_700to1000.Get("ptRecoTop"+isTwoStep+nobtag)
hMeas_tt1000_nonsemi = f_ttbar_nonsemilep_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag)

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
if options.pdf == "MG" and options.closureTest == True and options.whatClosure=="nom":
    hMeas_max700.Scale(252.89*1000.0*19.7/25424818.*0.438)
    hMeas = hMeas_max700.Clone()
    hMeas.SetName("ptRecoTop_measured")
elif options.pdf == "mcnlo" and options.closureTest == True and options.whatClosure=="nom":
    hMeas_max700.Scale(252.89*1000.0*19.7/32852589)
    hMeas = hMeas_max700.Clone()
    hMeas.SetName("ptRecoTop_measured")
# ttbar nominal as "measured" distribution
elif options.closureTest == True and options.whatClosure != "data": 
    hMeas_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hMeas_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hMeas_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hMeas = hMeas_max700.Clone()
    hMeas.SetName("ptRecoTop_measured")
    hMeas.Add(hMeas_700to1000)
    hMeas.Add(hMeas_1000toInf)    

    if options.troubleshoot :
        hMeas_max700_odd.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
        hMeas_700to1000_odd.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
        hMeas_1000toInf_odd.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
        hMeas_odd = hMeas_max700_odd.Clone()
        hMeas_odd.SetName("ptRecoTop_measured_odd")
        hMeas_odd.Add(hMeas_700to1000_odd)
        hMeas_odd.Add(hMeas_1000toInf_odd)    
# for closure test of data, need ttbar
elif options.closureTest == True and options.whatClosure == "data": 
    hMeas_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hMeas_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hMeas_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hMeasTT = hMeas_max700.Clone()
    hMeasTT.SetName("ptRecoTop_TT")
    hMeasTT.Add(hMeas_700to1000)
    hMeasTT.Add(hMeas_1000toInf)
        
    
if options.pdf == "MG" and ((options.closureTest == True and options.whatClosure=="nom") or options.closureTest == False): 
    hTrue_max700.Scale(252.89*1000.0*19.7/25424818.*0.438)
    hTrue = hTrue_max700.Clone()
    hTrue.SetName("pt_genTop")
elif options.pdf == "mcnlo" and ((options.closureTest == True and options.whatClosure=="nom") or options.closureTest == False): 
    hTrue_max700.Scale(252.89*1000.0*19.7/32852589)
    hTrue = hTrue_max700.Clone()
    hTrue.SetName("pt_genTop")
else :
    hTrue_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hTrue_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hTrue_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hTrue = hTrue_max700.Clone()
    hTrue.SetName("pt_genTop")
    hTrue.Add(hTrue_700to1000)
    hTrue.Add(hTrue_1000toInf)

if options.troubleshoot and options.twoStep :
    hTrue_max700_even.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hTrue_700to1000_even.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hTrue_1000toInf_even.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hTrue_even = hTrue_max700_even.Clone()
    hTrue_even.SetName("pt_genTop_even")
    hTrue_even.Add(hTrue_700to1000_even)
    hTrue_even.Add(hTrue_1000toInf_even)

if options.twoStep :
    if options.pdf == "MG" and ((options.closureTest == True and options.whatClosure=="nom") or options.closureTest == False):
        hPart_max700.Scale(252.89*1000.0*19.7/25424818.*0.438)
        hPart = hPart_max700.Clone()
        hPart.SetName("pt_partTop")
    elif options.pdf == "mcnlo" and ((options.closureTest == True and options.whatClosure=="nom") or options.closureTest == False): 
        hPart_max700.Scale(252.89*1000.0*19.7/32852589)
        hPart = hPart_max700.Clone()
        hPart.SetName("pt_partTop")
    else :
        hPart_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
        hPart_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
        hPart_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
        hPart = hPart_max700.Clone()
        hPart.SetName("pt_partTop")
        hPart.Add(hPart_700to1000)
        hPart.Add(hPart_1000toInf)

    if options.troubleshoot :
        hPart_max700_even.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
        hPart_700to1000_even.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
        hPart_1000toInf_even.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
        hPart_even = hPart_max700_even.Clone()
        hPart_even.SetName("pt_partTop_even")
        hPart_even.Add(hPart_700to1000_even)
        hPart_even.Add(hPart_1000toInf_even)

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
hMeas_SingleTop.SetName("ptRecoTop_SingleTop")

hMeas_WJets = hMeas_WJets_1jet.Clone()
hMeas_WJets.SetName("ptRecoTop_WJets")

for hist in [hMeas_Tbar_t, hMeas_T_s, hMeas_Tbar_s, hMeas_T_tW, hMeas_Tbar_tW] :
    hMeas_SingleTop.Add( hist )
for hist in [hMeas_WJets_2jet,hMeas_WJets_3jet,hMeas_WJets_4jet] :
    hMeas_WJets.Add( hist )

hMeas_tt0_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
hMeas_tt700_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
hMeas_tt1000_nonsemi.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))

hMeas_TTNonSemi = hMeas_tt0_nonsemi.Clone()
hMeas_TTNonSemi.SetName("ptRecoTop_TTNonSemilep")
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

if options.closureTest and options.troubleshoot and options.twoStep :
    ct1 = TCanvas("ct1", "", 800, 600)
    
    lt1 = TLegend(0.4, 0.65, 0.7, 0.9)
    lt1.SetFillStyle(0)
    lt1.SetTextFont(42)
    lt1.SetTextSize(0.045)
    lt1.SetBorderSize(0)
    
    hMeas.SetLineColor(2)
    hMeas.SetLineWidth(2)
    hMeas_odd.SetLineColor(4)
    hMeas_odd.SetLineWidth(2)
    hMeas.Draw("hist")
    hMeas_odd.Draw("hist,same")
    lt1.AddEntry(hMeas, "Unfolding input, even","l")
    lt1.AddEntry(hMeas_odd, "Unfolding input, odd","l")
    lt1.Draw()
    ct1.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hMeas_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png")

    ct2 = TCanvas("ct2", "", 800, 600)
    
    lt2 = TLegend(0.4, 0.65, 0.7, 0.9)
    lt2.SetFillStyle(0)
    lt2.SetTextFont(42)
    lt2.SetTextSize(0.045)
    lt2.SetBorderSize(0)
    
    hPart_even.SetLineColor(2)
    hPart_even.SetLineWidth(2)
    hPart.SetLineColor(4)
    hPart.SetLineWidth(2)
    hPart_even.Draw("hist")
    hPart.Draw("hist,same")
    lt2.AddEntry(hPart_even, "Particle-level truth, even","l")
    lt2.AddEntry(hPart, "Particle-level truth, odd","l")
    lt2.Draw()
    ct2.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hPart_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png")

    ct3 = TCanvas("ct3", "", 800, 600)
    
    lt3 = TLegend(0.4, 0.65, 0.7, 0.9)
    lt3.SetFillStyle(0)
    lt3.SetTextFont(42)
    lt3.SetTextSize(0.045)
    lt3.SetBorderSize(0)
    
    hTrue_even.SetLineColor(2)
    hTrue_even.SetLineWidth(2)
    hTrue.SetLineColor(4)
    hTrue.SetLineWidth(2)
    hTrue_even.Draw("hist")
    hTrue.Draw("hist,same")
    lt3.AddEntry(hTrue_even, "Parton-level truth, even","l")
    lt3.AddEntry(hTrue, "Parton-level truth, odd","l")
    lt3.Draw()
    ct3.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_hTrue_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png")


    
# -------------------------------------------------------------------------------------
# do the actual unfolding
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# one-step unfolding
if options.twoStep == False:                
    
    print "------------ UNFOLDING (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold = RooUnfoldBayes(response, hMeas, 4);
    unfold = RooUnfoldSvd(response, hMeas, 2);
    #unfold = RooUnfoldTUnfold(response, hMeas);
    
    # get the unfolded distribution
    hReco = unfold.Hreco()


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


# -------------------------------------------------------------------------------------
# Translate to cross section (not events) in bins of pt N/L/BR)
# -------------------------------------------------------------------------------------

hTrue.Scale(1.0/(lum*4/27)) # true @ parton level
hMeas.Scale(1.0/(lum*4/27)) # measured @ reco level
hReco.Scale(1.0/(lum*4/27)) # unfolded to parton level
if options.twoStep:
    hPart.Scale(1.0/(lum*4/27))    # true @ parton level
    hReco_rp.Scale(1.0/(lum*4/27)) # unfolded to particle level

    
# -------------------------------------------------------------------------------------
# Adjust for bin width
# -------------------------------------------------------------------------------------

sumReco = 0
sumTrue = 0
sumMeas = 0
sumReco_rp = 0
sumPart = 0
for ibin in range(1, hTrue.GetXaxis().GetNbins()+1 ) :

    # total cross section for pt > 400 GeV 
    if hReco.GetBinLowEdge(ibin) > 399. :
        sumReco += hReco.GetBinContent(ibin)
    if hTrue.GetBinLowEdge(ibin) > 399. :
        sumTrue += hTrue.GetBinContent(ibin)
    if hMeas.GetBinLowEdge(ibin) > 399. :
        sumMeas += hMeas.GetBinContent(ibin)
    if options.twoStep:
        if hReco_rp.GetBinLowEdge(ibin) > 399. :
            sumReco_rp += hReco_rp.GetBinContent(ibin)
        if hPart.GetBinLowEdge(ibin) > 399. :
            sumPart += hPart.GetBinContent(ibin)

    width = hTrue.GetBinWidth(ibin)
    
    hMeas.SetBinContent(ibin,  hMeas.GetBinContent(ibin) / width )
    hMeas.SetBinError(ibin,  hMeas.GetBinError(ibin) / width )

    hTrue.SetBinContent(ibin, hTrue.GetBinContent(ibin) / width )
    hTrue.SetBinError(ibin, hTrue.GetBinError(ibin) / width )

    hReco.SetBinContent(ibin, hReco.GetBinContent(ibin) / width )
    hReco.SetBinError(ibin, hReco.GetBinError(ibin) / width )
    if options.twoStep:
        hReco_rp.SetBinContent(ibin, hReco_rp.GetBinContent(ibin) / width )
        hReco_rp.SetBinError(ibin, hReco_rp.GetBinError(ibin) / width )
        hPart.SetBinContent(ibin, hPart.GetBinContent(ibin) / width )
        hPart.SetBinError(ibin, hPart.GetBinError(ibin) / width )            


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
# SCALE to total cross section from theta / MC ???
# -------------------------------------------------------------------------------------

if options.scale and options.closureTest == False: 
    hTrue.Scale(xs_parton/sumTrue)
    hReco.Scale(xs_theta_parton/sumReco)
    if options.twoStep:
        hReco_rp.Scale(xs_theta_particle/sumReco_rp)
        hPart.Scale(xs_particle/sumPart)
elif options.closureTest == True: 
    hTrue.Scale(xs_parton/sumTrue)
    hReco.Scale(xs_parton/sumTrue)
    if options.twoStep:
        hReco_rp.Scale(xs_particle/sumPart)
        hPart.Scale(xs_particle/sumPart)
    
        
# -------------------------------------------------------------------------------------
# print & draw
# -------------------------------------------------------------------------------------

## ratio of unfolded data to generator-level 
hFrac = hReco.Clone()
hFrac.SetName("hFrac")
hFrac.SetTitle(";Top quark p_{T} (GeV);Data/MC")
hFrac.Divide(hTrue)

## ratio of unfolded data to particle-level 
if options.twoStep:
    hFrac_rp = hReco_rp.Clone()
    hFrac_rp.SetName("hFrac_rp")
    hFrac_rp.SetTitle(";Particle-level top p_{T} (GeV);Data/MC")
    hFrac_rp.Divide(hPart)

if options.closureTest and options.whatClosure == "reverse":
    print ''
    print '-------------------------------------------------------------------------------------'
    print 'uncertainty from closure test for ' + options.pdf + ' ' + options.whatClosure
    print '-------------------------------------------------------------------------------------'
    print 'parton-level'
    for ibin in range(1, hFrac.GetXaxis().GetNbins()+1 ) :
        
        if hFrac.GetBinLowEdge(ibin) > 399. and hFrac.GetBinLowEdge(ibin) < 1199.:
            print '[' + str(hFrac.GetBinLowEdge(ibin)) + ',' + str(hFrac.GetBinLowEdge(ibin+1)) + '] = ' + str((hFrac.GetBinContent(ibin)-1.0)*100.0) + ' %' 
    if options.twoStep:
        print ''
        print 'particle-level'
        for ibin in range(1, hFrac_rp.GetXaxis().GetNbins()+1 ) :
            
            if hFrac_rp.GetBinLowEdge(ibin) > 399. and hFrac_rp.GetBinLowEdge(ibin) < 1199.:
                print '[' + str(hFrac_rp.GetBinLowEdge(ibin)) + ',' + str(hFrac_rp.GetBinLowEdge(ibin+1)) + '] = ' + str((hFrac_rp.GetBinContent(ibin)-1.0)*100.0) + ' %' 
    

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

hReco.GetXaxis().SetRangeUser(400.,1200.)
hTrue.GetXaxis().SetRangeUser(400.,1200.)
hMeas.GetXaxis().SetRangeUser(400.,1200.)


xsec_title = ";;d#sigma/dp_{T} [fb/GeV]"
if options.normalize:    
    xsec_title = ";;1/#sigma d#sigma/dp_{T} [1/GeV]"

hReco.SetTitle(xsec_title)
hReco.GetYaxis().SetTitleOffset(1.2)
hReco.SetMinimum(0.0)
max = hTrue.GetMaximum()
max2 = hReco.GetMaximum()
if max2 > max:
	max = max2
hReco.SetAxisRange(0,max*1.07,"Y")
hReco.Draw()
hTrue.Draw('hist same')
hMeas.Draw('same')
hTrue.UseCurrentStyle()
hTrue.SetLineColor(4);
hTrue.GetYaxis().SetTitleSize(25)
hTrue.GetXaxis().SetLabelSize(0)


leg = TLegend(0.45, 0.55, 0.85, 0.75)
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
    tt.DrawLatex(0.5,0.45, "Closure test, response")
    if options.pdf == "MG":
        tt.DrawLatex(0.5,0.40, "matrix from MadGraph")
    else: 
        tt.DrawLatex(0.5,0.40, "matrix from MC@NLO")
elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True:
    if options.pdf == "MG":
        leg.AddEntry( hReco, 'MadGraph (unfolded)', 'p')
        leg.AddEntry( hTrue, 'MadGraph (generated)', 'l')
        leg.AddEntry( hMeas, 'MadGraph (reco-level)', 'p')
    else :
        leg.AddEntry( hReco, 'MC@NLO (unfolded)', 'p')
        leg.AddEntry( hTrue, 'MC@NLO (generated)', 'l')
        leg.AddEntry( hMeas, 'MC@NLO (reco-level)', 'p')
    tt.DrawLatex(0.5,0.45, "Closure test, response")
    tt.DrawLatex(0.5,0.40, "matrix from Powheg")
else : 
    leg.AddEntry( hReco, 'Unfolded MC (Powheg)', 'p')
    leg.AddEntry( hTrue, 'Generated (Powheg)', 'l')
    leg.AddEntry( hMeas, 'Reco-level (Powheg)', 'p')
    tt.DrawLatex(0.5,0.45, "MC closure test")
    
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
text1.DrawLatex(0.5,0.8, "#scale[1.0]{L = 19.7 fb^{-1} at #sqrt{s} = 8 TeV}")


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

append = ""
if options.twoStep :
    append += "_2step"
if options.closureTest :
    append += "_closure"
if options.whatClosure == "reverse" :
    append += "_reverse"
    
if options.pdf == "CT10_nom" or options.pdf == "MG" or options.pdf == "mcnlo" or options.troubleshoot:
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".pdf", "pdf")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png", "png")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".eps", "eps")



# -------------------------------------------------------------------------------------
# draw particle-level unfolding
# -------------------------------------------------------------------------------------

if options.twoStep:
    pad1.cd();

    hReco_rp.SetMarkerStyle(21)
    hMeas.SetMarkerStyle(25);

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
    hReco_rp.SetAxisRange(0,max*1.07,"Y")
    hReco_rp.Draw()
    hPart.Draw('hist same')
    hMeas.Draw('same')
    hPart.UseCurrentStyle()
    hPart.SetLineColor(4);
    hPart.GetYaxis().SetTitleSize(25)
    hPart.GetXaxis().SetLabelSize(0)

        
    leg2 = TLegend(0.45, 0.55, 0.85, 0.75)
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
        tt.DrawLatex(0.5,0.45, "Closure test, response")
        if options.pdf == "MG":
            tt.DrawLatex(0.5,0.40, "matrix from MadGraph")
        else: 
            tt.DrawLatex(0.5,0.40, "matrix from MC@NLO")
    elif (options.pdf == "MG" or options.pdf == "mcnlo") and options.closureTest == True:
        if options.pdf == "MG":
            leg2.AddEntry( hReco, 'MadGraph (unfolded)', 'p')
            leg2.AddEntry( hTrue, 'MadGraph (generated)', 'l')
            leg2.AddEntry( hMeas, 'MadGraph (reco-level)', 'p')
        else :
            leg2.AddEntry( hReco, 'MC@NLO (unfolded)', 'p')
            leg2.AddEntry( hTrue, 'MC@NLO (generated)', 'l')
            leg2.AddEntry( hMeas, 'MC@NLO (reco-level)', 'p')
        tt.DrawLatex(0.5,0.45, "Closure test, response")
        tt.DrawLatex(0.5,0.40, "matrix from Powheg")
    else : 
        leg2.AddEntry( hReco, 'Unfolded MC (Powheg)', 'p')
        leg2.AddEntry( hTrue, 'Generated (Powheg)', 'l')
        leg2.AddEntry( hMeas, 'Reco-level (Powheg)', 'p')
        tt.DrawLatex(0.5,0.45, "MC closure test")
    
    leg2.Draw()

    # write histograms to file
    if options.closureTest:
        hReco_rp.SetName("UnfoldedMC_rp")
    else:
        hReco_rp.SetName("UnfoldedData_rp")

    hReco_rp.Write()
    hPart.Write()
    hMeas.Write()

    text1.DrawLatex(0.5,0.8, "#scale[1.0]{L = 19.7 fb^{-1} at #sqrt{s} = 8 TeV}")

    c1.cd()
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
    hFrac_rp.GetXaxis().SetRangeUser(400., 1200.)

    c1.Update()

    append = ""
    if options.closureTest :
        append += "_closure"
    if options.whatClosure == "reverse" :
        append += "_reverse"
    
    if options.pdf == "CT10_nom" or options.pdf == "MG" or options.pdf == "mcnlo" or options.troubleshoot:
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".pdf", "pdf")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".png", "png")
        c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+DIR+"_2step_particle"+append+"_"+options.pdf+"_"+options.syst+bkgout+nobtag+".eps", "eps")



# -------------------------------------------------------------------------------------
# plot response matrices 
# (do this in the end as the normalization otherwise will mess up the unfolding result!)
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# one-step unfolding
# -------------------------------------------------------------------------------------

gStyle.SetPadRightMargin(0.12);
cr = TCanvas("c_response", "", 800, 600)

if options.twoStep == False:
    
    hEmpty2D = response.Hresponse().Clone()
    hEmpty2D.SetName("empty2D")
    hEmpty2D.Reset()
    hEmpty2D.GetXaxis().SetTitle("Reconstructed top-jet p_{T} (GeV)")
    hEmpty2D.GetYaxis().SetTitle("Top quark p_{T} (GeV)")
    hEmpty2D.GetXaxis().SetLabelSize(0.045)
    hEmpty2D.GetYaxis().SetLabelSize(0.045)
    hEmpty2D.Draw()
    hResponse2D = response.Hresponse().Clone()
    hResponse2D.SetName("plottedResponse")
    
    # normalize so that for each bin of true top quark pt, the bins in measured top pt add up to 100%
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

    gStyle.SetPaintTextFormat(".1f")
    hResponse2D.Draw("colz,same,text")
    hEmpty2D.Draw("axis,same")
    if (options.pdf == "CT10_nom" or options.pdf == "MG" or options.pdf == "mcnlo" or options.troubleshoot) and options.closureTest == False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    hEmpty2D.SetAxisRange(450,1150,"X")
    hEmpty2D.SetAxisRange(450,1150,"Y")
    hResponse2D.SetAxisRange(450,1150,"X")
    hResponse2D.SetAxisRange(450,1150,"Y")
    hEmpty2D.Draw()
    hResponse2D.Draw("colz,same,text")
    hEmpty2D.Draw("axis,same")

    if (options.pdf == "CT10_nom" or options.pdf == "MG" or options.pdf == "mcnlo" or options.troubleshoot) and options.closureTest == False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_responseMatrix_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")
        
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
    hEmpty2D_rp.GetXaxis().SetTitle("Reconstructed top-jet p_{T} (GeV)")
    hEmpty2D_rp.GetYaxis().SetTitle("Particle-level top p_{T} (GeV)")
    hEmpty2D_rp.GetXaxis().SetLabelSize(0.05)
    hEmpty2D_rp.GetYaxis().SetLabelSize(0.05)
    hEmpty2D_rp.GetXaxis().SetTitleOffset(1.2)
    hEmpty2D_rp.GetYaxis().SetTitleOffset(1.2)
    hEmpty2D_rp.Draw()
    hResponse2D_rp = response_rp.Hresponse().Clone()
    hResponse2D_rp.SetName("plottedResponse_rp")

    if options.troubleshoot :
        hEmpty2D_rp_even = response_rp_even.Hresponse().Clone()
        hEmpty2D_rp_even.SetName("empty2D_rp_even")
        hEmpty2D_rp_even.Reset()
        hEmpty2D_rp_even.GetXaxis().SetTitle("Reconstructed top-jet p_{T} (GeV)")
        hEmpty2D_rp_even.GetYaxis().SetTitle("Particle-level top p_{T} (GeV)")
        hEmpty2D_rp_even.GetXaxis().SetLabelSize(0.045)
        hEmpty2D_rp_even.GetYaxis().SetLabelSize(0.045)
        hResponse2D_rp_even = response_rp_even.Hresponse().Clone()
        hResponse2D_rp_even.SetName("plottedResponse_rp_even")

        hEmpty2D_rp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp.Draw("colz,same,text")
        hEmpty2D_rp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_rp_odd_"+options.pdf+"_"+options.syst+nobtag+".png")

        hEmpty2D_rp_even.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp_even.Draw("colz,same,text")
        hEmpty2D_rp_even.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_rp_even_"+options.pdf+"_"+options.syst+nobtag+".png")
    
    # normalize so that for each bin of particle-level top pt, the bins in measured top pt add up to 100%
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
    gStyle.SetPaintTextFormat(".1f")
    hResponse2D_rp.SetMarkerSize(1.2)
    hResponse2D_rp.Draw("colz,same,text")
    hEmpty2D_rp.Draw("axis,same")
    if (options.pdf == "CT10_nom" or options.pdf == "MG" or options.pdf == "mcnlo" or options.troubleshoot) and options.closureTest == False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+".pdf")
    
    hEmpty2D_rp.SetAxisRange(450,1150,"X")
    hEmpty2D_rp.SetAxisRange(450,1150,"Y")
    hResponse2D_rp.SetAxisRange(450,1150,"X")
    hResponse2D_rp.SetAxisRange(450,1150,"Y")
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
    t1.DrawLatex(0.19,0.94, "CMS")
    
    t2 = TLatex()
    t2.SetNDC()
    t2.SetTextFont(52)
    t2.SetTextColor(1)
    t2.SetTextSize(extraTextSize)
    t2.DrawLatex(0.29,0.94, "Preliminary")
    
    t3 = TLatex()
    t3.SetNDC()
    t3.SetTextFont(42)
    t3.SetTextColor(1)
    t3.SetTextSize(extraTextSize)
    if (options.lepType == "ele"):
        t3.DrawLatex(0.49,0.94, "(e+Jets)")
    else:
        t3.DrawLatex(0.49,0.94, "(#mu+Jets)")
    t3.DrawLatex(0.66,0.94, "19.7 fb^{-1} (8 TeV)")    

    if (options.pdf == "CT10_nom" or options.pdf == "MG" or options.pdf == "mcnlo" or options.troubleshoot) and options.closureTest == False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_rp_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")


    response_rp.Hresponse().SetName("responseMatrix_rp_"+options.syst)
    response_rp.Hresponse().Write()
    
    
    # -------------------------------------------------------------------------------------
    ### particle level to parton level 
    hEmpty2D_pp = response_pp.Hresponse().Clone()
    hEmpty2D_pp.SetName("empty2D_pp")
    hEmpty2D_pp.Reset()
    hEmpty2D_pp.GetXaxis().SetTitle("Particle-level top p_{T} (GeV)")
    hEmpty2D_pp.GetYaxis().SetTitle("Top quark p_{T} (GeV)")
    hEmpty2D_pp.GetXaxis().SetLabelSize(0.05)
    hEmpty2D_pp.GetYaxis().SetLabelSize(0.05)
    hEmpty2D_pp.GetXaxis().SetTitleOffset(1.2)
    hEmpty2D_pp.GetYaxis().SetTitleOffset(1.2)
    hEmpty2D_pp.Draw()
    hResponse2D_pp = response_pp.Hresponse().Clone()
    hResponse2D_pp.SetName("plottedResponse_pp")

    if options.troubleshoot :
        hEmpty2D_pp_even = response_pp_even.Hresponse().Clone()
        hEmpty2D_pp_even.SetName("empty2D_pp_even")
        hEmpty2D_pp_even.Reset()
        hEmpty2D_pp_even.GetXaxis().SetTitle("Particle-level top p_{T} (GeV)")
        hEmpty2D_pp_even.GetYaxis().SetTitle("Top quark p_{T} (GeV)")
        hEmpty2D_pp_even.GetXaxis().SetLabelSize(0.045)
        hEmpty2D_pp_even.GetYaxis().SetLabelSize(0.045)
        hResponse2D_pp_even = response_pp_even.Hresponse().Clone()
        hResponse2D_pp_even.SetName("plottedResponse_pp_even")

        hEmpty2D_pp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp.Draw("colz,same,text")
        hEmpty2D_pp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_odd_"+options.pdf+"_"+options.syst+nobtag+".png")

        hEmpty2D_pp_even.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp_even.Draw("colz,same,text")
        hEmpty2D_pp_even.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot"+DIR+"_responseMatrix_pp_even_"+options.pdf+"_"+options.syst+nobtag+".png")
    
    # normalize so that for each bin of particle-level top pt, the bins in measured top pt add up to 100%
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

    gStyle.SetPaintTextFormat(".1f")
    hResponse2D_pp.SetMarkerSize(1.2)
    hResponse2D_pp.Draw("colz,same,text")
    hEmpty2D_pp.Draw("axis,same")
    if (options.pdf == "CT10_nom" or options.pdf == "MG" or options.pdf == "mcnlo" or options.troubleshoot) and options.closureTest == False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+".pdf")
    
    hEmpty2D_pp.SetAxisRange(450,1150,"X")
    hEmpty2D_pp.SetAxisRange(450,1150,"Y")
    hResponse2D_pp.SetAxisRange(450,1150,"X")
    hResponse2D_pp.SetAxisRange(450,1150,"Y")
    hEmpty2D_pp.Draw()
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
    t1.DrawLatex(0.19,0.94, "CMS")
    
    t2 = TLatex()
    t2.SetNDC()
    t2.SetTextFont(52)
    t2.SetTextColor(1)
    t2.SetTextSize(extraTextSize)
    t2.DrawLatex(0.29,0.94, "Preliminary")

    t3 = TLatex()
    t3.SetNDC()
    t3.SetTextFont(42)
    t3.SetTextColor(1)
    t3.SetTextSize(extraTextSize)
    if (options.lepType == "ele"):
        t3.DrawLatex(0.49,0.94, "(e+Jets)")
    else:
        t3.DrawLatex(0.49,0.94, "(#mu+Jets)")
    t3.DrawLatex(0.66,0.94, "19.7 fb^{-1} (8 TeV)")    
    
    if (options.pdf == "CT10_nom" or options.troubleshoot) and options.closureTest == False:
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".png")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".eps")
        cr.SaveAs("UnfoldingPlots/unfold"+DIR+"_2step"+append+"_responseMatrix_pp_zoom_"+options.pdf+"_"+options.syst+nobtag+".pdf")

    response_pp.Hresponse().SetName("responseMatrix_pp_"+options.syst)
    response_pp.Hresponse().Write()



fout.Close()
