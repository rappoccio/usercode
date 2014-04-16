#!/usr/bin/env python
# ==============================================================================
# Script for doing RooUnfold on the ttbar differential cross secion
# ==============================================================================

from optparse import OptionParser
parser = OptionParser()
  

parser.add_option('--closureTest', metavar='F', action='store_true',
                  default=False,
                  dest='closureTest',
                  help='Run Closure Test')

parser.add_option('--plotFullRange', metavar='F', action='store_true',
                  default=False,
                  dest='plotFullRange',
                  help='Plot the full pt range (pt > 300 GeV)')

parser.add_option('--subtractBackgrounds', metavar='F', action='store_true',
                  default=False,
                  dest='subtractBackgrounds',
                  help='Subtract off the backgrounds')


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


# Constants

# Performance numbers
lum = 19.7 # fb-1
#SF_t = 0.94
SF_t = 1.0

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
Nmc_TT_Mtt_700_1000 = 3082812
Nmc_TT_Mtt_1000_Inf = 1249111
Nmc_T_t = 3758227
Nmc_Tbar_t = 1935072
Nmc_T_s = 259961
Nmc_Tbar_s = 139974
Nmc_T_tW = 497658
Nmc_Tbar_tW = 493460
Nmc_WJets = 57709905

# ttbar filter efficiencies
e_TT_Mtt_700_1000 = 0.074
e_TT_Mtt_1000_Inf = 0.014
e_TT_Mtt_0_700 = 1.0   #   No efficiency here, we applied the cut at gen level

# QCD Normalization from MET fits
NQCD = 32.8 


# ==============================================================================
#  Example Unfolding
# ==============================================================================

f_data = TFile("histfiles/SingleMu_iheartNY_V1_mu_Run2012_nom.root")
f_QCD  = TFile("histfiles/SingleMu_iheartNY_V1_mu_Run2012_qcd.root")

f_ttbar_max700    = TFile("histfiles/TT_max700_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_response.root")
f_ttbar_700to1000 = TFile("histfiles/TT_Mtt-700to1000_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_response.root")
f_ttbar_1000toInf = TFile("histfiles/TT_Mtt-1000toInf_CT10_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom_response.root")

f_T_t     = TFile("histfiles/T_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
f_Tbar_t  = TFile("histfiles/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
f_T_s     = TFile("histfiles/T_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
f_Tbar_s  = TFile("histfiles/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
f_T_tW    = TFile("histfiles/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
f_Tbar_tW = TFile("histfiles/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_iheartNY_V1_mu_nom.root")
f_WJets   = TFile("histfiles/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_iheartNY_V1_mu_nom.root")

# the response matrices are simply added here, but have been filled with the full event weights (taking sample size, efficiency, etx. into account)
response_ttbar_max700    = f_ttbar_max700.Get("response_pt")
response_ttbar_700to1000 = f_ttbar_700to1000.Get("response_pt")
response_ttbar_1000toInf = f_ttbar_1000toInf.Get("response_pt")
response = response_ttbar_max700.Clone()
response.Add(response_ttbar_700to1000)
response.Add(response_ttbar_1000toInf)

gStyle.SetPadRightMargin(0.12);

cr = TCanvas("c_response", "", 800, 600)
hEmpty2D = response.Hresponse().Clone()
hEmpty2D.SetName("empty2D")
hEmpty2D.Reset()
hEmpty2D.GetXaxis().SetTitle("Measured p_{T} [GeV]")
hEmpty2D.GetYaxis().SetTitle("Truth p_{T} [GeV]")
hEmpty2D.GetXaxis().SetLabelSize(0.045)
hEmpty2D.Draw()
response.Hresponse().Draw("colz,same")
hEmpty2D.Draw("axis,same")
cr.SaveAs("unfold_responseMatrix.png")
cr.SaveAs("unfold_responseMatrix.eps")

gPad.SetLogz()
cr.SaveAs("unfold_responseMatrix_logz.png")
cr.SaveAs("unfold_responseMatrix_logz.eps")

gStyle.SetPadRightMargin(0.05);


print "==================================== Get Hists ====================================="
hTrue_max700    = f_ttbar_max700.Get("ptGenTop")
hTrue_700to1000 = f_ttbar_700to1000.Get("ptGenTop")
hTrue_1000toInf = f_ttbar_1000toInf.Get("ptGenTop")

hRecoMC_max700    = f_ttbar_max700.Get("ptRecoTop").Clone()
hRecoMC_700to1000 = f_ttbar_700to1000.Get("ptRecoTop").Clone()
hRecoMC_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop").Clone()
hRecoMC_max700.SetName("hRecoMC_max700")
hRecoMC_700to1000.SetName("hRecoMC_700to1000")
hRecoMC_1000toInf.SetName("hRecoMC_1000toInf")

hRecoData = f_data.Get("ptRecoTop").Clone()
hRecoData.SetName("hRecoData")

hRecoQCD = f_QCD.Get("ptRecoTop").Clone()
hRecoQCD.SetName("hRecoQCD")
hRecoQCD.Sumw2()
hRecoQCD.Scale( NQCD / hRecoQCD.Integral() )
hRecoQCD.SetFillColor(TColor.kYellow)

if options.closureTest == False : 
    hMeas = f_data.Get("ptRecoTop")
else :
    hMeas_max700    = f_ttbar_max700.Get("ptRecoTop")
    hMeas_700to1000 = f_ttbar_700to1000.Get("ptRecoTop")
    hMeas_1000toInf = f_ttbar_1000toInf.Get("ptRecoTop")
    

# Get the histogram files
hMeas_T_t     = f_T_t.Get("ptRecoTop")
hMeas_Tbar_t  = f_Tbar_t.Get("ptRecoTop")
hMeas_T_s     = f_T_s.Get("ptRecoTop")
hMeas_Tbar_s  = f_Tbar_s.Get("ptRecoTop")
hMeas_T_tW    = f_T_tW.Get("ptRecoTop")
hMeas_Tbar_tW = f_Tbar_tW.Get("ptRecoTop")
hMeas_WJets   = f_WJets.Get("ptRecoTop")

# Scale to desired normalization
# Options are :
#  1. From MC
#  2. From fit
#
# For now, we don't have the fit, so we do from MC


if options.closureTest == True : 
    hMeas_max700.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_t  )
    hMeas_700to1000.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_t  )
    hMeas_1000toInf.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_t  )
    hMeas = hMeas_max700.Clone()
    hMeas.Add(hMeas_700to1000)
    hMeas.Add(hMeas_1000toInf)
    
hTrue_max700.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_t  )
hTrue_700to1000.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_t  )
hTrue_1000toInf.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_t  )
hTrue = hTrue_max700.Clone()
hTrue.Add(hTrue_700to1000)
hTrue.Add(hTrue_1000toInf)

