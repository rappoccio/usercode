#!/usr/bin/env python
# ==============================================================================
#  File and Version Information:
#       $Id: RooUnfoldExample.py 302 2011-09-30 20:39:20Z T.J.Adye $
#
#  Description:
#       Simple example usage of the RooUnfold package using toy MC.
#
#  Author: Tim Adye <T.J.Adye@rl.ac.uk>
#
# ==============================================================================

import time
from optparse import OptionParser


parser = OptionParser()

  

parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='',
                  dest='outname',
                  help='Output name for png and pdf files')


(options, args) = parser.parse_args()

argv = []

from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor

gROOT.Macro("rootlogon.C")


gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
#gStyle.SetTitleFontSize(0.05)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(3.5, "X")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")


#gSystem.Load("RooUnfold-1.1.1/libRooUnfold.so")

#from ROOT import RooUnfoldResponse
#from ROOT import RooUnfold
#from ROOT import RooUnfoldBayes
#from ROOT import RooUnfoldSvd
# from ROOT import RooUnfoldTUnfold

# Constants

# Performance numbers
lum = 19.7 # fb-1
SF_b = 0.97
SF_t = 0.94

# Cross sections (in fb) and the number of MC events
sigma_ttbar_NNLO = 245.8 * 1000. # fb, from http://arxiv.org/pdf/1303.6254.pdf
sigma_T_t_NNLO = 56.4 * 1000.
sigma_Tbar_t_NNLO = 30.7 * 1000.
sigma_T_s_NNLO = 3.79 * 1000.
sigma_Tbar_s_NNLO = 1.76 * 1000.
sigma_T_tW_NNLO = 11.1 * 1000.
sigma_Tbar_tW_NNLO = 11.1 * 1000.
sigma_WJets_NNLO = 37509 * 1000.

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

names = [ 'Data', 'TTbar', 'WJets', 'SingleTop', 'QCD' ]
plots = [ 'TT_Mtt_jecdown' , 'TT_Mtt_jecup' , 'TT_Mtt_jerdown' , 'TT_Mtt_jerup' , 'TT_Mtt_pdfdown' , 'TT_Mtt_pdfup' ]
canvs = []
histsData = []

# Open the output file 

fout_0 = TFile("normalized_TT_Mtt_jecdn_entirephase.root" , "RECREATE")
fout_1 = TFile("normalized_TT_Mtt_jecup_entirephase.root" , "RECREATE")
fout_2 = TFile("normalized_TT_Mtt_jerdn_entirephase.root" , "RECREATE")
fout_3 = TFile("normalized_TT_Mtt_jerup_entirephase.root" , "RECREATE")
fout_4 = TFile("normalized_TT_Mtt_pdfdn_entirephase.root" , "RECREATE")
fout_5 = TFile("normalized_TT_Mtt_pdfup_entirephase.root" , "RECREATE")
fout = [ fout_0 , fout_1 , fout_2 , fout_3 , fout_4 , fout_5  ]

# ==============================================================================
#  Example Unfolding
# ==============================================================================

fdata = TFile("histfiles/TTSemilepAnalyzer_unfolding_data_type1.root")
fQCD = TFile("histfiles/QCD_hists_pt_type1.root")
fmc_ttbar = TFile("histfiles/TTSemilepAnalyzer_antibtag_w_mucut_type1.root")
fT_t = TFile("histfiles/T_t-channel_Histos_type1.root")
fTbar_t = TFile("histfiles/Tbar_t-channel_Histos_type1.root")
fT_s = TFile("histfiles/T_s-channel_Histos_type1.root")
fTbar_s = TFile("histfiles/Tbar_s-channel_Histos_type1.root")
fT_tW = TFile("histfiles/T_tW-channel_Histos_type1.root")
fTbar_tW = TFile("histfiles/Tbar_tW-channel_Histos_type1.root")
fWJets = TFile("histfiles/WJetsToLNu_Histos_type1.root")
fTT_Mtt_less_700_jecdown = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_less_700_jecup = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_less_700_jerdown = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
fTT_Mtt_less_700_jerup = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_less_700_pdfdown = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_less_700_pdfup = TFile("histfiles/TT_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")
#fTT_Mtt_700_1000 = TFile("histfiles/TT_Mtt-700to1000-channel_Histos_type1.root")
fTT_Mtt_700_1000_jecdown = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_700_1000_jecup = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_700_1000_jerdown = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
#fTT_Mtt_700_1000_jernom = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jernom_type1.root")
fTT_Mtt_700_1000_jerup = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_700_1000_pdfdown = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_700_1000_pdfup = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")
#fTT_Mtt_1000_Inf = TFile("histfiles/TT_Mtt-1000toInf-channel_Histos_type1.root")
fTT_Mtt_1000_Inf_jecdown = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecdn_type1.root")
fTT_Mtt_1000_Inf_jecup = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jecup_type1.root")
fTT_Mtt_1000_Inf_jerdown = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerdn_type1.root")
#fTT_Mtt_1000_Inf_jernom = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jernom_type1.root")
fTT_Mtt_1000_Inf_jerup = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_jerup_type1.root")
fTT_Mtt_1000_Inf_pdfdown = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfdn_type1.root")
fTT_Mtt_1000_Inf_pdfup = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_pdfup_type1.root")



