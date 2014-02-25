#!/usr/bin/env python
# ==============================================================================
# January 2014
# ==============================================================================

import time
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
SF_t = 0.94

# Cross sections (in fb) and the number of MC events
sigma_ttbar_NNLO = 245.8 * 1000. # fb, from http://arxiv.org/pdf/1303.6254.pdf
sigma_T_t_NNLO = 56.4 * 1000. * 3
sigma_Tbar_t_NNLO = 30.7 * 1000. * 3
sigma_T_s_NNLO = 3.79 * 1000. * 3
sigma_Tbar_s_NNLO = 1.76 * 1000. * 3
sigma_T_tW_NNLO = 11.1 * 1000. * 3
sigma_Tbar_tW_NNLO = 11.1 * 1000. * 3
sigma_WJets_NNLO = 36703.2 * 1000.

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
NQCD = 15.0

# ttbar filter efficiencies
e_TT_Mtt_700_1000 = 0.074
e_TT_Mtt_1000_Inf = 0.014
e_TT_Mtt_0_700 = 1.0 - e_TT_Mtt_700_1000 - e_TT_Mtt_1000_Inf
# 

names = [ 'DATA', 'TTbar', 'WJets', 'SingleTop', 'QCD' ]
plots = [ 'jec__down' , 'jec__up' , 'jer__down' , 'jer__up' , 'pdf__down' , 'pdf__up' , 'nom' , 'scale__down' , 'scale__up']
canvs = []
histsData = []

# Open the output file 

fout = TFile("normalized_" + options.outname + ".root" , "RECREATE")


# ==============================================================================
#  Example Unfolding
# ==============================================================================


if not options.ignoreData : 
    fdata = TFile("histfiles/SingleMu_iheartNY_V1_mu_nom_type1.root")

if not options.ignoreQCD :
    fQCD = TFile("histfiles/QCD_hists_pt_type1.root")


fT_t_nom     = TFile("histfiles/T_t-channel_Histos_type1.root")
fT_t_jecdown = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_t_jecup   = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_t_jerdown = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_t_jerup   = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")


fTbar_t_nom     = TFile("histfiles/Tbar_t-channel_Histos_type1.root")
fTbar_t_jecdown = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTbar_t_jecup   = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTbar_t_jerdown = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTbar_t_jerup   = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")


fT_s_nom     = TFile("histfiles/T_s-channel_Histos_type1.root")
fT_s_jecdown = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_s_jecup   = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_s_jerdown = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_s_jerup   = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")


fTbar_s_nom     = TFile("histfiles/Tbar_s-channel_Histos_type1.root")
fTbar_s_jecdown = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jecdn_type1.root")
fTbar_s_jecup   = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jecup_type1.root")
fTbar_s_jerdown = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jerdn_type1.root")
fTbar_s_jerup   = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_muu_jerup_type1.root")


fT_tW_nom     = TFile("histfiles/T_tW-channel_Histos_type1.root")
fT_tW_jecdown = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fT_tW_jecup   = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fT_tW_jerdown = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fT_tW_jerup   = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")


fTbar_tW_nom     = TFile("histfiles/Tbar_tW-channel_Histos_type1.root")
fTbar_tW_jecdown = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTbar_tW_jecup   = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTbar_tW_jerdown = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTbar_tW_jerup   = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")


fWJets_nom     = TFile("histfiles/WJetsToLNu_Histos_type1.root")
fWJets_jecdown = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jecdn_type1.root")
fWJets_jecup   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jecup_type1.root")
fWJets_jerdown = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jerdn_type1.root")
fWJets_jerup   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_jerup_type1.root")


fTT_Mtt_less_700_nom       = TFile("histfiles/TT_Mtt-max700-channel_Histos_type1.root")
fTT_Mtt_less_700_jecdown   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_less_700_jecup     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_less_700_jerdown   = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTT_Mtt_less_700_jerup     = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
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

if not options.ignoreQCD : 
    hRecoQCD = fQCD.Get("ptTopTagHist")
    hRecoQCD.Sumw2()
    hRecoQCD.Scale( NQCD / hRecoQCD.Integral() )
    hRecoQCD.SetFillColor(TColor.kYellow)
    hRecoQCD.Rebin(2)




