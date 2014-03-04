#!/usr/bin/env python
# ==============================================================================
# January 2014
# ==============================================================================

import time
import copy
from optparse import OptionParser


parser = OptionParser()

  

parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='mujets',
                  dest='outname',
                  help='Output name for png and pdf files')


parser.add_option('--hist', metavar='F', type='string', action='store',
                  default='ptRecoTop',
                  dest='hist',
                  help='Histogram to plot')
                  
                  
parser.add_option('--NQCD', metavar='F', type='float', action='store',
                  default=15.0 ,
                  dest='NQCD',
                  help='QCD Normalization')
                  

parser.add_option('--maxy', metavar='F', type='float', action='store',
                  default=500,
                  dest='maxy',
                  help='Maximum y in histogram')

parser.add_option('--ignoreData', metavar='F', action='store_true',
                  default=False,
                  dest='ignoreData',
                  help='Ignore plotting data')

parser.add_option('--ignoreQCD', metavar='F', action='store_true',
                  default=False,
                  dest='ignoreQCD',
                  help='Ignore plotting QCD')


parser.add_option('--drawLegend', metavar='F', action='store_true',
                  default=False,
                  dest='drawLegend',
                  help='Draw a legend')

(options, args) = parser.parse_args()

argv = []

from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor

gROOT.Macro("rootlogon.C")


gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
#gStyle.SetTitleFontSize(0.05)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(1.0, "X")
gStyle.SetTitleOffset(1.0, "Y")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(20, "XYZ")


# Performance numbers
lum = 19.7 # fb-1
SF_b = 0.97
SF_t = 1.0
#SF_t = 0.94

# Cross sections (in fb) and the number of MC events
sigma_ttbar_NNLO = 245.8 * 1000.    # fb, from http://arxiv.org/pdf/1303.6254.pdf
sigma_T_t_NNLO = 56.4 * 1000.       # 
sigma_Tbar_t_NNLO = 30.7 * 1000.    # All single-top approx NNLO cross sections from
sigma_T_s_NNLO = 3.79 * 1000.       # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
sigma_Tbar_s_NNLO = 1.76 * 1000.    # 
sigma_T_tW_NNLO = 11.1 * 1000.      # 
sigma_Tbar_tW_NNLO = 11.1 * 1000.   # 
sigma_WJets_NNLO = 36703.2 * 1000.  # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV

# MC event counts from B2G twiki here :
# https://twiki.cern.ch/twiki/bin/view/CMS/B2GTopLikeBSM53X#Backgrounds
Nmc_ttbar = 21675970
Nmc_T_t = 3758227
Nmc_Tbar_t = 1935072
Nmc_T_s = 259961
Nmc_Tbar_s = 139974
Nmc_T_tW = 497658
Nmc_Tbar_tW = 493460
Nmc_WJets = 57709905
Nmc_TT_Mtt_700_1000 = 3082812
Nmc_TT_Mtt_1000_Inf = 1249111

# QCD Normalization from MET fits
NQCD = options.NQCD

# ttbar filter efficiencies
e_TT_Mtt_700_1000 = 0.074
e_TT_Mtt_1000_Inf = 0.014
e_TT_Mtt_0_700 = 1.0 - e_TT_Mtt_700_1000 - e_TT_Mtt_1000_Inf
# 


thetaNamingDict = {
    'nom':'',
    'qcd':'qcd',
    'jecdn':'jec__down',
    'jecup':'jec__up',
    'jerdn':'jer__down',
    'jerup':'jer__up',
    'pdfdn':'pdf__down',
    'pdfup':'pdf__up',
    'scaledown':'scale__down',
    'scaleup':'scale__up'
    }
plots = [ 'nom', 'jecdn' , 'jecup' , 'jerdn' , 'jerup' , 'pdfdn' , 'pdfup']# , 'scaledown' , 'scaleup']
canvs = []
histsData = []

# Open the output file 

fout = TFile("normalized_" + options.outname + '_' + options.hist + ".root" , "RECREATE")


# ==============================================================================
#  Example Unfolding
# ==============================================================================

if not options.ignoreData : 
    fdata = TFile("histfiles/SingleMu_iheartNY_V1_mu_nom_type1.root")

if not options.ignoreQCD :
    fQCD = TFile("histfiles/QCD_hists_pt_type1.root")
    

fQCD_SingleMu = TFile("histfiles/SingleMu_Run2012_QCD_merged")

