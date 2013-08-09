#! /usr/bin/env python
import os
from math import *

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--pt', metavar='F', type='string', action='store',
                  default='low',
                  dest='pt',
                  help='low or high')

(options, args) = parser.parse_args()

argv = []



wjetsFactor = [
    0.259287,0.259287,0.259287,0.259287
    ]

ttjetsFactor = [
    0.626595,0.626595,0.626595,0.626595
    ]
singletopFactor = [
    0.103425,0.103425,0.103425,0.103425
    ]
zjetsFactor = [
    0.0275366,0.0275366,0.0275366,0.0275366
    ]

import ROOT
ROOT.gROOT.Macro("rootlogon.C")

Zpoverlay = ROOT.TFile("RSGluon_2TeV_forOverlay.root")
Zpoverlayt1 = ROOT.TFile("RSGluon_2TeV_type11_forOverlay.root")

type2ptsig = Zpoverlay.Get("type2TopPtSignal")
type1ptsig = Zpoverlayt1.Get("topTagPt")

import sys

fData = ROOT.TFile("TTSemilepAnalyzer_19invfb_TTWeight_type1.root")

#fTopMC = ROOT.TFile("TTSemilepAnalyzer_v9_TTJets_antibtag_w_mucut_withDR_loosenedType2Top_FULL_withPU.root")
fTopFL = ROOT.TFile("TTSemilepAnalyzer_TTJetsLeptonic_TTWeight_type1.root") 
fTopSL = ROOT.TFile("TTSemilepAnalyzer_TTJets_TTWeight_type1.root")



fWMC = ROOT.TFile("TTSemilepAnalyzer_WJets_TTWeight_type1.root")
fZJetsMC = ROOT.TFile("TTSemilepAnalyzer_ZJets_TTWeight_type1.root")
fSingletop = [
ROOT.TFile("TTSemilepAnalyzer_ST_t_TTWeight_type1.root"),
ROOT.TFile("TTSemilepAnalyzer_ST_tB_TTWeight_type1.root"),
ROOT.TFile("TTSemilepAnalyzer_ST_tW_TTWeight_type1.root"),
ROOT.TFile("TTSemilepAnalyzer_ST_tWB_TTWeight_type1.root"),
ROOT.TFile("TTSemilepAnalyzer_ST_s_TTWeight_type1.root"),
ROOT.TFile("TTSemilepAnalyzer_ST_sB_TTWeight_type1.root"),
]

hists = []
canvs = []

nEvents = [
    25424818.,
    57653686.,
    30404232., 
    12043695.,
    ]
stnEvents = [
    3748155.,
    1930185.,
    495559.,
    491463.,
    259176.,
    139604.,
]
xs = [
    103.0 * 0.97 * 0.93,
    37509.0 * 0.97 * 0.93,
    3503.71 * 0.97 * 0.93,
    24.8 * 0.97 * 0.93,
    ]
stxs=[
    56.4 * 0.97 * 0.93,
    30.7 * 0.97 * 0.93,
    11.1 * 0.97 * 0.93,
    11.1 * 0.97 * 0.93,
    3.79 * 0.97 * 0.93,
    1.76 * 0.97 * 0.93,
]

colors = [
    #ROOT.kRed-3,
    ROOT.TColor.GetColor(255, 80, 80),
    ROOT.kGreen,
    ROOT.kYellow
    ]
qcdFactor = [
    0.00957248,0.00957248,0.00957248,0.00957248
    ]

lumi = 19748.
#15379.91 * 1.066
#lumi = 4921.


t12ddata = fData.Get("leptopptvsnsj")
c2d = ROOT.TCanvas('c2d', 'leptoppt vs nsj')
t12ddata.Rebin2D(5,1)
t12ddata.GetYaxis().SetTitleOffset(0.8)
t12ddata.SetTitle(';Pt (leptonic top);Number of Subjets')
t12ddata.SetStats(0)
t12ddata.Draw('colz')
c2d.Print( 'leptoppt_vs_nsj.root', 'root')
c2d.Print( 'leptoppt_vs_nsj.pdf', 'pdf')

