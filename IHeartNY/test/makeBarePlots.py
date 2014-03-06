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

Nmc_ttbar_scaledown = 5387181
Nmc_ttbar_scaleup   = 5009488
Nmc_TT_Mtt_700_1000_scaledown = 2146989
Nmc_TT_Mtt_700_1000_scaleup = 2212832
Nmc_TT_Mtt_1000_Inf_scaledown = 1308090
Nmc_TT_Mtt_1000_Inf_scaleup = 1233938

# QCD Normalization from MET fits
NQCD = options.NQCD

# ttbar filter efficiencies
e_TT_Mtt_700_1000 = 0.074
e_TT_Mtt_1000_Inf = 0.014
e_TT_Mtt_0_700 = 1.0 - e_TT_Mtt_700_1000 - e_TT_Mtt_1000_Inf
# 

names = [ 'DATA', 'TTbar', 'WJets', 'SingleTop', 'QCD_SingleMu' ]
canvs = []
histsData = []

# Open the output file 

fout = TFile("normalized_" + options.outname + '_' + options.hist + ".root" , "RECREATE")


# ==============================================================================
#  Example Unfolding
# ==============================================================================

if not options.ignoreData : 
    fdata = TFile("histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom_type1.root")

if not options.ignoreQCD :
    fQCD = TFile("histfiles/SingleMu_iheartNY_V1_mu_Run2012_qcd_type1.root")
    

fQCD_SingleMu = TFile("histfiles/SingleMu_iheartNY_V1_mu_Run2012_qcd_type1.root")

fT_t_nom     = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_type1.root")
fT_t_jecdown = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_t_jecup   = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_t_jerdown = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_t_jerup   = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fT_t_qcd   = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")


fTbar_t_nom     = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_type1.root")
fTbar_t_jecdown = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTbar_t_jecup   = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTbar_t_jerdown = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTbar_t_jerup   = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTbar_t_qcd   = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")

fT_s_nom     = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_type1.root")
fT_s_jecdown = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_s_jecup   = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_s_jerdown = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_s_jerup   = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fT_s_qcd   = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")


fTbar_s_nom     = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_nom_type1.root")
fTbar_s_jecdown = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jecdn_type1.root")
fTbar_s_jecup   = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jecup_type1.root")
fTbar_s_jerdown = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jerdn_type1.root")
fTbar_s_jerup   = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jerup_type1.root")
fTbar_s_qcd   = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_qcd_type1.root")


fT_tW_nom     = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_type1.root")
fT_tW_jecdown = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_tW_jecup   = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_tW_jerdown = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_tW_jerup   = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fT_tW_qcd   = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")


fTbar_tW_nom     = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_type1.root")
fTbar_tW_jecdown = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTbar_tW_jecup   = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTbar_tW_jerdown = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTbar_tW_jerup   = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTbar_tW_qcd   = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")


fWJets_nom     = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_nom_type1.root")
fWJets_jecdown = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jecdn_type1.root")
fWJets_jecup   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jecup_type1.root")
fWJets_jerdown = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jerdn_type1.root")
fWJets_jerup   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jerup_type1.root")
fWJets_qcd   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_qcd_type1.root")


fTT_Mtt_less_700_nom       = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_type1.root")
fTT_Mtt_less_700_jecdown   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_less_700_jecup     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_less_700_jerdown   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTT_Mtt_less_700_jerup     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_less_700_qcd     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")
fTT_Mtt_less_700_pdfdown   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_less_700_pdfup     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")
fTT_Mtt_less_700_scaledown = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown_type1.root")
fTT_Mtt_less_700_scaleup   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup_type1.root")

fTT_Mtt_700_1000_nom       = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_type1.root")
fTT_Mtt_700_1000_jecdown   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_700_1000_jecup     = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_700_1000_jerdown   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
#fTT_Mtt_700_1000_jernom   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jernom_type1.root")
fTT_Mtt_700_1000_jerup     = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_700_1000_qcd     = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")
fTT_Mtt_700_1000_pdfdown   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_700_1000_pdfup     = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")
fTT_Mtt_700_1000_scaledown = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown_type1.root")
fTT_Mtt_700_1000_scaleup   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup_type1.root")

