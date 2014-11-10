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
                  help='Run Closure Test')

parser.add_option('--plotFullRange', metavar='F', action='store_true',
                  default=False,
                  dest='plotFullRange',
                  help='Plot the full pt range (pt > 300 GeV)')

parser.add_option('--subtractBackgrounds', metavar='F', action='store_true',
                  default=True,
                  dest='subtractBackgrounds',
                  help='Subtract off the backgrounds')


parser.add_option('--normalize', metavar='F', action='store_true',
                  default=False,
                  dest='normalize',
                  help='Normalize the cross section')

parser.add_option('--systVariation', metavar='F', type='string', action='store',
                  default='CT10_nom_2Dcut_nom',
                  dest='syst',
                  help='Run nominal or systematic variation?')

parser.add_option('--ttbarPDF', metavar='F', type='string', action='store',
                  default='CT10_nom',
                  dest='ttbarPDF',
                  help='Run nominal or systematic variation?')



# -------------------------------------------------------------------------------------
# load options & set plot style
# -------------------------------------------------------------------------------------

(options, args) = parser.parse_args()
argv = []

from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor

gROOT.Macro("rootlogon.C")


gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
#gStyle.SetTitleOffset(3.5, "X")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")

gStyle.SetPadTopMargin(0.07);
gStyle.SetPadRightMargin(0.05);
gStyle.SetPadBottomMargin(0.16);
gStyle.SetPadLeftMargin(0.18);
#gStyle.SetTitleXOffset(1.4);
#gStyle.SetTitleYOffset(1.0);

gStyle.SetOptTitle(0);
  

gSystem.Load("RooUnfold-1.1.1/libRooUnfold.so")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd
# from ROOT import RooUnfoldTUnfold


# -------------------------------------------------------------------------------------
# cross sections, efficiencies, total number of events
# -------------------------------------------------------------------------------------

# Performance numbers
lum = 19.7 #fb-1

# Cross sections (in fb) and the number of MC events
#sigma_ttbar_NNLO = [    # fb, from http://arxiv.org/pdf/1303.6254.pdf
#    245.8 * 1000., # nom
#    237.4 * 1000., # scaledown
#    252.0 * 1000., # scaleup
#    239.4 * 1000., # pdfdown
#    252.0 * 1000., # pdfup
#    ]
sigma_ttbar_NNLO = 245.8 * 1000.    # fb, from http://arxiv.org/pdf/1303.6254.pdf
sigma_T_t_NNLO = 56.4 * 1000.       # 
sigma_Tbar_t_NNLO = 30.7 * 1000.    # All single-top approx NNLO cross sections from
sigma_T_s_NNLO = 3.79 * 1000.       # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma8TeV
sigma_Tbar_s_NNLO = 1.76 * 1000.    # 
sigma_T_tW_NNLO = 11.1 * 1000.      # 
sigma_Tbar_tW_NNLO = 11.1 * 1000.   # 
sigma_WJets_NNLO = 36703.2 * 1000.  # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
sigma_WJets_1jet = 5400*1.207*1000. #
sigma_WJets_2jet = 1750*1.207*1000. #
sigma_WJets_3jet = 519 *1.207*1000. #
sigma_WJets_4jet = 214 *1.207*1000. #


## hack to account for that when doing closure test, the ttbar sample is split in two 
eff_closure = 1.0
if options.closureTest == True:
    eff_closure = 2.0


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
Nmc_WJets_1jet = 23141598
Nmc_WJets_2jet = 34044921
Nmc_WJets_3jet = 15539503
Nmc_WJets_4jet = 13382803
Nmc_TT_Mtt_700_1000 = 3082812
Nmc_TT_Mtt_1000_Inf = 1249111

Nmc_ttbar_scaledown = 14998606
Nmc_ttbar_scaleup   = 14998720
Nmc_TT_Mtt_700_1000_scaledown = 2170074
Nmc_TT_Mtt_700_1000_scaleup = 2243672
Nmc_TT_Mtt_1000_Inf_scaledown = 1308090
Nmc_TT_Mtt_1000_Inf_scaleup = 1241650