fT_t_nom     = TFile("histfiles/T_t-channel_Histos_type1.root")
fT_t_jecdown = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_t_jecup   = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_t_jerdown = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_t_jerup   = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fT_t_qcd   = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")


fTbar_t_nom     = TFile("histfiles/Tbar_t-channel_Histos_type1.root")
fTbar_t_jecdown = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTbar_t_jecup   = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTbar_t_jerdown = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTbar_t_jerup   = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTbar_t_qcd   = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")

fT_s_nom     = TFile("histfiles/T_s-channel_Histos_type1.root")
fT_s_jecdown = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_s_jecup   = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_s_jerdown = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_s_jerup   = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fT_s_qcd   = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")


fTbar_s_nom     = TFile("histfiles/Tbar_s-channel_Histos_type1.root")
fTbar_s_jecdown = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jecdn_type1.root")
fTbar_s_jecup   = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jecup_type1.root")
fTbar_s_jerdown = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jerdn_type1.root")
fTbar_s_jerup   = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jerup_type1.root")
fTbar_s_qcd   = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_qcd_type1.root")


fT_tW_nom     = TFile("histfiles/T_tW-channel_Histos_type1.root")
fT_tW_jecdown = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_tW_jecup   = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_tW_jerdown = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_tW_jerup   = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fT_tW_qcd   = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")


fTbar_tW_nom     = TFile("histfiles/Tbar_tW-channel_Histos_type1.root")
fTbar_tW_jecdown = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTbar_tW_jecup   = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTbar_tW_jerdown = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTbar_tW_jerup   = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTbar_tW_qcd   = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")


fWJets_nom     = TFile("histfiles/WJetsToLNu_Histos_type1.root")
fWJets_jecdown = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jecdn_type1.root")
fWJets_jecup   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jecup_type1.root")
fWJets_jerdown = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jerdn_type1.root")
fWJets_jerup   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jerup_type1.root")
fWJets_qcd   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_qcd_type1.root")


fTT_Mtt_less_700_nom       = TFile("histfiles/TT_Mtt-max700-channel_Histos_type1.root")
fTT_Mtt_less_700_jecdown   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_less_700_jecup     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_less_700_jerdown   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTT_Mtt_less_700_jerup     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_less_700_qcd     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")
fTT_Mtt_less_700_pdfdown   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_less_700_pdfup     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")
fTT_Mtt_less_700_scaledown = TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown_type1.root")
fTT_Mtt_less_700_scaleup   = TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup_type1.root")

fTT_Mtt_700_1000_nom       = TFile("histfiles/TT_Mtt-700to1000-channel_Histos_type1.root")
fTT_Mtt_700_1000_jecdown   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_700_1000_jecup     = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_700_1000_jerdown   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
#fTT_Mtt_700_1000_jernom   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jernom_type1.root")
fTT_Mtt_700_1000_jerup     = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_700_1000_qcd     = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")
fTT_Mtt_700_1000_pdfdown   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_700_1000_pdfup     = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")
fTT_Mtt_700_1000_scaledown = TFile("histfiles/TT_700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown_type1.root")
fTT_Mtt_700_1000_scaleup   = TFile("histfiles/TT_700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup_type1.root")

fTT_Mtt_1000_Inf_nom       = TFile("histfiles/TT_Mtt-1000toInf-channel_Histos_type1.root")
fTT_Mtt_1000_Inf_jecdown   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_1000_Inf_jecup     = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_1000_Inf_jerdown   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
#fTT_Mtt_1000_Inf_jernom   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jernom_type1.root")
fTT_Mtt_1000_Inf_jerup     = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_1000_Inf_qcd     = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")
fTT_Mtt_1000_Inf_pdfdown   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_1000_Inf_pdfup     = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")
fTT_Mtt_1000_Inf_scaledown = TFile("histfiles/TT_1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaledown_type1.root")
fTT_Mtt_1000_Inf_scaleup   = TFile("histfiles/TT_1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_1_mu_scaleup_type1.root")



print "==================================== Get Hists ====================================="

#hRecoMC.SetName("hRecoMC")
hRecoData = None
hMeas = None
hRecoQCD = None
if not options.ignoreData : 
    hRecoData= fdata.Get(options.hist).Clone()
    hRecoData.SetName("hRecoData")


# Get the histogram files
hMeas_QCD_SingleMu = fQCD_SingleMu.Get(options.hist).Clone()