hRecoMC_max700.Scale( sigma_ttbar_NNLO * e_TT_Mtt_0_700 * lum / float(Nmc_ttbar) * SF_t  )
hRecoMC_700to1000.Scale( sigma_ttbar_NNLO * e_TT_Mtt_700_1000 * lum / float(Nmc_TT_Mtt_700_1000) * SF_t  )
hRecoMC_1000toInf.Scale( sigma_ttbar_NNLO * e_TT_Mtt_1000_Inf * lum / float(Nmc_TT_Mtt_1000_Inf) * SF_t  )
hRecoMC = hRecoMC_max700.Clone()
hRecoMC.Add(hRecoMC_700to1000)
hRecoMC.Add(hRecoMC_1000toInf)

hMeas_T_t.Scale( sigma_T_t_NNLO * lum / float(Nmc_T_t) * SF_t  )
hMeas_Tbar_t.Scale( sigma_Tbar_t_NNLO * lum / float(Nmc_Tbar_t) * SF_t  )
hMeas_T_s.Scale( sigma_T_s_NNLO * lum / float(Nmc_T_s) * SF_t  )
hMeas_Tbar_s.Scale( sigma_Tbar_s_NNLO * lum / float(Nmc_Tbar_s) * SF_t  )
hMeas_T_tW.Scale( sigma_T_tW_NNLO * lum / float(Nmc_T_tW) * SF_t  )
hMeas_Tbar_tW.Scale( sigma_Tbar_tW_NNLO * lum / float(Nmc_Tbar_tW) * SF_t  )
hMeas_WJets.Scale( sigma_WJets_NNLO * lum / float(Nmc_WJets) * SF_t  )

hMeas_SingleTop = hMeas_T_t.Clone()

hMeas_SingleTop.SetFillColor(TColor.kMagenta)
hMeas_WJets.SetFillColor(TColor.kGreen-3)
hMeas.SetFillColor(TColor.kRed+1)
hRecoMC.SetFillColor(TColor.kRed+1)

for hist in [hMeas_Tbar_t, hMeas_T_s, hMeas_Tbar_s, hMeas_T_tW, hMeas_Tbar_tW] :
    hMeas_SingleTop.Add( hist )