# NEW ttbar filter efficiencies
# These were determined "by eye" to make the generated mttbar spectrum smooth in the "makeMttGenPlots.py" script
#                    nom      scaledown scaleup
#e_TT_Mtt_700_1000 = [0.074,   0.081,    0.074]
#e_TT_Mtt_1000_Inf = [0.015,   0.016,    0.014]
#e_TT_Mtt_0_700 =    [1.0  ,   1.0,      1.0  ] #   No efficiency here, we applied the cut at gen level
e_TT_Mtt_700_1000 = 0.074
e_TT_Mtt_1000_Inf = 0.015
e_TT_Mtt_0_700 =    1.0    # No efficiency here, we applied the cut at gen level


# Scaling of the various backgrounds from the theta fit
fitted_qcd = 9.5
fitted_singletop = 3.9
fitted_wjets = 4.2
fitted_ttbarnonsemilep = 30.8
fitted_ttbar = 291.3


# -------------------------------------------------------------------------------------
#  read histogram files
# -------------------------------------------------------------------------------------

f_data = TFile("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_nom.root")
f_QCD  = TFile("histfiles/2Dhist/SingleMu_iheartNY_V1_mu_Run2012_2Dcut_qcd.root")

if options.closureTest == True : 
    f_ttbar_max700    = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+"_even.root")
    f_ttbar_700to1000 = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+"_even.root")
    f_ttbar_1000toInf = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+"_even.root")
    f_ttbar_max700_odd    = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+"_odd.root")
    f_ttbar_700to1000_odd = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+"_odd.root")
    f_ttbar_1000toInf_odd = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+"_odd.root")
else :
    f_ttbar_max700    = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+".root")
    f_ttbar_700to1000 = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+".root")
    f_ttbar_1000toInf = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+".root")

f_ttbar_nonsemilep_max700    = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_nonSemiLep_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+".root")
f_ttbar_nonsemilep_700to1000 = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_nonSemiLep_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+".root")
f_ttbar_nonsemilep_1000toInf = TFile("histfiles_" + options.ttbarPDF + "/2Dhists/TT_nonSemiLep_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_"+options.syst+".root")

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
    response_ttbar_max700    = f_ttbar_max700_odd.Get("response_pt")
    response_ttbar_700to1000 = f_ttbar_700to1000_odd.Get("response_pt")
    response_ttbar_1000toInf = f_ttbar_1000toInf_odd.Get("response_pt")
else :
    response_ttbar_max700    = f_ttbar_max700.Get("response_pt")
    response_ttbar_700to1000 = f_ttbar_700to1000.Get("response_pt")
    response_ttbar_1000toInf = f_ttbar_1000toInf.Get("response_pt")

response = response_ttbar_max700.Clone()
response.SetName("response_pt_"+options.syst)
response.Add(response_ttbar_700to1000)
response.Add(response_ttbar_1000toInf)


TH1.AddDirectory(0)

# -------------------------------------------------------------------------------------
# output file for storing histograms to  
# -------------------------------------------------------------------------------------

fout = TFile("UnfoldingPlots/unfold_"+options.syst+".root","recreate");


# -------------------------------------------------------------------------------------
# plot response matrices 
# -------------------------------------------------------------------------------------

gStyle.SetPadRightMargin(0.12);
cr = TCanvas("c_response", "", 800, 600)

hEmpty2D = response.Hresponse().Clone()
hEmpty2D.SetName("empty2D")
hEmpty2D.Reset()
hEmpty2D.GetXaxis().SetTitle("Measured top-jet p_{T} [GeV]")
hEmpty2D.GetYaxis().SetTitle("Top quark p_{T} [GeV]")
hEmpty2D.GetXaxis().SetLabelSize(0.045)
hEmpty2D.GetYaxis().SetLabelSize(0.045)
hEmpty2D.Draw()
hResponse2D = response.Hresponse().Clone()
hResponse2D.SetName("plottedResponse")

