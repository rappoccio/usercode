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


(options, args) = parser.parse_args()

argv = []

from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gROOT, gStyle, THStack, TLegend, TLatex

gROOT.Macro("rootlogon.C")


gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
#gStyle.SetTitleFontSize(0.05)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(3.5, "X")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")


gSystem.Load("RooUnfold-1.1.1/libRooUnfold.so")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd
# from ROOT import RooUnfoldTUnfold

# Constants
if options.closureTest == False : 
    lum = 19.7 # fb-1
    sigma_ttbar_NNLO = 245.8 * 1000. # fb, from http://arxiv.org/pdf/1303.6254.pdf
    Nmc = 21675970
    SF_b = 0.97
    SF_t = 0.94
else :
    lum = 1.0
    sigma_ttbar_NNLO = 1.0
    Nmc = 1.0
    SF_b = 1.0
    SF_t = 1.0

# ==============================================================================
#  Example Unfolding
# ==============================================================================

fdata = TFile("TTSemilepAnalyzer_unfolding_data_type1.root")
fmc = TFile("TTSemilepAnalyzer_antibtag_w_mucut_type1.root")

response= fmc.Get("response_pt")

print "==================================== Get Hists ====================================="
hTrue= fmc.Get("ptGenTop")
if options.closureTest == False : 
    hMeas= fdata.Get("ptRecoTop")
else :
    hMeas= fmc.Get("ptRecoTop")

hTrue.Scale( sigma_ttbar_NNLO * lum / float(Nmc) * SF_b * SF_t  )

print "==================================== UNFOLD ==================================="
unfold= RooUnfoldBayes     (response, hMeas, 10);    #  OR
#unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
# unfold= RooUnfoldTUnfold (response, hMeas);



c1 = TCanvas("c", "c", 700, 700)
pad1 =  TPad("pad1","pad1",0,0.3,1,1)
pad1.SetBottomMargin(0.05);
pad1.SetLeftMargin(0.2)
pad1.Draw();
pad1.cd();

   
hReco= unfold.Hreco();



hFrac = hReco.Clone()
hFrac.SetName("hFrac")
hFrac.SetTitle(";p_{T} (GeV);Measured/Truth")
hFrac.Divide(hTrue)
hMeas.Sumw2()


#unfold.PrintTable (cout, hTrue);
hReco.SetMarkerStyle(21)
hMeas.SetMarkerStyle( 25);

hReco.SetTitle(";;d #sigma / d p_{T} (fb / GeV)")
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

leg = TLegend(0.4, 0.6, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)

if options.closureTest == False : 
    leg.AddEntry( hReco, 'Unfolded data', 'p')
    leg.AddEntry( hTrue, 'Generated', 'l')
    leg.AddEntry( hMeas, 'Raw data', 'p')
else : 
    leg.AddEntry( hReco, 'Unfolded MC : Closure test', 'p')
    leg.AddEntry( hTrue, 'Generated', 'l')
    leg.AddEntry( hMeas, 'Raw MC', 'p')


leg.Draw()

text1 = TLatex()
text1.SetNDC()
text1.SetTextFont(42)
text1.DrawLatex(0.20,0.87, "#scale[1.0]{CMS Preliminary, L = 19.7 fb^{-1} at  #sqrt{s} = 8 TeV}")


c1.cd();
pad2 =  TPad("pad2","pad2",0,0.0,1,0.28)
pad2.SetTopMargin(0.05);
pad2.SetBottomMargin(0.4);
pad2.SetLeftMargin(0.2)
pad2.Draw();
pad2.cd();
hFrac.SetMaximum(2.0)
hFrac.SetMinimum(0.0)
hFrac.UseCurrentStyle()
hFrac.GetYaxis().SetTitleSize(25)
hFrac.GetYaxis().SetTitleOffset(1.7)
hFrac.GetXaxis().SetLabelSize(20)
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