# Get the histogram files
hMeas_T_t_nom     = fT_t_nom.Get(options.hist).Clone()
hMeas_T_t_jecdown = fT_t_jecdown.Get(options.hist).Clone()
hMeas_T_t_jecup   = fT_t_jecup.Get(options.hist).Clone()
hMeas_T_t_jerdown = fT_t_jerdown.Get(options.hist).Clone()
hMeas_T_t_jerup   = fT_t_jerup.Get(options.hist).Clone()


hMeas_Tbar_t_nom     = fTbar_t_nom.Get(options.hist).Clone()
hMeas_Tbar_t_jecdown = fTbar_t_jecdown.Get(options.hist).Clone()
hMeas_Tbar_t_jecup   = fTbar_t_jecup.Get(options.hist).Clone()
hMeas_Tbar_t_jerdown = fTbar_t_jerdown.Get(options.hist).Clone()
hMeas_Tbar_t_jerup   = fTbar_t_jerup.Get(options.hist).Clone()


hMeas_T_s_nom     = fT_s_nom.Get(options.hist).Clone()
hMeas_T_s_jecdown = fT_s_jecdown.Get(options.hist).Clone()
hMeas_T_s_jecup   = fT_s_jecup.Get(options.hist).Clone()
hMeas_T_s_jerdown = fT_s_jerdown.Get(options.hist).Clone()
hMeas_T_s_jerup   = fT_s_jerup.Get(options.hist).Clone()


hMeas_Tbar_s_nom     = fTbar_s_nom.Get(options.hist).Clone()
hMeas_Tbar_s_jecdown = fTbar_s_jecdown.Get(options.hist).Clone()
hMeas_Tbar_s_jecup   = fTbar_s_jecup.Get(options.hist).Clone()
hMeas_Tbar_s_jerdown = fTbar_s_jerdown.Get(options.hist).Clone()
hMeas_Tbar_s_jerup   = fTbar_s_jerup.Get(options.hist).Clone()


hMeas_T_tW_nom     = fT_tW_nom.Get(options.hist).Clone()
hMeas_T_tW_jecdown = fT_tW_jecdown.Get(options.hist).Clone()
hMeas_T_tW_jecup   = fT_tW_jecup.Get(options.hist).Clone()
hMeas_T_tW_jerdown = fT_tW_jerdown.Get(options.hist).Clone()
hMeas_T_tW_jerup   = fT_tW_jerup.Get(options.hist).Clone()


hMeas_Tbar_tW_nom     = fTbar_tW_nom.Get(options.hist).Clone()
hMeas_Tbar_tW_jecdown = fTbar_tW_jecdown.Get(options.hist).Clone()
hMeas_Tbar_tW_jecup   = fTbar_tW_jecup.Get(options.hist).Clone()
hMeas_Tbar_tW_jerdown = fTbar_tW_jerdown.Get(options.hist).Clone()
hMeas_Tbar_tW_jerup   = fTbar_tW_jerup.Get(options.hist).Clone()


hMeas_WJets_nom     = fWJets_nom.Get(options.hist).Clone()
hMeas_WJets_jecdown = fWJets_jecdown.Get(options.hist).Clone()
hMeas_WJets_jecup   = fWJets_jecup.Get(options.hist).Clone()
hMeas_WJets_jerdown = fWJets_jerdown.Get(options.hist).Clone()
hMeas_WJets_jerup   = fWJets_jerup.Get(options.hist).Clone()


hMeas_TT_Mtt_less_700_nom       = fTT_Mtt_less_700_nom.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jecdown   = fTT_Mtt_less_700_jecdown.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jecup     = fTT_Mtt_less_700_jecup.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jerdown   = fTT_Mtt_less_700_jerdown.Get(options.hist).Clone()
hMeas_TT_Mtt_less_700_jerup     = fTT_Mtt_less_700_jerup.Get(options.hist).Clone()
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
hMeas_TT_Mtt_1000_Inf_pdfdown   = fTT_Mtt_1000_Inf_pdfdown.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_pdfup     = fTT_Mtt_1000_Inf_pdfup.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_scaledown = fTT_Mtt_1000_Inf_scaledown.Get(options.hist).Clone()
hMeas_TT_Mtt_1000_Inf_scaleup   = fTT_Mtt_1000_Inf_scaleup.Get(options.hist).Clone()