# normalize so that for each bin of true top quark pt, the bins in measured top pt add up to 100%
#nbinsX = hResponse2D.GetNbinsX()
#nbinsY = hResponse2D.GetNbinsX()
#print "nbr bins in x = " + str(nbinsX) + "nbr bins in y = " + str(nbinsY)
#for iby in range(1,nbinsY) :
#    rowIntegral = hResponse2D.Integral(1,nbinsX,iby,iby)
#    print "for y-bin " + str(iby) + " row integral = " + str(rowIntegral)
#    for ibx in range(1,nbinsX+1) :
#        binContent = hResponse2D.GetBinContent(ibx,iby)
#        newContent = 0
#        if rowIntegral > 0:
#            newContent = binContent/rowIntegral*100.0
#        #print "bin content x-bin " + str(ibx) + " y-bin " + str(iby) + " binContent " + str(binContent) + " newContent " + str(newContent)
#        hResponse2D.SetBinContent(ibx,iby,newContent)


gStyle.SetPaintTextFormat(".1f")
#gStyle.SetPalette(1)
hResponse2D.Draw("colz,same,text")
hEmpty2D.Draw("axis,same")
cr.SaveAs("UnfoldingPlots/unfold_responseMatrix_"+options.syst+".png")
cr.SaveAs("UnfoldingPlots/unfold_responseMatrix_"+options.syst+".eps")

response.Hresponse().SetName("responseMatrix_"+options.syst)
response.Hresponse().Write()

gPad.SetLogz()
cr.SaveAs("UnfoldingPlots/unfold_responseMatrix_logz_"+options.syst+".png")
cr.SaveAs("UnfoldingPlots/unfold_responseMatrix_logz_"+options.syst+".eps")

gStyle.SetPadRightMargin(0.05);


# -------------------------------------------------------------------------------------
# read actual histograms
# -------------------------------------------------------------------------------------

if options.closureTest == True : 
    hTrue_max700    = f_ttbar_max700_odd.Get("ptGenTop")
    hTrue_700to1000 = f_ttbar_700to1000_odd.Get("ptGenTop")
    hTrue_1000toInf = f_ttbar_1000toInf_odd.Get("ptGenTop")
else :
    hTrue_max700    = f_ttbar_max700.Get("ptGenTop")
    hTrue_700to1000 = f_ttbar_700to1000.Get("ptGenTop")
    hTrue_1000toInf = f_ttbar_1000toInf.Get("ptGenTop")

hTrue_max700.Sumw2()
hTrue_700to1000.Sumw2()
hTrue_1000toInf.Sumw2()

hRecoMC_max700    = f_ttbar_max700.Get("ptRecoTop").Clone()
hRecoMC_max700.SetName("hRecoMC_max700")
hRecoMC_max700.Sumw2()
hRecoMC_700to1000 = f_ttbar_700to1000.Get("ptRecoTop").Clone()
hRecoMC_700to1000.SetName("hRecoMC_700to1000")
hRecoMC_700to1000.Sumw2()
hRecoMC_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop").Clone()
hRecoMC_1000toInf.SetName("hRecoMC_1000toInf")
hRecoMC_1000toInf.Sumw2()

hRecoData = f_data.Get("ptRecoTop").Clone()
hRecoData.SetName("hRecoData")

hRecoQCD = f_QCD.Get("ptRecoTop").Clone()
hRecoQCD.SetName("hRecoQCD")
hRecoQCD.Sumw2()
hRecoQCD.SetFillColor(TColor.kYellow)

if options.closureTest == False : 
    hMeas = f_data.Get("ptRecoTop")
else :
    hMeas_max700    = f_ttbar_max700.Get("ptRecoTop")
    hMeas_700to1000 = f_ttbar_700to1000.Get("ptRecoTop")
    hMeas_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop")
    hMeas_max700.Sumw2()
    hMeas_700to1000.Sumw2()
    hMeas_1000toInf.Sumw2()
    

