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

f_nominal = TFile('../RootFiles_v5b/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8.root')

hist_PUup = 'pfShyftAnaPUup/Top_secvtxMass_'
hist_PUdn = 'pfShyftAnaPUdown/Top_secvtxMass_'
hist_nom  = 'pfShyftAna/Top_secvtxMass_'

hists_tag_nominal = []
hists_tag_jesup = []
hists_tag_PUup = []
hists_tag_PUdn = []

c1 = TCanvas('c1', 'c1')

# >= 1jets, >=1tags
for ijet in range(3,6) :
    for itag in range(1, min(ijet,2) + 1) :
        hist_tag_nominal = f_nominal.Get( hist_nom + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hist_tag_PUup   = f_nominal.Get( hist_PUup + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hist_tag_PUdn   = f_nominal.Get( hist_PUdn + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hists_tag_nominal.append( hist_tag_nominal )
        hists_tag_PUup.append( hist_tag_PUup )
        hists_tag_PUdn.append( hist_tag_PUdn )

hist_tag_nominal_sum = hists_tag_nominal[0]
for hist in range(1,len(hists_tag_nominal)):
    hist_tag_nominal_sum.Add( hists_tag_nominal[hist] )

hist_tag_PUup_sum = hists_tag_PUup[0]
for hist in range(1,len(hists_tag_PUup)):
    hist_tag_PUup_sum.Add( hists_tag_PUup[hist] )

hist_tag_PUdn_sum = hists_tag_PUdn[0]
for hist in range(1,len(hists_tag_PUdn)):
    hist_tag_PUdn_sum.Add( hists_tag_PUdn[hist] )

hist_tag_nominal_sum.Sumw2()
hist_tag_nominal_sum.Scale( 1.0 / hist_tag_nominal_sum.GetEntries() )
hist_tag_nominal_sum.SetLineColor(1)
hist_tag_nominal_sum.SetTitle(';SVM (GeV);Number (arbs)')
hist_tag_nominal_sum.GetXaxis().SetRangeUser(0., 6.)
hist_tag_nominal_sum.Draw('hist')

hist_tag_PUup_sum.Sumw2()
hist_tag_PUup_sum.Scale( 1.0 / hist_tag_PUup_sum.GetEntries() )
hist_tag_PUup_sum.SetLineColor(2)
hist_tag_PUup_sum.Draw('same hist')

hist_tag_PUdn_sum.Sumw2()
hist_tag_PUdn_sum.Scale( 1.0 / hist_tag_PUdn_sum.GetEntries() )
hist_tag_PUdn_sum.SetLineColor(kBlue)
hist_tag_PUdn_sum.Draw('same hist')

leg = TLegend(0.6, 0.6, 0.84, 0.84)
leg.SetBorderSize(0)
leg.SetFillColor(0)

leg.AddEntry(hist_tag_PUup_sum, 'Pileup Up', 'l')
leg.AddEntry(hist_tag_PUdn_sum, 'Pileup Down', 'l')
leg.AddEntry(hist_tag_nominal_sum, 'Nominal', 'l')
leg.Draw()

latex = TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.6,0.96, "CMS Preliminary")
#c1.Print('pileup_sys_mass_ele_EB.png', 'png')
c1.Print('pileup_sys_mass_ele_EB.pdf', 'pdf')