hist2ds = ["leptopptvstopmassprekin","leptopptvstopmasspostkin","leptopptvstopmasspostnsj","leptopptvstopmasspostminmass","leptopptvstopmassposttau32","leptopptvstopmasspostbmax"]
c2d1 = []
c2d2 = []
j=0
for hist2dn in hist2ds:
	c2d1.append(ROOT.TCanvas('c2d'+hist2dn,hist2dn ))
	c2d2.append(ROOT.TCanvas('c2d2'+hist2dn,hist2dn ))
	hist2d=fData.Get(hist2dn)

	singletopt1temp2d = fSingletop[0].Get(hist2dn)
	singletopt1temp2d.Scale((stxs[0] / stnEvents[0]) * lumi)
	singletopt1temp2d.Rebin2D(10,15)
	singletopt12d = singletopt1temp2d.Clone("singletopt12d")
	for ifile in range(1,len(fSingletop)):
		singletopt1temp2d = fSingletop[ifile].Get(hist2dn)
		singletopt1temp2d.Scale((stxs[ifile] / stnEvents[ifile]) * lumi)
       	        singletopt1temp2d.Rebin2D(10,15)
		singletopt12d.Add(singletopt1temp2d)

	t1wjets2d= fWMC.Get(hist2dn)
	t1zjets2d= fZJetsMC.Get(hist2dn)
	t1ttbarSL2d= fTopSL.Get(hist2dn)
	t1ttbarFL2d= fTopFL.Get(hist2dn)
	t1wjets2d.Scale(xs[1]*lumi/nEvents[1])
	#t1ttbar2d.Scale(xs[0]*lumi/nEvents[0])
        t1zjets2d.Scale(xs[2]*lumi/nEvents[2])
	t1ttbarFL2d.Scale(xs[3]*lumi/nEvents[3])
	t1ttbarSL2d.Scale(xs[0]*lumi/nEvents[0])

	t1wjets2d.Rebin2D(10,15)
	t1ttbarSL2d.Rebin2D(10,15)
	t1ttbarFL2d.Rebin2D(10,15)
        t1zjets2d.Rebin2D(10,15)

	bkg2d = t1ttbarSL2d.Clone("bkg")
	bkg2d.Add(t1ttbarFL2d,1)
	bkg2d.Add(t1wjets2d,1)
	bkg2d.Add(t1zjets2d,1)
	bkg2d.Add(singletopt12d,1)
	c2d1[j].cd()
	hist2d.Rebin2D(10,15)
	hist2d.GetYaxis().SetTitleOffset(0.8)
	hist2d.SetTitle(';Pt (leptonic top);Top Mass (hadronic top)')
	hist2d.SetStats(0)
	hist2d.Draw('colz')
	
	c2d1[j].Print( hist2dn+".root", 'root')
	c2d1[j].Print( hist2dn+".pdf", 'pdf')

	c2d2[j].cd()
	bkg2d.GetYaxis().SetTitleOffset(0.8)
	bkg2d.SetTitle(';Pt (leptonic top);Top Mass (hadronic top)')
	bkg2d.SetStats(0)
	bkg2d.Draw('colz')
	c2d2[j].Print( hist2dn+"_bkg.pdf", 'pdf')
	c2d2[j].Print( hist2dn+"_bkg.root", 'root')
	j+=1
if options.pt == 'high':
	t1titles = ["t1TopPtpresub","LeptonicTopPt","t1TopMassprekin","t1TopMasspostkin","t1TopMasspostnsj","t1TopMasspostminmass","t1TopPthighpt","TopPttype2"]
else:
	t1titles = ["t1TopPtpresub","LeptonicTopPt","t1TopMassprekin","t1TopMasspostkin","t1TopMasspostnsj","t1TopMasspostminmass","t1TopMassposttau32","t1TopMasspostbmax","t1TopPt","t1TopPttype2"]
t1axis = ["pt(top) (GeV/c)","pt(leptonic top) (GeV/c)","m(top) (GeV/c^{2})","m(top) (GeV/c^{2})","m(top) (GeV/c^{2})","m(top) (GeV/c^{2})","m(top) (GeV/c^{2})","m(top) (GeV/c^{2})","pt(top) (GeV/c)","pt(W+b) (GeV/c)"]
t1rebins = [5,5,10,10,10,10,10,10,15,5]
i=0
output = ROOT.TFile( "ttbarNewSel_weight.root", "recreate" )
output1 = ROOT.TFile( "ptlepNewSel_weight.root", "recreate" )
output.cd()
		    
if options.pt == 'high':
	t1hists = ["topTagptHistprecuts","ptlep","topcandmassprekin","topcandmasspostkin","topcandmasspostnsj","topcandmasspostminmass","topTagptHisthighpt"]
else:
	t1hists = ["topTagptHistprecuts","ptlep","topcandmassprekin","topcandmasspostkin","topcandmasspostnsj","topcandmasspostminmass","topcandmassposttau32","topcandmasspostbmax","topTagptHist"]