# Make a stack plot of the MC to compare to data
hEmpty = hMeas_WJets.Clone()
hEmpty.SetName("empty")
hEmpty.Reset()
hEmpty.GetXaxis().SetTitle("p_{T} [GeV]")
hEmpty.GetYaxis().SetTitle("Events / 100 GeV")
hMC_stack = THStack("hMC_stack", "")
hMC_stack.Add( hMeas_WJets )
hMC_stack.Add( hMeas_SingleTop )
hMC_stack.Add( hRecoQCD )
hMC_stack.Add( hRecoMC )
max = hMC_stack.GetMaximum()
hEmpty.SetAxisRange(0, max*1.05, "Y")

c = TCanvas("datamc", "", 800, 600)

l = TLegend(0.7, 0.65, 0.9, 0.9)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.045)
l.SetBorderSize(0)

#if options.closureTest == False:
if False :  #for now make sure to not draw data / MC distribution
    hRecoData.Draw("e")
    hMC_stack.Draw("hist,same")
    hRecoData.Draw("e,same")
    hEmpty.Draw("axis,same")
    l.AddEntry(hRecoData, "Data","pel")
    l.AddEntry(hRecoMC, "t#bar{t} ","f")
    l.AddEntry(hRecoQCD, "QCD","f")
    l.AddEntry(hMeas_SingleTop, "Single Top","f")
    l.AddEntry(hMeas_WJets, "W #rightarrow #mu#nu","f")
else:
    hEmpty.Draw("hist")
    hMC_stack.Draw("hist,same")
    hEmpty.Draw("axis,same")
    l.AddEntry(hRecoMC, "t#bar{t} ","f")
    l.AddEntry(hRecoQCD, "QCD","f")
    l.AddEntry(hMeas_SingleTop, "Single Top","f")
    l.AddEntry(hMeas_WJets, "W #rightarrow #mu#nu","f")

l.Draw()
c.SaveAs("unfold_datamc.png")
c.SaveAs("unfold_datamc.eps")


# First plot RECO data-to-MC
c2 = TCanvas("unfolding", "unfolding")

if options.subtractBackgrounds :
    for hist in [hMeas_SingleTop, hMeas_WJets, hRecoQCD] :
        hMeas.Add(hist, -1.)
    # Someday soon, we subtract QCD and W+Jets. For now, they are empty.
    

print "==================================== UNFOLD ==================================="
unfold= RooUnfoldBayes     (response, hMeas, 10);    #  OR
#unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
#unfold= RooUnfoldTUnfold (response, hMeas);


c1 = TCanvas("c", "c", 700, 700)
pad1 =  TPad("pad1","pad1",0,0.3,1,1)
pad1.SetBottomMargin(0.05);
#pad1.SetLeftMargin(0.2)
pad1.Draw();
pad1.cd();

   
hReco = unfold.Hreco();


hFrac = hReco.Clone()
hFrac.SetName("hFrac")
hFrac.SetTitle(";p_{T} [GeV];Measured/Truth")
hFrac.Divide(hTrue)
hMeas.Sumw2()


#unfold.PrintTable (cout, hTrue);
hReco.SetMarkerStyle(21)
hMeas.SetMarkerStyle(25);

hReco.SetTitle(";;d#sigma / dp_{T} [fb / GeV]")
hReco.GetYaxis().SetTitleOffset(1.2)
hReco.SetMinimum(0.0)
hReco.Draw()
hTrue.Draw('hist same')
hMeas.Draw('same')
hTrue.UseCurrentStyle()
hTrue.SetLineColor(4);
hTrue.GetYaxis().SetTitleSize(25)
hTrue.GetXaxis().SetLabelSize(0)

if options.plotFullRange == False : 
    hReco.GetXaxis().SetRangeUser(400., 10000.)



# Correct for bin width
for ibin in range(1, hTrue.GetXaxis().GetNbins() ) :
    width = hTrue.GetBinWidth(ibin)
    hTrue.SetBinContent(ibin,  hTrue.GetBinContent(ibin) / width )
    hMeas.SetBinContent(ibin,  hMeas.GetBinContent(ibin) / width )
    hReco.SetBinContent(ibin,  hReco.GetBinContent(ibin) / width )
    hTrue.SetBinError(ibin,  hTrue.GetBinError(ibin) / width )
    hMeas.SetBinError(ibin,  hMeas.GetBinError(ibin) / width )
    hReco.SetBinError(ibin,  hReco.GetBinError(ibin) / width )

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
    hFrac.GetXaxis().SetRangeUser(400., 10000.)
    

c1.Update()

append = ""
if options.closureTest :
    append += "_closure"
if options.plotFullRange :
    append += "_fullrange"

c1.Print("unfolded_ttbar_xs" + append + ".pdf", "pdf")
c1.Print("unfolded_ttbar_xs" + append + ".png", "png")
c1.Print("unfolded_ttbar_xs" + append + ".eps", "eps")