hMeas_T_t     = f_T_t.Get("ptRecoTop")
hMeas_Tbar_t  = f_Tbar_t.Get("ptRecoTop")
hMeas_T_s     = f_T_s.Get("ptRecoTop")
hMeas_Tbar_s  = f_Tbar_s.Get("ptRecoTop")
hMeas_T_tW    = f_T_tW.Get("ptRecoTop")
hMeas_Tbar_tW = f_Tbar_tW.Get("ptRecoTop")
hMeas_WJets_1jet   = f_WJets_1jet.Get("ptRecoTop")
hMeas_WJets_2jet   = f_WJets_2jet.Get("ptRecoTop")
hMeas_WJets_3jet   = f_WJets_3jet.Get("ptRecoTop")
hMeas_WJets_4jet   = f_WJets_4jet.Get("ptRecoTop")
hMeas_tt0_nonsemi = f_ttbar_nonsemilep_max700.Get("ptRecoTop")
hMeas_tt700_nonsemi = f_ttbar_nonsemilep_700to1000.Get("ptRecoTop")
hMeas_tt1000_nonsemi = f_ttbar_nonsemilep_1000toInf.Get("ptRecoTop")

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
# Scale to desired normalization
# Options are :
#  1. From MC
#  2. From fit
# For now, we don't have the fit, so we do from MC
# -------------------------------------------------------------------------------------

# if doing closure test, use ttbar nominal as the "measured" distribution
if options.closureTest == True : 
    hMeas_max700.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar))
    hMeas_700to1000.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) )
    hMeas_1000toInf.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) )
    hMeas = hMeas_max700.Clone()
    hMeas.SetName("ptRecoTop_measured")
    hMeas.Add(hMeas_700to1000)
    hMeas.Add(hMeas_1000toInf)    

hTrue_max700.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) )
hTrue_700to1000.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) )
hTrue_1000toInf.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) )
hTrue = hTrue_max700.Clone()
hTrue.SetName("pt_genTop")
hTrue.Add(hTrue_700to1000)
hTrue.Add(hTrue_1000toInf)

hRecoMC_max700.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) )
hRecoMC_700to1000.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) )
hRecoMC_1000toInf.Scale( eff_closure * sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) )
hRecoMC = hRecoMC_max700.Clone()
hRecoMC.SetName("ptRecoTop_ttbar")
hRecoMC.Add(hRecoMC_700to1000)
hRecoMC.Add(hRecoMC_1000toInf)


hMeas_T_t.Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) )
hMeas_Tbar_t.Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) )
hMeas_T_s.Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) )
hMeas_Tbar_s.Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) )
hMeas_T_tW.Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) )
hMeas_Tbar_tW.Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) )

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

hMeas_tt0_nonsemi.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) )
hMeas_tt700_nonsemi.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) )
hMeas_tt1000_nonsemi.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) )

hMeas_TTNonSemi = hMeas_tt0_nonsemi.Clone()
hMeas_TTNonSemi.SetName("ptRecoTop_TTNonSemilep")
hMeas_TTNonSemi.Add( hMeas_tt700_nonsemi )
hMeas_TTNonSemi.Add( hMeas_tt1000_nonsemi )

hMeas_SingleTop.SetFillColor(TColor.kMagenta)
hMeas_WJets.SetFillColor(TColor.kGreen-3)
hMeas.SetFillColor(TColor.kRed+1)
hRecoMC.SetFillColor(TColor.kRed+1)
hMeas_TTNonSemi.SetFillColor(TColor.kRed-7)

#number of events before scaling each sample to that fitted by theta
print 'number of events before scaling each sample to that fitted by theta'
print 'Nqcd   '            + str( hRecoQCD.Integral() )
print 'Nt     '            + str( hMeas_SingleTop.Integral() )
print 'Nwjets '            + str( hMeas_WJets.Integral() )
print 'Nttbar nonsemilep ' + str( hMeas_TTNonSemi.Integral() )
print 'Nttbar '            + str( hRecoMC.Integral() )
print 'NData  '            + str( hRecoData.Integral() )

# -------------------------------------------------------------------------------------
# Scale each sample to that fitted by theta
# -------------------------------------------------------------------------------------

hRecoMC.Scale( fitted_ttbar / hRecoMC.Integral() )
hRecoQCD.Scale( fitted_qcd / hRecoQCD.Integral() )
hMeas_SingleTop.Scale( fitted_singletop / hMeas_SingleTop.Integral() )
hMeas_WJets.Scale( fitted_wjets / hMeas_WJets.Integral() )
hMeas_TTNonSemi.Scale( fitted_ttbarnonsemilep / hMeas_TTNonSemi.Integral() )


