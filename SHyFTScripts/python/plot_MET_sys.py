#!/bin/python

from ROOT import *
from array import *
from setTDRStyle import *
setTDRStyle()
#gROOT.Macro("~/rootlogon.C")
#gStyle.SetCanvasColor(10)
#gStyle.SetStatColor(10)
gStyle.SetTitleFillColor(10)
gStyle.SetTitleBorderSize(0)
gStyle.SetOptStat(000000)

f = TFile('../RootFiles_v5/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8.root')

leg = TLegend(0.65, 0.65, 0.88, 0.88)
leg.SetBorderSize(0)
leg.SetFillColor(0)

c1 = TCanvas('c1', 'c1')
h_njets_1 = f.Get('pfShyftAnaMETRES090/nJets')
h_njets_2 = f.Get('pfShyftAna/nJets')
h_njets_3 = f.Get('pfShyftAnaMETRES110/nJets')

h_njets_3.SetTitle("")
h_njets_3.GetXaxis().SetTitle("N_{Jets}; p_{T} > 30 GeV, |#eta| < 2.4")

h_njets_3.SetLineColor(4)
h_njets_2.SetLineColor(1)
h_njets_1.SetLineColor(2)

leg.AddEntry(h_njets_3, '0.9', 'l')
leg.AddEntry(h_njets_2, '1.0', 'l')
leg.AddEntry(h_njets_1, '1.1', 'l')

h_njets_3.Draw('hist')
h_njets_2.Draw('hist same')
h_njets_1.Draw('hist same')
leg.Draw()

latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.6,0.96, "CMS Preliminary")
#latex.DrawLatex(0.6,0.92,"#int Ldt = 771 pb^{-1}")

#c1.Print('unclmet_sys_njets_ele.png', 'png')
c1.Print('unclmet_sys_njets_ele.pdf', 'pdf')


c5 = TCanvas('c5', 'c5')
h_metPt_1 = f.Get('pfShyftAnaMETRES090/metPt')
h_metPt_2 = f.Get('pfShyftAna/metPt')
h_metPt_3 = f.Get('pfShyftAnaMETRES110/metPt')

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
#latex.DrawLatex(0.6,0.92,"#int Ldt = 771 pb^{-1}")
#c5.Print('unclmet_sys_metPt_ele.png', 'png')
c5.Print('unclmet_sys_metPt_ele.pdf', 'pdf')
