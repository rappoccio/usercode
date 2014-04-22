
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


parser.add_option('--hist1', metavar='F', type='string', action='store',
                  default='mttbarGen',
                  dest='hist1',
                  help='Histogram2 is subtracted from histogram1')                  

parser.add_option('--maxy', metavar='F', type='float', action='store',
                  default=500,
                  dest='maxy',
                  help='Maximum y in histogram')


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

Nmc_ttbar_scaledown = 14998606
Nmc_ttbar_scaleup   = 14998720
Nmc_TT_Mtt_700_1000_scaledown = 2170074
Nmc_TT_Mtt_700_1000_scaleup = 2243672
Nmc_TT_Mtt_1000_Inf_scaledown = 1308090
Nmc_TT_Mtt_1000_Inf_scaleup = 1241650

# ttbar filter efficiencies
#                    nom      scaledown scaleup
e_TT_Mtt_700_1000 = [0.074,   0.078,    0.069]
e_TT_Mtt_1000_Inf = [0.014,   0.016,    0.013]
e_TT_Mtt_0_700 =    [1.0  ,   1.0,      1.0  ] #   No efficiency here, we applied the cut at gen level


# 
names = [ 'DATA', 'TTbar', 'WJets', 'SingleTop', 'QCD_SingleMu' ]
plots = [ 'jec__down' , 'jec__up' , 'jer__down' , 'jer__up' , 'pdf__down' , 'pdf__up' , 'nom' , 'scale__down' , 'scale__up']
canvs = []
histsData = []
hists = []
hMeas_TT_Mtt_less_700 = []
hMeas_TT_Mtt_700_1000 = []
hMeas_TT_Mtt_1000_Inf = []
hMeas_T_t = []
hMeas_Tbar_t = []
hMeas_T_s = []
hMeas_Tbar_s = []
hMeas_T_tW = []
hMeas_Tbar_tW = []
hMeas_WJets = []
hMeas_qcd = []
hMeas_TT_Mtt = []
hMeas_SingleTop = []
# ttbar 
fTT_Mtt_less_700_nom       = TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
fTT_Mtt_less_700_scaledown = TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown_nom.root")
fTT_Mtt_less_700_scaleup   = TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup_nom.root")

fTT_Mtt_700_1000_nom       = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
fTT_Mtt_700_1000_scaledown = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown_nom.root")
fTT_Mtt_700_1000_scaleup   = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup_nom.root")

fTT_Mtt_1000_Inf_nom       = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
fTT_Mtt_1000_Inf_scaledown = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaledown_nom.root")
fTT_Mtt_1000_Inf_scaleup   = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_scaleup_nom.root")




print "==================================== Get Hists ====================================="



histname = options.hist1
hMeas_TT_Mtt_less_700_nom       = fTT_Mtt_less_700_nom.Get(options.hist1).Clone()
hMeas_TT_Mtt_less_700_scaledown = fTT_Mtt_less_700_scaledown.Get(options.hist1).Clone()
hMeas_TT_Mtt_less_700_scaleup   = fTT_Mtt_less_700_scaleup.Get(options.hist1).Clone()


hMeas_TT_Mtt_700_1000_nom       = fTT_Mtt_700_1000_nom.Get(options.hist1).Clone() 
hMeas_TT_Mtt_700_1000_scaledown = fTT_Mtt_700_1000_scaledown.Get(options.hist1).Clone()
hMeas_TT_Mtt_700_1000_scaleup   = fTT_Mtt_700_1000_scaleup.Get(options.hist1).Clone()


hMeas_TT_Mtt_1000_Inf_nom       = fTT_Mtt_1000_Inf_nom.Get(options.hist1).Clone()
hMeas_TT_Mtt_1000_Inf_scaledown = fTT_Mtt_1000_Inf_scaledown.Get(options.hist1).Clone()
hMeas_TT_Mtt_1000_Inf_scaleup   = fTT_Mtt_1000_Inf_scaleup.Get(options.hist1).Clone()

hMeas_TT_Mtt_less_700_nom       .SetName( options.hist1 + '__TTbar_Mtt_less_700' )
hMeas_TT_Mtt_less_700_scaledown .SetName( options.hist1 + '__TTbar_Mtt_less_700__scale__down')
hMeas_TT_Mtt_less_700_scaleup   .SetName( options.hist1 + '__TTbar_Mtt_less_700__scale__up')