hMeas_T_t_nom     = fT_t_nom.Get(options.hist).Clone()
hMeas_T_t_jecdown = fT_t_jecdown.Get(options.hist).Clone()
hMeas_T_t_jecup   = fT_t_jecup.Get(options.hist).Clone()
hMeas_T_t_jerdown = fT_t_jerdown.Get(options.hist).Clone()
hMeas_T_t_jerup   = fT_t_jerup.Get(options.hist).Clone()
hMeas_T_t_qcd   = fT_t_qcd.Get(options.hist).Clone()


hMeas_Tbar_t_nom     = fTbar_t_nom.Get(options.hist).Clone()
hMeas_Tbar_t_jecdown = fTbar_t_jecdown.Get(options.hist).Clone()
hMeas_Tbar_t_jecup   = fTbar_t_jecup.Get(options.hist).Clone()
hMeas_Tbar_t_jerdown = fTbar_t_jerdown.Get(options.hist).Clone()
hMeas_Tbar_t_jerup   = fTbar_t_jerup.Get(options.hist).Clone()
hMeas_Tbar_t_qcd   = fTbar_t_qcd.Get(options.hist).Clone()


hMeas_T_s_nom     = fT_s_nom.Get(options.hist).Clone()
hMeas_T_s_jecdown = fT_s_jecdown.Get(options.hist).Clone()
hMeas_T_s_jecup   = fT_s_jecup.Get(options.hist).Clone()
hMeas_T_s_jerdown = fT_s_jerdown.Get(options.hist).Clone()
hMeas_T_s_jerup   = fT_s_jerup.Get(options.hist).Clone()
hMeas_T_s_qcd   = fT_s_qcd.Get(options.hist).Clone()


hMeas_Tbar_s_nom     = fTbar_s_nom.Get(options.hist).Clone()
hMeas_Tbar_s_jecdown = fTbar_s_jecdown.Get(options.hist).Clone()
hMeas_Tbar_s_jecup   = fTbar_s_jecup.Get(options.hist).Clone()
hMeas_Tbar_s_jerdown = fTbar_s_jerdown.Get(options.hist).Clone()
hMeas_Tbar_s_jerup   = fTbar_s_jerup.Get(options.hist).Clone()
hMeas_Tbar_s_qcd   = fTbar_s_qcd.Get(options.hist).Clone()


hMeas_T_tW_nom     = fT_tW_nom.Get(options.hist).Clone()
hMeas_T_tW_jecdown = fT_tW_jecdown.Get(options.hist).Clone()
hMeas_T_tW_jecup   = fT_tW_jecup.Get(options.hist).Clone()
hMeas_T_tW_jerdown = fT_tW_jerdown.Get(options.hist).Clone()
hMeas_T_tW_jerup   = fT_tW_jerup.Get(options.hist).Clone()
hMeas_T_tW_qcd   = fT_tW_qcd.Get(options.hist).Clone()


hMeas_Tbar_tW_nom     = fTbar_tW_nom.Get(options.hist).Clone()
hMeas_Tbar_tW_jecdown = fTbar_tW_jecdown.Get(options.hist).Clone()
hMeas_Tbar_tW_jecup   = fTbar_tW_jecup.Get(options.hist).Clone()
hMeas_Tbar_tW_jerdown = fTbar_tW_jerdown.Get(options.hist).Clone()
hMeas_Tbar_tW_jerup   = fTbar_tW_jerup.Get(options.hist).Clone()
hMeas_Tbar_tW_qcd   = fTbar_tW_qcd.Get(options.hist).Clone()


hMeas_WJets_nom     = fWJets_nom.Get(options.hist).Clone()
hMeas_WJets_jecdown = fWJets_jecdown.Get(options.hist).Clone()
hMeas_WJets_jecup   = fWJets_jecup.Get(options.hist).Clone()
hMeas_WJets_jerdown = fWJets_jerdown.Get(options.hist).Clone()
hMeas_WJets_jerup   = fWJets_jerup.Get(options.hist).Clone()
hMeas_WJets_qcd   = fWJets_qcd.Get(options.hist).Clone()


hMeas_TT_Mtt_less_700_nom       = fTT_Mtt_less_700_nom.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jecdown   = fTT_Mtt_less_700_jecdown.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jecup     = fTT_Mtt_less_700_jecup.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jerdown   = fTT_Mtt_less_700_jerdown.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jerup     = fTT_Mtt_less_700_jerup.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_qcd     = fTT_Mtt_less_700_qcd.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_pdfdown   = fTT_Mtt_less_700_pdfdown.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_pdfup     = fTT_Mtt_less_700_pdfup.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_scaledown = fTT_Mtt_less_700_scaledown.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_scaleup   = fTT_Mtt_less_700_scaleup.Get(options.hist).Clone()