# -------------------------------------------------------------------------------------
# Make a stack plot of the MC to compare to data
# -------------------------------------------------------------------------------------

hEmpty = hMeas_WJets.Clone()
hEmpty.SetName("empty")
hEmpty.Reset()
hEmpty.GetXaxis().SetTitle("p_{T} [GeV]")
hEmpty.GetYaxis().SetTitle("Events / 100 GeV")
hMC_stack = THStack("hMC_stack", "")
hMC_stack.Add( hMeas_WJets )
hMC_stack.Add( hMeas_SingleTop )
hMC_stack.Add( hMeas_TTNonSemi )
hMC_stack.Add( hRecoQCD )
hMC_stack.Add( hRecoMC )
max = hTrue.GetMaximum()
hEmpty.SetAxisRange(0, max*1.05, "Y")

c = TCanvas("datamc", "", 800, 600)

l = TLegend(0.7, 0.65, 0.9, 0.9)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.045)
l.SetBorderSize(0)

if options.closureTest == False:
    hRecoData.Draw("e")
    hMC_stack.Draw("hist,same")
    hRecoData.Draw("e,same")
    hEmpty.Draw("axis,same")
    hRecoData.SetMaximum( hMC_stack.GetMaximum() * 1.2 )
    l.AddEntry(hRecoData, "Data","pel")
    l.AddEntry(hRecoMC, "t#bar{t} ","f")
    l.AddEntry(hRecoQCD, "QCD","f")
    l.AddEntry(hMeas_TTNonSemi, "Non-semilep t#bar{t}","f")
    l.AddEntry(hMeas_SingleTop, "Single Top","f")
    l.AddEntry(hMeas_WJets, "W #rightarrow #mu#nu","f")
else:
    hEmpty.Draw("hist")
    hMC_stack.Draw("hist,same")
    hEmpty.Draw("axis,same")
    hEmpty.SetMaximum( hMC_stack.GetMaximum() * 1.2 )
    l.AddEntry(hRecoMC, "t#bar{t} ","f")
    l.AddEntry(hRecoQCD, "QCD","f")
    l.AddEntry(hMeas_TTNonSemi, "Non-semilep t#bar{t}","f")
    l.AddEntry(hMeas_SingleTop, "Single Top","f")
    l.AddEntry(hMeas_WJets, "W #rightarrow #mu#nu","f")

l.Draw()
c.SaveAs("UnfoldingPlots/unfold_datamc_"+options.syst+".png")
c.SaveAs("UnfoldingPlots/unfold_datamc_"+options.syst+".eps")


#number of events after scaling each sample to that fitted by theta
print 'number of events after scaling each sample to that fitted by theta'
print 'Nqcd   '            + str( hRecoQCD.Integral() )
print 'Nt     '            + str( hMeas_SingleTop.Integral() )
print 'Nwjets '            + str( hMeas_WJets.Integral() )
print 'Nttbar nonsemilep ' + str( hMeas_TTNonSemi.Integral() )
print 'Nttbar '            + str( hRecoMC.Integral() )
print 'NData  '            + str( hRecoData.Integral() )                      

                       

# -------------------------------------------------------------------------------------
# Now do the actual unfolding
# -------------------------------------------------------------------------------------

c2 = TCanvas("unfolding", "unfolding")

if options.subtractBackgrounds :
    for hist in [hMeas_SingleTop, hMeas_WJets, hRecoQCD, hMeas_TTNonSemi] :
        hMeas.Add(hist, -1.)

for ibin in xrange( hMeas.GetNbinsX() ) :
    if ( hMeas.GetBinContent( ibin ) < 0.0 ) :
        hMeas.SetBinContent( ibin, 0.0 )

print "------------ UNFOLDING (" + options.syst + ") ------------"
#unfold= RooUnfoldBayes     (response, hMeas, 10);    #  OR
unfold= RooUnfoldSvd     (response, hMeas, 4);   #  OR
#unfold= RooUnfoldTUnfold (response, hMeas);


c1 = TCanvas("c", "c", 700, 700)
pad1 =  TPad("pad1","pad1",0,0.3,1,1)
pad1.SetBottomMargin(0.05);
pad1.Draw();
pad1.cd();