hMeas_TT_Mtt_700_1000_nom       .SetName( options.hist1 + '__TTbar_Mtt_700_1000' )
hMeas_TT_Mtt_700_1000_scaledown .SetName( options.hist1 + '__TTbar_Mtt_700_1000__scale__down')
hMeas_TT_Mtt_700_1000_scaleup   .SetName( options.hist1 + '__TTbar_Mtt_700_1000__scale__up')

hMeas_TT_Mtt_1000_Inf_nom       .SetName( options.hist1 + '__TTbar_Mtt_1000' )
hMeas_TT_Mtt_1000_Inf_scaledown .SetName( options.hist1 + '__TTbar_Mtt_1000_Inf__scale__down')
hMeas_TT_Mtt_1000_Inf_scaleup   .SetName( options.hist1 + '__TTbar_Mtt_1000_Inf__scale__up')

hMeas_TT_Mtt_less_700_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700[0] * lum / float(Nmc_ttbar) * SF_t)
hMeas_TT_Mtt_less_700_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700[1] * lum / float(Nmc_ttbar_scaledown) * SF_t)
hMeas_TT_Mtt_less_700_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700[2] * lum / float(Nmc_ttbar_scaleup) * SF_t)

hMeas_TT_Mtt_700_1000_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000[0] * lum / float(Nmc_TT_Mtt_700_1000) * SF_t)
hMeas_TT_Mtt_700_1000_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000[1] * lum / float(Nmc_TT_Mtt_700_1000_scaledown) * SF_t)
hMeas_TT_Mtt_700_1000_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000[2] * lum / float(Nmc_TT_Mtt_700_1000_scaleup) * SF_t)

hMeas_TT_Mtt_1000_Inf_nom      .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf[0] * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_t )
hMeas_TT_Mtt_1000_Inf_scaledown.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf[1] * lum / float(Nmc_TT_Mtt_1000_Inf_scaledown) * SF_t )
hMeas_TT_Mtt_1000_Inf_scaleup  .Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf[2] * lum / float(Nmc_TT_Mtt_1000_Inf_scaleup) * SF_t )




######### Combine ttbar samples #############
ttbar_canv = TCanvas( "ttbar", "ttbar", 1500, 450 )
ttbar_canv.Divide(3,1)
ttbar_canv.cd(1)
ttbar_nom_stack = THStack("ttbar_nom", "ttbar_nom")
hMeas_TT_Mtt_less_700_nom .SetLineColor( 2 )
hMeas_TT_Mtt_700_1000_nom .SetLineColor( 3 )
hMeas_TT_Mtt_1000_Inf_nom .SetLineColor( 4 )
ttbar_nom_stack.Add( hMeas_TT_Mtt_less_700_nom )
ttbar_nom_stack.Add( hMeas_TT_Mtt_700_1000_nom )
ttbar_nom_stack.Add( hMeas_TT_Mtt_1000_Inf_nom )
ttbar_nom_stack.Draw("nostack hist")


ttbar_canv.cd(2)
ttbar_scaleup_stack = THStack("ttbar_scaleup", "ttbar_scaleup")
hMeas_TT_Mtt_less_700_scaleup .SetLineColor( 2 )
hMeas_TT_Mtt_700_1000_scaleup .SetLineColor( 3 )
hMeas_TT_Mtt_1000_Inf_scaleup .SetLineColor( 4 )
ttbar_scaleup_stack.Add( hMeas_TT_Mtt_less_700_scaleup )
ttbar_scaleup_stack.Add( hMeas_TT_Mtt_700_1000_scaleup )
ttbar_scaleup_stack.Add( hMeas_TT_Mtt_1000_Inf_scaleup )
ttbar_scaleup_stack.Draw("nostack hist")


ttbar_canv.cd(3)
ttbar_scaledown_stack = THStack("ttbar_scaledown", "ttbar_scaledown")
hMeas_TT_Mtt_less_700_scaledown .SetLineColor( 2 )
hMeas_TT_Mtt_700_1000_scaledown .SetLineColor( 3 )
hMeas_TT_Mtt_1000_Inf_scaledown .SetLineColor( 4 )
ttbar_scaledown_stack.Add( hMeas_TT_Mtt_less_700_scaledown )
ttbar_scaledown_stack.Add( hMeas_TT_Mtt_700_1000_scaledown )
ttbar_scaledown_stack.Add( hMeas_TT_Mtt_1000_Inf_scaledown )
ttbar_scaledown_stack.Draw("nostack hist")


ttbar_canv.Print("q2woes.pdf", "pdf")
ttbar_canv.Print("q2woes.png", "png")