hMeas_TT_Mtt_700_1000_nom       = fTT_Mtt_700_1000_nom.Get(options.hist).Clone() 
hMeas_TT_Mtt_700_1000_jecdown   = fTT_Mtt_700_1000_jecdown.Get(options.hist).Clone()
hMeas_TT_Mtt_700_1000_jecup     = fTT_Mtt_700_1000_jecup.Get(options.hist).Clone()
hMeas_TT_Mtt_700_1000_jerdown   = fTT_Mtt_700_1000_jerdown.Get(options.hist).Clone()
#hMeas_TT_Mtt_700_1000_jernom   = fTT_Mtt_700_1000_jernom.Get(options.hist).Clone()
hMeas_TT_Mtt_700_1000_jerup     = fTT_Mtt_700_1000_jerup.Get(options.hist).Clone()
hMeas_TT_Mtt_700_1000_qcd     = fTT_Mtt_700_1000_qcd.Get(options.hist).Clone()
hMeas_TT_Mtt_700_1000_pdfdown   = fTT_Mtt_700_1000_pdfdown.Get(options.hist).Clone()
hMeas_TT_Mtt_700_1000_pdfup     = fTT_Mtt_700_1000_pdfup.Get(options.hist).Clone()
hMeas_TT_Mtt_700_1000_scaledown = fTT_Mtt_700_1000_scaledown.Get(options.hist).Clone()
hMeas_TT_Mtt_700_1000_scaleup   = fTT_Mtt_700_1000_scaleup.Get(options.hist).Clone()


hMeas_TT_Mtt_1000_Inf_nom       = fTT_Mtt_1000_Inf_nom.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_jecdown   = fTT_Mtt_1000_Inf_jecdown.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_jecup     = fTT_Mtt_1000_Inf_jecup.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_jerdown   = fTT_Mtt_1000_Inf_jerdown.Get(options.hist).Clone()
#hMeas_TT_Mtt_1000_Inf_jernom   = fTT_Mtt_1000_Inf_jernom.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_jerup     = fTT_Mtt_1000_Inf_jerup.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_qcd     = fTT_Mtt_1000_Inf_qcd.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_pdfdown   = fTT_Mtt_1000_Inf_pdfdown.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_pdfup     = fTT_Mtt_1000_Inf_pdfup.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_scaledown = fTT_Mtt_1000_Inf_scaledown.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_scaleup   = fTT_Mtt_1000_Inf_scaleup.Get(options.hist).Clone()



hMeas_QCD_SingleMu.SetName('hMeas_fQCD_SingleMu')

hMeas_T_t_nom     .SetName( 'hMeas_T_t')
hMeas_T_t_jecdown .SetName( 'hMeas_T_t_jecdown' )
hMeas_T_t_jecup   .SetName( 'hMeas_T_t_jecup' )
hMeas_T_t_jerdown .SetName( 'hMeas_T_t_jerdown' )
hMeas_T_t_jerup   .SetName( 'hMeas_T_t_jerup' )
hMeas_T_t_qcd   .SetName( 'hMeas_T_t_qcd' )

hMeas_Tbar_t_nom     .SetName( 'hMeas_Tbar_t')
hMeas_Tbar_t_jecdown .SetName( 'hMeas_Tbar_t_jecdown' )
hMeas_Tbar_t_jecup   .SetName( 'hMeas_Tbar_t_jecup' )
hMeas_Tbar_t_jerdown .SetName( 'hMeas_Tbar_t_jerdown' )
hMeas_Tbar_t_jerup   .SetName( 'hMeas_Tbar_t_jerup' )
hMeas_Tbar_t_qcd   .SetName( 'hMeas_Tbar_t_qcd' )

hMeas_T_s_nom     .SetName( 'hMeas_T_s')
hMeas_T_s_jecdown .SetName( 'hMeas_T_s_jecdown' )
hMeas_T_s_jecup   .SetName( 'hMeas_T_s_jecup' )
hMeas_T_s_jerdown .SetName( 'hMeas_T_s_jerdown' )
hMeas_T_s_jerup   .SetName( 'hMeas_T_s_jerup' )
hMeas_T_s_qcd   .SetName( 'hMeas_T_s_qcd' )