response= fmc_ttbar.Get("response_pt")


print "==================================== Get Hists ====================================="
#hTrue= fmc_ttbar.Get("ptGenTop")
#hRecoMC = fmc_ttbar.Get("ptRecoTop").Clone()
#hRecoMC.SetName("hRecoMC")
hRecoData= fdata.Get("ptRecoTop").Clone()
hRecoData.SetName("hRecoData")

hRecoQCD = fQCD.Get("ptTopTagHist")
hRecoQCD.Sumw2()
hRecoQCD.Scale( NQCD / hRecoQCD.Integral() )
hRecoQCD.SetFillColor(TColor.kYellow)
hRecoQCD.Rebin(2)

    
hMeas= fdata.Get("ptRecoTop")





# Get the histogram files
hMeas_T_t     = fT_t.Get("ptRecoTop").Clone()
hMeas_Tbar_t  = fTbar_t.Get("ptRecoTop").Clone()
hMeas_T_s     = fT_s.Get("ptRecoTop").Clone()
hMeas_Tbar_s  = fTbar_s.Get("ptRecoTop").Clone()
hMeas_T_tW    = fT_tW.Get("ptRecoTop").Clone()
hMeas_Tbar_tW = fTbar_tW.Get("ptRecoTop").Clone()
hMeas_WJets   = fWJets.Get("ptRecoTop").Clone()
#hMeas_TT_Mtt_700_1000 = fTT_Mtt_700_1000.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_less_700_jecdown = fTT_Mtt_less_700_jecdown.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_less_700_jecup = fTT_Mtt_less_700_jecup.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_less_700_jerdown = fTT_Mtt_less_700_jerdown.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_less_700_jerup = fTT_Mtt_less_700_jerup.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_less_700_pdfdown = fTT_Mtt_less_700_pdfdown.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_less_700_pdfup = fTT_Mtt_less_700_pdfup.Get("ptRecoTop").Clone()

hMeas_TT_Mtt_700_1000_jecdown = fTT_Mtt_700_1000_jecdown.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_700_1000_jecup = fTT_Mtt_700_1000_jecup.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_700_1000_jerdown = fTT_Mtt_700_1000_jerdown.Get("ptRecoTop").Clone()
#hMeas_TT_Mtt_700_1000_jernom = fTT_Mtt_700_1000_jernom.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_700_1000_jerup = fTT_Mtt_700_1000_jerup.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_700_1000_pdfdown = fTT_Mtt_700_1000_pdfdown.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_700_1000_pdfup = fTT_Mtt_700_1000_pdfup.Get("ptRecoTop").Clone()
#hMeas_TT_Mtt_1000_Inf = fTT_Mtt_1000_Inf.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_1000_Inf_jecdown = fTT_Mtt_1000_Inf_jecdown.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_1000_Inf_jecup = fTT_Mtt_1000_Inf_jecup.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_1000_Inf_jerdown = fTT_Mtt_1000_Inf_jerdown.Get("ptRecoTop").Clone()
#hMeas_TT_Mtt_1000_Inf_jernom = fTT_Mtt_1000_Inf_jernom.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_1000_Inf_jerup = fTT_Mtt_1000_Inf_jerup.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_1000_Inf_pdfdown = fTT_Mtt_1000_Inf_pdfdown.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_1000_Inf_pdfup = fTT_Mtt_1000_Inf_pdfup.Get("ptRecoTop").Clone()



