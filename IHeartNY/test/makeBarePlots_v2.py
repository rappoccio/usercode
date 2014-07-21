#!/usr/bin/env python

import time
from optparse import OptionParser
parser = OptionParser()


parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='mujets',
                  dest='outname',
                  help='Output name for png and pdf files')


parser.add_option('--hist1', metavar='F', type='string', action='store',
                  default='ptRecoTop',
                  dest='hist1',
                  help='Histogram2 is subtracted from histogram1')

parser.add_option('--hist2', metavar='F', type='string', action='store',
                  default= None ,
                  dest= None ,
                  help='Histogram2 to be subtracted form Histogram1')
                                    

parser.add_option('--NQCD', metavar='F', type='float', action='store',
                  default=0.0 ,
                  dest='NQCD',
                  help='QCD Normalization')
                  
parser.add_option('--ignoreData', metavar='F', action='store_true',
                  default=False,
                  dest='ignoreData',
                  help='Ignore plotting data')

parser.add_option('--drawLegend', metavar='F', action='store_true',
                  default=True,
                  dest='drawLegend',
                  help='Draw a legend')

parser.add_option('--rebin', metavar='R', type='int', action='store',
                  default=None,
                  dest='rebin',
                  help='Rebin histogram?')

parser.add_option('--newYlabel', metavar='F', type='string', action='store',
                  default= None ,
                  dest= None ,
                  help='Fixed y-label is needed if rebinning the histogram')

parser.add_option('--RunAllSyst', metavar='F', action='store_true',
                  default=False,
                  dest='RunAllSyst',
                  help='Run all systematics variations to get the root file for theta')

# Choose which systematic to run for: "nom" , "jecdn" , "jecup" , "jerdn" , "jerup" , "toptagdn" , "toptagup" , "btagdn" , "btagup" , "pdfdn" , "pdfup" , "scaledown_nom" , "scaleup_nom"
parser.add_option('--systVariation', metavar='F', type='string', action='store',
                  default='nom',
                  dest='systVariation',
                  help='Run nominal or systematic variation')


(options, args) = parser.parse_args()

argv = []

from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor

gROOT.Macro("rootlogon.C")

gStyle.SetOptTitle(0);
gStyle.SetOptStat(0);
gStyle.SetOptFit(0);

gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
#gStyle.SetTitleFontSize(0.05)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(2.0, "X")
gStyle.SetTitleOffset(1.25, "Y")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(20, "XYZ")


# Performance numbers
lum = 19.7 # fb-1
SF_t = 1.0
#SF_t = 0.94

# Cross sections (in fb) and the number of MC events
sigma_ttbar_NNLO           = [    # fb, from http://arxiv.org/pdf/1303.6254.pdf
    245.8 * 1000., # nom
    237.4 * 1000., # scaledown
    252.0 * 1000., # scaleup
    239.4 * 1000., # pdfdown
    252.0 * 1000., # pdfup
    ]
sigma_T_t_NNLO = 56.4 * 1000.       # 
sigma_Tbar_t_NNLO = 30.7 * 1000.    # All single-top approx NNLO cross sections from
sigma_T_s_NNLO = 3.79 * 1000.       # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
sigma_Tbar_s_NNLO = 1.76 * 1000.    # 
sigma_T_tW_NNLO = 11.1 * 1000.      # 
sigma_Tbar_tW_NNLO = 11.1 * 1000.   # 
#sigma_WJets_NNLO = 36703.2 * 1000.  # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
sigma_WJets_NNLO  = [
	5400. * 1.207 * 1000.,       # W+1 jets
	1750. * 1.207 * 1000.,       # W+2 jets
	519. * 1.207 * 1000. ,       # W+3 jets
	214. * 1.207 * 1000.         # W+4 jets
	]

# MC event counts from B2G twiki here :
# https://twiki.cern.ch/twiki/bin/view/CMS/B2GTopLikeBSM53X#Backgrounds
Nmc_WJets = [
	23141598 ,       # W+1 jets
	34044921 ,       # W+2 jets
	15539503 ,       # W+3 jets
	13382803         # W+4 jets
	]
	
Nmc_ttbar = 21675970
Nmc_T_t = 3758227
Nmc_Tbar_t = 1935072
Nmc_T_s = 259961
Nmc_Tbar_s = 139974
Nmc_T_tW = 497658
Nmc_Tbar_tW = 493460
#Nmc_WJets = 57709905
Nmc_TT_Mtt_700_1000 = 3082812
Nmc_TT_Mtt_1000_Inf = 1249111

Nmc_ttbar_scaledown = 14998606
Nmc_ttbar_scaleup   = 14998720
Nmc_TT_Mtt_700_1000_scaledown = 2170074
Nmc_TT_Mtt_700_1000_scaleup = 2243672
Nmc_TT_Mtt_1000_Inf_scaledown = 1308090
Nmc_TT_Mtt_1000_Inf_scaleup = 1241650

# QCD Normalization from MET fits
NQCD = options.NQCD


#
# NEW ttbar filter efficiencies
# These were determined "by eye" to make the generated mttbar spectrum smooth in the "makeMttGenPlots.py" script
#                    nom      scaledown scaleup
e_TT_Mtt_700_1000 = [0.074,   0.081,    0.074]
e_TT_Mtt_1000_Inf = [0.015,   0.016,    0.014]
e_TT_Mtt_0_700 =    [1.0  ,   1.0,      1.0  ] #   No efficiency here, we applied the cut at gen level

# ttbar filter efficiencies
#                    nom      scaledown scaleup
#e_TT_Mtt_700_1000 = [0.074,   0.078,    0.069]
#e_TT_Mtt_1000_Inf = [0.014,   0.016,    0.013]
#e_TT_Mtt_0_700 =    [1.0  ,   1.0,      1.0  ] #   No efficiency here, we applied the cut at gen level


canvs = []

fT_t = []
fTbar_t = []
fT_s = []
fTbar_s = []
fT_tW = []
fTbar_tW = []
fW1Jets = []
fW2Jets = []
fW3Jets = []
fW4Jets = []
fTT_Mtt_less_700 = []
fTT_Mtt_700_1000 = []
fTT_Mtt_1000_Inf = []
fTT_nonSemiLep_Mtt_less_700 = []
fTT_nonSemiLep_Mtt_700_1000 = []
fTT_nonSemiLep_Mtt_1000_Inf = []

hMeas_TT_Mtt_less_700 = []
hMeas_TT_Mtt_700_1000 = []
hMeas_TT_Mtt_1000_Inf = []
hMeas_TT_nonSemiLep_Mtt_less_700 = []
hMeas_TT_nonSemiLep_Mtt_700_1000 = []
hMeas_TT_nonSemiLep_Mtt_1000_Inf = []
hMeas_T_t = []
hMeas_Tbar_t = []
hMeas_T_s = []
hMeas_Tbar_s = []
hMeas_T_tW = []
hMeas_Tbar_tW = []
hMeas_W1Jets = []
hMeas_W2Jets = []
hMeas_W3Jets = []
hMeas_W4Jets = []

fT_t_1 = []
fTbar_t_1 = []
fT_s_1 = []
fTbar_s_1 = []
fT_tW_1 = []
fTbar_tW_1 = []
fW1Jets_1 = []
fW2Jets_1 = []
fW3Jets_1 = []
fW4Jets_1 = []
fTT_Mtt_less_700_1 = []
fTT_Mtt_700_1000_1 = []
fTT_Mtt_1000_Inf_1 = []
fTT_nonSemiLep_Mtt_less_700_1 = []
fTT_nonSemiLep_Mtt_700_1000_1 = []
fTT_nonSemiLep_Mtt_1000_Inf_1 = []

hMeas_TT_Mtt_less_700_1 = []
hMeas_TT_Mtt_700_1000_1 = []
hMeas_TT_Mtt_1000_Inf_1 = []
hMeas_TT_nonSemiLep_Mtt_less_700_1 = []
hMeas_TT_nonSemiLep_Mtt_700_1000_1 = []
hMeas_TT_nonSemiLep_Mtt_1000_Inf_1 = []
hMeas_T_t_1 = []
hMeas_Tbar_t_1 = []
hMeas_T_s_1 = []
hMeas_Tbar_s_1 = []
hMeas_T_tW_1 = []
hMeas_Tbar_tW_1 = []
hMeas_W1Jets_1 = []
hMeas_W2Jets_1 = []
hMeas_W3Jets_1 = []
hMeas_W4Jets_1 = []

fT_t_2 = []
fTbar_t_2 = []
fT_s_2 = []
fTbar_s_2 = []
fT_tW_2 = []
fTbar_tW_2 = []
fW1Jets_2 = []
fW2Jets_2 = []
fW3Jets_2 = []
fW4Jets_2 = []
fTT_Mtt_less_700_2 = []
fTT_Mtt_700_1000_2 = []
fTT_Mtt_1000_Inf_2 = []
fTT_nonSemiLep_Mtt_less_700_2 = []
fTT_nonSemiLep_Mtt_700_1000_2 = []
fTT_nonSemiLep_Mtt_1000_Inf_2 = []

hMeas_TT_Mtt_less_700_2 = []
hMeas_TT_Mtt_700_1000_2 = []
hMeas_TT_Mtt_1000_Inf_2 = []
hMeas_TT_nonSemiLep_Mtt_less_700_2 = []
hMeas_TT_nonSemiLep_Mtt_700_1000_2 = []
hMeas_TT_nonSemiLep_Mtt_1000_Inf_2 = []
hMeas_T_t_2 = []
hMeas_Tbar_t_2 = []
hMeas_T_s_2 = []
hMeas_Tbar_s_2 = []
hMeas_T_tW_2 = []
hMeas_Tbar_tW_2 = []
hMeas_W1Jets_2 = []
hMeas_W2Jets_2 = []
hMeas_W3Jets_2 = []
hMeas_W4Jets_2 = []

hMeas_SingleTop = []
hMeas_TTbar_nonSemiLep = []
hMeas_TTbar = []
hMeas_QCD = []
hMeas_WJets = []

# Open the output file 
if options.RunAllSyst :
	if options.hist2 is None:
		fout = TFile("normalized_" + options.outname + '_' + options.hist1  + ".root" , "RECREATE")
	elif options.hist2 is not None:
		fout = TFile("normalized_" + options.outname + '_' + options.hist2 + '_subtracted_from_' + options.hist1 + ".root" , "RECREATE")

if not options.RunAllSyst :
	if options.hist2 is None:
		fout = TFile("normalized_" + options.outname + '_' + options.systVariation + '_' + options.hist1  + ".root" , "RECREATE")
	elif options.hist2 is not None:
		fout = TFile("normalized_" + options.outname + '_' + options.systVariation + '_' + options.hist2 + '_subtracted_from_' + options.hist1 + ".root" , "RECREATE")


# ==============================================================================
#  Example Unfolding
# ==============================================================================

## Input files:

if not options.ignoreData : 
    fdata = TFile("histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root") 

fQCD_SingleMu = TFile("histfiles/SingleMu_iheartNY_V1_mu_Run2012_qcd.root")