hMeas_T_t_nom     .SetName( 'hMeas_T_t')
hMeas_T_t_jecdown .SetName( 'hMeas_T_t_jecdown' )
hMeas_T_t_jecup   .SetName( 'hMeas_T_t_jecup' )
hMeas_T_t_jerdown .SetName( 'hMeas_T_t_jerdown' )
hMeas_T_t_jerup   .SetName( 'hMeas_T_t_jerup' )

hMeas_Tbar_t_nom     .SetName( 'hMeas_Tbar_t')
hMeas_Tbar_t_jecdown .SetName( 'hMeas_Tbar_t_jecdown' )
hMeas_Tbar_t_jecup   .SetName( 'hMeas_Tbar_t_jecup' )
hMeas_Tbar_t_jerdown .SetName( 'hMeas_Tbar_t_jerdown' )
hMeas_Tbar_t_jerup   .SetName( 'hMeas_Tbar_t_jerup' )

hMeas_T_s_nom     .SetName( 'hMeas_T_s')
hMeas_T_s_jecdown .SetName( 'hMeas_T_s_jecdown' )
hMeas_T_s_jecup   .SetName( 'hMeas_T_s_jecup' )
hMeas_T_s_jerdown .SetName( 'hMeas_T_s_jerdown' )
hMeas_T_s_jerup   .SetName( 'hMeas_T_s_jerup' )

hMeas_Tbar_s_nom     .SetName( 'hMeas_Tbar_s')
hMeas_Tbar_s_jecdown .SetName( 'hMeas_Tbar_s_jecdown' )
hMeas_Tbar_s_jecup   .SetName( 'hMeas_Tbar_s_jecup' )
hMeas_Tbar_s_jerdown .SetName( 'hMeas_Tbar_s_jerdown' )
hMeas_Tbar_s_jerup   .SetName( 'hMeas_Tbar_s_jerup' )

hMeas_T_tW_nom     .SetName( 'hMeas_T_tW')
hMeas_T_tW_jecdown .SetName( 'hMeas_T_tW_jecdow' )
hMeas_T_tW_jecup   .SetName( 'hMeas_T_tW_jecup' )
hMeas_T_tW_jerdown .SetName( 'hMeas_T_tW_jerdown' )
hMeas_T_tW_jerup   .SetName( 'hMeas_T_tW_jerup' )

hMeas_Tbar_tW_nom     .SetName( 'hMeas_Tbar_tW')
hMeas_Tbar_tW_jecdown .SetName( 'hMeas_Tbar_tW_jecdown' )
hMeas_Tbar_tW_jecup   .SetName( 'hMeas_Tbar_tW_jecup' )
hMeas_Tbar_tW_jerdown .SetName( 'hMeas_Tbar_tW_jerdown' )
hMeas_Tbar_tW_jerup   .SetName( 'hMeas_Tbar_tW_jerup ' )

hMeas_WJets_nom     .SetName( 'hMeas_WJets')
hMeas_WJets_jecdown .SetName( 'hMeas_WJets_jecdown' )
hMeas_WJets_jecup   .SetName( 'hMeas_WJets_jecup' )
hMeas_WJets_jerdown .SetName( 'hMeas_WJets_jerdown' )
hMeas_WJets_jerup   .SetName( 'hMeas_WJets_jerup' )

hMeas_TT_Mtt_less_700_nom       .SetName( 'hMeas_TT_Mtt_less_70' )
hMeas_TT_Mtt_less_700_jecdown   .SetName( 'hMeas_TT_Mtt_less_700_jecdown')
hMeas_TT_Mtt_less_700_jecup     .SetName( 'hMeas_TT_Mtt_less_700_jecup')
hMeas_TT_Mtt_less_700_jerdown   .SetName( 'hMeas_TT_Mtt_less_700_jerdown')
hMeas_TT_Mtt_less_700_jerup     .SetName( 'hMeas_TT_Mtt_less_700_jerup')
hMeas_TT_Mtt_less_700_pdfdown   .SetName( 'hMeas_TT_Mtt_less_700_pdfdown')
hMeas_TT_Mtt_less_700_pdfup     .SetName( 'hMeas_TT_Mtt_less_700_pdfup')
hMeas_TT_Mtt_less_700_scaledown .SetName( 'hMeas_TT_Mtt_less_700_scaledown')
hMeas_TT_Mtt_less_700_scaleup   .SetName( 'hMeas_TT_Mtt_less_700_scaleup')

