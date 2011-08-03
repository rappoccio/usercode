#!/bin/python

from ROOT import *
from array import *
from setTDRStyle import *
setTDRStyle()

#gROOT.Macro("~/rootlogon.C")
gStyle.SetTitleFillColor(10)
gStyle.SetTitleBorderSize(0)
gStyle.SetOptStat(000000)

f = TFile('../RootFiles_v5/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8.root')

leg = TLegend(0.65, 0.65, 0.88, 0.88)
leg.SetBorderSize(0)
leg.SetFillColor(0)

c1 = TCanvas('c1', 'c1')
h_njets_1 = f.Get('pfShyftAnaJER000/nJets')
h_njets_2 = f.Get('pfShyftAna/nJets')
h_njets_3 = f.Get('pfShyftAnaJER020/nJets')

h_njets_3.SetTitle("")
h_njets_3.GetXaxis().SetTitle("N_{Jets}; p_{T} > 30 GeV, |#eta| < 2.4")

h_njets_3.SetLineColor(4)
h_njets_2.SetLineColor(1)
h_njets_1.SetLineColor(2)

leg.AddEntry(h_njets_3, 'JER + 20%', 'l')
leg.AddEntry(h_njets_2, 'JER + 10%', 'l')
leg.AddEntry(h_njets_1, 'JER + 0%', 'l')

h_njets_3.Draw('hist')
h_njets_2.Draw('hist same')
h_njets_1.Draw('hist same')
leg.Draw()
#c1.Print('jer_sys_njets.png', 'png')
c1.Print('jer_sys_njets.pdf', 'pdf')

c2 = TCanvas('c2', 'c2')
h_jet1Pt_1 = f.Get('pfShyftAnaJER000/jet1Pt')
h_jet1Pt_2 = f.Get('pfShyftAna/jet1Pt')
h_jet1Pt_3 = f.Get('pfShyftAnaJER020/jet1Pt')

h_jet1Pt_1.Rebin(5)
h_jet1Pt_2.Rebin(5)
h_jet1Pt_3.Rebin(5)

h_jet1Pt_3.SetTitle("")
h_jet1Pt_3.GetXaxis().SetTitle("Jet 1; p_{T} (GeV/c)")

h_jet1Pt_3.SetLineColor(4)
h_jet1Pt_2.SetLineColor(1)
h_jet1Pt_1.SetLineColor(2)

h_jet1Pt_3.Draw('hist')
h_jet1Pt_2.Draw('hist same')
h_jet1Pt_1.Draw('hist same')
leg.Draw()

latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.6,0.96, "CMS Preliminary")
#c2.Print('jer_sys_jet1Pt_ele.png', 'png')
c2.Print('jer_sys_jet1Pt_ele.pdf', 'pdf')


c3 = TCanvas('c3', 'c3')
h_jet2Pt_1 = f.Get('pfShyftAnaJER000/jet2Pt')
h_jet2Pt_2 = f.Get('pfShyftAna/jet2Pt')
h_jet2Pt_3 = f.Get('pfShyftAnaJER020/jet2Pt')

h_jet2Pt_1.Rebin(5)
h_jet2Pt_2.Rebin(5)
h_jet2Pt_3.Rebin(5)

h_jet2Pt_3.SetTitle("")
h_jet2Pt_3.GetXaxis().SetTitle("Jet 2; p_{T} (GeV/c)")

h_jet2Pt_3.SetLineColor(4)
h_jet2Pt_2.SetLineColor(1)
h_jet2Pt_1.SetLineColor(2)

h_jet2Pt_3.Draw('hist')
h_jet2Pt_2.Draw('hist same')
h_jet2Pt_1.Draw('hist same')
leg.Draw()
latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.6,0.96, "CMS Preliminary")
#c3.Print('jer_sys_jet2Pt_ele.png', 'png')
c3.Print('jer_sys_jet2Pt_ele.pdf', 'pdf')

c4 = TCanvas('c4', 'c4')
h_jet3Pt_1 = f.Get('pfShyftAnaJER000/jet3Pt')
h_jet3Pt_2 = f.Get('pfShyftAna/jet3Pt')
h_jet3Pt_3 = f.Get('pfShyftAnaJER020/jet3Pt')

h_jet3Pt_1.Rebin(5)
h_jet3Pt_2.Rebin(5)
h_jet3Pt_3.Rebin(5)

h_jet3Pt_3.SetTitle("")
h_jet3Pt_3.GetXaxis().SetTitle("Jet 3; p_{T} (GeV/c)")

h_jet3Pt_3.SetLineColor(4)
h_jet3Pt_2.SetLineColor(1)
h_jet3Pt_1.SetLineColor(2)

h_jet3Pt_3.Draw('hist')
h_jet3Pt_2.Draw('hist same')
h_jet3Pt_1.Draw('hist same')
leg.Draw()
latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.6,0.96, "CMS Preliminary" )
#c4.Print('jer_sys_jet3Pt_ele.png', 'png')
c4.Print('jer_sys_jet3Pt_ele.pdf', 'pdf')


c5 = TCanvas('c5', 'c5')
h_jet4Pt_1 = f.Get('pfShyftAnaJER000/jet4Pt')
h_jet4Pt_2 = f.Get('pfShyftAna/jet4Pt')
h_jet4Pt_3 = f.Get('pfShyftAnaJER020/jet4Pt')

h_jet4Pt_1.Rebin(5)
h_jet4Pt_2.Rebin(5)
h_jet4Pt_3.Rebin(5)

h_jet4Pt_3.SetTitle("")
h_jet4Pt_3.GetXaxis().SetTitle("Jet 4; p_{T} (GeV/c)")

h_jet4Pt_3.SetLineColor(4)
h_jet4Pt_2.SetLineColor(1)
h_jet4Pt_1.SetLineColor(2)

h_jet4Pt_3.Draw('hist')
h_jet4Pt_2.Draw('hist same')
h_jet4Pt_1.Draw('hist same')
leg.Draw()
latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.6,0.96, "CMS Preliminary")
#latex.DrawLatex(0.6,0.92,"#int Ldt = 771 pb^{-1}")
#c5.Print('jer_sys_jet4Pt_ele.png', 'png')
c5.Print('jer_sys_jet4Pt_ele.pdf', 'pdf')


c6 = TCanvas('c6', 'c6')
h_metPt_1 = f.Get('pfShyftAnaJER000/metPt')
h_metPt_2 = f.Get('pfShyftAna/metPt')
h_metPt_3 = f.Get('pfShyftAnaJER020/metPt')

h_metPt_1.Rebin(5)
h_metPt_2.Rebin(5)
h_metPt_3.Rebin(5)

h_metPt_3.SetLineColor(4)
h_metPt_2.SetLineColor(1)
h_metPt_1.SetLineColor(2)

h_metPt_3.SetTitle("")
h_metPt_3.GetXaxis().SetTitle("#slash{E}_{T}(GeV/c)")

h_metPt_3.Draw('hist')
h_metPt_2.Draw('hist same')
h_metPt_1.Draw('hist same')
leg.Draw()
latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.6,0.96, "CMS Preliminary")
#c6.Print('jer_sys_metPt_ele.png', 'png')
c6.Print('jer_sys_metPt_ele.pdf', 'pdf')