if options.RunAllSyst :
	ST_Wjets_histFiles = [ "qcd" , "nom" , "jecdn" , "jecup" , "jerdn" , "jerup" , "toptagdn" , "toptagup" , "btagdn" , "btagup" , "nom" ,"nom" ,"nom" ,"nom"]
	for ihist in xrange(len(ST_Wjets_histFiles)) :
		file = ST_Wjets_histFiles[ihist]
		# single top
		fT_t    .append(TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"       + file +".root"))
		fTbar_t .append(TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"    + file +".root"))
		fT_s    .append(TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"       + file +".root"))
		fTbar_s .append(TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"    + file +".root"))
		fT_tW   .append(TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"   + file +".root"))
		fTbar_tW.append(TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
		# W+jets
		fW1Jets.append(TFile("histfiles/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
		fW2Jets.append(TFile("histfiles/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
		fW3Jets.append(TFile("histfiles/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
		fW4Jets.append(TFile("histfiles/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
		
	TTjets_nonSemilepTT_histFiles = [ "qcd" , "nom" , "jecdn" , "jecup" , "jerdn" , "jerup" , "toptagdn" , "toptagup" , "btagdn" , "btagup" , "pdfdn" , "pdfup" , "scaledown_nom" , "scaleup_nom" ]
	for ihist in xrange(len(TTjets_nonSemilepTT_histFiles)) : 
		file = TTjets_nonSemilepTT_histFiles[ihist]
		# ttbar
		fTT_Mtt_less_700.append(TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
		fTT_Mtt_700_1000.append(TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
		fTT_Mtt_1000_Inf.append(TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
		# non-semileptonic ttbar 
		fTT_nonSemiLep_Mtt_less_700.append(TFile("histfiles/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
		fTT_nonSemiLep_Mtt_700_1000.append(TFile("histfiles/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
		fTT_nonSemiLep_Mtt_1000_Inf.append(TFile("histfiles/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))

	
if not options.RunAllSyst :
	if "pdfdn" in options.systVariation or "pdfup" in options.systVariation or "scaledown_nom" in options.systVariation or "scaleup_nom" in options.systVariation :			
		ST_Wjets_histFiles = [ "qcd" , "nom" ]
		for ihist in xrange(len(ST_Wjets_histFiles)):
			file = ST_Wjets_histFiles[ihist]
			# single top
			fT_t    .append(TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTbar_t .append(TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fT_s    .append(TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTbar_s .append(TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fT_tW   .append(TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTbar_tW.append(TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			# W+jets
			fW1Jets.append(TFile("histfiles/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
			fW2Jets.append(TFile("histfiles/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
			fW3Jets.append(TFile("histfiles/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
			fW4Jets.append(TFile("histfiles/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
		TTjets_nonSemilepTT_histFiles = [ options.systVariation , "qcd" ]
		for ihist in xrange(len(TTjets_nonSemilepTT_histFiles)):
			file = TTjets_nonSemilepTT_histFiles[ihist]	
			# ttbar
			fTT_Mtt_less_700.append(TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTT_Mtt_700_1000.append(TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTT_Mtt_1000_Inf.append(TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			# non-semileptonic ttbar 
			fTT_nonSemiLep_Mtt_less_700.append(TFile("histfiles/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTT_nonSemiLep_Mtt_700_1000.append(TFile("histfiles/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTT_nonSemiLep_Mtt_1000_Inf.append(TFile("histfiles/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))

	else:
		Files = [ "qcd" , options.systVariation ]
		for ihist in xrange(0 , len(Files)):
			file = Files[ihist]
			# single top
			fT_t    .append(TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"       + file +".root"))
			fTbar_t .append(TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"    + file +".root"))
			fT_s    .append(TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"       + file +".root"))
			fTbar_s .append(TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"    + file +".root"))
			fT_tW   .append(TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"   + file +".root"))
			fTbar_tW.append(TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			# W+jets
			fW1Jets.append(TFile("histfiles/W1JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
			fW2Jets.append(TFile("histfiles/W2JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
			fW3Jets.append(TFile("histfiles/W3JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
			fW4Jets.append(TFile("histfiles/W4JetsToLNu_TuneZ2Star_8TeV-madgraph_iheartNY_V1_mu_"+ file +".root"))
			# ttbar
			fTT_Mtt_less_700.append(TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTT_Mtt_700_1000.append(TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTT_Mtt_1000_Inf.append(TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			# non-semileptonic ttbar 
			fTT_nonSemiLep_Mtt_less_700.append(TFile("histfiles/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTT_nonSemiLep_Mtt_700_1000.append(TFile("histfiles/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))
			fTT_nonSemiLep_Mtt_1000_Inf.append(TFile("histfiles/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+ file +".root"))

if "nom" in options.systVariation :
	label = ""
if "jecdn" in options.systVariation :
	label = "__jec__down"
if "jecup" in options.systVariation :
	label = "__jec__up"
if "jerdn" in options.systVariation :
	label = "__jer__down"
if "jerup" in options.systVariation :
	label = "__jer__up"
if "toptagdn" in options.systVariation :
	label = "__toptag__down"
if "toptagup" in options.systVariation :
	label = "__toptag__up"
if "btagdn" in options.systVariation :
	label = "__btag__down"
if "btagup" in options.systVariation :
	label = "__btag__up"
if "pdfdn" in options.systVariation :
	label = "__pdf__down"
if "pdfup" in options.systVariation :
	label = "__pdf__up" 
if "scaledown" in options.systVariation :
	label = "__scale__down"
if "scaleup" in options.systVariation :
	label = "__scale__up"


print "==================================== Get Hists ====================================="



#hRecoMC.SetName("hRecoMC")
hRecoData = None
hMeas = None
hRecoQCD = None

if options.hist2 is None:
    	histname = options.hist1
elif options.hist2 is not None:
    	histname = options.hist2 + '_subtracted_from_' + options.hist1
    	
if not options.ignoreData : 
    hRecoData= fdata.Get(options.hist1).Clone()
    hRecoData.SetName(options.hist1 + "__DATA"  )

# Getting histogram files and scaling only to plot one histogram

if options.hist2 is None:

	hMeas_QCD_SingleMu = fQCD_SingleMu.Get(options.hist1).Clone()
	hMeas_QCD_SingleMu.SetName(options.hist1 + "__QCD")
		
	if options.RunAllSyst :
		ST_Wjets_Names = [ "__qcd" , "" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "" ,"" ,"" ,""]
		for ihist in xrange(len(ST_Wjets_Names)) :
			name = ST_Wjets_Names[ihist]
			##Single Top
			hMeas_T_t       .append(fT_t[ihist].Get(options.hist1).Clone())
			hMeas_T_t[ihist].SetName( options.hist1 + '__T_t' + name )
			hMeas_Tbar_t       .append(fTbar_t[ihist].Get(options.hist1).Clone())
			hMeas_Tbar_t[ihist].SetName( options.hist1 + '__Tbar_t' + name )
			hMeas_T_s       .append(fT_s[ihist].Get(options.hist1).Clone())
			hMeas_T_s[ihist].SetName( options.hist1 + '__T_s' + name )
			hMeas_Tbar_s       .append(fTbar_s[ihist].Get(options.hist1).Clone())
			hMeas_Tbar_s[ihist].SetName( options.hist1 + '__Tbar_s' + name )
			hMeas_T_tW       .append(fT_tW[ihist].Get(options.hist1).Clone())
			hMeas_T_tW[ihist].SetName( options.hist1 + '__T_tW' + name )
			hMeas_Tbar_tW       .append(fTbar_tW[ihist].Get(options.hist1).Clone())
			hMeas_Tbar_tW[ihist].SetName( options.hist1 + '__Tbar_tW' + name )
			#Wjets
			hMeas_W1Jets       .append(fW1Jets[ihist].Get(options.hist1).Clone())
			hMeas_W1Jets[ihist].SetName( options.hist1 + '__W1Jets' + name )
			hMeas_W2Jets       .append(fW2Jets[ihist].Get(options.hist1).Clone())
			hMeas_W2Jets[ihist].SetName( options.hist1 + '__W2Jets' + name )
			hMeas_W3Jets       .append(fW3Jets[ihist].Get(options.hist1).Clone())
			hMeas_W3Jets[ihist].SetName( options.hist1 + '__W3Jets' + name )
			hMeas_W4Jets       .append(fW4Jets[ihist].Get(options.hist1).Clone())
			hMeas_W4Jets[ihist].SetName( options.hist1 + '__W4Jets' + name )
			
			#print "number of Single top" , name , hMeas_T_t[ihist].GetSum() + hMeas_Tbar_t[ihist].GetSum() + hMeas_T_s[ihist].GetSum() + hMeas_Tbar_s[ihist].GetSum() + hMeas_T_tW[ihist].GetSum() + hMeas_Tbar_tW[ihist].GetSum()
			#print "number of WJets" , name , hMeas_W1Jets[ihist].GetSum() + hMeas_W2Jets[ihist].GetSum() + hMeas_W3Jets[ihist].GetSum() + hMeas_W4Jets[ihist].GetSum() 
			#print ""
			
		TTjets_nonSemilepTT_Names = [ "__qcd" , "" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "__pdf__down" , "__pdf__up" , "__scale__down" , "__scale__up" ]
		for ihist in xrange(len(TTjets_nonSemilepTT_Names)) : 
			name = TTjets_nonSemilepTT_Names[ihist]
			hMeas_TT_Mtt_less_700       .append(fTT_Mtt_less_700[ihist].Get(options.hist1).Clone())
			hMeas_TT_Mtt_less_700[ihist].SetName( options.hist1 + '__TTbar_Mtt_less_700' + name )
			hMeas_TT_Mtt_700_1000       .append(fTT_Mtt_700_1000[ihist].Get(options.hist1).Clone())
			hMeas_TT_Mtt_700_1000[ihist].SetName( options.hist1 + '__TTbar_Mtt_700_1000' + name )
			hMeas_TT_Mtt_1000_Inf       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
			hMeas_TT_Mtt_1000_Inf[ihist].SetName( options.hist1 + '__TTbar_Mtt_1000_Inf' + name ) 
	
			hMeas_TT_nonSemiLep_Mtt_less_700       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist1).Clone())
			hMeas_TT_nonSemiLep_Mtt_less_700[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_less_700' + name )
			hMeas_TT_nonSemiLep_Mtt_700_1000       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist1).Clone())
			hMeas_TT_nonSemiLep_Mtt_700_1000[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_700_1000' + name ) 
			hMeas_TT_nonSemiLep_Mtt_1000_Inf       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
			hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name )
			
			#print "number of TTbar " , name , hMeas_TT_Mtt_less_700[ihist].GetSum() + hMeas_TT_Mtt_700_1000[ihist].GetSum() + hMeas_TT_Mtt_1000_Inf[ihist].GetSum()
			#print "number of non semilep TTbar " , name , hMeas_TT_nonSemiLep_Mtt_less_700[ihist].GetSum() + hMeas_TT_nonSemiLep_Mtt_700_1000[ihist].GetSum() + hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist].GetSum()
			#print ""
			
	if not options.RunAllSyst :
		if "pdfdn" in options.systVariation or "pdfup" in options.systVariation or "scaledown_nom" in options.systVariation or "scaleup_nom" in options.systVariation :			
			ST_Wjets_Names = [ "__qcd" , "" ]
			for ihist in xrange(len(ST_Wjets_Names)):
				name = ST_Wjets_Names[ihist]
				##Single Top
				hMeas_T_t       .append(fT_t[ihist].Get(options.hist1).Clone())
				hMeas_T_t[ihist].SetName( options.hist1 + '__T_t' + name )
				hMeas_Tbar_t       .append(fTbar_t[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_t[ihist].SetName( options.hist1 + '__Tbar_t' + name )
				hMeas_T_s       .append(fT_s[ihist].Get(options.hist1).Clone())
				hMeas_T_s[ihist].SetName( options.hist1 + '__T_s' + name )
				hMeas_Tbar_s     .append(fTbar_s[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_s[ihist].SetName( options.hist1 + '__Tbar_s' + name )
				hMeas_T_tW       .append(fT_tW[ihist].Get(options.hist1).Clone())
				hMeas_T_tW[ihist].SetName( options.hist1 + '__T_tW' + name )
				hMeas_Tbar_tW       .append(fTbar_tW[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_tW[ihist].SetName( options.hist1 + '__Tbar_tW' + name )
				#Wjets
				hMeas_W1Jets       .append(fW1Jets[ihist].Get(options.hist1).Clone())
				hMeas_W1Jets[ihist].SetName( options.hist1 + '__W1Jets' + name )
				hMeas_W2Jets       .append(fW2Jets[ihist].Get(options.hist1).Clone())
				hMeas_W2Jets[ihist].SetName( options.hist1 + '__W2Jets' + name )
				hMeas_W3Jets       .append(fW3Jets[ihist].Get(options.hist1).Clone())
				hMeas_W3Jets[ihist].SetName( options.hist1 + '__W3Jets' + name )
				hMeas_W4Jets       .append(fW4Jets[ihist].Get(options.hist1).Clone())
				hMeas_W4Jets[ihist].SetName( options.hist1 + '__W4Jets' + name )
			
			TTjets_nonSemilepTT_Names = [ "__qcd" , label ]
			for ihist in xrange(len(TTjets_nonSemilepTT_Names)):
				name = TTjets_nonSemilepTT_Names[ihist]	
				hMeas_TT_Mtt_less_700       .append(fTT_Mtt_less_700[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_less_700[ihist].SetName( options.hist1 + '__TTbar_Mtt_less_700' + name )
				hMeas_TT_Mtt_700_1000       .append(fTT_Mtt_700_1000[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_700_1000[ihist].SetName( options.hist1 + '__TTbar_Mtt_700_1000' + name )
				hMeas_TT_Mtt_1000_Inf       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_1000_Inf[ihist].SetName( options.hist1 + '__TTbar_Mtt_1000_Inf' + name ) 
	
				hMeas_TT_nonSemiLep_Mtt_less_700       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_less_700[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_less_700' + name )
				hMeas_TT_nonSemiLep_Mtt_700_1000       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_700_1000[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_700_1000' + name ) 
				hMeas_TT_nonSemiLep_Mtt_1000_Inf       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name )
		else:
			Names = [ "__qcd" , label ]
			for ihist in xrange(len(Names)):
				name = Names[ihist]
				##Single Top
				hMeas_T_t       .append(fT_t[ihist].Get(options.hist1).Clone())
				hMeas_T_t[ihist].SetName( options.hist1 + '__T_t' + name )
				hMeas_Tbar_t       .append(fTbar_t[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_t[ihist].SetName( options.hist1 + '__Tbar_t' + name )
				hMeas_T_s       .append(fT_s[ihist].Get(options.hist1).Clone())
				hMeas_T_s[ihist].SetName( options.hist1 + '__T_s' + name )
				hMeas_Tbar_s     .append(fTbar_s[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_s[ihist].SetName( options.hist1 + '__Tbar_s' + name )
				hMeas_T_tW       .append(fT_tW[ihist].Get(options.hist1).Clone())
				hMeas_T_tW[ihist].SetName( options.hist1 + '__T_tW' + name )
				hMeas_Tbar_tW       .append(fTbar_tW[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_tW[ihist].SetName( options.hist1 + '__Tbar_tW' + name )
				#Wjets
				hMeas_W1Jets       .append( fW1Jets[ihist].Get(options.hist1).Clone())
				hMeas_W1Jets[ihist].SetName( options.hist1 + '__W1Jets' + name )
				hMeas_W2Jets       .append( fW2Jets[ihist].Get(options.hist1).Clone())
				hMeas_W2Jets[ihist].SetName( options.hist1 + '__W2Jets' + name )
				hMeas_W3Jets       .append( fW3Jets[ihist].Get(options.hist1).Clone())
				hMeas_W3Jets[ihist].SetName( options.hist1 + '__W3Jets' + name )
				hMeas_W4Jets       .append( fW4Jets[ihist].Get(options.hist1).Clone())
				hMeas_W4Jets[ihist].SetName( options.hist1 + '__W4Jets' + name )
			
				hMeas_TT_Mtt_less_700       .append(fTT_Mtt_less_700[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_less_700[ihist].SetName( options.hist1 + '__TTbar_Mtt_less_700' + name )
				hMeas_TT_Mtt_700_1000       .append(fTT_Mtt_700_1000[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_700_1000[ihist].SetName( options.hist1 + '__TTbar_Mtt_700_1000' + name )
				hMeas_TT_Mtt_1000_Inf       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_1000_Inf[ihist].SetName( options.hist1 + '__TTbar_Mtt_1000_Inf' + name ) 
	
				hMeas_TT_nonSemiLep_Mtt_less_700       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_less_700[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_less_700' + name )
				hMeas_TT_nonSemiLep_Mtt_700_1000       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_700_1000[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_700_1000' + name ) 
				hMeas_TT_nonSemiLep_Mtt_1000_Inf       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name )

				#print "number of Single top" , name , hMeas_T_t[ihist].GetSum() + hMeas_Tbar_t[ihist].GetSum() + hMeas_T_s[ihist].GetSum() + hMeas_Tbar_s[ihist].GetSum() + hMeas_T_tW[ihist].GetSum() + hMeas_Tbar_tW[ihist].GetSum()
				#print "number of WJets" , name , hMeas_W1Jets[ihist].GetSum() + hMeas_W2Jets[ihist].GetSum() + hMeas_W3Jets[ihist].GetSum() + hMeas_W4Jets[ihist].GetSum() 
				#print "number of TTbar " , name , hMeas_TT_Mtt_less_700[ihist].GetSum() + hMeas_TT_Mtt_700_1000[ihist].GetSum() + hMeas_TT_Mtt_1000_Inf[ihist].GetSum()
				#print "number of non semilep TTbar " , name , hMeas_TT_nonSemiLep_Mtt_less_700[ihist].GetSum() + hMeas_TT_nonSemiLep_Mtt_700_1000[ihist].GetSum() + hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist].GetSum()
				#print ""

# Scale to desired normalization
# Options are :
#  1. From MC
#  2. From fit
#
# For now, we don't have the fit, so we do from MC	
	
	##Scale
	for i in xrange(len(hMeas_T_t)) :
		hMeas_T_t[i]     .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) )
		hMeas_Tbar_t[i]  .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) )
		hMeas_T_s[i]     .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) )
		hMeas_Tbar_s[i]  .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) )
		hMeas_T_tW[i]    .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) )
		hMeas_Tbar_tW[i] .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) )

		hMeas_W1Jets[i].Scale( sigma_WJets_NNLO[0] * lum / float(Nmc_WJets[0]) )
		hMeas_W2Jets[i].Scale( sigma_WJets_NNLO[1] * lum / float(Nmc_WJets[1]) )
		hMeas_W3Jets[i].Scale( sigma_WJets_NNLO[2] * lum / float(Nmc_WJets[2]) )
		hMeas_W4Jets[i].Scale( sigma_WJets_NNLO[3] * lum / float(Nmc_WJets[3]) )

		hMeas_TT_Mtt_less_700[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_0_700[0] * lum / float(Nmc_ttbar))
		hMeas_TT_Mtt_700_1000[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_700_1000[0] * lum / float(Nmc_TT_Mtt_700_1000))
		hMeas_TT_Mtt_1000_Inf[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_1000_Inf[0] * lum / float(Nmc_TT_Mtt_1000_Inf) )

		hMeas_TT_nonSemiLep_Mtt_less_700[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_0_700[0] * lum / float(Nmc_ttbar))
		hMeas_TT_nonSemiLep_Mtt_700_1000[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_700_1000[0] * lum / float(Nmc_TT_Mtt_700_1000))
		hMeas_TT_nonSemiLep_Mtt_1000_Inf[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_1000_Inf[0] * lum / float(Nmc_TT_Mtt_1000_Inf) )


	

#Getting histogram files and scaling to plot histogram2 subtracted from histogram1
elif options.hist2 is not None:	

	if not options.ignoreData : 
            hRecoData1= fdata.Get(options.hist1).Clone()
            hRecoData1.SetName(histname + "__DATA1"  )
            hRecoData2= fdata.Get(options.hist2).Clone()
            hRecoData2.SetName(histname + "__DATA2"  )
            hRecoData = hRecoData1.Clone()
            hRecoData.Add( hRecoData2 , -1.0 )	
            hRecoData.SetName(histname + "__DATA"  )
	
	# Get the histogram files for hist 1        
	hMeas_QCD_SingleMu_1 = fQCD_SingleMu.Get(options.hist1).Clone()
	hMeas_QCD_SingleMu_1.SetName(options.hist1 + "__QCD__1")
	
	if options.RunAllSyst :
		ST_Wjets_Names = [ "__qcd" , "" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "" ,"" ,"" ,""]
		for ihist in xrange(len(ST_Wjets_Names)) :
			name = ST_Wjets_Names[ihist]
			##Single Top
			hMeas_T_t_1       .append(fT_t[ihist].Get(options.hist1).Clone())
			hMeas_T_t_1[ihist].SetName( options.hist1 + '__T_t' + name + '__1' )
			hMeas_Tbar_t_1       .append(fTbar_t[ihist].Get(options.hist1).Clone())
			hMeas_Tbar_t_1[ihist].SetName( options.hist1 + '__Tbar_t' + name + '__1' )
			hMeas_T_s_1       .append(fT_s[ihist].Get(options.hist1).Clone())
			hMeas_T_s_1[ihist].SetName( options.hist1 + '__T_s' + name + '__1' )
			hMeas_Tbar_s_1       .append(fTbar_s[ihist].Get(options.hist1).Clone())
			hMeas_Tbar_s_1[ihist].SetName( options.hist1 + '__Tbar_s' + name + '__1' )
			hMeas_T_tW_1       .append(fT_tW[ihist].Get(options.hist1).Clone())
			hMeas_T_tW_1[ihist].SetName( options.hist1 + '__T_tW' + name + '__1' )
			hMeas_Tbar_tW_1       .append(fTbar_tW[ihist].Get(options.hist1).Clone())
			hMeas_Tbar_tW_1[ihist].SetName( options.hist1 + '__Tbar_tW' + name + '__1' )
			#Wjets
			hMeas_W1Jets_1       .append(fW1Jets[ihist].Get(options.hist1).Clone())
			hMeas_W1Jets_1[ihist].SetName( options.hist1 + '__W1Jets' + name + '__1' )
			hMeas_W2Jets_1       .append(fW2Jets[ihist].Get(options.hist1).Clone())
			hMeas_W2Jets_1[ihist].SetName( options.hist1 + '__W2Jets' + name + '__1' )
			hMeas_W3Jets_1       .append(fW3Jets[ihist].Get(options.hist1).Clone())
			hMeas_W3Jets_1[ihist].SetName( options.hist1 + '__W3Jets' + name + '__1' )
			hMeas_W4Jets_1       .append(fW4Jets[ihist].Get(options.hist1).Clone())
			hMeas_W4Jets_1[ihist].SetName( options.hist1 + '__W4Jets' + name + '__1' )
			
		TTjets_nonSemilepTT_Names = [ "__qcd" , "" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "__pdf__down" , "__pdf__up" , "__scale__down" , "__scale__up" ]
		for ihist in xrange(len(TTjets_nonSemilepTT_Names)) : 
			name = TTjets_nonSemilepTT_Names[ihist]
			hMeas_TT_Mtt_less_700_1       .append(fTT_Mtt_less_700[ihist].Get(options.hist1).Clone())
			hMeas_TT_Mtt_less_700_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_less_700' + name + '__1' )
			hMeas_TT_Mtt_700_1000_1       .append(fTT_Mtt_700_1000[ihist].Get(options.hist1).Clone())
			hMeas_TT_Mtt_700_1000_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_700_1000' + name + '__1' )
			hMeas_TT_Mtt_1000_Inf_1       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
			hMeas_TT_Mtt_1000_Inf_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_1000_Inf' + name + '__1' ) 
	
			hMeas_TT_nonSemiLep_Mtt_less_700_1       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist1).Clone())
			hMeas_TT_nonSemiLep_Mtt_less_700_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_less_700' + name + '__1' )
			hMeas_TT_nonSemiLep_Mtt_700_1000_1       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist1).Clone())
			hMeas_TT_nonSemiLep_Mtt_700_1000_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_700_1000' + name + '__1' ) 
			hMeas_TT_nonSemiLep_Mtt_1000_Inf_1       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
			hMeas_TT_nonSemiLep_Mtt_1000_Inf_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name + '__1' )

	if not options.RunAllSyst :
		if "pdfdn" in options.systVariation or "pdfup" in options.systVariation or "scaledown_nom" in options.systVariation or "scaleup_nom" in options.systVariation :			
			ST_Wjets_Names = [ "__qcd" , "" ]
			for ihist in xrange(len(ST_Wjets_Names)):
				name = ST_Wjets_Names[ihist]
				##Single Top
				hMeas_T_t_1       .append(fT_t[ihist].Get(options.hist1).Clone())
				hMeas_T_t_1[ihist].SetName( options.hist1 + '__T_t' + name + '__1' )
				hMeas_Tbar_t_1       .append(fTbar_t[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_t_1[ihist].SetName( options.hist1 + '__Tbar_t' + name + '__1' )
				hMeas_T_s_1       .append(fT_s[ihist].Get(options.hist1).Clone())
				hMeas_T_s_1[ihist].SetName( options.hist1 + '__T_s' + name + '__1' )
				hMeas_Tbar_s_1     .append(fTbar_s[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_s_1[ihist].SetName( options.hist1 + '__Tbar_s' + name + '__1' )
				hMeas_T_tW_1       .append(fT_tW[ihist].Get(options.hist1).Clone())
				hMeas_T_tW_1[ihist].SetName( options.hist1 + '__T_tW' + name + '__1' )
				hMeas_Tbar_tW_1       .append(fTbar_tW[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_tW_1[ihist].SetName( options.hist1 + '__Tbar_tW' + name + '__1' )
				#Wjets
				hMeas_W1Jets_1       .append(fW1Jets[ihist].Get(options.hist1).Clone())
				hMeas_W1Jets_1[ihist].SetName( options.hist1 + '__W1Jets' + name + '__1' )
				hMeas_W2Jets_1       .append(fW2Jets[ihist].Get(options.hist1).Clone())
				hMeas_W2Jets_1[ihist].SetName( options.hist1 + '__W2Jets' + name + '__1' )
				hMeas_W3Jets_1       .append(fW3Jets[ihist].Get(options.hist1).Clone())
				hMeas_W3Jets_1[ihist].SetName( options.hist1 + '__W3Jets' + name + '__1' )
				hMeas_W4Jets_1       .append(fW4Jets[ihist].Get(options.hist1).Clone())
				hMeas_W4Jets_1[ihist].SetName( options.hist1 + '__W4Jets' + name + '__1' )
			
			TTjets_nonSemilepTT_Names = [ "__qcd" , label ]
			for ihist in xrange(len(TTjets_nonSemilepTT_Names)):
				name = TTjets_nonSemilepTT_Names[ihist]	
				hMeas_TT_Mtt_less_700_1       .append(fTT_Mtt_less_700[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_less_700_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_less_700' + name + '__1' )
				hMeas_TT_Mtt_700_1000_1       .append(fTT_Mtt_700_1000[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_700_1000_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_700_1000' + name + '__1' )
				hMeas_TT_Mtt_1000_Inf_1       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_1000_Inf_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_1000_Inf' + name + '__1' ) 
	
				hMeas_TT_nonSemiLep_Mtt_less_700_1       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_less_700_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_less_700' + name + '__1' )
				hMeas_TT_nonSemiLep_Mtt_700_1000_1       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_700_1000_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_700_1000' + name + '__1' ) 
				hMeas_TT_nonSemiLep_Mtt_1000_Inf_1       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_1000_Inf_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name + '__1' )
		else:
			Names = [ "__qcd" , label ]
			for ihist in xrange(len(Names)):
				name = Names[ihist]
				##Single Top
				hMeas_T_t_1       .append(fT_t[ihist].Get(options.hist1).Clone())
				hMeas_T_t_1[ihist].SetName( options.hist1 + '__T_t' + name + '__1' )
				hMeas_Tbar_t_1       .append(fTbar_t[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_t_1[ihist].SetName( options.hist1 + '__Tbar_t' + name + '__1' )
				hMeas_T_s_1       .append(fT_s[ihist].Get(options.hist1).Clone())
				hMeas_T_s_1[ihist].SetName( options.hist1 + '__T_s' + name + '__1' )
				hMeas_Tbar_s_1     .append(fTbar_s[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_s_1[ihist].SetName( options.hist1 + '__Tbar_s' + name + '__1' )
				hMeas_T_tW_1       .append(fT_tW[ihist].Get(options.hist1).Clone())
				hMeas_T_tW_1[ihist].SetName( options.hist1 + '__T_tW' + name + '__1' )
				hMeas_Tbar_tW_1       .append(fTbar_tW[ihist].Get(options.hist1).Clone())
				hMeas_Tbar_tW_1[ihist].SetName( options.hist1 + '__Tbar_tW' + name + '__1' )
				#Wjets
				hMeas_W1Jets_1       .append( fW1Jets[ihist].Get(options.hist1).Clone())
				hMeas_W1Jets_1[ihist].SetName( options.hist1 + '__W1Jets' + name + '__1' )
				hMeas_W2Jets_1       .append( fW2Jets[ihist].Get(options.hist1).Clone())
				hMeas_W2Jets_1[ihist].SetName( options.hist1 + '__W2Jets' + name + '__1' )
				hMeas_W3Jets_1       .append( fW3Jets[ihist].Get(options.hist1).Clone())
				hMeas_W3Jets_1[ihist].SetName( options.hist1 + '__W3Jets' + name + '__1' )
				hMeas_W4Jets_1       .append( fW4Jets[ihist].Get(options.hist1).Clone())
				hMeas_W4Jets_1[ihist].SetName( options.hist1 + '__W4Jets' + name + '__1' )
			
				hMeas_TT_Mtt_less_700_1       .append(fTT_Mtt_less_700[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_less_700_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_less_700' + name + '__1' )
				hMeas_TT_Mtt_700_1000_1       .append(fTT_Mtt_700_1000[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_700_1000_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_700_1000' + name + '__1' )
				hMeas_TT_Mtt_1000_Inf_1       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
				hMeas_TT_Mtt_1000_Inf_1[ihist].SetName( options.hist1 + '__TTbar_Mtt_1000_Inf' + name + '__1' ) 
	
				hMeas_TT_nonSemiLep_Mtt_less_700_1       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_less_700_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_less_700' + name + '__1' )
				hMeas_TT_nonSemiLep_Mtt_700_1000_1       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_700_1000_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_700_1000' + name + '__1' ) 
				hMeas_TT_nonSemiLep_Mtt_1000_Inf_1       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist1).Clone())
				hMeas_TT_nonSemiLep_Mtt_1000_Inf_1[ihist].SetName( options.hist1 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name + '__1' )
	
	for i in xrange(len(hMeas_T_t_1)) :
			hMeas_T_t_1[i]     .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) )
			hMeas_Tbar_t_1[i]  .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) )
			hMeas_T_s_1[i]     .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) )
			hMeas_Tbar_s_1[i]  .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) )
			hMeas_T_tW_1[i]    .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) )
			hMeas_Tbar_tW_1[i] .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) )
	
			hMeas_W1Jets_1[i].Scale( sigma_WJets_NNLO[0] * lum / float(Nmc_WJets[0]) )
			hMeas_W2Jets_1[i].Scale( sigma_WJets_NNLO[1] * lum / float(Nmc_WJets[1]) )
			hMeas_W3Jets_1[i].Scale( sigma_WJets_NNLO[2] * lum / float(Nmc_WJets[2]) )
			hMeas_W4Jets_1[i].Scale( sigma_WJets_NNLO[3] * lum / float(Nmc_WJets[3]) )
	
			hMeas_TT_Mtt_less_700_1[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_0_700[0] * lum / float(Nmc_ttbar))
			hMeas_TT_Mtt_700_1000_1[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_700_1000[0] * lum / float(Nmc_TT_Mtt_700_1000))
			hMeas_TT_Mtt_1000_Inf_1[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_1000_Inf[0] * lum / float(Nmc_TT_Mtt_1000_Inf) )
	
			hMeas_TT_nonSemiLep_Mtt_less_700_1[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_0_700[0] * lum / float(Nmc_ttbar))
			hMeas_TT_nonSemiLep_Mtt_700_1000_1[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_700_1000[0] * lum / float(Nmc_TT_Mtt_700_1000))
			hMeas_TT_nonSemiLep_Mtt_1000_Inf_1[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_1000_Inf[0] * lum / float(Nmc_TT_Mtt_1000_Inf) )
	
	

	# Get the histogram files for hist 2
	hMeas_QCD_SingleMu_2 = fQCD_SingleMu.Get(options.hist2).Clone()
	hMeas_QCD_SingleMu_2.SetName(options.hist2 + "__QCD__2")

	if options.RunAllSyst :
		ST_Wjets_Names = [ "__qcd" , "" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "" ,"" ,"" ,""]
		for ihist in xrange(len(ST_Wjets_Names)) :
			name = ST_Wjets_Names[ihist]
			##Single Top
			hMeas_T_t_2       .append(fT_t[ihist].Get(options.hist2).Clone())
			hMeas_T_t_2[ihist].SetName( options.hist2 + '__T_t' + name + '__2' )
			hMeas_Tbar_t_2       .append(fTbar_t[ihist].Get(options.hist2).Clone())
			hMeas_Tbar_t_2[ihist].SetName( options.hist2 + '__Tbar_t' + name + '__2' )
			hMeas_T_s_2       .append(fT_s[ihist].Get(options.hist2).Clone())
			hMeas_T_s_2[ihist].SetName( options.hist2 + '__T_s' + name + '__2' )
			hMeas_Tbar_s_2       .append(fTbar_s[ihist].Get(options.hist2).Clone())
			hMeas_Tbar_s_2[ihist].SetName( options.hist2 + '__Tbar_s' + name + '__2' )
			hMeas_T_tW_2       .append(fT_tW[ihist].Get(options.hist2).Clone())
			hMeas_T_tW_2[ihist].SetName( options.hist2 + '__T_tW' + name + '__2' )
			hMeas_Tbar_tW_2       .append(fTbar_tW[ihist].Get(options.hist2).Clone())
			hMeas_Tbar_tW_2[ihist].SetName( options.hist2 + '__Tbar_tW' + name + '__2' )
			#Wjets
			hMeas_W1Jets_2       .append(fW1Jets[ihist].Get(options.hist2).Clone())
			hMeas_W1Jets_2[ihist].SetName( options.hist2 + '__W1Jets' + name + '__2' )
			hMeas_W2Jets_2       .append(fW2Jets[ihist].Get(options.hist2).Clone())
			hMeas_W2Jets_2[ihist].SetName( options.hist2 + '__W2Jets' + name + '__2' )
			hMeas_W3Jets_2       .append(fW3Jets[ihist].Get(options.hist2).Clone())
			hMeas_W3Jets_2[ihist].SetName( options.hist2 + '__W3Jets' + name + '__2' )
			hMeas_W4Jets_2       .append(fW4Jets[ihist].Get(options.hist2).Clone())
			hMeas_W4Jets_2[ihist].SetName( options.hist2 + '__W4Jets' + name + '__2' )
			
		TTjets_nonSemilepTT_Names = [ "__qcd" , "" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "__pdf__down" , "__pdf__up" , "__scale__down" , "__scale__up" ]
		for ihist in xrange(len(TTjets_nonSemilepTT_Names)) : 
			name = TTjets_nonSemilepTT_Names[ihist]
			hMeas_TT_Mtt_less_700_2       .append(fTT_Mtt_less_700[ihist].Get(options.hist2).Clone())
			hMeas_TT_Mtt_less_700_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_less_700' + name + '__2' )
			hMeas_TT_Mtt_700_1000_2       .append(fTT_Mtt_700_1000[ihist].Get(options.hist2).Clone())
			hMeas_TT_Mtt_700_1000_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_700_1000' + name + '__2' )
			hMeas_TT_Mtt_1000_Inf_2       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist2).Clone())
			hMeas_TT_Mtt_1000_Inf_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_1000_Inf' + name + '__2' ) 
	
			hMeas_TT_nonSemiLep_Mtt_less_700_2       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist2).Clone())
			hMeas_TT_nonSemiLep_Mtt_less_700_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_less_700' + name + '__2' )
			hMeas_TT_nonSemiLep_Mtt_700_1000_2       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist2).Clone())
			hMeas_TT_nonSemiLep_Mtt_700_1000_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_700_1000' + name + '__2' ) 
			hMeas_TT_nonSemiLep_Mtt_1000_Inf_2       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist2).Clone())
			hMeas_TT_nonSemiLep_Mtt_1000_Inf_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name + '__2' )

	if not options.RunAllSyst :
		if "pdfdn" in options.systVariation or "pdfup" in options.systVariation or "scaledown_nom" in options.systVariation or "scaleup_nom" in options.systVariation :			
			ST_Wjets_Names = [ "__qcd" , "" ]
			for ihist in xrange(len(ST_Wjets_Names)):
				name = ST_Wjets_Names[ihist]
				##Single Top
				hMeas_T_t_2       .append(fT_t[ihist].Get(options.hist2).Clone())
				hMeas_T_t_2[ihist].SetName( options.hist2 + '__T_t' + name + '__2' )
				hMeas_Tbar_t_2       .append(fTbar_t[ihist].Get(options.hist2).Clone())
				hMeas_Tbar_t_2[ihist].SetName( options.hist2 + '__Tbar_t' + name + '__2' )
				hMeas_T_s_2       .append(fT_s[ihist].Get(options.hist2).Clone())
				hMeas_T_s_2[ihist].SetName( options.hist2 + '__T_s' + name + '__2' )
				hMeas_Tbar_s_2     .append(fTbar_s[ihist].Get(options.hist2).Clone())
				hMeas_Tbar_s_2[ihist].SetName( options.hist2 + '__Tbar_s' + name + '__2' )
				hMeas_T_tW_2       .append(fT_tW[ihist].Get(options.hist2).Clone())
				hMeas_T_tW_2[ihist].SetName( options.hist2 + '__T_tW' + name + '__2' )
				hMeas_Tbar_tW_2       .append(fTbar_tW[ihist].Get(options.hist2).Clone())
				hMeas_Tbar_tW_2[ihist].SetName( options.hist2 + '__Tbar_tW' + name + '__2' )
				#Wjets
				hMeas_W1Jets_2       .append(fW1Jets[ihist].Get(options.hist2).Clone())
				hMeas_W1Jets_2[ihist].SetName( options.hist2 + '__W1Jets' + name + '__2' )
				hMeas_W2Jets_2       .append(fW2Jets[ihist].Get(options.hist2).Clone())
				hMeas_W2Jets_2[ihist].SetName( options.hist2 + '__W2Jets' + name + '__2' )
				hMeas_W3Jets_2       .append(fW3Jets[ihist].Get(options.hist2).Clone())
				hMeas_W3Jets_2[ihist].SetName( options.hist2 + '__W3Jets' + name + '__2' )
				hMeas_W4Jets_2       .append(fW4Jets[ihist].Get(options.hist2).Clone())
				hMeas_W4Jets_2[ihist].SetName( options.hist2 + '__W4Jets' + name + '__2' )
			
			TTjets_nonSemilepTT_Names = [ "__qcd" , label ]
			for ihist in xrange(len(TTjets_nonSemilepTT_Names)):
				name = TTjets_nonSemilepTT_Names[ihist]	
				hMeas_TT_Mtt_less_700_2       .append(fTT_Mtt_less_700[ihist].Get(options.hist2).Clone())
				hMeas_TT_Mtt_less_700_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_less_700' + name + '__2' )
				hMeas_TT_Mtt_700_1000_2       .append(fTT_Mtt_700_1000[ihist].Get(options.hist2).Clone())
				hMeas_TT_Mtt_700_1000_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_700_1000' + name + '__2' )
				hMeas_TT_Mtt_1000_Inf_2       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist2).Clone())
				hMeas_TT_Mtt_1000_Inf_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_1000_Inf' + name + '__2' ) 
	
				hMeas_TT_nonSemiLep_Mtt_less_700_2       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist2).Clone())
				hMeas_TT_nonSemiLep_Mtt_less_700_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_less_700' + name + '__2' )
				hMeas_TT_nonSemiLep_Mtt_700_1000_2       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist2).Clone())
				hMeas_TT_nonSemiLep_Mtt_700_1000_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_700_1000' + name + '__2' ) 
				hMeas_TT_nonSemiLep_Mtt_1000_Inf_2       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist2).Clone())
				hMeas_TT_nonSemiLep_Mtt_1000_Inf_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name + '__2' )
		else:
			Names = [ "__qcd" , label ]
			for ihist in xrange(len(Names)):
				name = Names[ihist]
				##Single Top
				hMeas_T_t_2       .append(fT_t[ihist].Get(options.hist2).Clone())
				hMeas_T_t_2[ihist].SetName( options.hist2 + '__T_t' + name + '__2' )
				hMeas_Tbar_t_2       .append(fTbar_t[ihist].Get(options.hist2).Clone())
				hMeas_Tbar_t_2[ihist].SetName( options.hist2 + '__Tbar_t' + name + '__2' )
				hMeas_T_s_2       .append(fT_s[ihist].Get(options.hist2).Clone())
				hMeas_T_s_2[ihist].SetName( options.hist2 + '__T_s' + name + '__2' )
				hMeas_Tbar_s_2     .append(fTbar_s[ihist].Get(options.hist2).Clone())
				hMeas_Tbar_s_2[ihist].SetName( options.hist2 + '__Tbar_s' + name + '__2' )
				hMeas_T_tW_2       .append(fT_tW[ihist].Get(options.hist2).Clone())
				hMeas_T_tW_2[ihist].SetName( options.hist2 + '__T_tW' + name + '__2' )
				hMeas_Tbar_tW_2       .append(fTbar_tW[ihist].Get(options.hist2).Clone())
				hMeas_Tbar_tW_2[ihist].SetName( options.hist2 + '__Tbar_tW' + name + '__2' )
				#Wjets
				hMeas_W1Jets_2       .append( fW1Jets[ihist].Get(options.hist2).Clone())
				hMeas_W1Jets_2[ihist].SetName( options.hist2 + '__W1Jets' + name + '__2' )
				hMeas_W2Jets_2       .append( fW2Jets[ihist].Get(options.hist2).Clone())
				hMeas_W2Jets_2[ihist].SetName( options.hist2 + '__W2Jets' + name + '__2' )
				hMeas_W3Jets_2       .append( fW3Jets[ihist].Get(options.hist2).Clone())
				hMeas_W3Jets_2[ihist].SetName( options.hist2 + '__W3Jets' + name + '__2' )
				hMeas_W4Jets_2       .append( fW4Jets[ihist].Get(options.hist2).Clone())
				hMeas_W4Jets_2[ihist].SetName( options.hist2 + '__W4Jets' + name + '__2' )
			
			
				hMeas_TT_Mtt_less_700_2       .append(fTT_Mtt_less_700[ihist].Get(options.hist2).Clone())
				hMeas_TT_Mtt_less_700_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_less_700' + name + '__2' )
				hMeas_TT_Mtt_700_1000_2       .append(fTT_Mtt_700_1000[ihist].Get(options.hist2).Clone())
				hMeas_TT_Mtt_700_1000_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_700_1000' + name + '__2' )
				hMeas_TT_Mtt_1000_Inf_2       .append(fTT_Mtt_1000_Inf[ihist].Get(options.hist2).Clone())
				hMeas_TT_Mtt_1000_Inf_2[ihist].SetName( options.hist2 + '__TTbar_Mtt_1000_Inf' + name + '__2' ) 
	
				hMeas_TT_nonSemiLep_Mtt_less_700_2       .append(fTT_nonSemiLep_Mtt_less_700[ihist].Get(options.hist2).Clone())
				hMeas_TT_nonSemiLep_Mtt_less_700_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_less_700' + name + '__2' )
				hMeas_TT_nonSemiLep_Mtt_700_1000_2       .append(fTT_nonSemiLep_Mtt_700_1000[ihist].Get(options.hist2).Clone())
				hMeas_TT_nonSemiLep_Mtt_700_1000_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_700_1000' + name + '__2' ) 
				hMeas_TT_nonSemiLep_Mtt_1000_Inf_2       .append(fTT_nonSemiLep_Mtt_1000_Inf[ihist].Get(options.hist2).Clone())
				hMeas_TT_nonSemiLep_Mtt_1000_Inf_2[ihist].SetName( options.hist2 + '__TTbar_nonSemiLep_Mtt_1000_Inf' + name + '__2' )
	
	for i in xrange(len(hMeas_T_t_2)) :
			hMeas_T_t_2[i]     .Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) )
			hMeas_Tbar_t_2[i]  .Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) )
			hMeas_T_s_2[i]     .Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) )
			hMeas_Tbar_s_2[i]  .Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) )
			hMeas_T_tW_2[i]    .Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) )
			hMeas_Tbar_tW_2[i] .Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) )
	
			hMeas_W1Jets_2[i].Scale( sigma_WJets_NNLO[0] * lum / float(Nmc_WJets[0]) )
			hMeas_W2Jets_2[i].Scale( sigma_WJets_NNLO[1] * lum / float(Nmc_WJets[1]) )
			hMeas_W3Jets_2[i].Scale( sigma_WJets_NNLO[2] * lum / float(Nmc_WJets[2]) )
			hMeas_W4Jets_2[i].Scale( sigma_WJets_NNLO[3] * lum / float(Nmc_WJets[3]) )
	
			hMeas_TT_Mtt_less_700_2[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_0_700[0] * lum / float(Nmc_ttbar))
			hMeas_TT_Mtt_700_1000_2[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_700_1000[0] * lum / float(Nmc_TT_Mtt_700_1000))
			hMeas_TT_Mtt_1000_Inf_2[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_1000_Inf[0] * lum / float(Nmc_TT_Mtt_1000_Inf) )
	
			hMeas_TT_nonSemiLep_Mtt_less_700_2[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_0_700[0] * lum / float(Nmc_ttbar))
			hMeas_TT_nonSemiLep_Mtt_700_1000_2[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_700_1000[0] * lum / float(Nmc_TT_Mtt_700_1000))
			hMeas_TT_nonSemiLep_Mtt_1000_Inf_2[i].Scale( sigma_ttbar_NNLO[0] * e_TT_Mtt_1000_Inf[0] * lum / float(Nmc_TT_Mtt_1000_Inf) )
	
   

	#Subtract hist2 from hist1
	for ihist in xrange(len(hMeas_T_t_1)):
		hMeas_T_t       .append(hMeas_T_t_1[ihist].Clone())
		hMeas_T_t[ihist].Add( hMeas_T_t_2[ihist] , -1.0 )
		hMeas_Tbar_t .append( hMeas_Tbar_t_1[ihist].Clone())
		hMeas_Tbar_t[ihist].Add( hMeas_Tbar_t_2[ihist] , -1.0 )
		hMeas_T_s .append(hMeas_T_s_1[ihist].Clone())
		hMeas_T_s[ihist].Add( hMeas_T_s_2[ihist] , -1.0 )
		hMeas_Tbar_s .append( hMeas_Tbar_s_1[ihist].Clone())
		hMeas_Tbar_s[ihist].Add( hMeas_Tbar_s_2[ihist] , -1.0 )
		hMeas_T_tW .append(  hMeas_T_tW_1[ihist].Clone())
		hMeas_T_tW[ihist].Add( hMeas_T_tW_2[ihist] , -1.0 )
		hMeas_Tbar_tW .append( hMeas_Tbar_tW_1[ihist].Clone())
		hMeas_Tbar_tW[ihist].Add( hMeas_Tbar_tW_2[ihist] , -1.0 )

		hMeas_W1Jets .append( hMeas_W1Jets_1[ihist].Clone())
		hMeas_W1Jets[ihist].Add( hMeas_W1Jets_2[ihist] , -1.0 )
		hMeas_W2Jets .append( hMeas_W2Jets_1[ihist].Clone())
		hMeas_W2Jets[ihist].Add( hMeas_W2Jets_2[ihist] , -1.0 )
		hMeas_W3Jets .append( hMeas_W3Jets_1[ihist].Clone())
		hMeas_W3Jets[ihist].Add( hMeas_W3Jets_2[ihist] , -1.0 )
		hMeas_W4Jets .append( hMeas_W4Jets_1[ihist].Clone())
		hMeas_W4Jets[ihist].Add( hMeas_W4Jets_2[ihist] , -1.0 )

		hMeas_TT_Mtt_less_700 .append( hMeas_TT_Mtt_less_700_1[ihist].Clone())
		hMeas_TT_Mtt_less_700[ihist].Add( hMeas_TT_Mtt_less_700_2[ihist] , -1.0 )
		hMeas_TT_Mtt_700_1000 .append(hMeas_TT_Mtt_700_1000_1[ihist].Clone())
		hMeas_TT_Mtt_700_1000[ihist].Add( hMeas_TT_Mtt_700_1000_2[ihist] , -1.0 )
		hMeas_TT_Mtt_1000_Inf .append(hMeas_TT_Mtt_1000_Inf_1[ihist].Clone())
		hMeas_TT_Mtt_1000_Inf[ihist].Add( hMeas_TT_Mtt_1000_Inf_2[ihist] , -1.0 )

		hMeas_TT_nonSemiLep_Mtt_less_700 .append( hMeas_TT_nonSemiLep_Mtt_less_700_1[ihist].Clone())
		hMeas_TT_nonSemiLep_Mtt_less_700[ihist].Add( hMeas_TT_nonSemiLep_Mtt_less_700_2[ihist] , -1.0 )
		hMeas_TT_nonSemiLep_Mtt_700_1000 .append( hMeas_TT_nonSemiLep_Mtt_700_1000_1[ihist].Clone())
		hMeas_TT_nonSemiLep_Mtt_700_1000[ihist].Add( hMeas_TT_nonSemiLep_Mtt_700_1000_2[ihist] , -1.0 )
		hMeas_TT_nonSemiLep_Mtt_1000_Inf .append( hMeas_TT_nonSemiLep_Mtt_1000_Inf_1[ihist].Clone())
		hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist].Add( hMeas_TT_nonSemiLep_Mtt_1000_Inf_2[ihist] , -1.0 )

		hMeas_QCD_SingleMu = hMeas_QCD_SingleMu_1.Clone()
		hMeas_QCD_SingleMu.Add( hMeas_QCD_SingleMu_2 , -1.0 )
		hMeas_QCD_SingleMu.SetName(histname + "__QCD")

######Correcting the QCD - plotting - writing in a root file
qcdcanvs = []

######### Correct the QCD estimate with the known MC backgrounds in the noniso region. ########
iiqcd = 0
qcdstack = THStack("qcdstack", "qcdstack")
hMeas_QCD_SingleMu_ToPlot = hMeas_QCD_SingleMu.Clone()
qcdcolors = [TColor.kMagenta, TColor.kMagenta,
             TColor.kMagenta, TColor.kMagenta,
             TColor.kMagenta, TColor.kMagenta,
             TColor.kGreen-3, TColor.kGreen-3,
             TColor.kGreen-3, TColor.kGreen-3,
             TColor.kRed+1, TColor.kRed+1, TColor.kRed+1,
             TColor.kRed-7, TColor.kRed-7, TColor.kRed-7
             ]
hMeas_QCD_SingleMu_ToPlot.SetName("hmeas_QCD_SingleMu_ToPlot")


for iqcdHist in [ hMeas_T_t[0], hMeas_Tbar_t[0],
				  hMeas_T_s[0], hMeas_Tbar_s[0],
				  hMeas_T_tW[0], hMeas_Tbar_tW[0],
				  hMeas_W1Jets[0], hMeas_W2Jets[0],
				  hMeas_W3Jets[0], hMeas_W4Jets[0],
				  hMeas_TT_Mtt_less_700[0], hMeas_TT_Mtt_700_1000[0],
				  hMeas_TT_Mtt_1000_Inf[0],
				  hMeas_TT_nonSemiLep_Mtt_less_700[0], hMeas_TT_nonSemiLep_Mtt_700_1000[0],
				  hMeas_TT_nonSemiLep_Mtt_1000_Inf[0]] :
	iqcdHist.SetFillColor(qcdcolors[iiqcd])
	hMeas_QCD_SingleMu.Add( iqcdHist, -1.0 )
	qcdstack.Add( iqcdHist )
	iiqcd += 1

#qcdcanv = TCanvas( "qcddatamc", "qcddatamc")
#hMeas_QCD_SingleMu_ToPlot.Draw("e")
#qcdstack.Draw("same hist")
#hMeas_QCD_SingleMu_ToPlot.Draw("e same")
#hMeas_QCD_SingleMu_ToPlot.Draw("e same axis")

# scale the QCD

if hMeas_QCD_SingleMu.GetSum() > 0.0 : 
	hMeas_QCD_SingleMu.Scale( NQCD / hMeas_QCD_SingleMu.GetSum() )
else : 
	hMeas_QCD_SingleMu.Scale( 0.0 )

    
######### Combine ttbar samples ############# 
if 1==0 :
	if options.RunAllSyst or "nom" in options.systVariation :
		ttbar_canv = TCanvas( "ttbar", "ttbar", 2000, 600 )
		ttbar_canv.Divide(3,1)
		ttbar_nom_stack = THStack("ttbar_nom", "ttbar_nom")
		hMeas_TT_Mtt_less_700[1] .SetLineColor( 2 )
		hMeas_TT_Mtt_700_1000[1] .SetLineColor( 3 )
		hMeas_TT_Mtt_1000_Inf[1] .SetLineColor( 4 )
		ttbar_nom_stack.Add( hMeas_TT_Mtt_less_700[1] )
		ttbar_nom_stack.Add( hMeas_TT_Mtt_700_1000[1] )
		ttbar_nom_stack.Add( hMeas_TT_Mtt_1000_Inf[1] )
		ttbar_nom_stack.Draw("nostack hist")
		ttbar_nom_stack.SetMaximum(500.)
	
	if options.RunAllSyst or "scaleup_nom" in options.systVariation :
		ttbar_canv.cd(2)
		ttbar_scaleup_stack = THStack("ttbar_scaleup", "ttbar_scaleup")
		hMeas_TT_Mtt_less_700[14] .SetLineColor( 2 )
		hMeas_TT_Mtt_700_1000[14] .SetLineColor( 3 )
		hMeas_TT_Mtt_1000_Inf[14] .SetLineColor( 4 )
		ttbar_scaleup_stack.Add( hMeas_TT_Mtt_less_700[14] )
		ttbar_scaleup_stack.Add( hMeas_TT_Mtt_700_1000[14] )
		ttbar_scaleup_stack.Add( hMeas_TT_Mtt_1000_Inf[14] )
		ttbar_scaleup_stack.Draw("nostack hist")
		ttbar_scaleup_stack.SetMaximum(500.)

	if options.RunAllSyst or "scaledown_nom" in options.systVariation :
		ttbar_canv.cd(3)
		ttbar_scaledown_stack = THStack("ttbar_scaledown", "ttbar_scaledown")
		hMeas_TT_Mtt_less_700[13] .SetLineColor( 2 )
		hMeas_TT_Mtt_700_1000[13] .SetLineColor( 3 )
		hMeas_TT_Mtt_1000_Inf[13] .SetLineColor( 4 )
		ttbar_scaledown_stack.Add( hMeas_TT_Mtt_less_700[13] )
		ttbar_scaledown_stack.Add( hMeas_TT_Mtt_700_1000[13] )
		ttbar_scaledown_stack.Add( hMeas_TT_Mtt_1000_Inf[13] )
		ttbar_scaledown_stack.Draw("nostack hist")
		ttbar_scaledown_stack.SetMaximum(500.)

	ttbar_canv.Print("q2woes.pdf", "pdf")
	ttbar_canv.Print("q2woes.png", "png")

## combining ttbar samples, TTbar non semilep samples, Single Top samples
if options.RunAllSyst :
	ST_Wjets_Names = [ "__qcd" , "" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "" ,"" ,"" ,""]
	for ihist in xrange(len(ST_Wjets_Names)) :
		name = ST_Wjets_Names[ihist]
		hMeas_WJets.append(hMeas_W1Jets[ihist].Clone())
		hMeas_WJets[ihist].SetName( histname + '__WJets' + name )
		hMeas_SingleTop.append(hMeas_T_t[ihist].Clone())
		hMeas_SingleTop[ihist].SetName(histname + '__SingleTop' + name )
		for hist in [hMeas_Tbar_t[ihist], hMeas_T_s[ihist], hMeas_Tbar_s[ihist], hMeas_T_tW[ihist], hMeas_Tbar_tW[ihist]] :
			hMeas_SingleTop[ihist].Add( hist )
		for hist in [ hMeas_W2Jets[ihist], hMeas_W3Jets[ihist], hMeas_W4Jets[ihist] ] :
			hMeas_WJets[ihist].Add( hist )
		
	TTjets_nonSemilepTT_Names = [ "__qcd" , "" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "__pdf__down" , "__pdf__up" , "__scale__down" , "__scale__up" ]
	for ihist in xrange(len(TTjets_nonSemilepTT_Names)):
		name = TTjets_nonSemilepTT_Names[ihist]
		hMeas_TTbar.append(hMeas_TT_Mtt_less_700[ihist].Clone())
		hMeas_TTbar[ihist].SetName(histname + '__TTbar' + name )
		for hist in [hMeas_TT_Mtt_700_1000[ihist], hMeas_TT_Mtt_1000_Inf[ihist]] :
			hMeas_TTbar[ihist].Add( hist )
	
		hMeas_TTbar_nonSemiLep.append(hMeas_TT_nonSemiLep_Mtt_less_700[ihist].Clone())
		hMeas_TTbar_nonSemiLep[ihist].SetName(histname + '__TTbar_nonSemiLep' +name )
		for hist in [hMeas_TT_nonSemiLep_Mtt_700_1000[ihist], hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist]] :
			hMeas_TTbar_nonSemiLep[ihist].Add( hist )
	
	
if not options.RunAllSyst :
	if "pdfdn" in options.systVariation or "pdfup" in options.systVariation or "scaledown_nom" in options.systVariation or "scaleup_nom" in options.systVariation :			
			ST_Wjets_Names = [ "__qcd" , "" ]
			for ihist in xrange(len(ST_Wjets_Names)):
				name = ST_Wjets_Names[ihist]
				hMeas_WJets.append(hMeas_W1Jets[ihist].Clone())
				hMeas_WJets[ihist].SetName( histname + '__WJets' + name )
				hMeas_SingleTop.append(hMeas_T_t[ihist].Clone())
				hMeas_SingleTop[ihist].SetName(histname + '__SingleTop' + name )
				for hist in [hMeas_Tbar_t[ihist], hMeas_T_s[ihist], hMeas_Tbar_s[ihist], hMeas_T_tW[ihist], hMeas_Tbar_tW[ihist]] :
					hMeas_SingleTop[ihist].Add( hist )
				for hist in [ hMeas_W2Jets[ihist], hMeas_W3Jets[ihist], hMeas_W4Jets[ihist] ] :
					hMeas_WJets[ihist].Add( hist )
	
			TTjets_nonSemilepTT_Names = [ "__qcd" , label ]
			for ihist in xrange(len(TTjets_nonSemilepTT_Names)):
				name = TTjets_nonSemilepTT_Names[ihist]
				hMeas_TTbar.append(hMeas_TT_Mtt_less_700[ihist].Clone())
				hMeas_TTbar[ihist].SetName(histname + '__TTbar' + name )
				for hist in [hMeas_TT_Mtt_700_1000[ihist], hMeas_TT_Mtt_1000_Inf[ihist]] :
					hMeas_TTbar[ihist].Add( hist )
				hMeas_TTbar_nonSemiLep.append(hMeas_TT_nonSemiLep_Mtt_less_700[ihist].Clone())
				hMeas_TTbar_nonSemiLep[ihist].SetName(histname + '__TTbar_nonSemiLep' +name )
				for hist in [hMeas_TT_nonSemiLep_Mtt_700_1000[ihist], hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist]] :
					hMeas_TTbar_nonSemiLep[ihist].Add( hist )
	else:
		Names = [ "__qcd" , label ]
		for ihist in xrange(len(Names)):
			name = Names[ihist]
			hMeas_WJets.append(hMeas_W1Jets[ihist].Clone())
			hMeas_WJets[ihist].SetName( histname + '__WJets' + name )
			hMeas_SingleTop.append(hMeas_T_t[ihist].Clone())
			hMeas_SingleTop[ihist].SetName(histname + '__SingleTop' + name )
			for hist in [hMeas_Tbar_t[ihist], hMeas_T_s[ihist], hMeas_Tbar_s[ihist], hMeas_T_tW[ihist], hMeas_Tbar_tW[ihist]]:
				hMeas_SingleTop[ihist].Add( hist )
			for hist in [ hMeas_W2Jets[ihist], hMeas_W3Jets[ihist], hMeas_W4Jets[ihist] ] :
				hMeas_WJets[ihist].Add( hist )
	
			hMeas_TTbar.append(hMeas_TT_Mtt_less_700[ihist].Clone())
			hMeas_TTbar[ihist].SetName(histname + '__TTbar' + name )
			for hist in [hMeas_TT_Mtt_700_1000[ihist], hMeas_TT_Mtt_1000_Inf[ihist]] :
				hMeas_TTbar[ihist].Add( hist )
			hMeas_TTbar_nonSemiLep.append(hMeas_TT_nonSemiLep_Mtt_less_700[ihist].Clone())
			hMeas_TTbar_nonSemiLep[ihist].SetName(histname + '__TTbar_nonSemiLep' +name )
			for hist in [hMeas_TT_nonSemiLep_Mtt_700_1000[ihist], hMeas_TT_nonSemiLep_Mtt_1000_Inf[ihist]] :
				hMeas_TTbar_nonSemiLep[ihist].Add( hist )
			

########## Make some easy-access lists ##########
if options.RunAllSyst :
	plots = [ "" , "nom" , "__jec__down" , "__jec__up" , "__jer__down" , "__jer__up" , "__toptag__down" , "__toptag__up" , "__btag__down" , "__btag__up" , "__pdf__down" , "__pdf__up" , "__scale__down" , "__scale__up" ]
if not options.RunAllSyst :
	if "nom" in options.systVariation and not "scale" in options.systVariation :
		plots = [ "" , "nom" ]
	else:
		plots = [ "" , label ]	
	
stacks = []
for i in xrange(len(plots)):
	hMeas_QCD.append(hMeas_QCD_SingleMu.Clone())

for thehist in hMeas_TTbar :
    thehist.SetFillColor( TColor.kRed+1 )

for thehist in hMeas_TTbar_nonSemiLep :
    thehist.SetFillColor( TColor.kRed-7 )

for thehist in hMeas_WJets :
    thehist.SetFillColor( TColor.kGreen-3 )

for thehist in hMeas_SingleTop :
    thehist.SetFillColor( TColor.kMagenta )

for thehist in hMeas_QCD :
    thehist.SetFillColor( TColor.kYellow )

if options.rebin != None and options.rebin != 1:

    for i in xrange(len(hMeas_TTbar)):
    	hMeas_TTbar[i].Rebin( options.rebin )
    
    for i in xrange(len(hMeas_TTbar_nonSemiLep)):
    	hMeas_TTbar_nonSemiLep[i].Rebin( options.rebin )
    
    for i in xrange(len(hMeas_SingleTop)):
	    hMeas_SingleTop[i].Rebin( options.rebin )

    for i in xrange(len(hMeas_WJets)):
	    hMeas_WJets[i].Rebin( options.rebin )
    
    for i in xrange(len(hMeas_QCD)):
    	hMeas_QCD[i].Rebin( options.rebin )  
    	
    hRecoData.Rebin( options.rebin )   
    
    if options.newYlabel is not 'None':
    	hRecoData.GetYaxis().SetTitle(options.newYlabel)
    
    
legs = []

summedhists = []
eventcounts = []


# plotting options
hRecoData.SetLineWidth(1)
hRecoData.SetMarkerStyle(8)


if 'csv1LepJet' in options.hist1 or 'csv2LepJet' in options.hist1 :
    hRecoData.SetAxisRange(0,1.05,"X")
if 'hadtop_mass3' in options.hist1 or 'hadtop_mass4' in options.hist1 :
    hRecoData.SetAxisRange(0,250,"X")
if 'hadtop_pt3' in options.hist1 or 'leptop_pt3' in options.hist1 :
    hRecoData.SetAxisRange(150,700,"X")
if 'hadtop_pt4' in options.hist1  or 'leptop_pt4' in options.hist1 :
    hRecoData.SetAxisRange(350,900,"X")
if 'hadtop_pt6' in options.hist1 or 'hadtop_pt7' in options.hist1  or 'leptop_pt6' in options.hist1 or 'leptop_pt7' in options.hist1 :
    hRecoData.SetAxisRange(350,1200,"X")
if 'hadtop_y' in options.hist1 :
    hRecoData.SetAxisRange(-3,3,"X")
if 'ht2' in options.hist1 or 'htLep2' in options.hist1:
    hRecoData.SetAxisRange(0,800,"X")
if 'ht3' in options.hist1 or 'htLep3' in options.hist1 :
    hRecoData.SetAxisRange(0,1400,"X")
if 'ht4' in options.hist1 or 'ht6' in options.hist1 or 'ht7' in options.hist1 :
    hRecoData.SetAxisRange(0,2500,"X")
if 'htLep4' in options.hist1 or 'htLep6' in options.hist1 or 'htLep7' in options.hist1 :
    hRecoData.SetAxisRange(0,2500,"X")
if 'pt1LepJet2' in options.hist1 :
    hRecoData.SetAxisRange(0,250,"X")
if 'ptLep0' in options.hist1 or 'ptLep2' in options.hist1 :
    hRecoData.SetAxisRange(0,200,"X")
if 'ptMET0' in options.hist1 or 'ptMET2' in options.hist1 :
    hRecoData.SetAxisRange(0,200,"X")


for m in range(1,len(plots)):

    if 'csv' in options.hist1 :
        leg = TLegend(0.59,0.56,0.84,0.9)
    else :
        leg = TLegend(0.67,0.56,0.92,0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.05)

    
    leg.AddEntry( hRecoData, 'Data', 'pel')
    leg.AddEntry( hMeas_TTbar[m], 't#bar{t} Signal', 'f')
    leg.AddEntry( hMeas_TTbar_nonSemiLep[m], 't#bar{t} Other', 'f')
    leg.AddEntry( hMeas_SingleTop[m], 'Single Top', 'f')
    leg.AddEntry( hMeas_WJets[m], 'W #rightarrow #mu#nu', 'f')
    leg.AddEntry( hMeas_QCD[m], 'QCD' , 'f')

    
    
    # Make a stack plot of the MC to compare to data
    hMC_stack = THStack("hMC_stack_" + str(m),
                        hMeas_TTbar[m].GetTitle() + ';' +
                        hMeas_TTbar[m].GetXaxis().GetTitle() + ';' +
                        hMeas_TTbar[m].GetYaxis().GetTitle()
                        )
    
    hMC_stack.Add( hMeas_QCD[m] )
    hMC_stack.Add( hMeas_WJets[m] )
    hMC_stack.Add( hMeas_SingleTop[m] )
    hMC_stack.Add( hMeas_TTbar_nonSemiLep[m] )
    hMC_stack.Add( hMeas_TTbar[m] )
	
    summedhist = hMeas_TTbar[m].Clone()
    summedhist.SetName( 'summed_' + plots[m] )
    summedhist.Add( hMeas_TTbar_nonSemiLep[m] )
    summedhist.Add( hMeas_WJets[m] )
    summedhist.Add( hMeas_SingleTop[m] )
    summedhist.Add( hMeas_QCD[m] )
    summedhist.Sumw2()

    ratiohist = hRecoData.Clone()
    ratiohist.SetName( 'ratio_' + plots[m] )
    ratiohist.Sumw2()
    ratiohist.Divide( summedhist )

    summedhists.append( [ratiohist,summedhist] )
    

    # automatically set y-range
    max = summedhist.GetMaximum();
    if not options.ignoreData and (hRecoData.GetMaximum() + hRecoData.GetBinError(hRecoData.GetMaximumBin())) > max :
        max = (hRecoData.GetMaximum() + hRecoData.GetBinError(hRecoData.GetMaximumBin()))
    if "eta" in options.hist1 or "_y" in options.hist1 :
        max = max*1.5

    hRecoData.SetAxisRange(0,max*1.05,"Y");

  
    c = TCanvas("datamc" + plots[m] , "datamc" + plots[m],200,10,900,800)
    p1 = TPad("datamcp1" + plots[m] , "datamc" + plots[m],0.0,0.3,1.0,0.97)
    p1.SetTopMargin(0.05)
    p1.SetBottomMargin(0.05)
    p1.SetNumber(1)
    p2 = TPad("datamcp2" + plots[m] , "datamc" + plots[m],0.0,0.00,1.0,0.3)
    p2.SetNumber(2)
    p2.SetTopMargin(0.05)
    #p2.SetBottomMargin(0.50)
    p2.SetBottomMargin(0.40)


    c.cd()
    p1.Draw()
    p1.cd()


    if not options.ignoreData :
        hRecoData.UseCurrentStyle()
        hRecoData.GetXaxis().SetTitle('')        
        hRecoData.GetXaxis().SetLabelSize(24);
        hRecoData.GetYaxis().SetLabelSize(24);
        hRecoData.Draw('lep')
        hMC_stack.Draw("hist same")
        hRecoData.Draw('lep same')
        hRecoData.Draw('lep same axis')
    else :
        hMC_stack.UseCurrentStyle()
        hMC_stack.Draw("hist")
        hMC_stack.GetXaxis().SetTitle('')
    if options.drawLegend :
        leg.Draw()
        
        l = TLatex()
        l.SetTextSize(0.05) 
        l.SetTextFont(42) 
        l.SetNDC()
        l.SetTextColor(1)
        if 'csv' in options.hist1 :
            l.DrawLatex(0.40,0.81,"#intLdt = 19.7 fb^{-1}")
            l.DrawLatex(0.40,0.72,"#sqrt{s} = 8 TeV")
        else :
            l.DrawLatex(0.48,0.81,"#intLdt = 19.7 fb^{-1}")
            l.DrawLatex(0.48,0.72,"#sqrt{s} = 8 TeV")
        


    eventcounts.append( [plots[m], hMeas_TTbar[m].GetSum(), hMeas_TTbar_nonSemiLep[m].GetSum(), hMeas_WJets[m].GetSum(), hMeas_SingleTop[m].GetSum(), hMeas_QCD[m].GetSum(), hRecoData.GetSum() ] )


    c.cd()
    p2.Draw()
    p2.cd()
    p2.SetGridy()
    ratiohist.UseCurrentStyle()
    ratiohist.Draw('lep')
    ratiohist.SetMaximum(2.0)
    ratiohist.SetMinimum(0.0)
    ratiohist.GetYaxis().SetNdivisions(2,4,0,False)
    ratiohist.GetYaxis().SetTitle( 'Data/MC' )
    ratiohist.GetXaxis().SetTitle( hMeas_TTbar[m].GetXaxis().GetTitle() )
    #ratiohist.GetXaxis().SetTitleOffset( 3.0 )
    ratiohist.GetXaxis().SetTitleOffset( 4.0 )
    ratiohist.GetXaxis().SetLabelSize(24);
    ratiohist.GetYaxis().SetLabelSize(24);

    
    canvs.append( [c, p1, p2] )
    legs.append(leg)
    if options.hist2 is None:
    	if not options.ignoreData : 
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist1 + '.png' )
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist1 + '.pdf' )
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist1 + '.eps' )
    	else : 
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist1 + '_nodata.png' )
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist1 + '_nodata.pdf' )

    elif options.hist2 is not None:
    	if not options.ignoreData : 
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist2 + '_subtracted_from_' + options.hist1 + '.png' )
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist2 + '_subtracted_from_' + options.hist1 + '.pdf' )
    	else : 
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist2 + '_subtracted_from_' + options.hist1 + '_nodata.png' )
        	c.Print( 'normalized_' + plots[m] + '_' + options.outname + '_' + options.hist2 + '_subtracted_from_' + options.hist1 + '_nodata.pdf' )


# Print event counts

if options.hist2 is None : 
    print '------------ Cut Flow Stage ' + options.hist1 + ' -----------------'
else :
    print '------------ Cut Flow Stage ' + options.hist1 + ' minus Stage ' + options.hist2 + ' -----------------'
print '{0:21s} '.format( 'Variation' ),
for name in ['TTbar', 'TTbar_nonSemiLep', 'WJets', 'S.T.', 'QCD', 'Data'] :
    print '{0:8s} '.format(name),
print ''
for count in eventcounts :
    print '{0:20s} '.format( count[0] ),    
    for val in count[1:] :
        print '{0:8.5f} '.format( val ),
    print ''
              
# write the histogram in a rootfile

if options.RunAllSyst :

##  For Single Top and W+jets we have : 0->qcd , 1->nom , 2->jecdown , 3->jecup , 4->jerdown , 5->jerup , 6->toptagdown , 7->toptagup , 8->btagdown , 9->btagup
## For TTbar and TTnonSemilep we have : 0->qcd , 1->nom , 2->jecdown , 3->jecup , 4->jerdown , 5->jerup , 6->toptagdown , 7->toptagup , 8->btagdown , 9->btagup , 10->pdfdown , 11->pdfup , 12->scaledown , 13->scaleup 

	histsAll = [hRecoData            , hMeas_QCD[1] ,
				hMeas_TTbar[1]       , hMeas_TTbar[2]     , 
				hMeas_TTbar[3]       , hMeas_TTbar[4]     , 
				hMeas_TTbar[5]       , hMeas_TTbar[6]     ,
				hMeas_TTbar[7]       , hMeas_TTbar[8]     , 
				hMeas_TTbar[9]       , hMeas_TTbar[10]    ,
				hMeas_TTbar[11]      , hMeas_TTbar[12]    ,
				hMeas_TTbar[13]      ,
				hMeas_TTbar_nonSemiLep[1]      , hMeas_TTbar_nonSemiLep[2]  , 
				hMeas_TTbar_nonSemiLep[3]      , hMeas_TTbar_nonSemiLep[4]  , 
				hMeas_TTbar_nonSemiLep[5]      , hMeas_TTbar_nonSemiLep[6]  , 
				hMeas_TTbar_nonSemiLep[7]      , hMeas_TTbar_nonSemiLep[8]  , 
				hMeas_TTbar_nonSemiLep[9]      , hMeas_TTbar_nonSemiLep[10] ,
				hMeas_TTbar_nonSemiLep[11]     , hMeas_TTbar_nonSemiLep[12] ,
				hMeas_TTbar_nonSemiLep[13]     ,
				hMeas_SingleTop[1]   , hMeas_SingleTop[2] , 
				hMeas_SingleTop[3]   , hMeas_SingleTop[4] , 
				hMeas_SingleTop[5]   , hMeas_SingleTop[6] ,
				hMeas_SingleTop[7]   , hMeas_SingleTop[8] , 
				hMeas_SingleTop[9]   ,
				hMeas_WJets[1]     , hMeas_WJets[2]  , 
				hMeas_WJets[3]     , hMeas_WJets[4]  , 
				hMeas_WJets[5]     , hMeas_WJets[6]  , 
				hMeas_WJets[7]     , hMeas_WJets[8]  , 
				hMeas_WJets[9]
				]

if not options.RunAllSyst :

## if "pdfdn" in options.systVariation or "pdfup" in options.systVariation or "scaledown_nom" in options.systVariation or "scaleup_nom" in options.systVariation :			
##  For Single Top and W+jets we have : 0->qcd , 1->nom
## For TTbar and TTnonSemilep we have : 0->qcd , 1->pdfdown or pdfup or scaledown or scaleup
## else:
##  For Single Top and W+jets we have : 0->qcd , 1->chosen systematic
## For TTbar and TTnonSemilep we have : 0->qcd , 1->chosen systematic
	histsAll = [hRecoData                 , hMeas_QCD[1] ,
				hMeas_TTbar[1]            ,
				hMeas_TTbar_nonSemiLep[1] , 
				hMeas_SingleTop[1]        ,
				hMeas_WJets[1]     
				]


fout.cd()
for ihist in xrange(len(histsAll)) :
    hist = histsAll[ihist]
    if hist is not None :
        hist.Write()

fout.Close()