fTT_Mtt_1000_Inf_nom       = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_type1.root")
fTT_Mtt_1000_Inf_jecdown   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_1000_Inf_jecup     = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_1000_Inf_jerdown   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
#fTT_Mtt_1000_Inf_jernom   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jernom_type1.root")
fTT_Mtt_1000_Inf_jerup     = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_1000_Inf_qcd     = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_qcd_type1.root")
fTT_Mtt_1000_Inf_pdfdown   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_1000_Inf_pdfup     = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")
fTT_Mtt_1000_Inf_scaledown = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown_type1.root")
fTT_Mtt_1000_Inf_scaleup   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup_type1.root")



print "==================================== Get Hists ====================================="

#hRecoMC.SetName("hRecoMC")
hRecoData = None
hMeas = None
hRecoQCD = None
if not options.ignoreData : 
    hRecoData= fdata.Get(options.hist).Clone()
    hRecoData.SetName(options.hist + "__DATA"  )


# Get the histogram files
hMeas_QCD_SingleMu = fQCD_SingleMu.Get(options.hist).Clone()
hMeas_QCD_SingleMu.SetName(options.hist + "__QCD")

hMeas_T_t_nom     = fT_t_nom.Get(options.hist).Clone()
hMeas_T_t_jecdown = fT_t_jecdown.Get(options.hist).Clone()
hMeas_T_t_jecup   = fT_t_jecup.Get(options.hist).Clone()
hMeas_T_t_jerdown = fT_t_jerdown.Get(options.hist).Clone()
hMeas_T_t_jerup   = fT_t_jerup.Get(options.hist).Clone()
hMeas_T_t_qcd     = fT_t_qcd.Get(options.hist).Clone()


hMeas_Tbar_t_nom     = fTbar_t_nom.Get(options.hist).Clone()
hMeas_Tbar_t_jecdown = fTbar_t_jecdown.Get(options.hist).Clone()
hMeas_Tbar_t_jecup   = fTbar_t_jecup.Get(options.hist).Clone()
hMeas_Tbar_t_jerdown = fTbar_t_jerdown.Get(options.hist).Clone()
hMeas_Tbar_t_jerup   = fTbar_t_jerup.Get(options.hist).Clone()
hMeas_Tbar_t_qcd     = fTbar_t_qcd.Get(options.hist).Clone()


hMeas_T_s_nom     = fT_s_nom.Get(options.hist).Clone()
hMeas_T_s_jecdown = fT_s_jecdown.Get(options.hist).Clone()
hMeas_T_s_jecup   = fT_s_jecup.Get(options.hist).Clone()
hMeas_T_s_jerdown = fT_s_jerdown.Get(options.hist).Clone()
hMeas_T_s_jerup   = fT_s_jerup.Get(options.hist).Clone()
hMeas_T_s_qcd     = fT_s_qcd.Get(options.hist).Clone()


hMeas_Tbar_s_nom     = fTbar_s_nom.Get(options.hist).Clone()
hMeas_Tbar_s_jecdown = fTbar_s_jecdown.Get(options.hist).Clone()
hMeas_Tbar_s_jecup   = fTbar_s_jecup.Get(options.hist).Clone()
hMeas_Tbar_s_jerdown = fTbar_s_jerdown.Get(options.hist).Clone()
hMeas_Tbar_s_jerup   = fTbar_s_jerup.Get(options.hist).Clone()
hMeas_Tbar_s_qcd     = fTbar_s_qcd.Get(options.hist).Clone()


hMeas_T_tW_nom     = fT_tW_nom.Get(options.hist).Clone()
hMeas_T_tW_jecdown = fT_tW_jecdown.Get(options.hist).Clone()
hMeas_T_tW_jecup   = fT_tW_jecup.Get(options.hist).Clone()
hMeas_T_tW_jerdown = fT_tW_jerdown.Get(options.hist).Clone()
hMeas_T_tW_jerup   = fT_tW_jerup.Get(options.hist).Clone()
hMeas_T_tW_qcd     = fT_tW_qcd.Get(options.hist).Clone()


