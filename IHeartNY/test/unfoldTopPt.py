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

parser.add_option('--twoStep', metavar='F', action='store_true',
                  default=False,
                  dest='twoStep',
                  help='Do reco-particle and particle-parton unfolding')

parser.add_option('--systVariation', metavar='F', type='string', action='store',
                  default='nom',
                  dest='syst',
                  help='Run nominal or systematic variation?')

parser.add_option('--ttbarPDF', metavar='F', type='string', action='store',
                  default='CT10_nom',
                  dest='pdf',
                  help='Which PDF set and nominal vs up/down? Or Q2 up/down?')

parser.add_option('--unfoldType', metavar='F', type='string', action='store',
                  default='pt400',
                  dest='unfold',
                  help='Unfold using pt > 0 ("full") or pt > 400 ("pt400", default)?')

parser.add_option('--addNoBtag', metavar='F', action='store_true',
                  default=False,
                  dest='addNoBtag',
                  help='Unfold only using category \"1 top-tag, 1 b-tag\" (default) or adding \"1 top-tag, 0 b-tag\" (use --addNoBtag)')

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

unfoldType = "_"
if (options.unfold == "full" or options.unfold == "pt400") == False:
    print ""
    print "WARNING - not a valid option for unfolding type (use either \"full\" or \"pt400\"), exiting...!"
    print ""
    sys.exit()
else :
    unfoldType += options.unfold 
    print ""
    print "Unfolding using option \"" + options.unfold +"\" "
    print ""


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
# cross sections, efficiencies, total number of events
# -------------------------------------------------------------------------------------

# luminosity
lum = 19.7 #fb-1

# cross sections
sigma_ttbar = [ 
    [245.8*1000., 245.8*1000., 245.8*1000.],  # nominal (m<700, 700-1000, 1000-inf)
    [252.0*1000., 252.0*1000., 252.0*1000.],  # Q2 up
    [237.4*1000., 237.4*1000., 237.4*1000.]   # Q2 down
    ]
eff_ttbar = [ 
    [1.0, 0.074, 0.015],  # nominal
    [1.0, 0.074, 0.014],  # Q2 up
    [1.0, 0.081, 0.016]   # Q2 down
    ]