## get the unfolded distribution
hReco = unfold.Hreco()

hFrac = hReco.Clone()
hFrac.SetName("hFrac")
hFrac.SetTitle(";Top quark p_{T} [GeV];Measured/Truth")
hFrac.Divide(hTrue)


# Translate to cross section (not events) in bins of pt N/L/BR)
hTrue.Scale(1.0/(lum*4/27))
hMeas.Scale(1.0/(lum*4/27))
hReco.Scale(1.0/(lum*4/27))

# Correct for selection bias in requiring trigger 
#SF [300,400]: 0 +/- 0
#SF [400,500]: 1.67023 +/- 0.00847072
#SF [500,600]: 1.62007 +/- 0.0139264
#SF [600,700]: 1.54549 +/- 0.0209462
#SF [700,800]: 1.61978 +/- 0.041841
#SF [800,1300]: 1.47689 +/- 0.037455
SF = [0.0, 1.67023, 1.62007, 1.54549, 1.61978, 1.47689]

bin400 = hMeas.GetXaxis().FindBin(400.)
binmax = hMeas.GetXaxis().FindBin(10000.)

if options.normalize :
    hTrue.Scale( 1.0 / hTrue.Integral(bin400,binmax) )
    hMeas.Scale( 1.0 / hMeas.Integral(bin400,binmax) )
    hReco.Scale( 1.0 / hReco.Integral(bin400,binmax) )


# Correct for bin width
for ibin in range(1, hTrue.GetXaxis().GetNbins()+1 ) :
    width = hTrue.GetBinWidth(ibin)
    hTrue.SetBinContent(ibin,  hTrue.GetBinContent(ibin) * SF[ibin-1] / width )
    hMeas.SetBinContent(ibin,  hMeas.GetBinContent(ibin) / width )
    hReco.SetBinContent(ibin,  hReco.GetBinContent(ibin) * SF[ibin-1] / width )
    hTrue.SetBinError(ibin,  hTrue.GetBinError(ibin) * SF[ibin-1] / width )
    hMeas.SetBinError(ibin,  hMeas.GetBinError(ibin) / width )
    hReco.SetBinError(ibin,  hReco.GetBinError(ibin) * SF[ibin-1] / width )

print 'htrue = ' + str(hTrue.Integral(bin400,binmax) )
print 'hmeas = ' + str(hMeas.Integral(bin400,binmax) )
print 'hreco = ' + str(hReco.Integral(bin400,binmax) )


#unfold.PrintTable (cout, hTrue);
hReco.SetMarkerStyle(21)
hMeas.SetMarkerStyle(25);

if options.normalize == False : 
    hReco.SetTitle(";;#frac{d#sigma}{dp_{T}} [fb/GeV]")
else : 
    hReco.SetTitle(";;#frac{1}{#sigma} #frac{d#sigma}{dp_{T}} [1 / GeV]")
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

if options.plotFullRange == False : 
    hReco.GetXaxis().SetRangeUser(400., 1300.)



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
#pad2.SetLeftMargin(0.2)
pad2.Draw();
pad2.cd();
hFrac.SetMaximum(2.0)
hFrac.SetMinimum(0.0)
hFrac.UseCurrentStyle()
hFrac.GetYaxis().SetTitleSize(25)
#hFrac.GetYaxis().SetTitleOffset(1.7)
hFrac.GetYaxis().SetTitleOffset(2.0)
hFrac.GetXaxis().SetTitleOffset(4.0)
#hFrac.GetXaxis().SetLabelSize(20)
hFrac.GetXaxis().SetLabelSize(25)
hFrac.GetYaxis().SetNdivisions(2,4,0,False)

hFrac.Draw("e")
if options.plotFullRange == False : 
    hFrac.GetXaxis().SetRangeUser(400., 1300.)
    

c1.Update()

append = ""
if options.closureTest :
    append += "_closure"
if options.plotFullRange :
    append += "_fullrange"

c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+append+"_"+options.syst+".pdf", "pdf")
c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+append+"_"+options.syst+".png", "png")
c1.Print("UnfoldingPlots/unfolded_ttbar_xs"+append+"_"+options.syst+".eps", "eps")


fout.Close()