hMeas_TT_Mtt_700_1000_nom       .SetName( 'hMeas_TT_Mtt_700_100' )
hMeas_TT_Mtt_700_1000_jecdown   .SetName( 'hMeas_TT_Mtt_700_1000_jecdown')
hMeas_TT_Mtt_700_1000_jecup     .SetName( 'hMeas_TT_Mtt_700_1000_jecup')
hMeas_TT_Mtt_700_1000_jerdown   .SetName( 'hMeas_TT_Mtt_700_1000_jerdown')
hMeas_TT_Mtt_700_1000_jerup     .SetName( 'hMeas_TT_Mtt_700_1000_jerup')
hMeas_TT_Mtt_700_1000_pdfdown   .SetName( 'hMeas_TT_Mtt_700_1000_pdfdown')
hMeas_TT_Mtt_700_1000_pdfup     .SetName( 'hMeas_TT_Mtt_700_1000_pdfup')
hMeas_TT_Mtt_700_1000_scaledown .SetName( 'hMeas_TT_Mtt_700_1000_scaledown')
hMeas_TT_Mtt_700_1000_scaleup   .SetName( 'hMeas_TT_Mtt_700_1000_scaleup')

hMeas_TT_Mtt_1000_Inf_nom       .SetName( 'hMeas_TT_Mtt_1000 ' )
hMeas_TT_Mtt_1000_Inf_jecdown   .SetName( 'hMeas_TT_Mtt_1000_Inf_jecdown')
hMeas_TT_Mtt_1000_Inf_jecup     .SetName( 'hMeas_TT_Mtt_1000_Inf_jecup')
hMeas_TT_Mtt_1000_Inf_jerdown   .SetName( 'hMeas_TT_Mtt_1000_Inf_jerdown')
hMeas_TT_Mtt_1000_Inf_jerup     .SetName( 'hMeas_TT_Mtt_1000_Inf_jerup')
hMeas_TT_Mtt_1000_Inf_pdfdown   .SetName( 'hMeas_TT_Mtt_1000_Inf_pdfdown')
hMeas_TT_Mtt_1000_Inf_pdfup     .SetName( 'hMeas_TT_Mtt_1000_Inf_pdfup')
hMeas_TT_Mtt_1000_Inf_scaledown .SetName( 'hMeas_TT_Mtt_1000_Inf_scaledown')
hMeas_TT_Mtt_1000_Inf_scaleup   .SetName( 'hMeas_TT_Mtt_1000_Inf_scaleup')




# Scale to desired normalization
# Options are :
#  1. From MC
#  2. From fit
#
# For now, we don't have the fit, so we do from MC



hMeas_T_t_nom    .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_jecdown.Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_jecup  .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_jerdown.Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_T_t_jerup  .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )

hMeas_Tbar_t_nom    .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_jecdown.Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_jecup  .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_jerdown.Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_Tbar_t_jerup  .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )

hMeas_T_s_nom    .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_jecdown.Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_jecup  .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_jerdown.Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_T_s_jerup  .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )

hMeas_Tbar_s_nom    .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_jecdown.Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_jecup  .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_jerdown.Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_Tbar_s_jerup  .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )

hMeas_T_tW_nom    .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_jecdown.Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_jecup  .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_jerdown.Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_T_tW_jerup  .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )

hMeas_Tbar_tW_nom    .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_jecdown.Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_jecup  .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_jerdown.Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_Tbar_tW_jerup  .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )

hMeas_WJets_nom    .Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_jecdown.Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_jecup  .Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_jerdown.Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_WJets_jerup  .Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )

hMeas_TT_Mtt_less_700_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jecdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jecup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jerdown  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jerup    .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
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