hMeas_Tbar_tW_nom     = fTbar_tW_nom.Get(options.hist).Clone()
hMeas_Tbar_tW_jecdown = fTbar_tW_jecdown.Get(options.hist).Clone()
hMeas_Tbar_tW_jecup   = fTbar_tW_jecup.Get(options.hist).Clone()
hMeas_Tbar_tW_jerdown = fTbar_tW_jerdown.Get(options.hist).Clone()
hMeas_Tbar_tW_jerup   = fTbar_tW_jerup.Get(options.hist).Clone()
hMeas_Tbar_tW_qcd     = fTbar_tW_qcd.Get(options.hist).Clone()


hMeas_WJets_nom     = fWJets_nom.Get(options.hist).Clone()
hMeas_WJets_jecdown = fWJets_jecdown.Get(options.hist).Clone()
hMeas_WJets_jecup   = fWJets_jecup.Get(options.hist).Clone()
hMeas_WJets_jerdown = fWJets_jerdown.Get(options.hist).Clone()
hMeas_WJets_jerup   = fWJets_jerup.Get(options.hist).Clone()
hMeas_WJets_qcd     = fWJets_qcd.Get(options.hist).Clone()


hMeas_TT_Mtt_less_700_nom       = fTT_Mtt_less_700_nom.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jecdown   = fTT_Mtt_less_700_jecdown.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jecup     = fTT_Mtt_less_700_jecup.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jerdown   = fTT_Mtt_less_700_jerdown.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jerup     = fTT_Mtt_less_700_jerup.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_qcd       = fTT_Mtt_less_700_qcd.Get(options.hist).Clone()
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
hMeas_TT_Mtt_700_1000_qcd       = fTT_Mtt_700_1000_qcd.Get(options.hist).Clone()
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
hMeas_TT_Mtt_1000_Inf_qcd       = fTT_Mtt_1000_Inf_qcd.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_pdfdown   = fTT_Mtt_1000_Inf_pdfdown.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_pdfup     = fTT_Mtt_1000_Inf_pdfup.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_scaledown = fTT_Mtt_1000_Inf_scaledown.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_scaleup   = fTT_Mtt_1000_Inf_scaleup.Get(options.hist).Clone()


hMeas_T_t_nom     .SetName( options.hist + '__T_t')
hMeas_T_t_jecdown .SetName( options.hist + '__T_t__jec__down' )
hMeas_T_t_jecup   .SetName( options.hist + '__T_t__jec__up' )
hMeas_T_t_jerdown .SetName( options.hist + '__T_t__jer__down' )
hMeas_T_t_jerup   .SetName( options.hist + '__T_t__jer__up' )
hMeas_T_t_qcd     .SetName( options.hist + '__T_t__qcd' )

hMeas_Tbar_t_nom     .SetName( options.hist + '__Tbar_t')
hMeas_Tbar_t_jecdown .SetName( options.hist + '__Tbar_t__jec__down' )
hMeas_Tbar_t_jecup   .SetName( options.hist + '__Tbar_t__jec__up' )
hMeas_Tbar_t_jerdown .SetName( options.hist + '__Tbar_t__jer__down' )
hMeas_Tbar_t_jerup   .SetName( options.hist + '__Tbar_t__jer__up' )
hMeas_Tbar_t_qcd     .SetName( options.hist + '__Tbar_t__qcd' )


hMeas_T_s_nom     .SetName( options.hist + '__T_s')
hMeas_T_s_jecdown .SetName( options.hist + '__T_s__jec__down' )
hMeas_T_s_jecup   .SetName( options.hist + '__T_s__jec__up' )
hMeas_T_s_jerdown .SetName( options.hist + '__T_s__jer__down' )
hMeas_T_s_jerup   .SetName( options.hist + '__T_s__jer__up' )
hMeas_T_s_qcd     .SetName( options.hist + '__T_s__qcd' )

hMeas_Tbar_s_nom     .SetName( options.hist + '__Tbar_s')
hMeas_Tbar_s_jecdown .SetName( options.hist + '__Tbar_s__jec__down' )
hMeas_Tbar_s_jecup   .SetName( options.hist + '__Tbar_s__jec__up' )
hMeas_Tbar_s_jerdown .SetName( options.hist + '__Tbar_s__jer__down' )
hMeas_Tbar_s_jerup   .SetName( options.hist + '__Tbar_s__jer__up' )
hMeas_Tbar_s_qcd     .SetName( options.hist + '__Tbar_s__qcd' )