hMeas_Tbar_s_nom     .SetName( 'hMeas_Tbar_s')
hMeas_Tbar_s_jecdown .SetName( 'hMeas_Tbar_s_jecdown' )
hMeas_Tbar_s_jecup   .SetName( 'hMeas_Tbar_s_jecup' )
hMeas_Tbar_s_jerdown .SetName( 'hMeas_Tbar_s_jerdown' )
hMeas_Tbar_s_jerup   .SetName( 'hMeas_Tbar_s_jerup' )
hMeas_Tbar_s_qcd   .SetName( 'hMeas_Tbar_s_qcd' )

hMeas_T_tW_nom     .SetName( 'hMeas_T_tW')
hMeas_T_tW_jecdown .SetName( 'hMeas_T_tW_jecdow' )
hMeas_T_tW_jecup   .SetName( 'hMeas_T_tW_jecup' )
hMeas_T_tW_jerdown .SetName( 'hMeas_T_tW_jerdown' )
hMeas_T_tW_jerup   .SetName( 'hMeas_T_tW_jerup' )
hMeas_T_tW_qcd   .SetName( 'hMeas_T_tW_qcd' )

hMeas_Tbar_tW_nom     .SetName( 'hMeas_Tbar_tW')
hMeas_Tbar_tW_jecdown .SetName( 'hMeas_Tbar_tW_jecdown' )
hMeas_Tbar_tW_jecup   .SetName( 'hMeas_Tbar_tW_jecup' )
hMeas_Tbar_tW_jerdown .SetName( 'hMeas_Tbar_tW_jerdown' )
hMeas_Tbar_tW_jerup   .SetName( 'hMeas_Tbar_tW_jerup ' )
hMeas_Tbar_tW_qcd   .SetName( 'hMeas_Tbar_tW_qcd ' )

hMeas_WJets_nom     .SetName( 'hMeas_WJets')
hMeas_WJets_jecdown .SetName( 'hMeas_WJets_jecdown' )
hMeas_WJets_jecup   .SetName( 'hMeas_WJets_jecup' )
hMeas_WJets_jerdown .SetName( 'hMeas_WJets_jerdown' )
hMeas_WJets_jerup   .SetName( 'hMeas_WJets_jerup' )
hMeas_WJets_qcd   .SetName( 'hMeas_WJets_qcd' )

hMeas_TT_Mtt_less_700_nom       .SetName( 'hMeas_TT_Mtt_less_70' )
hMeas_TT_Mtt_less_700_jecdown   .SetName( 'hMeas_TT_Mtt_less_700_jecdown')
hMeas_TT_Mtt_less_700_jecup     .SetName( 'hMeas_TT_Mtt_less_700_jecup')
hMeas_TT_Mtt_less_700_jerdown   .SetName( 'hMeas_TT_Mtt_less_700_jerdown')
hMeas_TT_Mtt_less_700_jerup     .SetName( 'hMeas_TT_Mtt_less_700_jerup')
hMeas_TT_Mtt_less_700_qcd     .SetName( 'hMeas_TT_Mtt_less_700_qcd')
hMeas_TT_Mtt_less_700_pdfdown   .SetName( 'hMeas_TT_Mtt_less_700_pdfdown')
hMeas_TT_Mtt_less_700_pdfup     .SetName( 'hMeas_TT_Mtt_less_700_pdfup')
hMeas_TT_Mtt_less_700_scaledown .SetName( 'hMeas_TT_Mtt_less_700_scaledown')
hMeas_TT_Mtt_less_700_scaleup   .SetName( 'hMeas_TT_Mtt_less_700_scaleup')

hMeas_TT_Mtt_700_1000_nom       .SetName( 'hMeas_TT_Mtt_700_100' )
hMeas_TT_Mtt_700_1000_jecdown   .SetName( 'hMeas_TT_Mtt_700_1000_jecdown')
hMeas_TT_Mtt_700_1000_jecup     .SetName( 'hMeas_TT_Mtt_700_1000_jecup')
hMeas_TT_Mtt_700_1000_jerdown   .SetName( 'hMeas_TT_Mtt_700_1000_jerdown')
hMeas_TT_Mtt_700_1000_jerup     .SetName( 'hMeas_TT_Mtt_700_1000_jerup')
hMeas_TT_Mtt_700_1000_qcd     .SetName( 'hMeas_TT_Mtt_700_1000_qcd')
hMeas_TT_Mtt_700_1000_pdfdown   .SetName( 'hMeas_TT_Mtt_700_1000_pdfdown')
hMeas_TT_Mtt_700_1000_pdfup     .SetName( 'hMeas_TT_Mtt_700_1000_pdfup')
hMeas_TT_Mtt_700_1000_scaledown .SetName( 'hMeas_TT_Mtt_700_1000_scaledown')
hMeas_TT_Mtt_700_1000_scaleup   .SetName( 'hMeas_TT_Mtt_700_1000_scaleup')