for t1hist in t1hists:
	t1data= fData.Get(t1hist)
	t1data.Sumw2()
	#t1ttbar= fTopMC.Get(t1hist)
	t1SLttbar= fTopSL.Get(t1hist)
	t1FLttbar= fTopFL.Get(t1hist)
		

	t1FLttbar.Scale(xs[3]*lumi/nEvents[3])
	t1SLttbar.Scale(xs[0]*lumi/nEvents[0])	

	t1wjets= fWMC.Get(t1hist)
	t1wjets.Scale(xs[1]*lumi/nEvents[1])
	t1zjets= fZJetsMC.Get(t1hist)

	singletopt1temp = fSingletop[0].Get(t1hist)
	singletopt1temp.Scale((stxs[0] / stnEvents[0]) * lumi)
	singletopt1temp.Rebin(t1rebins[i])
	singletopt1 = singletopt1temp.Clone("singletopt1")
	for ifile in range(1,len(fSingletop)):
		singletopt1temp = fSingletop[ifile].Get(t1hist)
		singletopt1temp.Scale((stxs[ifile] / stnEvents[ifile]) * lumi)
       	        singletopt1temp.Rebin(t1rebins[i])
		singletopt1.Add(singletopt1temp)
	singletopt1.SetMarkerStyle( 0 )
	singletopt1.SetFillColor( 6 )


	#t1ttbar.Scale(xs[0]*lumi/nEvents[0])
        t1zjets.Scale(xs[2]*lumi/nEvents[2])

	t1wjets.Rebin(t1rebins[i])
	t1zjets.Rebin(t1rebins[i])
	t1SLttbar.Rebin(t1rebins[i])
	t1FLttbar.Rebin(t1rebins[i])
	t1data.Rebin(t1rebins[i])

	t1SLttbar.SetFillColor( colors[0] )
	t1FLttbar.SetFillColor( 7 )
	t1wjets.SetFillColor( colors[1] )
	t1data.SetMarkerStyle( 8 ) 

	t1SLttbar.SetMarkerStyle( 0 )
	t1FLttbar.SetMarkerStyle( 0 )
	t1wjets.SetMarkerStyle( 0 )
	t1zjets.SetFillColor( 30 )
	t1zjets.SetMarkerStyle( 0 )
	if i==0:
		leg = ROOT.TLegend( 0.65, 0.65, 0.84, 0.84)
		leg.AddEntry( t1data,  'Data', 'p')
		leg.AddEntry( t1SLttbar, 'Semi-Leptonic t#bar{t}', 'f')
		leg.AddEntry( t1FLttbar, 'Fully-Leptonic t#bar{t}', 'f')
		leg.AddEntry( t1wjets, 'W+Jets', 'f')
		leg.AddEntry( t1zjets, 'Z+Jets', 'f')
		leg.AddEntry( singletopt1, 'Singletop', 'f')
		leg.SetFillColor(0)
		leg.SetBorderSize(0)

	hs = ROOT.THStack( 't1 BkgStack', 't1')

	hs.Add( t1zjets )
	hs.Add( singletopt1 )
	hs.Add( t1wjets )
	hs.Add( t1FLttbar )
	hs.Add( t1SLttbar )

        if i==0:
		output.cd()
		num = t1data.Clone("weight")
		den = hs.GetStack().Last().Clone("den")
                num.Divide(den)
		num.Write()
		
	print t1hist

	c = ROOT.TCanvas('ct1'+t1hist, 'ct1'+t1hist)
	t1data.SetTitle(';'+t1axis[i]+';Events')
	t1data.SetStats(0)
	t1data.Draw('e')

	t1data.SetMaximum( 1.8 * t1data.GetMaximum() )
	hs.Draw('same hist')
	t1data.GetYaxis().SetTitleOffset(0.8)
	t1data.Draw('e same')
        if (i==1) :
		output1.cd()
		leppptweight = t1data.Clone("lepptweight")
		leppptweight.Divide(hs.GetStack().Last())
		leppptweight.Write()
	if (i==8) :
		type1ptsig.Rebin(8)
		type1ptsig.SetLineStyle(2)
		type1ptsig.SetLineWidth(2)
		type1ptsig.Scale(t1data.Integral()/type1ptsig.Integral())
		leg.AddEntry( type1ptsig,'RSGluon at 2000GeV/c^{2}', 'l')
		type1ptsig.Draw("same hist")
		
	leg.Draw()
	prelim = ROOT.TLatex()
	prelim.SetTextFont(42)
	prelim.SetNDC()
	prelim.DrawLatex( 0.15, 0.91, "#scale[1.0]{CMS Preliminary #sqrt{s} = 8 TeV, 19.7 fb^{-1}}" )


	c.Print( 'semiLepMassNewSel_'+t1titles[i]+'.root', 'root')
	c.Print( 'semiLepMassNewSel_'+t1titles[i]+'.pdf', 'pdf')
	i+=1