hMeas_T_tW_nom     .SetName( options.hist + '__T_s')
hMeas_T_tW_jecdown .SetName( options.hist + '__T_tW__jec__down' )
hMeas_T_tW_jecup   .SetName( options.hist + '__T_tW__jec__up' )
hMeas_T_tW_jerdown .SetName( options.hist + '__T_tW__jer__down' )
hMeas_T_tW_jerup   .SetName( options.hist + '__T_tW__jer__up' )
hMeas_T_tW_qcd     .SetName( options.hist + '__T_tW__qcd' )

hMeas_Tbar_tW_nom     .SetName( options.hist + '__Tbar_s')
hMeas_Tbar_tW_jecdown .SetName( options.hist + '__Tbar_tW__jec__down' )
hMeas_Tbar_tW_jecup   .SetName( options.hist + '__Tbar_tW__jec__up' )
hMeas_Tbar_tW_jerdown .SetName( options.hist + '__Tbar_tW__jer__down' )
hMeas_Tbar_tW_jerup   .SetName( options.hist + '__Tbar_tW__jer__up' )
hMeas_Tbar_tW_qcd     .SetName( options.hist + '__Tbar_tW__qcd' )



hMeas_WJets_nom     .SetName( options.hist + '__WJets')
hMeas_WJets_jecdown .SetName( options.hist + '__WJets__jec__down' )
hMeas_WJets_jecup   .SetName( options.hist + '__WJets__jec__up' )
hMeas_WJets_jerdown .SetName( options.hist + '__WJets__jer__down' )
hMeas_WJets_jerup   .SetName( options.hist + '__WJets__jer__up' )
hMeas_WJets_qcd     .SetName( options.hist + '__WJets__qcd' )

hMeas_TT_Mtt_less_700_nom       .SetName( options.hist + '__TTbar_Mtt_less_700' )
hMeas_TT_Mtt_less_700_jecdown   .SetName( options.hist + '__TTbar_Mtt_less_700__jec__down')
hMeas_TT_Mtt_less_700_jecup     .SetName( options.hist + '__TTbar_Mtt_less_700__jec__up')
hMeas_TT_Mtt_less_700_jerdown   .SetName( options.hist + '__TTbar_Mtt_less_700__jer__down')
hMeas_TT_Mtt_less_700_jerup     .SetName( options.hist + '__TTbar_Mtt_less_700__jer__up')
hMeas_TT_Mtt_less_700_qcd       .SetName( options.hist + '__TTbar_Mtt_less_700__qcd')
hMeas_TT_Mtt_less_700_pdfdown   .SetName( options.hist + '__TTbar_Mtt_less_700__pdf__down')
hMeas_TT_Mtt_less_700_pdfup     .SetName( options.hist + '__TTbar_Mtt_less_700__pdf__up')
hMeas_TT_Mtt_less_700_scaledown .SetName( options.hist + '__TTbar_Mtt_less_700__scale__down')
hMeas_TT_Mtt_less_700_scaleup   .SetName( options.hist + '__TTbar_Mtt_less_700__scale__up')

hMeas_TT_Mtt_700_1000_nom       .SetName( options.hist + '__TTbar_Mtt_700_100' )
hMeas_TT_Mtt_700_1000_jecdown   .SetName( options.hist + '__TTbar_Mtt_700_1000__jec__down')
hMeas_TT_Mtt_700_1000_jecup     .SetName( options.hist + '__TTbar_Mtt_700_1000__jec__up')
hMeas_TT_Mtt_700_1000_jerdown   .SetName( options.hist + '__TTbar_Mtt_700_1000__jer__down')
hMeas_TT_Mtt_700_1000_jerup     .SetName( options.hist + '__TTbar_Mtt_700_1000__jer__up')
hMeas_TT_Mtt_700_1000_qcd       .SetName( options.hist + '__TTbar_Mtt_700_1000__qcd')
hMeas_TT_Mtt_700_1000_pdfdown   .SetName( options.hist + '__TTbar_Mtt_700_1000__pdf__down')
hMeas_TT_Mtt_700_1000_pdfup     .SetName( options.hist + '__TTbar_Mtt_700_1000__pdf__up')
hMeas_TT_Mtt_700_1000_scaledown .SetName( options.hist + '__TTbar_Mtt_700_1000__scale__down')
hMeas_TT_Mtt_700_1000_scaleup   .SetName( options.hist + '__TTbar_Mtt_700_1000__scale__up')