hMeas_T_t     .SetName( 'hMeas_T_t')
hMeas_Tbar_t  .SetName( 'hMeas_Tbar_t')
hMeas_T_s     .SetName( 'hMeas_T_s')
hMeas_Tbar_s  .SetName( 'hMeas_Tbar_s')
hMeas_T_tW    .SetName( 'hMeas_T_tW')
hMeas_Tbar_tW .SetName( 'hMeas_Tbar_tW')
hMeas_WJets   .SetName( 'hMeas_WJets')
#hMeas_TT_Mtt_700_1000 .SetName( )fTT_Mtt_700_1000.Get("ptRecoTop").Clone()
hMeas_TT_Mtt_less_700_jecdown .SetName( 'hMeas_TT_Mtt_less_700_jecdown')
hMeas_TT_Mtt_less_700_jecup   .SetName( 'hMeas_TT_Mtt_less_700_jecup')
hMeas_TT_Mtt_less_700_jerdown .SetName( 'hMeas_TT_Mtt_less_700_jerdown')
hMeas_TT_Mtt_less_700_jerup   .SetName( 'hMeas_TT_Mtt_less_700_jerup')
hMeas_TT_Mtt_less_700_pdfdown .SetName( 'hMeas_TT_Mtt_less_700_pdfdown')
hMeas_TT_Mtt_less_700_pdfup   .SetName( 'hMeas_TT_Mtt_less_700_pdfup')
                                                                      
hMeas_TT_Mtt_700_1000_jecdown .SetName( 'hMeas_TT_Mtt_700_1000_jecdown')
hMeas_TT_Mtt_700_1000_jecup   .SetName( 'hMeas_TT_Mtt_700_1000_jecup')
hMeas_TT_Mtt_700_1000_jerdown .SetName( 'hMeas_TT_Mtt_700_1000_jerdown')
hMeas_TT_Mtt_700_1000_jerup   .SetName( 'hMeas_TT_Mtt_700_1000_jerup')
hMeas_TT_Mtt_700_1000_pdfdown .SetName( 'hMeas_TT_Mtt_700_1000_pdfdown')
hMeas_TT_Mtt_700_1000_pdfup   .SetName( 'hMeas_TT_Mtt_700_1000_pdfup')
hMeas_TT_Mtt_1000_Inf_jecdown .SetName( 'hMeas_TT_Mtt_1000_Inf_jecdown')
hMeas_TT_Mtt_1000_Inf_jecup   .SetName( 'hMeas_TT_Mtt_1000_Inf_jecup')
hMeas_TT_Mtt_1000_Inf_jerdown .SetName( 'hMeas_TT_Mtt_1000_Inf_jerdown')
hMeas_TT_Mtt_1000_Inf_jerup   .SetName( 'hMeas_TT_Mtt_1000_Inf_jerup')
hMeas_TT_Mtt_1000_Inf_pdfdown .SetName( 'hMeas_TT_Mtt_1000_Inf_pdfdown')
hMeas_TT_Mtt_1000_Inf_pdfup   .SetName( 'hMeas_TT_Mtt_1000_Inf_pdfup')




# Scale to desired normalization
# Options are :
#  1. From MC
#  2. From fit
#
# For now, we don't have the fit, so we do from MC



hMeas_T_t.Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_b * SF_t  )
hMeas_Tbar_t.Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_b * SF_t  )
hMeas_T_s.Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_b * SF_t  )
hMeas_Tbar_s.Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_b * SF_t  )
hMeas_T_tW.Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_b * SF_t  )
hMeas_Tbar_tW.Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_b * SF_t  )
hMeas_WJets.Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_b * SF_t  )
hMeas_TT_Mtt_less_700_jecdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jecup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jerdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_jerup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_pdfdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
hMeas_TT_Mtt_less_700_pdfup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_b * SF_t)
#hMeas_TT_Mtt_700_1000.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jecdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jecup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jerdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
#hMeas_TT_Mtt_700_1000_jernom.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_jerup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_pdfdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
hMeas_TT_Mtt_700_1000_pdfup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_b * SF_t)
#hMeas_TT_Mtt_1000_Inf.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jecdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jecup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jerdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
#hMeas_TT_Mtt_1000_Inf_jernom.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_jerup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_pdfdown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )
hMeas_TT_Mtt_1000_Inf_pdfup.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_b * SF_t )

hists = []