hMeas_TT_Mtt_1000_Inf_nom       .SetName( 'hMeas_TT_Mtt_1000 ' )
hMeas_TT_Mtt_1000_Inf_jecdown   .SetName( 'hMeas_TT_Mtt_1000_Inf_jecdown')
hMeas_TT_Mtt_1000_Inf_jecup     .SetName( 'hMeas_TT_Mtt_1000_Inf_jecup')
hMeas_TT_Mtt_1000_Inf_jerdown   .SetName( 'hMeas_TT_Mtt_1000_Inf_jerdown')
hMeas_TT_Mtt_1000_Inf_jerup     .SetName( 'hMeas_TT_Mtt_1000_Inf_jerup')
hMeas_TT_Mtt_1000_Inf_qcd     .SetName( 'hMeas_TT_Mtt_1000_Inf_qcd')
hMeas_TT_Mtt_1000_Inf_pdfdown   .SetName( 'hMeas_TT_Mtt_1000_Inf_pdfdown')
hMeas_TT_Mtt_1000_Inf_pdfup     .SetName( 'hMeas_TT_Mtt_1000_Inf_pdfup')
hMeas_TT_Mtt_1000_Inf_scaledown .SetName( 'hMeas_TT_Mtt_1000_Inf_scaledown')
hMeas_TT_Mtt_1000_Inf_scaleup   .SetName( 'hMeas_TT_Mtt_1000_Inf_scaleup')



hMeas_T_t_nom    .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_jecdown.Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_jecup  .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_jerdown.Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_jerup  .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_qcd  .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )

hMeas_Tbar_t_nom    .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_jecdown.Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_jecup  .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_jerdown.Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_jerup  .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_qcd  .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )

hMeas_T_s_nom    .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_jecdown.Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_jecup  .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_jerdown.Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_jerup  .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_qcd  .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )

hMeas_Tbar_s_nom    .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_jecdown.Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_jecup  .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_jerdown.Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_jerup  .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_qcd  .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )

hMeas_T_tW_nom    .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_jecdown.Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_jecup  .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_jerdown.Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_jerup  .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_qcd  .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )

hMeas_Tbar_tW_nom    .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_jecdown.Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_jecup  .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_jerdown.Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_jerup  .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_qcd  .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )

hMeas_WJets_nom    .Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_jecdown.Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_jecup  .Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_jerdown.Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_jerup  .Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_qcd  .Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )

hMeas_TT_Mtt_less_700_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jecdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jecup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jerdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jerup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_qcd    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_pdfdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_pdfup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)

hMeas_TT_Mtt_700_1000_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jecdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jecup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jerdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
#hMeas_TT_Mtt_700_1000_jernom  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jerup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_qcd    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_pdfdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_pdfup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)

hMeas_TT_Mtt_1000_Inf_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jecdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jecup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jerdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
#hMeas_TT_Mtt_1000_Inf_jernom  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jerup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_qcd    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_pdfdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_pdfup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )

hists = []

hMeas_TT_Mtt_less_700 = [ hMeas_TT_Mtt_less_700_jecdown   , hMeas_TT_Mtt_less_700_jecup   , 
                          hMeas_TT_Mtt_less_700_jerdown   , hMeas_TT_Mtt_less_700_jerup   , 
                          hMeas_TT_Mtt_less_700_pdfdown   , hMeas_TT_Mtt_less_700_pdfup   , hMeas_TT_Mtt_less_700_nom , 
                          hMeas_TT_Mtt_less_700_scaledown , hMeas_TT_Mtt_less_700_scaleup ]

hMeas_TT_Mtt_700_1000 = [ hMeas_TT_Mtt_700_1000_jecdown   , hMeas_TT_Mtt_700_1000_jecup   , 
                          hMeas_TT_Mtt_700_1000_jerdown   , hMeas_TT_Mtt_700_1000_jerup   , 
                          hMeas_TT_Mtt_700_1000_pdfdown   , hMeas_TT_Mtt_700_1000_pdfup   , hMeas_TT_Mtt_700_1000_nom ,
                          hMeas_TT_Mtt_700_1000_scaledown , hMeas_TT_Mtt_700_1000_scaleup ]