Nmc_ttbar = [
    [21675970., 3082812., 1249111.],  # nominal
    [14983686., 2243672., 1241650.],  # Q2 up
    [1789004., 2170074., 1308090.]    # Q2 down
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


## hack to account for that when doing closure test, the ttbar sample is split in two 
eff_closure = 1.0
if options.closureTest == True:
    eff_closure = 2.0


# -------------------------------------------------------------------------------------
# Scaling of the various backgrounds from the theta fit
# -------------------------------------------------------------------------------------

if nobtag == "_nobtag":
    fitted_qcd = 9.5+38
    fitted_singletop = 3.7+11.3
    fitted_wjets = 4.2+154
    fitted_ttbarnonsemilep = 30.8+36.7
    fitted_ttbar = 291.3+293
else:
    fitted_qcd = 9.5
    fitted_singletop = 3.7
    fitted_wjets = 4.2
    fitted_ttbarnonsemilep = 30.8
    fitted_ttbar = 291.3


# -------------------------------------------------------------------------------------
#  read histogram files
# -------------------------------------------------------------------------------------

f_data = TFile("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root")
f_QCD  = TFile("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root")

if options.closureTest == True : 
    f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+"_even.root")
    f_ttbar_max700_odd    = TFile("histfiles_"+options.pdf+"/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    f_ttbar_700to1000_odd = TFile("histfiles_"+options.pdf+"/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    f_ttbar_1000toInf_odd = TFile("histfiles_"+options.pdf+"/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+"_odd.root")
    ## full truth samples for unfolding (two-step) particle-level to parton 
    f_ttbar_max700_pp    = TFile("TruthStudy/TT_max700_"+options.pdf+"_fullTruth_even.root")
    f_ttbar_700to1000_pp = TFile("TruthStudy/TT_Mtt-700to1000_"+options.pdf+"_fullTruth_even.root")
    f_ttbar_1000toInf_pp = TFile("TruthStudy/TT_Mtt-1000toInf_"+options.pdf+"_fullTruth_even.root")
    f_ttbar_max700_pp_odd    = TFile("TruthStudy/TT_max700_"+options.pdf+"_fullTruth_odd.root")
    f_ttbar_700to1000_pp_odd = TFile("TruthStudy/TT_Mtt-700to1000_"+options.pdf+"_fullTruth_odd.root")
    f_ttbar_1000toInf_pp_odd = TFile("TruthStudy/TT_Mtt-1000toInf_"+options.pdf+"_fullTruth_odd.root")
else :
    f_ttbar_max700    = TFile("histfiles_"+options.pdf+"/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+".root")
    f_ttbar_700to1000 = TFile("histfiles_"+options.pdf+"/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+".root")
    f_ttbar_1000toInf = TFile("histfiles_"+options.pdf+"/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+".root")
    ## full truth samples for unfolding (two-step) particle-level to parton 
    f_ttbar_max700_pp    = TFile("TruthStudy/TT_max700_"+options.pdf+"_fullTruth.root")
    f_ttbar_700to1000_pp = TFile("TruthStudy/TT_Mtt-700to1000_"+options.pdf+"_fullTruth.root")
    f_ttbar_1000toInf_pp = TFile("TruthStudy/TT_Mtt-1000toInf_"+options.pdf+"_fullTruth.root")

f_ttbar_nonsemilep_max700    = TFile("histfiles_"+options.pdf+"/2Dhists/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+".root")
f_ttbar_nonsemilep_700to1000 = TFile("histfiles_"+options.pdf+"/2Dhists/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+".root")
f_ttbar_nonsemilep_1000toInf = TFile("histfiles_"+options.pdf+"/2Dhists/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.pdf+"_2Dcut_"+options.syst+".root")

f_T_t     = TFile("histfiles/2Dhist/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_2Dcut_nom.root")
f_Tbar_t  = TFile("histfiles/2Dhist/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_2Dcut_nom.root")
f_T_s     = TFile("histfiles/2Dhist/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_2Dcut_nom.root")
f_Tbar_s  = TFile("histfiles/2Dhist/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_2Dcut_nom.root")
f_T_tW    = TFile("histfiles/2Dhist/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_2Dcut_nom.root")
f_Tbar_tW = TFile("histfiles/2Dhist/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_2Dcut_nom.root")

f_WJets_1jet   = TFile("histfiles/2Dhist/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_2Dcut_nom.root")
f_WJets_2jet   = TFile("histfiles/2Dhist/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_2Dcut_nom.root")
f_WJets_3jet   = TFile("histfiles/2Dhist/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_2Dcut_nom.root")
f_WJets_4jet   = TFile("histfiles/2Dhist/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_2Dcut_nom.root")

# the response matrices are simply added here, but have been filled with the full event weights (taking sample size, efficiency, etx. into account)
if options.closureTest == True : 
    response_ttbar_max700    = f_ttbar_max700_odd.Get("response_pt"+nobtag+unfoldType)
    response_ttbar_700to1000 = f_ttbar_700to1000_odd.Get("response_pt"+nobtag+unfoldType)
    response_ttbar_1000toInf = f_ttbar_1000toInf_odd.Get("response_pt"+nobtag+unfoldType)
else :
    response_ttbar_max700    = f_ttbar_max700.Get("response_pt"+nobtag+unfoldType)
    response_ttbar_700to1000 = f_ttbar_700to1000.Get("response_pt"+nobtag+unfoldType)
    response_ttbar_1000toInf = f_ttbar_1000toInf.Get("response_pt"+nobtag+unfoldType)

response = response_ttbar_max700.Clone()
response.SetName("response_pt_"+options.syst)
response.Add(response_ttbar_700to1000)
response.Add(response_ttbar_1000toInf)

## response matrices for two-step unfolding
if options.twoStep == True :
    if options.closureTest == True : 
        response_ttbar_max700_rp    = f_ttbar_max700_odd.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000_odd.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf_odd.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700_pp_odd.Get("response_pt"+unfoldType+"_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000_pp_odd.Get("response_pt"+unfoldType+"_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf_pp_odd.Get("response_pt"+unfoldType+"_pp")
        if options.troubleshoot == True:
            response_ttbar_max700_rp_even    = f_ttbar_max700.Get("response_pt"+nobtag+unfoldType+"_rp")
            response_ttbar_700to1000_rp_even = f_ttbar_700to1000.Get("response_pt"+nobtag+unfoldType+"_rp")
            response_ttbar_1000toInf_rp_even = f_ttbar_1000toInf.Get("response_pt"+nobtag+unfoldType+"_rp")
            response_ttbar_max700_pp_even    = f_ttbar_max700_pp.Get("response_pt"+unfoldType+"_pp")
            response_ttbar_700to1000_pp_even = f_ttbar_700to1000_pp.Get("response_pt"+unfoldType+"_pp")
            response_ttbar_1000toInf_pp_even = f_ttbar_1000toInf_pp.Get("response_pt"+unfoldType+"_pp")
    else:
        response_ttbar_max700_rp    = f_ttbar_max700.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_700to1000_rp = f_ttbar_700to1000.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_1000toInf_rp = f_ttbar_1000toInf.Get("response_pt"+nobtag+unfoldType+"_rp")
        response_ttbar_max700_pp    = f_ttbar_max700_pp.Get("response_pt"+unfoldType+"_pp")
        response_ttbar_700to1000_pp = f_ttbar_700to1000_pp.Get("response_pt"+unfoldType+"_pp")
        response_ttbar_1000toInf_pp = f_ttbar_1000toInf_pp.Get("response_pt"+unfoldType+"_pp")

    response_rp = response_ttbar_max700_rp.Clone()
    response_rp.SetName("response_pt_"+options.syst+"_rp")
    response_rp.Add(response_ttbar_700to1000_rp)
    response_rp.Add(response_ttbar_1000toInf_rp)
    
    response_pp = response_ttbar_max700_pp.Clone()
    response_pp.SetName("response_pt_"+options.syst+"_pp")
    response_pp.Add(response_ttbar_700to1000_pp)
    response_pp.Add(response_ttbar_1000toInf_pp)

    if options.troubleshoot :
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

if options.twoStep :
    fout = TFile("UnfoldingPlots/unfold_2step_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".root","recreate");
else :
    fout = TFile("UnfoldingPlots/unfold_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".root","recreate");


# -------------------------------------------------------------------------------------
# read actual histograms
# -------------------------------------------------------------------------------------

if options.closureTest == True : 
    hTrue_max700    = f_ttbar_max700_odd.Get("ptGenTop"+unfoldType)
    hTrue_700to1000 = f_ttbar_700to1000_odd.Get("ptGenTop"+unfoldType)
    hTrue_1000toInf = f_ttbar_1000toInf_odd.Get("ptGenTop"+unfoldType)

    if options.twoStep :
        hPart_max700    = f_ttbar_max700_odd.Get("ptPartTop"+unfoldType)
        hPart_700to1000 = f_ttbar_700to1000_odd.Get("ptPartTop"+unfoldType)
        hPart_1000toInf = f_ttbar_1000toInf_odd.Get("ptPartTop"+unfoldType)

        if options.troubleshoot :
            hTrue_max700_even    = f_ttbar_max700.Get("ptGenTop"+unfoldType)
            hTrue_700to1000_even = f_ttbar_700to1000.Get("ptGenTop"+unfoldType)
            hTrue_1000toInf_even = f_ttbar_1000toInf.Get("ptGenTop"+unfoldType)
            hPart_max700_even    = f_ttbar_max700.Get("ptPartTop"+unfoldType)
            hPart_700to1000_even = f_ttbar_700to1000.Get("ptPartTop"+unfoldType)
            hPart_1000toInf_even = f_ttbar_1000toInf.Get("ptPartTop"+unfoldType)
else :
    hTrue_max700    = f_ttbar_max700.Get("ptGenTop"+unfoldType)
    hTrue_700to1000 = f_ttbar_700to1000.Get("ptGenTop"+unfoldType)
    hTrue_1000toInf = f_ttbar_1000toInf.Get("ptGenTop"+unfoldType)

    if options.twoStep :
        hPart_max700    = f_ttbar_max700.Get("ptPartTop"+unfoldType)
        hPart_700to1000 = f_ttbar_700to1000.Get("ptPartTop"+unfoldType)
        hPart_1000toInf = f_ttbar_1000toInf.Get("ptPartTop"+unfoldType)

hTrue_max700.Sumw2()
hTrue_700to1000.Sumw2()
hTrue_1000toInf.Sumw2()

if options.twoStep:
    hPart_max700.Sumw2()
    hPart_700to1000.Sumw2()
    hPart_1000toInf.Sumw2()
    
    if options.troubleshoot:
        hTrue_max700_even.Sumw2()
        hTrue_700to1000_even.Sumw2()
        hTrue_1000toInf_even.Sumw2()
        hPart_max700_even.Sumw2()
        hPart_700to1000_even.Sumw2()
        hPart_1000toInf_even.Sumw2()

isTwoStep = ""
if options.twoStep:
    isTwoStep = "_2step"

hRecoMC_max700    = f_ttbar_max700.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType).Clone()
hRecoMC_max700.SetName("hRecoMC_max700")
hRecoMC_max700.Sumw2()
hRecoMC_700to1000 = f_ttbar_700to1000.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType).Clone()
hRecoMC_700to1000.SetName("hRecoMC_700to1000")
hRecoMC_700to1000.Sumw2()
hRecoMC_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType).Clone()
hRecoMC_1000toInf.SetName("hRecoMC_1000toInf")
hRecoMC_1000toInf.Sumw2()
    

hRecoData = f_data.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType).Clone()
hRecoData.SetName("hRecoData"+unfoldType)

hRecoQCD = f_QCD.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType).Clone()
hRecoQCD.SetName("hRecoQCD")
hRecoQCD.Sumw2()
hRecoQCD.SetFillColor(TColor.kYellow)

if options.closureTest == False : 
    hMeas = f_data.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
else :
    hMeas_max700    = f_ttbar_max700.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
    hMeas_700to1000 = f_ttbar_700to1000.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
    hMeas_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
    hMeas_max700.Sumw2()
    hMeas_700to1000.Sumw2()
    hMeas_1000toInf.Sumw2()

    if options.troubleshoot :
        hMeas_max700_odd    = f_ttbar_max700_odd.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
        hMeas_700to1000_odd = f_ttbar_700to1000_odd.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
        hMeas_1000toInf_odd = f_ttbar_1000toInf_odd.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
        hMeas_max700_odd.Sumw2()
        hMeas_700to1000_odd.Sumw2()
        hMeas_1000toInf_odd.Sumw2()
    

hMeas_T_t     = f_T_t.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_Tbar_t  = f_Tbar_t.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_T_s     = f_T_s.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_Tbar_s  = f_Tbar_s.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_T_tW    = f_T_tW.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_Tbar_tW = f_Tbar_tW.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_WJets_1jet   = f_WJets_1jet.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_WJets_2jet   = f_WJets_2jet.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_WJets_3jet   = f_WJets_3jet.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_WJets_4jet   = f_WJets_4jet.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_tt0_nonsemi = f_ttbar_nonsemilep_max700.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_tt700_nonsemi = f_ttbar_nonsemilep_700to1000.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)
hMeas_tt1000_nonsemi = f_ttbar_nonsemilep_1000toInf.Get("ptRecoTop"+isTwoStep+nobtag+unfoldType)

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

# if doing closure test, use ttbar nominal as the "measured" distribution
if options.closureTest == True : 
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

hTrue_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
hTrue_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
hTrue_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
hTrue = hTrue_max700.Clone()
hTrue.SetName("pt_genTop")
hTrue.Add(hTrue_700to1000)
hTrue.Add(hTrue_1000toInf)

if options.troubleshoot :
    hTrue_max700_even.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
    hTrue_700to1000_even.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
    hTrue_1000toInf_even.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
    hTrue_even = hTrue_max700_even.Clone()
    hTrue_even.SetName("pt_genTop_even")
    hTrue_even.Add(hTrue_700to1000_even)
    hTrue_even.Add(hTrue_1000toInf_even)

if options.twoStep :
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

hRecoMC_max700.Scale( eff_closure * sigma_ttbar[ipdf][0] * eff_ttbar[ipdf][0] * lum / float(Nmc_ttbar[ipdf][0]))
hRecoMC_700to1000.Scale( eff_closure * sigma_ttbar[ipdf][1] * eff_ttbar[ipdf][1] * lum / float(Nmc_ttbar[ipdf][1]))
hRecoMC_1000toInf.Scale( eff_closure * sigma_ttbar[ipdf][2] * eff_ttbar[ipdf][2] * lum / float(Nmc_ttbar[ipdf][2]))
hRecoMC = hRecoMC_max700.Clone()
hRecoMC.SetName("ptRecoTop_ttbar")
hRecoMC.Add(hRecoMC_700to1000)
hRecoMC.Add(hRecoMC_1000toInf)

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

hRecoMC.Scale( fitted_ttbar / hRecoMC.Integral() )
hRecoQCD.Scale( fitted_qcd / hRecoQCD.Integral() )
hMeas_SingleTop.Scale( fitted_singletop / hMeas_SingleTop.Integral() )
hMeas_WJets.Scale( fitted_wjets / hMeas_WJets.Integral() )
hMeas_TTNonSemi.Scale( fitted_ttbarnonsemilep / hMeas_TTNonSemi.Integral() )


# -------------------------------------------------------------------------------------
# subtract backgrounds from the data distribution, but not for closure test!!! 
# -------------------------------------------------------------------------------------

if options.closureTest == False : 
    for hist in [hMeas_SingleTop, hMeas_WJets, hRecoQCD, hMeas_TTNonSemi] :
        hMeas.Add(hist, -1.)

    for ibin in xrange( hMeas.GetNbinsX() ) :
        if ( hMeas.GetBinContent( ibin ) < 0.0 ) :
            hMeas.SetBinContent( ibin, 0.0 )


# -------------------------------------------------------------------------------------
# draw background-subtracted data distribution 
# -------------------------------------------------------------------------------------

if options.closureTest == False : 
    cc = TCanvas("cc", "", 800, 600)
    
    ll = TLegend(0.4, 0.65, 0.7, 0.9)
    ll.SetFillStyle(0)
    ll.SetTextFont(42)
    ll.SetTextSize(0.045)
    ll.SetBorderSize(0)
    
    hMeas.SetLineColor(1)
    hMeas.SetLineWidth(2)
    hMeas.Draw("hist")
    hMeas.Draw("axis,same")
    ll.AddEntry(hMeas, "Background-subtracted data","l")
    ll.Draw()
    cc.SaveAs("UnfoldingPlots/unfold_input"+isTwoStep+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    cc.SaveAs("UnfoldingPlots/unfold_input"+isTwoStep+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")

if options.closureTest and options.troubleshoot :
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
    ct1.SaveAs("UnfoldingPlots/troubleshoot_hMeas_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")

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
    ct2.SaveAs("UnfoldingPlots/troubleshoot_hPart_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")

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
    ct3.SaveAs("UnfoldingPlots/troubleshoot_hTrue_evenVsOdd"+isTwoStep+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")


# -------------------------------------------------------------------------------------
# do the actual unfolding
# -------------------------------------------------------------------------------------

## if doing unfolding for pt(top quark) > 400 GeV only, apply acceptance correction!
## this corrects for events which fails parton-level cut (i.e. has pt(gen top)<400), 
## which enters the signal region 


# one-step unfolding
#accCorr [400,500]:  0.713124 +/- 0.0116647
#accCorr [500,600]:  0.899743 +/- 0.0123778
#accCorr [600,700]:  0.912729 +/- 0.019871
#accCorr [700,800]:  0.911112 +/- 0.0319739
#accCorr [800,1200]: 0.952454 +/- 0.0234787
accCorr = [0.713124, 0.899743, 0.912729, 0.911112, 0.952454]

# two-step unfolding
#accCorr_rp [400,500]:  0.829239 +/- 0.00924507
#accCorr_rp [500,600]:  0.984784 +/- 0.00474956
#accCorr_rp [600,700]:  0.992851 +/- 0.00333441
#accCorr_rp [700,800]:  1 +/- 0
#accCorr_rp [800,1200]: 1 +/- 0
accCorr_rp = [0.829239, 0.984784, 0.992851, 1.0, 1.0]

#accCorr_pp [400,500]:  0.515877 +/- 0.00371986
#accCorr_pp [500,600]:  0.55938 +/- 0.00624021
#accCorr_pp [600,700]:  0.577836 +/- 0.010334
#accCorr_pp [700,800]:  0.611004 +/- 0.0166818
#accCorr_pp [800,1200]: 0.653409 +/- 0.0191128
accCorr_pp = [0.515877, 0.55938, 0.577836, 0.611004, 0.653409]

# two-step unfolding for "_full" option, meaning no passParton at pp-step, and only passParticleLoose at rp-step
#accCorr_rp [400,500]:  0.994535 +/- 0.00149084
#accCorr_rp [500,600]:  0.99138 +/- 0.00342479
#accCorr_rp [600,700]:  0.992851 +/- 0.00333441
#accCorr_rp [700,800]:  1 +/- 0
#accCorr_rp [800,1300]: 1 +/- 0
accCorr_rp_full = [0.0, 0.0, 0.0, 0.0, 0.994535, 0.99138, 0.992851, 1.0, 1.0, 0.0]

# trigger SF for particle-level 
#trigSF_rp [400,500]:  1.22372 +/- 0.0042528
#trigSF_rp [500,600]:  1.24353 +/- 0.00729263
#trigSF_rp [600,700]:  1.23862 +/- 0.0118791
#trigSF_rp [700,800]:  1.28546 +/- 0.0216951
#trigSF_rp [800,1200]: 1.28605 +/- 0.0262931
trigSF_rp = [1.22372, 1.24353, 1.23862, 1.28546, 1.28605]
trigSF_rp_full = [0.0, 0.0, 0.0, 0.0, 1.22372, 1.24353, 1.23862, 1.28546, 1.28605, 0.0]



hMeasCorr = hMeas.Clone()
hMeasCorr.SetName("correctedMeas")


# -------------------------------------------------------------------------------------
# one-step unfolding
if options.twoStep == False:

    # apply acceptance correction
    if unfoldType == "_pt400" and options.closureTest == False:
        for ibin in range(1, hMeasCorr.GetXaxis().GetNbins()+1 ) :
            hMeasCorr.SetBinContent(ibin,  hMeas.GetBinContent(ibin) * accCorr[ibin-1] )
            hMeasCorr.SetBinError(ibin,  hMeas.GetBinError(ibin) * accCorr[ibin-1] )
    
    
    print "------------ UNFOLDING (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold = RooUnfoldBayes(response, hMeasCorr, 10);
    unfold = RooUnfoldSvd(response, hMeasCorr, 4);
    #unfold = RooUnfoldTUnfold(response, hMeasCorr);

    # get the unfolded distribution
    hReco = unfold.Hreco()

# -------------------------------------------------------------------------------------
# two-step unfolding
else :

    # apply acceptance correction for reco -> particle-level
    if options.closureTest == False:
        if unfoldType == "_pt400":
            for ibin in range(1, hMeasCorr.GetXaxis().GetNbins()+1 ) :
                hMeasCorr.SetBinContent(ibin, hMeas.GetBinContent(ibin) * accCorr_rp[ibin-1] )
                hMeasCorr.SetBinError(ibin, hMeas.GetBinError(ibin) * accCorr_rp[ibin-1] )
        elif unfoldType == "_full":
            for ibin in range(1, hMeasCorr.GetXaxis().GetNbins()+1 ) :
                hMeasCorr.SetBinContent(ibin, hMeas.GetBinContent(ibin) * accCorr_rp_full[ibin-1] )
                hMeasCorr.SetBinError(ibin, hMeas.GetBinError(ibin) * accCorr_rp_full[ibin-1] )
        else:
            print "invalid unfolding option for two-step unfolding!!!" 
    
    
    print "------------ UNFOLD TO PARTICLE-LEVEL (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold_rp = RooUnfoldBayes(response_rp, hMeasCorr, 10);
    unfold_rp = RooUnfoldSvd(response_rp, hMeasCorr, 4);
    #unfold_rp = RooUnfoldTUnfold(response_rp, hMeasCorr);

    # get the distribution unfolded to particle-level
    hReco_rp = unfold_rp.Hreco()

    # apply acceptance correction *AND* trigger SF correction for particle-level -> parton
    hRecoCorr_rp = hReco_rp.Clone()
    hRecoCorr_rp.SetName("hRecoCorr_rp")
    if unfoldType == "_pt400":
        for ibin in range(1, hReco_rp.GetXaxis().GetNbins()+1 ) :
            hRecoCorr_rp.SetBinContent(ibin, hReco_rp.GetBinContent(ibin) * accCorr_pp[ibin-1] * trigSF_rp[ibin-1] )
            hRecoCorr_rp.SetBinError(ibin, hReco_rp.GetBinError(ibin) * accCorr_pp[ibin-1] * trigSF_rp[ibin-1] )
    elif unfoldType == "_full":
        for ibin in range(1, hReco_rp.GetXaxis().GetNbins()+1 ) :
            hRecoCorr_rp.SetBinContent(ibin,  hReco_rp.GetBinContent(ibin) * trigSF_rp_full[ibin-1] )
            hRecoCorr_rp.SetBinError(ibin,  hReco_rp.GetBinError(ibin) * trigSF_rp_full[ibin-1] )
    else: 
        print "invalid unfolding option for two-step unfolding!!!" 

    print "------------ UNFOLD TO PARTON-LEVEL (set: " + options.pdf + ", syst: " + options.syst + ") ------------"
    #unfold = RooUnfoldBayes(response_pp, hRecoCorr_rp, 10);
    unfold = RooUnfoldSvd(response_pp, hRecoCorr_rp, 4);
    #unfold = RooUnfoldTUnfold(response_pp, hRecoCorr_rp);

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

## correct also to post-fit top-tagging SF !!! 
if options.closureTest == False : 
    hMeas.Scale(1.0/(1.0+0.25*0.27))
    hReco.Scale(1.0/(1.0+0.25*0.27))
    if options.twoStep:
        hReco_rp.Scale(1.0/(1.0+0.25*0.27))


    
# -------------------------------------------------------------------------------------
# Correct for selection bias in requiring trigger & bin width
# -------------------------------------------------------------------------------------

## trigger SF (this is for correcting parton-level distribution & one-step unfolded distribution @ parton-level 
#trigSF [400,500]:  1.66655 +/- 0.00842579
#trigSF [500,600]:  1.62051 +/- 0.0140173
#trigSF [600,700]:  1.54945 +/- 0.0210899
#trigSF [700,800]:  1.63045 +/- 0.0426413
#trigSF [800,1200]: 1.48044 +/- 0.0373831

if unfoldType == "":
    trigSF = [0.0, 1.66655, 1.62051, 1.54945, 1.63045, 1.480044]
elif unfoldType == "_full":
    trigSF = [0.0, 0.0, 0.0, 0.0, 1.66655, 1.62051, 1.54945, 1.63045, 1.480044, 0.0]
elif unfoldType == "_pt400":
    trigSF = [1.66655, 1.62051, 1.54945, 1.63045, 1.480044]
else:
    print "Unvalid unfolding type!!" 

    
sumReco = 0
sumTrue = 0
sumMeas = 0
sumReco_rp = 0
sumPart = 0
for ibin in range(1, hTrue.GetXaxis().GetNbins()+1 ) :

    width = hTrue.GetBinWidth(ibin)

    # correct top-quark pt @ gen-level for trigger bias (for both one-step & two-step)
    hTrue.SetBinContent(ibin, hTrue.GetBinContent(ibin) * trigSF[ibin-1] / width )
    hTrue.SetBinError(ibin, hTrue.GetBinError(ibin) * trigSF[ibin-1] / width )

    # correct one-step unfolded distribution for trigger bias
    if options.twoStep == False:
        hReco.SetBinContent(ibin, hReco.GetBinContent(ibin) * trigSF[ibin-1] / width )
        hReco.SetBinError(ibin, hReco.GetBinError(ibin) * trigSF[ibin-1] / width )
    else:
        hReco.SetBinContent(ibin, hReco.GetBinContent(ibin) / width )
        hReco.SetBinError(ibin, hReco.GetBinError(ibin) / width )
        if unfoldType == "_pt400":
            hReco_rp.SetBinContent(ibin, hReco_rp.GetBinContent(ibin) * trigSF_rp[ibin-1] / width )
            hReco_rp.SetBinError(ibin, hReco_rp.GetBinError(ibin) * trigSF_rp[ibin-1] / width )
            hPart.SetBinContent(ibin, hPart.GetBinContent(ibin) * trigSF_rp[ibin-1] / width )
            hPart.SetBinError(ibin, hPart.GetBinError(ibin) * trigSF_rp[ibin-1] / width )
        elif unfoldType == "_full":
            hReco_rp.SetBinContent(ibin, hReco_rp.GetBinContent(ibin) * trigSF_rp_full[ibin-1] / width )
            hReco_rp.SetBinError(ibin, hReco_rp.GetBinError(ibin) * trigSF_rp_full[ibin-1] / width )
            hPart.SetBinContent(ibin, hPart.GetBinContent(ibin) * trigSF_rp_full[ibin-1] / width )
            hPart.SetBinError(ibin, hPart.GetBinError(ibin) * trigSF_rp_full[ibin-1] / width )
            
    
    # correct measured distribution for bin width
    hMeas.SetBinContent(ibin,  hMeas.GetBinContent(ibin) / width )
    hMeas.SetBinError(ibin,  hMeas.GetBinError(ibin) / width )
    
    sumReco += hReco.GetBinContent(ibin)*width
    sumTrue += hTrue.GetBinContent(ibin)*width
    sumMeas += hMeas.GetBinContent(ibin)*width
    if options.twoStep:
        sumReco_rp += hReco_rp.GetBinContent(ibin)*width
        sumPart += hPart.GetBinContent(ibin)*width
    

# -------------------------------------------------------------------------------------
# print & draw
# -------------------------------------------------------------------------------------

## ratio of unfolded data to generator-level 
hFrac = hReco.Clone()
hFrac.SetName("hFrac")
hFrac.SetTitle(";Top quark p_{T} [GeV];Data/MC")
hFrac.Divide(hTrue)

## ratio of unfolded data to particle-level 
if options.twoStep:
    hFrac_rp = hReco_rp.Clone()
    hFrac_rp.SetName("hFrac_rp")
    hFrac_rp.SetTitle(";Particle-level top p_{T} [GeV];Data/MC")
    hFrac_rp.Divide(hPart)


bin400 = hMeas.GetXaxis().FindBin(400.)
binmax = hMeas.GetXaxis().FindBin(10000.)

print 'htrue = ' + str(hTrue.Integral(bin400,binmax))
print 'hmeas = ' + str(hMeas.Integral(bin400,binmax))
print 'hreco = ' + str(hReco.Integral(bin400,binmax))
if options.twoStep:
    print 'hreco_rp = ' + str(hReco_rp.Integral(bin400,binmax))
    print 'hpart    = ' + str(hPart.Integral(bin400,binmax))
        
print 'true sigma = ' + str(sumTrue)
print 'meas sigma = ' + str(sumMeas)
print 'reco sigma = ' + str(sumReco)
if options.twoStep:
    print 'reco_rp sigma = ' + str(sumReco_rp)
    print 'part sigma    = ' + str(sumPart)


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

hReco.GetXaxis().SetRangeUser(400.,1300.)
hTrue.GetXaxis().SetRangeUser(400.,1300.)
hMeas.GetXaxis().SetRangeUser(400.,1300.)

if unfoldType == "_full" or unfoldType == "_pt400":
    hReco.GetXaxis().SetRangeUser(400.,1200.)
    hTrue.GetXaxis().SetRangeUser(400.,1200.)
    hMeas.GetXaxis().SetRangeUser(400.,1200.)

hReco.SetTitle(";;d#sigma/dp_{T} [fb/GeV]")
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

if options.closureTest == False : 
    leg.AddEntry( hReco, 'Unfolded data', 'p')
    leg.AddEntry( hTrue, 'Generated', 'l')
    leg.AddEntry( hMeas, 'Raw data', 'p')
else : 
    leg.AddEntry( hReco, 'Unfolded MC: Closure test', 'p')
    leg.AddEntry( hTrue, 'Generated', 'l')
    leg.AddEntry( hMeas, 'Raw MC', 'p')

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
#text1.DrawLatex(0.20,0.87, "#scale[1.0]{CMS Preliminary, L = 19.7 fb^{-1} at  #sqrt{s} = 8 TeV}")
text1.DrawLatex(0.5,0.8, "#scale[1.0]{L = 19.7 fb^{-1} at #sqrt{s} = 8 TeV}")


c1.cd();
pad2 =  TPad("pad2","pad2",0,0.0,1,0.28)
pad2.SetTopMargin(0.05);
pad2.SetBottomMargin(0.4);
pad2.Draw();
pad2.cd();
hFrac.SetMaximum(2.0)
hFrac.SetMinimum(0.0)
hFrac.UseCurrentStyle()
hFrac.GetYaxis().SetTitleSize(25)
hFrac.GetYaxis().SetTitleOffset(2.0)
hFrac.GetXaxis().SetTitleOffset(4.0)
hFrac.GetXaxis().SetLabelSize(25)
hFrac.GetYaxis().SetNdivisions(2,4,0,False)

hFrac.Draw("e")
hFrac.GetXaxis().SetRangeUser(400., 1300.)

if unfoldType == "_full" or unfoldType == "_pt400":
    hFrac.GetXaxis().SetRangeUser(400., 1200.)

c1.Update()

append = ""
if options.twoStep :
    append += "_2step"
if options.closureTest :
    append += "_closure"

c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+append+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf", "pdf")
c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+append+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png", "png")
c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+append+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps", "eps")



# -------------------------------------------------------------------------------------
# draw particle-level unfolding
# -------------------------------------------------------------------------------------

if options.twoStep:
    pad1.cd();

    hReco_rp.SetMarkerStyle(21)
    hMeas.SetMarkerStyle(25);

    hReco_rp.GetXaxis().SetRangeUser(400.,1300.)
    hPart.GetXaxis().SetRangeUser(400.,1300.)
    hMeas.GetXaxis().SetRangeUser(400.,1300.)
    
    if unfoldType == "_full" or unfoldType == "_pt400":
        hReco_rp.GetXaxis().SetRangeUser(400.,1200.)
        hPart.GetXaxis().SetRangeUser(400.,1200.)
        hMeas.GetXaxis().SetRangeUser(400.,1200.)

    hReco_rp.SetTitle(";;d#sigma/dp_{T} [fb/GeV]")
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
        leg2.AddEntry( hReco_rp, 'Unfolded data', 'p')
        leg2.AddEntry( hTrue, 'Generated', 'l')
        leg2.AddEntry( hMeas, 'Raw data', 'p')
    else : 
        leg2.AddEntry( hReco_rp, 'Unfolded MC: Closure test', 'p')
        leg2.AddEntry( hTrue, 'Generated', 'l')
        leg2.AddEntry( hMeas, 'Raw MC', 'p')
    
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

    hFrac_rp.SetMaximum(2.0)
    hFrac_rp.SetMinimum(0.0)
    hFrac_rp.UseCurrentStyle()
    hFrac_rp.GetYaxis().SetTitleSize(25)
    hFrac_rp.GetYaxis().SetTitleOffset(2.0)
    hFrac_rp.GetXaxis().SetTitleOffset(4.0)
    hFrac_rp.GetXaxis().SetLabelSize(25)
    hFrac_rp.GetYaxis().SetNdivisions(2,4,0,False)

    hFrac_rp.Draw("e")
    hFrac_rp.GetXaxis().SetRangeUser(400., 1300.)

    if unfoldType == "_full" or unfoldType == "_pt400":
        hFrac_rp.GetXaxis().SetRangeUser(400., 1200.)

    c1.Update()

    append = ""
    if options.closureTest :
        append += "_closure"
        
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs_2step_particle"+append+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf", "pdf")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs_2step_particle"+append+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png", "png")
    c1.Print("UnfoldingPlots/unfolded_ttbar_xs_2step_particle"+append+"_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps", "eps")



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
    hEmpty2D.GetXaxis().SetTitle("Top-tagged jet p_{T} [GeV]")
    hEmpty2D.GetYaxis().SetTitle("Top quark p_{T} [GeV]")
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
    cr.SaveAs("UnfoldingPlots/unfold_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    cr.SaveAs("UnfoldingPlots/unfold_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
    cr.SaveAs("UnfoldingPlots/unfold_responseMatrix_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")
    
    response.Hresponse().SetName("responseMatrix_"+options.syst)
    response.Hresponse().Write()
    

# -------------------------------------------------------------------------------------
# two-step unfolding
# -------------------------------------------------------------------------------------

if options.twoStep:

    # -------------------------------------------------------------------------------------
    ### reco to particle level
    hEmpty2D_rp = response_rp.Hresponse().Clone()
    hEmpty2D_rp.SetName("empty2D_rp")
    hEmpty2D_rp.Reset()
    hEmpty2D_rp.GetXaxis().SetTitle("Top-tagged jet p_{T} [GeV]")
    hEmpty2D_rp.GetYaxis().SetTitle("Particle-level top p_{T} [GeV]")
    hEmpty2D_rp.GetXaxis().SetLabelSize(0.045)
    hEmpty2D_rp.GetYaxis().SetLabelSize(0.045)
    hEmpty2D_rp.Draw()
    hResponse2D_rp = response_rp.Hresponse().Clone()
    hResponse2D_rp.SetName("plottedResponse_rp")

    if options.troubleshoot :
        hEmpty2D_rp_even = response_rp_even.Hresponse().Clone()
        hEmpty2D_rp_even.SetName("empty2D_rp_even")
        hEmpty2D_rp_even.Reset()
        hEmpty2D_rp_even.GetXaxis().SetTitle("Top-tagged jet p_{T} [GeV]")
        hEmpty2D_rp_even.GetYaxis().SetTitle("Particle-level top p_{T} [GeV]")
        hEmpty2D_rp_even.GetXaxis().SetLabelSize(0.045)
        hEmpty2D_rp_even.GetYaxis().SetLabelSize(0.045)
        #hEmpty2D_rp_even.Draw()
        hResponse2D_rp_even = response_rp_even.Hresponse().Clone()
        hResponse2D_rp_even.SetName("plottedResponse_rp_even")

        hEmpty2D_rp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp.Draw("colz,same,text")
        hEmpty2D_rp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot_responseMatrix_rp_odd_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")

        hEmpty2D_rp_even.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_rp_even.Draw("colz,same,text")
        hEmpty2D_rp_even.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot_responseMatrix_rp_even_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    
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
    hResponse2D_rp.Draw("colz,same,text")
    hEmpty2D_rp.Draw("axis,same")
    cr.SaveAs("UnfoldingPlots/unfold_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    cr.SaveAs("UnfoldingPlots/unfold_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
    cr.SaveAs("UnfoldingPlots/unfold_2step"+append+"_responseMatrix_rp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")
    
    response_rp.Hresponse().SetName("responseMatrix_rp_"+options.syst)
    response_rp.Hresponse().Write()
    
    
    # -------------------------------------------------------------------------------------
    ### particle level to parton level 
    hEmpty2D_pp = response_pp.Hresponse().Clone()
    hEmpty2D_pp.SetName("empty2D_pp")
    hEmpty2D_pp.Reset()
    hEmpty2D_pp.GetXaxis().SetTitle("Particle-level top p_{T} [GeV]")
    hEmpty2D_pp.GetYaxis().SetTitle("Top quark p_{T} [GeV]")
    hEmpty2D_pp.GetXaxis().SetLabelSize(0.045)
    hEmpty2D_pp.GetYaxis().SetLabelSize(0.045)
    hEmpty2D_pp.Draw()
    hResponse2D_pp = response_pp.Hresponse().Clone()
    hResponse2D_pp.SetName("plottedResponse_pp")

    if options.troubleshoot :
        hEmpty2D_pp_even = response_pp_even.Hresponse().Clone()
        hEmpty2D_pp_even.SetName("empty2D_pp_even")
        hEmpty2D_pp_even.Reset()
        hEmpty2D_pp_even.GetXaxis().SetTitle("Particle-level top p_{T} [GeV]")
        hEmpty2D_pp_even.GetYaxis().SetTitle("Top quark p_{T} [GeV]")
        hEmpty2D_pp_even.GetXaxis().SetLabelSize(0.045)
        hEmpty2D_pp_even.GetYaxis().SetLabelSize(0.045)
        #hEmpty2D_pp_even.Draw()
        hResponse2D_pp_even = response_pp_even.Hresponse().Clone()
        hResponse2D_pp_even.SetName("plottedResponse_pp_even")

        hEmpty2D_pp.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp.Draw("colz,same,text")
        hEmpty2D_pp.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot_responseMatrix_pp_odd_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
        cr.SaveAs("UnfoldingPlots/troubleshoot_responseMatrix_pp_odd_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
        cr.SaveAs("UnfoldingPlots/troubleshoot_responseMatrix_pp_odd_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")

        hEmpty2D_pp_even.Draw()
        gStyle.SetPaintTextFormat(".1f")
        hResponse2D_pp_even.Draw("colz,same,text")
        hEmpty2D_pp_even.Draw("axis,same")
        cr.SaveAs("UnfoldingPlots/troubleshoot_responseMatrix_pp_even_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
        cr.SaveAs("UnfoldingPlots/troubleshoot_responseMatrix_pp_even_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
        cr.SaveAs("UnfoldingPlots/troubleshoot_responseMatrix_pp_even_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")
    
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
    hResponse2D_pp.Draw("colz,same,text")
    hEmpty2D_pp.Draw("axis,same")
    cr.SaveAs("UnfoldingPlots/unfold_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".png")
    cr.SaveAs("UnfoldingPlots/unfold_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".eps")
    cr.SaveAs("UnfoldingPlots/unfold_2step"+append+"_responseMatrix_pp_"+options.pdf+"_"+options.syst+nobtag+unfoldType+".pdf")
    
    response_pp.Hresponse().SetName("responseMatrix_pp_"+options.syst)
    response_pp.Hresponse().Write()



fout.Close()
