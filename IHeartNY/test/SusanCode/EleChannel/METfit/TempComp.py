#! /usr/bin/env python
import os
from math import *

import ROOT
ROOT.gROOT.Macro("rootlogon.C")

import sys

fTop = [
ROOT.TFile("TTjets_POWHEG_Var.root"),
ROOT.TFile("St_tW_Var.root"),
ROOT.TFile("St_tWB_Var.root"),
ROOT.TFile("St_t_Var.root"),
ROOT.TFile("St_tB_Var.root"),
ROOT.TFile("St_s_Var.root"),
ROOT.TFile("St_sB_Var.root")
]

flist = [
ROOT.TFile("Data_Var.root"),
ROOT.TFile("QCD_old_Var.root"),
ROOT.TFile("QCD_loose_Var.root"),
ROOT.TFile("QCD_btag_Var.root")
]

filename = [
"Data",
"QCD_old",
"QCD_loose",
"QCD_btag"
]

hists = ["histMET", 
         "histMETnjet", 
         "histMETbtag",
         "histMETnsj", 
         "histMETminm", 
         "histMETmass",
	 "histMETtoppt", 
         "histMETtop"]

histname = ["full sel",
            "no njets cut",
            "no btag cut",
            "no nsj cut",
            "no minm cut",
            "no topm cut",
            "no toppt cut",
            "no top cuts"]

colors = [
    ROOT.kRed,
    ROOT.kOrange,
    ROOT.kYellow,
    ROOT.kGreen,
    ROOT.kCyan,
    ROOT.kBlue,
    ROOT.kViolet,
    ROOT.kMagenta
    ]

canvs = []

nEvents = [
    21560109.,#TTbar
    495559.,  #St_tW
    491463.,  #St_tWB
    3748155., #St_t
    1930185., #St_tB
    259176.,  #St_s
    139604.,  #St_sB
]

xs = [
    234. * 0.97 * 0.93, #TTbar
    11.1 * 0.97 * 0.93, #St_tW
    11.1 * 0.97 * 0.93, #St_tWB
    56.4 * 0.97 * 0.93, #St_t
    30.7 * 0.97 * 0.93, #St_tB
    3.79 * 0.97 * 0.93, #St_s
    1.76 * 0.97 * 0.93, #St_sB
]

# Using SingleEle A, B, C, Cextra, D
lumi = 19748.

ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetOptFit(0000)

###########################
# Do inter-QCD comparison #
###########################

# Get top template
hTopMC = fTop[0].Get("histMET").Clone()
hTopMC.Scale( (xs[0] / nEvents[0]) * lumi)
for ifile in range(1, len(fTop)):
    toptemp = fTop[ifile].Get("histMET").Clone()
    toptemp.Scale((xs[ifile] / nEvents[ifile]) * lumi)
    hTopMC.Add(toptemp)
if hTopMC.Integral() > 0.:
    hTopMC.Scale(1. / hTopMC.Integral())
hTopMC.SetLineColor(ROOT.kRed)
hTopMC.SetLineWidth(5)

# Get old QCD template
fQCDold = ROOT.TFile("QCD_old_Var.root")
hQCDold = fQCDold.Get("histMET").Clone()
if hQCDold.Integral() > 0.:
    hQCDold.Scale(1. / hQCDold.Integral())
hQCDold.SetLineColor(ROOT.kGreen+3)
hQCDold.SetLineWidth(5)

# Get loose QCD template
fQCDloose = ROOT.TFile("QCD_loose_Var.root")
hQCDloose = fQCDloose.Get("histMET").Clone()
if hQCDloose.Integral() > 0.:
    hQCDloose.Scale(1. / hQCDloose.Integral())
hQCDloose.SetLineColor(ROOT.kBlue)
hQCDloose.SetLineWidth(5)

# Get 0 btag QCD template
fQCDbtag = ROOT.TFile("QCD_btag_Var.root")
hQCDbtag = fQCDbtag.Get("histMET").Clone()
if hQCDbtag.Integral() > 0.:
    hQCDbtag.Scale(1. / hQCDbtag.Integral())
hQCDbtag.SetLineColor(ROOT.kViolet)
hQCDbtag.SetLineWidth(5)