hMeas_TT_Mtt_1000_Inf_nom       .SetName( options.hist + '__TTbar_Mtt_1000' )
hMeas_TT_Mtt_1000_Inf_jecdown   .SetName( options.hist + '__TTbar_Mtt_1000_Inf__jec__down')
hMeas_TT_Mtt_1000_Inf_jecup     .SetName( options.hist + '__TTbar_Mtt_1000_Inf__jec__up')
hMeas_TT_Mtt_1000_Inf_jerdown   .SetName( options.hist + '__TTbar_Mtt_1000_Inf__jer__down')
hMeas_TT_Mtt_1000_Inf_jerup     .SetName( options.hist + '__TTbar_Mtt_1000_Inf__jer__up')
hMeas_TT_Mtt_1000_Inf_qcd       .SetName( options.hist + '__TTbar_Mtt_1000_Inf__qcd')
hMeas_TT_Mtt_1000_Inf_pdfdown   .SetName( options.hist + '__TTbar_Mtt_1000_Inf__pdf__down')
hMeas_TT_Mtt_1000_Inf_pdfup     .SetName( options.hist + '__TTbar_Mtt_1000_Inf__pdf__up')
hMeas_TT_Mtt_1000_Inf_scaledown .SetName( options.hist + '__TTbar_Mtt_1000_Inf__scale__down')
hMeas_TT_Mtt_1000_Inf_scaleup   .SetName( options.hist + '__TTbar_Mtt_1000_Inf__scale__up')



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
hMeas_TT_Mtt_less_700_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar_scaledown) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar_scaleup) * SF_b * SF_t)

hMeas_TT_Mtt_700_1000_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jecdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jecup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jerdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
#hMeas_TT_Mtt_700_1000_jernom  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jerup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_qcd    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_pdfdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_pdfup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000_scaledown) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000_scaleup) * SF_b * SF_t)

hMeas_TT_Mtt_1000_Inf_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jecdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jecup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jerdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
#hMeas_TT_Mtt_1000_Inf_jernom  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jerup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_qcd    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_pdfdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_pdfup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf_scaledown) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf_scaleup) * SF_b * SF_t )



qcdcanvs = []

######### Correct the QCD estimate with the known MC backgrounds in the noniso region. ########
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


hMeas_QCD_SingleMu.Scale( NQCD / hMeas_QCD_SingleMu.Integral() )


######### Combine ttbar samples #############
hMeas_TTbar_nom = hMeas_TT_Mtt_less_700_nom.Clone()
hMeas_TTbar_nom.SetName(options.hist + '__TTbar'  )
for hist in [hMeas_TT_Mtt_700_1000_nom, hMeas_TT_Mtt_1000_Inf_nom] :
    hMeas_TTbar_nom.Add( hist )

hMeas_TTbar_jecdown = hMeas_TT_Mtt_less_700_jecdown.Clone()
hMeas_TTbar_jecdown.SetName(options.hist + '__TTbar__jec__down'  )
for hist in [hMeas_TT_Mtt_700_1000_jecdown, hMeas_TT_Mtt_1000_Inf_jecdown] :
    hMeas_TTbar_jecdown.Add( hist )

hMeas_TTbar_jecup = hMeas_TT_Mtt_less_700_jecup.Clone()
hMeas_TTbar_jecup.SetName(options.hist + '__TTbar__jec__up'  )
for hist in [hMeas_TT_Mtt_700_1000_jecup, hMeas_TT_Mtt_1000_Inf_jecup] :
    hMeas_TTbar_jecup.Add( hist )

hMeas_TTbar_jerdown = hMeas_TT_Mtt_less_700_jerdown.Clone()
hMeas_TTbar_jerdown.SetName(options.hist + '__TTbar__jer__down'  )
for hist in [hMeas_TT_Mtt_700_1000_jerdown, hMeas_TT_Mtt_1000_Inf_jerdown] :
    hMeas_TTbar_jerdown.Add( hist )

hMeas_TTbar_jerup = hMeas_TT_Mtt_less_700_jerup.Clone()
hMeas_TTbar_jerup.SetName(options.hist + '__TTbar__jer__up'  )
for hist in [hMeas_TT_Mtt_700_1000_jerup, hMeas_TT_Mtt_1000_Inf_jerup] :
    hMeas_TTbar_jerup.Add( hist )

