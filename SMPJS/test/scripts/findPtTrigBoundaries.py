#!/bin/python


# ===================================================
#             plotJetSpectrum.py
#
# ===================================================
# ===================================================


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFile', metavar='F', type='string', action='store',
                  default="Jet_dijetTriggerAna.root",
                  dest='inputFile',
                  help='Input file')


(options, args) = parser.parse_args()

argv = []

from ROOT import *

gROOT.Macro("rootlogon.C")


histsToWrite = []

gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
#gStyle.SetTitleFontSize(0.05)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(3.5, "X")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")


f = TFile(options.inputFile)

dirs = [
    'jet110Trigger',
    'jet190Trigger',
    'jet240Trigger',
    'jet370Trigger'
    ]


xbins = [
    [ 40.0,350.0],
    [ 90.0,400.0],
    [180.0,500.0],
    [250.0,650.0]
    ]

hists = []
canvs = []
leg = TLegend(0.86, 0.5, 1.0, 1.0 )
leg.SetFillColor(0)
leg.SetBorderSize(0)

cuts = [150., 220., 300., 450.]

hs = THStack("hs", "hs")
l = TLine()
l.SetLineWidth(2)

for itrig in range(0,len(dirs)):
    h1 = f.Get( dirs[itrig] + '/jetPtNum' )
    h2 = f.Get( dirs[itrig] + '/jetPtDen' )
    h1.Sumw2()
    h2.Sumw2()

    heff = h1
    heff.Divide( h1, h2, 1.0, 1.0, 'B')
    heff.SetTitle( dirs[itrig] + ';p_{T}^{AVG} (GeV);Efficiency')

    c = TCanvas('c' + str(itrig), 'c' + str(itrig))
    heff.SetMarkerStyle(20)
    heff.Draw("e")
    heff.GetXaxis().SetRangeUser( xbins[itrig][0], xbins[itrig][1])
    heff.GetYaxis().SetRangeUser(0,1)

    l.DrawLine(cuts[itrig], 0., cuts[itrig], 1.0)
    canvs.append(c)
    hists.append([heff,h1,h2])
    c.Print('efficiency_' + dirs[itrig] +'.png', 'png')
    c.Print('efficiency_' + dirs[itrig] +'.pdf', 'pdf')