leg1 = ROOT.TLegend( 0.7, 0.65, 0.9, 0.85)
leg1.AddEntry( hTopMC, 't#bar{t}', 'l')
leg1.AddEntry( hQCDold, 'QCD old', 'l')
leg1.AddEntry( hQCDloose, 'QCD loose', 'l')
leg1.AddEntry( hQCDbtag, 'QCD btag', 'l')
            
leg1.SetFillColor(0)
leg1.SetBorderSize(0)

c1 = ROOT.TCanvas('c1', 'c1')
hTopMC.Draw()
hTopMC.SetMaximum( 0.1 )
hQCDold.Draw('same')
hQCDloose.Draw('same')
hQCDbtag.Draw('same')

c1.RedrawAxis()

leg1.Draw()

c1.Print( 'QCDcomp.png', 'png')

##########################
# Do template comparison #
##########################

#Data

leg2 = ROOT.TLegend( 0.7, 0.65, 0.9, 0.85)

c2 = ROOT.TCanvas('c2', 'c2')

hAll = flist[0].Get(hists[0]).Clone()
hAll.SetTitle("Template shape comparison")
if hAll.Integral() > 0. :
    hAll.Scale(1. / hAll.Integral())
hAll.SetLineColor(colors[0])
hAll.SetLineWidth(5)

hNjet = flist[0].Get(hists[1]).Clone()
hNjet.SetTitle("Template shape comparison")
if hNjet.Integral() > 0. :
    hNjet.Scale(1. / hNjet.Integral())
hNjet.SetLineColor(colors[1])
hNjet.SetLineWidth(5)

hBtag = flist[0].Get(hists[2]).Clone()
hBtag.SetTitle("Template shape comparison")
if hBtag.Integral() > 0. :
    hBtag.Scale(1. / hBtag.Integral())
hBtag.SetLineColor(colors[2])
hBtag.SetLineWidth(5)

hNsj = flist[0].Get(hists[3]).Clone()
hNsj.SetTitle("Template shape comparison")
if hNsj.Integral() > 0. :
    hNsj.Scale(1. / hNsj.Integral())
hNsj.SetLineColor(colors[3])
hNsj.SetLineWidth(5)

hMinm = flist[0].Get(hists[4]).Clone()
hMinm.SetTitle("Template shape comparison")
if hMinm.Integral() > 0. :
    hMinm.Scale(1. / hMinm.Integral())
hMinm.SetLineColor(colors[4])
hMinm.SetLineWidth(5)

hMass = flist[0].Get(hists[5]).Clone()
hMass.SetTitle("Template shape comparison")
if hMass.Integral() > 0. :
    hMass.Scale(1. / hMass.Integral())
hMass.SetLineColor(colors[5])
hMass.SetLineWidth(5)

hToppt = flist[0].Get(hists[6]).Clone()
hToppt.SetTitle("Template shape comparison")
if hToppt.Integral() > 0. :
    hToppt.Scale(1. / hToppt.Integral())
hToppt.SetLineColor(colors[6])
hToppt.SetLineWidth(5)

hTop = flist[0].Get(hists[7]).Clone()
hTop.SetTitle("Template shape comparison")
if hTop.Integral() > 0. :
    hTop.Scale(1. / hTop.Integral())
hTop.SetLineColor(colors[7])
hTop.SetLineWidth(5)

leg2.AddEntry( hAll, "Full sel", 'l')
#leg2.AddEntry( hNjet, "No njets cut", 'l')
#leg2.AddEntry( hBtag, "No btag cut", 'l')
leg2.AddEntry( hNsj, "No nsj cut", 'l')
#leg2.AddEntry( hMinm, "No minmass cut", 'l')
#leg2.AddEntry( hMass, "No top mass cut", 'l')
#leg2.AddEntry( hToppt, "No top pt cut", 'l')
#leg2.AddEntry( hTop, "No top cuts", 'l')
leg2.SetFillColor(0)
leg2.SetBorderSize(0)

hAll.Draw()
#hNjet.Draw("same")
#hBtag.Draw("same")
hNsj.Draw("same")
#hMinm.Draw("same")
#hMass.Draw("same")
#hToppt.Draw("same")
#hTop.Draw("same")

#c2.RedrawAxis()
            
leg2.Draw()

c2.Print( 'DataComp.png', 'png')