hMeas_TTbar_pdfdown = hMeas_TT_Mtt_less_700_pdfdown.Clone()
hMeas_TTbar_pdfdown.SetName(options.hist + '__TTbar__pdf__down'  )
for hist in [hMeas_TT_Mtt_700_1000_pdfdown, hMeas_TT_Mtt_1000_Inf_pdfdown] :
    hMeas_TTbar_pdfdown.Add( hist )

hMeas_TTbar_pdfup = hMeas_TT_Mtt_less_700_pdfup.Clone()
hMeas_TTbar_pdfup.SetName(options.hist + '__TTbar__pdf__up'  )
for hist in [hMeas_TT_Mtt_700_1000_pdfup, hMeas_TT_Mtt_1000_Inf_pdfup] :
    hMeas_TTbar_pdfup.Add( hist )

hMeas_TTbar_scaledown = hMeas_TT_Mtt_less_700_scaledown.Clone()    
hMeas_TTbar_scaledown.SetName(options.hist + '__TTbar__scale__down'  )
for hist in [hMeas_TT_Mtt_700_1000_scaledown, hMeas_TT_Mtt_1000_Inf_scaledown] :
    hMeas_TTbar_scaledown.Add( hist )

hMeas_TTbar_scaleup = hMeas_TT_Mtt_less_700_scaleup.Clone()    
hMeas_TTbar_scaleup.SetName(options.hist + '__TTbar__scale__up'  )
for hist in [hMeas_TT_Mtt_700_1000_scaleup, hMeas_TT_Mtt_1000_Inf_scaleup] :
    hMeas_TTbar_scaleup.Add( hist )



######### Combine Single Top samples #############
hMeas_SingleTop_nom = hMeas_T_t_nom.Clone()
hMeas_SingleTop_nom.SetName(options.hist + '__SingleTop'  )
for hist in [hMeas_Tbar_t_nom, hMeas_T_s_nom, hMeas_Tbar_s_nom, hMeas_T_tW_nom, hMeas_Tbar_tW_nom] :
    hMeas_SingleTop_nom.Add( hist )

hMeas_SingleTop_jecdown = hMeas_T_t_jecdown.Clone()
hMeas_SingleTop_jecdown.SetName(options.hist + '__SingleTop__jec__down'  )
for hist in [hMeas_Tbar_t_jecdown, hMeas_T_s_jecdown, hMeas_Tbar_s_jecdown, hMeas_T_tW_jecdown, hMeas_Tbar_tW_jecdown] :
    hMeas_SingleTop_jecdown.Add( hist )

hMeas_SingleTop_jecup = hMeas_T_t_jecup.Clone()
hMeas_SingleTop_jecup.SetName(options.hist + '__SingleTop__jec__up'  )
for hist in [hMeas_Tbar_t_jecup, hMeas_T_s_jecup, hMeas_Tbar_s_jecup, hMeas_T_tW_jecup, hMeas_Tbar_tW_jecup] :
    hMeas_SingleTop_jecup.Add( hist )

hMeas_SingleTop_jerdown = hMeas_T_t_jerdown.Clone()
hMeas_SingleTop_jerdown.SetName(options.hist + '__SingleTop__jer__down'  )
for hist in [hMeas_Tbar_t_jerdown, hMeas_T_s_jerdown, hMeas_Tbar_s_jerdown, hMeas_T_tW_jerdown, hMeas_Tbar_tW_jerdown] :
    hMeas_SingleTop_jerdown.Add( hist )

hMeas_SingleTop_jerup = hMeas_T_t_jerup.Clone()
hMeas_SingleTop_jerup.SetName(options.hist + '__SingleTop__jer__up'  )
for hist in [hMeas_Tbar_t_jerup, hMeas_T_s_jerup, hMeas_Tbar_s_jerup, hMeas_T_tW_jerup, hMeas_Tbar_tW_jerup] :
    hMeas_SingleTop_jerup.Add( hist )



hists = []