hMeas_TT_Mtt_1000_Inf = [ hMeas_TT_Mtt_1000_Inf_jecdown   , hMeas_TT_Mtt_1000_Inf_jecup   , 
                          hMeas_TT_Mtt_1000_Inf_jerdown   , hMeas_TT_Mtt_1000_Inf_jerup   , 
                          hMeas_TT_Mtt_1000_Inf_pdfdown   , hMeas_TT_Mtt_1000_Inf_pdfup   , hMeas_TT_Mtt_1000_Inf_nom ,
                          hMeas_TT_Mtt_1000_Inf_scaledown , hMeas_TT_Mtt_1000_Inf_scaleup ]

hMeas_T_t     = [ hMeas_T_t_jecdown     , hMeas_T_t_jecup     , hMeas_T_t_jerdown     , hMeas_T_t_jerup     , hMeas_T_t_nom    , hMeas_T_t_nom      , hMeas_T_t_nom     , hMeas_T_t_nom     , hMeas_T_t_nom]

hMeas_Tbar_t  = [ hMeas_Tbar_t_jecdown  , hMeas_Tbar_t_jecup  , hMeas_Tbar_t_jerdown  , hMeas_Tbar_t_jerup  , hMeas_Tbar_t_nom , hMeas_Tbar_t_nom   , hMeas_Tbar_t_nom  , hMeas_Tbar_t_nom  , hMeas_Tbar_t_nom]

hMeas_T_s     = [ hMeas_T_s_jecdown     , hMeas_T_s_jecup     , hMeas_T_s_jerdown     , hMeas_T_s_jerup     , hMeas_T_s_nom     , hMeas_T_s_nom     , hMeas_T_s_nom     , hMeas_T_s_nom     , hMeas_T_s_nom]

hMeas_Tbar_s  = [ hMeas_Tbar_s_jecdown  , hMeas_Tbar_s_jecup  , hMeas_Tbar_s_jerdown  , hMeas_Tbar_s_jerup  , hMeas_Tbar_s_nom  , hMeas_Tbar_s_nom  , hMeas_Tbar_s_nom  , hMeas_Tbar_s_nom  , hMeas_Tbar_s_nom]

hMeas_T_tW    = [ hMeas_T_t_jecdown     , hMeas_T_t_jecup     , hMeas_T_t_jerdown     , hMeas_T_t_jerup     , hMeas_T_t_nom     , hMeas_T_t_nom     , hMeas_T_t_nom     , hMeas_T_t_nom     , hMeas_T_t_nom]

hMeas_Tbar_tW = [ hMeas_Tbar_tW_jecdown , hMeas_Tbar_tW_jecup , hMeas_Tbar_tW_jerdown , hMeas_Tbar_tW_jerup , hMeas_Tbar_tW_nom , hMeas_Tbar_tW_nom , hMeas_Tbar_tW_nom , hMeas_Tbar_tW_nom , hMeas_Tbar_tW_nom]

hMeas_WJets   = [ hMeas_WJets_jecdown   , hMeas_WJets_jecup   , hMeas_WJets_jerdown   , hMeas_WJets_jerup   , hMeas_WJets_nom   , hMeas_WJets_nom   , hMeas_WJets_nom   , hMeas_WJets_nom   , hMeas_WJets_nom]

#hMeas_QCD     = [ hMeas_QCD_SingleMu    , hMeas_QCD_SingleMu  , hMeas_QCD_SingleMu    , hMeas_QCD_SingleMu  , hMeas_QCD_SingleMu, hMeas_QCD_SingleMu, hMeas_QCD_SingleMu, hMeas_QCD_SingleMu, hMeas_QCD_SingleMu]

hMeas_TT_Mtt = []
hMeas_SingleTop = []

stacks = []

qcdcanvs = []

# First, we need to correct the QCD estimate with the known MC backgrounds.
iiqcd = 0
qcdstack = THStack("qcdstack", "qcdstack")
hMeas_QCD_SingleMu_ToPlot = hMeas_QCD_SingleMu.Clone()
qcdcolors = [TColor.kMagenta, TColor.kMagenta,
             TColor.kMagenta, TColor.kMagenta,
             TColor.kMagenta, TColor.kMagenta,
             TColor.kGreen, TColor.kRed, TColor.kRed, TColor.kRed
             ]
hMeas_QCD_SingleMu_ToPlot.SetName("hmeas_QCD_SingleMu_ToPlot")