hMeas_WJets   = [ hMeas_WJets_jecdown   , hMeas_WJets_jecup   , hMeas_WJets_jerdown   , hMeas_WJets_jerup   ,hMeas_WJets_nom    , hMeas_WJets_nom   , hMeas_WJets_nom   , hMeas_WJets_nom   , hMeas_WJets_nom]

hMeas_TT_Mtt = []
hMeas_SingleTop = []


legs = []
#m = input(" Choose the distribution: 0) TT_Mtt_jecdown  1) TT_Mtt_jecup  2) TT_Mtt_jerdown  3) TT_Mtt_jerup  4) TT_Mtt_pdfdown  5) TT_Mtt_pdfup : #")
for m in range(0,len(plots)):

    leg = TLegend(0.5, 0.55, 0.84, 0.84)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)

    hMeas_TT_Mtt.append(hMeas_TT_Mtt_less_700[m].Clone())
    hMeas_TT_Mtt[m].SetFillColor( TColor.kRed )
    for hist in [ hMeas_TT_Mtt_700_1000[m] , hMeas_TT_Mtt_1000_Inf[m] ] :
            print 'Adding mtt for' + plots[m]
            hMeas_TT_Mtt[m].Add( hist )


    hists.append( hMeas_TT_Mtt[m] )
    hMeas_SingleTop.append( hMeas_T_t[m].Clone())

    hists.append( hMeas_SingleTop[m] )

    hMeas_SingleTop[m].SetFillColor( TColor.kMagenta )
    hMeas_WJets[m].SetFillColor( TColor.kGreen )
    #hMeas.SetFillColor( TColor.kRed )
    #hRecoMC.SetFillColor( 2 )



    

    for hist in [hMeas_Tbar_t[m], hMeas_T_s[m], hMeas_Tbar_s[m], hMeas_T_tW[m], hMeas_Tbar_tW[m]] :
        print 'adding hist ' + hist.GetName()
        hMeas_SingleTop[m].Add( hist )


    leg.AddEntry( hMeas_TT_Mtt[m], 't#bar{t}', 'f')
    leg.AddEntry( hMeas_SingleTop[m], 'single top', 'f')
    leg.AddEntry( hMeas_WJets[m], 'W+jets', 'f')

    
    if 'vtxMass' in  options.hist :
        for zerohist in [hMeas_WJets[m], hMeas_SingleTop[m], hMeas_TT_Mtt[m] ] :
            zerohist.SetBinContent(1, 0.0)
        if options.ignoreData == False :
            hRecoData.SetBinContent(1, 0.0)
    
    # Make a stack plot of the MC to compare to data
    hMC_stack = THStack("hMC_stack",
                        hMeas_TT_Mtt[m].GetTitle() + ';' +
                        hMeas_TT_Mtt[m].GetXaxis().GetTitle() + ';' +
                        hMeas_TT_Mtt[m].GetYaxis().GetTitle()
                        )
    print 'Making stack'
    hMC_stack.Add( hMeas_WJets[m] )
    hMC_stack.Add( hMeas_SingleTop[m] )
    hMC_stack.Add( hMeas_TT_Mtt[m] )
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
        c.Print( 'normalized_' + plots[m] + options.outname + '.png' )
        c.Print( 'normalized_' + plots[m] + options.outname + '.pdf' )
    else : 
        c.Print( 'normalized_' + plots[m] + options.outname + '_nodata.png' )
        c.Print( 'normalized_' + plots[m] + options.outname + '_nodata.pdf' )


        
    # write the histogram in a rootfile

    histsAll = [hRecoData , hMeas_TT_Mtt[m], hMeas_WJets[m], hMeas_SingleTop[m], hRecoQCD]
    fout.cd()
    for ihist in xrange(len(histsAll)) :
        hist = histsAll[ihist]
        if hist is not None :
            if plots[m] == 'nom'  : 
                hist.SetName(options.hist + '__' + names[ihist]  )
                hist.Write()
            elif ihist != 0 :
                hist.SetName(options.hist + '__' + names[ihist] + '__' + plots [m] )
                hist.Write()

fout.Close()
   
    