########## Make some easy-access lists ##########
plots = [ 'jec__down' , 'jec__up' , 'jer__down' , 'jer__up' , 'pdf__down' , 'pdf__up' , 'scale__down' , 'scale__up', 'nom']
hMeas_TTbar = [ hMeas_TTbar_jecdown   , hMeas_TTbar_jecup   , 
                hMeas_TTbar_jerdown   , hMeas_TTbar_jerup   , 
                hMeas_TTbar_pdfdown   , hMeas_TTbar_pdfup   , 
                hMeas_TTbar_scaledown , hMeas_TTbar_scaleup,
                hMeas_TTbar_nom ]

hMeas_SingleTop = [ hMeas_SingleTop_jecdown   , hMeas_SingleTop_jecup   , 
                    hMeas_SingleTop_jerdown   , hMeas_SingleTop_jerup   , 
                    hMeas_SingleTop_nom       , hMeas_SingleTop_nom   , 
                    hMeas_SingleTop_nom       , hMeas_SingleTop_nom,
                    hMeas_SingleTop_nom ]


hMeas_WJets = [ hMeas_WJets_jecdown   , hMeas_WJets_jecup   , 
                hMeas_WJets_jerdown   , hMeas_WJets_jerup   , 
                hMeas_WJets_nom       , hMeas_WJets_nom   , 
                hMeas_WJets_nom       , hMeas_WJets_nom,
                hMeas_WJets_nom ]
    
        
hMeas_QCD    = [ hMeas_QCD_SingleMu    , hMeas_QCD_SingleMu  ,
                 hMeas_QCD_SingleMu    , hMeas_QCD_SingleMu  ,
                 hMeas_QCD_SingleMu    , hMeas_QCD_SingleMu,
                 hMeas_QCD_SingleMu    , hMeas_QCD_SingleMu,
                 hMeas_QCD_SingleMu]

stacks = []


for thehist in hMeas_TTbar :
    thehist.SetFillColor( TColor.kRed )

for thehist in hMeas_WJets :
    thehist.SetFillColor( TColor.kGreen )

for thehist in hMeas_SingleTop :
    thehist.SetFillColor( TColor.kMagenta )

for thehist in hMeas_QCD :
    thehist.SetFillColor( TColor.kYellow )

legs = []

for m in range(0,len(hMeas_TTbar)):



    if 'vtxMass' in  options.hist :
        for zerohist in [hMeas_WJets[m], hMeas_SingleTop[m], hMeas_TTbar[m], hMeas_QCD[m] ] :
            zerohist.SetBinContent(1, 0.0)
        if options.ignoreData == False :
            hRecoData.SetBinContent(1, 0.0)


                
    leg = TLegend(0.5, 0.55, 0.84, 0.84)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)

    
    leg.AddEntry( hMeas_TTbar[m], 't#bar{t}', 'f')
    leg.AddEntry( hMeas_SingleTop[m], 'single top', 'f')
    leg.AddEntry( hMeas_WJets[m], 'W+jets', 'f')
    leg.AddEntry( hMeas_QCD[m], 'QCD' , 'f')

    

    
    # Make a stack plot of the MC to compare to data
    hMC_stack = THStack("hMC_stack_" + str(m),
                        hMeas_TTbar[m].GetTitle() + ';' +
                        hMeas_TTbar[m].GetXaxis().GetTitle() + ';' +
                        hMeas_TTbar[m].GetYaxis().GetTitle()
                        )
    print 'Making stack'
    hMC_stack.Add( hMeas_QCD[m] )
    hMC_stack.Add( hMeas_WJets[m] )
    hMC_stack.Add( hMeas_SingleTop[m] )
    hMC_stack.Add( hMeas_TTbar[m] )
    
   
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
        c.Print( 'normalized_' + plots[m] + options.outname + '_' + options.hist + '.png' )
        c.Print( 'normalized_' + plots[m] + options.outname + '_' + options.hist + '.pdf' )
    else : 
        c.Print( 'normalized_' + plots[m] + options.outname + '_' + options.hist + '_nodata.png' )
        c.Print( 'normalized_' + plots[m] + options.outname + '_' + options.hist + '_nodata.pdf' )


        
    # write the histogram in a rootfile

    histsAll = [hRecoData , hMeas_TTbar[m], hMeas_WJets[m], hMeas_SingleTop[m], hMeas_QCD[m] ]
    fout.cd()
    for ihist in xrange(len(histsAll)) :
        hist = histsAll[ihist]
        if hist is not None :
            hist.Write()

fout.Close()