# Scale to desired normalization
# Options are :
#  1. From MC
#  2. From fit
#
# For now, we don't have the fit, so we do from MC

hMeas_QCD_SingleMu.Scale( NQCD / hMeas_QCD_SingleMu.Integral() )


for iqcdHist in [ hMeas_T_t_qcd, hMeas_Tbar_t_qcd,
                  hMeas_T_s_qcd, hMeas_Tbar_s_qcd,
                  hMeas_T_tW_qcd, hMeas_Tbar_tW_qcd,
                  hMeas_WJets_qcd,
                  hMeas_TT_Mtt_less_700_qcd, hMeas_TT_Mtt_700_1000_qcd,
                  hMeas_TT_Mtt_1000_Inf_qcd] :
    iqcdHist.SetFillColor(qcdcolors[iiqcd])
    hMeas_QCD_SingleMu.Add( iqcdHist, -1.0 )
    qcdstack.Add( iqcdHist )
    iiqcd += 1

qcdcanv = TCanvas( "qcddatamc", "qcddatamc")
hMeas_QCD_SingleMu_ToPlot.Draw("e")
qcdstack.Draw("same hist")
hMeas_QCD_SingleMu_ToPlot.Draw("e same")



legs = []

for m in range(0,len(plots)):

    

    leg = TLegend(0.5, 0.55, 0.84, 0.84)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)

    hMeas_TTbar     = TTbar.get(plots[m])
    hMeas_SingleTop = SingleTop.get(plots[m])
    hMeas_WJets     = WJets.get(plots[m])
    hMeas_QCD       = QCD.get(plots[m])

    hRecoData       = Data.get(plots[m])
     
    leg.AddEntry( hMeas_TTbar, 't#bar{t}', 'f')
    leg.AddEntry( hMeas_SingleTop, 'single top', 'f')
    leg.AddEntry( hMeas_WJets, 'W+jets', 'f')
    leg.AddEntry( hMeas_QCD, 'QCD' , 'f')

    
    if 'vtxMass' in  options.hist :
        for zerohist in [hMeas_WJets, hMeas_SingleTop, hMeas_TTbar, hMeas_QCD ] :
            zerohist.SetBinContent(1, 0.0)
        if options.ignoreData == False :
            hRecoData.SetBinContent(1, 0.0)
    
    # Make a stack plot of the MC to compare to data
    hMC_stack = THStack("hMC_stack",
                        hMeas_TTbar.GetTitle() + ';' +
                        hMeas_TTbar.GetXaxis().GetTitle() + ';' +
                        hMeas_TTbar.GetYaxis().GetTitle()
                        )
    hMC_stack.Add( hMeas_QCD )
    hMC_stack.Add( hMeas_WJets )
    hMC_stack.Add( hMeas_SingleTop )
    hMC_stack.Add( hMeas_TTbar )


    print 'Normalizations : ttbar = {0:10.2f}, single top = {1:10.2f}, wjets = {2:10.2f}, qcd = {3:10.2f}   ===== data = {4:10.2f}'.format(
        hMeas_TTbar.Integral(), hMeas_SingleTop.Integral(), hMeas_WJets.Integral(), hMeas_QCD.Integral(), hRecoData.Integral()
            )

    stacks.append( hMC_stack )
    # TO DO : NEED TO FIX THE BINNING FOR QCD : 
    #MC_stack.Add( hRecoQCD )
    #hMC_stack.Add( hRecoMC )

   
    c = TCanvas("datamc" + plots[m] , "datamc" + plots[m])
    if not options.ignoreData :
        leg.AddEntry( hRecoData, '19.6 fb^{-1}', 'p')
        hRecoData.UseCurrentStyle()
        hRecoData.Draw('e')
        hMC_stack.Draw("hist same")
        hRecoData.Draw('e same')
        hRecoData.SetMaximum( options.maxy )
    else :
        hMC_stack.UseCurrentStyle()
        hMC_stack.Draw("hist")
    if options.drawLegend :
        leg.Draw()

    canvs.append(c)
    legs.append(leg)
    if not options.ignoreData : 
        c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist + '.png' )
        c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist + '.pdf' )
    else : 
        c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist + '_nodata.png' )
        c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist + '_nodata.pdf' )


        
    # write the histogram in a rootfile



for sample in [Data, QCD, TTbar, SingleTop, WJets]:
    sample.writeForTheta(fout)

fout.Close()
   
    