#m = input(" Choose the distribution: 0) TT_Mtt_jecdown  1) TT_Mtt_jecup  2) TT_Mtt_jerdown  3) TT_Mtt_jerup  4) TT_Mtt_pdfdown  5) TT_Mtt_pdfup : #")
for m in xrange(6):

    if m == 0:
        hMeas_TT_Mtt = hMeas_TT_Mtt_less_700_jecdown.Clone()
        hMeas_TT_Mtt.SetFillColor( TColor.kRed )
        for hist in [ hMeas_TT_Mtt_700_1000_jecdown , hMeas_TT_Mtt_1000_Inf_jecdown ] :
            print 'Adding mtt for jecdown'
            hMeas_TT_Mtt.Add( hist )
        hists.append( hMeas_TT_Mtt )

    elif m == 1:
        hMeas_TT_Mtt = hMeas_TT_Mtt_less_700_jecup.Clone()
        hMeas_TT_Mtt.SetFillColor( TColor.kRed )
        for hist in [ hMeas_TT_Mtt_700_1000_jecup , hMeas_TT_Mtt_1000_Inf_jecup ] :
            print 'Adding mtt for jecup'
            hMeas_TT_Mtt.Add( hist )
        hists.append( hMeas_TT_Mtt )

    elif m == 2:
        hMeas_TT_Mtt = hMeas_TT_Mtt_less_700_jerdown.Clone()
        hMeas_TT_Mtt.SetFillColor( TColor.kRed )
        for hist in [ hMeas_TT_Mtt_700_1000_jerdown , hMeas_TT_Mtt_1000_Inf_jerdown ] :
            print 'Adding mtt for jerdown'            
            hMeas_TT_Mtt.Add( hist )
        hists.append( hMeas_TT_Mtt )

    elif m == 3:
        hMeas_TT_Mtt = hMeas_TT_Mtt_less_700_jerup.Clone()
        hMeas_TT_Mtt.SetFillColor( TColor.kRed )
        for hist in [ hMeas_TT_Mtt_700_1000_jerup , hMeas_TT_Mtt_1000_Inf_jerup ] :
            print 'Adding mtt for jerup'
            hMeas_TT_Mtt.Add( hist )
        hists.append( hMeas_TT_Mtt )

    elif m == 4:
        hMeas_TT_Mtt = hMeas_TT_Mtt_less_700_pdfdown.Clone()
        hMeas_TT_Mtt.SetFillColor( TColor.kRed )
        for hist in [ hMeas_TT_Mtt_700_1000_pdfdown , hMeas_TT_Mtt_1000_Inf_pdfdown ] :
            print 'Adding mtt for pdfdown'            
            hMeas_TT_Mtt.Add( hist )
        hists.append( hMeas_TT_Mtt )

    else:
        hMeas_TT_Mtt = hMeas_TT_Mtt_less_700_pdfup.Clone()
        hMeas_TT_Mtt.SetFillColor( TColor.kRed )
        for hist in [ hMeas_TT_Mtt_700_1000_pdfup , hMeas_TT_Mtt_1000_Inf_pdfup ] :
            print 'Adding mtt for pdfup'
            hMeas_TT_Mtt.Add( hist )
        hists.append( hMeas_TT_Mtt )
    
        
    hMeas_SingleTop = hMeas_T_t.Clone()

    hists.append( hMeas_SingleTop )

    hMeas_SingleTop.SetFillColor( TColor.kMagenta )
    hMeas_WJets.SetFillColor( TColor.kGreen )
    hMeas.SetFillColor( TColor.kRed )
    #hRecoMC.SetFillColor( 2 )

    for hist in [hMeas_Tbar_t, hMeas_T_s, hMeas_Tbar_s, hMeas_T_tW, hMeas_Tbar_tW] :
        print 'adding hist ' + hist.GetName()
        hMeas_SingleTop.Add( hist )

    
    # Make a stack plot of the MC to compare to data
    hMC_stack = THStack("hMC_stack", "hMC_stack")
    print 'Making stack'
    hMC_stack.Add( hMeas_WJets )
    hMC_stack.Add( hMeas_SingleTop )
    hMC_stack.Add( hMeas_TT_Mtt )
    # TO DO : NEED TO FIX THE BINNING FOR QCD : 
    #MC_stack.Add( hRecoQCD )
    #hMC_stack.Add( hRecoMC )

   
    c = TCanvas("datamc" + plots[m] , "datamc" + plots[m])
    hRecoData.Draw('e')
    hMC_stack.Draw("hist same")
    hRecoData.Draw('e same')
    hRecoData.SetMaximum( 500 )
    canvs.append(c)
    c.Print( plots[m] + options.outname + '.png' )
    c.Print( plots[m] + options.outname + '.pdf' )

    # write the histogram in a rootfile

    histsAll = [hRecoData, hMeas_TT_Mtt, hMeas_WJets, hMeas_SingleTop, hRecoQCD]
    fout[m].cd()
    for ihist in xrange(len(histsAll)) :
        hist = histsAll[ihist]
        hist.SetName('ptRecoTop_' + names[ihist] + plots [m] )
        hist.Write()
    fout[m].Close()
   
    
