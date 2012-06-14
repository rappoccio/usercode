#!/bin/python


# ===================================================
#             plotJetSpectrum.py
#
# ===================================================
# ===================================================


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFile', metavar='F', type='string', action='store',
                  default='Jet_Run2011_plots.root',
                  dest='inputFile',
                  help='Input file')


parser.add_option('--hist', metavar='H', type='string', action='store',
                  default='histAK7MjjVsEtaMax',
                  dest='hist',
                  help='Histogram to plot')


parser.add_option('--outname', metavar='D', type='string', action='store',
                  default='Jet_Run2011',
                  dest='outname',
                  help='Output name')


(options, args) = parser.parse_args()

argv = []

from ROOT import *

gROOT.Macro("rootlogon.C")


trigs = [
    'HLT_Jet60',
    'HLT_Jet110',
    'HLT_Jet190',
    'HLT_Jet240',
    'HLT_Jet370'
    ]

colors = [
    2, 3, 4, 5, 6
    ]

normalizations = [
#    10439., 647., 28.9, 8.6, 1.0
    12300, 690, 32.9, 9.6, 1.0
    ]

f = TFile( options.inputFile )

hists2D = []
hists = []
canvs = []
legs = []
stacks = []

gStyle.SetOptStat(000000)

etas = [
    [0.0,0.5],
    [0.5,1.0],
    [1.0,1.5],
    [1.5,2.0],
    [2.0,2.5],
    ]

for iieta in range(0,len(etas)):

    ieta = etas[iieta]

    leg = TLegend(0.3, 0.86, 0.6, 1.0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)



    c = TCanvas('c' + str(iieta), 'c' + str(iieta))
    if options.hist.find('Mjet') < 0 :
        massStr = 'm_{jj}'
    else :
        massStr = 'm_{jet}'
    hs = THStack( options.hist + '_hs', str(ieta[0]) + ' < |#eta| < ' + str(ieta[1]) + ';' + massStr + ' (GeV);Number')
    for iitrig in xrange(len(trigs) -1, -1, -1) :
        itrig = trigs[iitrig]
        hist2D = f.Get(options.hist + '_' + itrig)
        hists2D.append( hist2D )
        bin0 = hist2D.GetYaxis().FindBin( ieta[0] )
        bin1 = hist2D.GetYaxis().FindBin( ieta[1] )
        hist = hist2D.ProjectionX( 'px_' + str(iieta) + '_' + itrig, bin0, bin0 )
        hist.SetFillColor( colors[iitrig] )
        hist.Scale( normalizations[iitrig] )
        hists.append(hist)
        hs.Add( hist )
        leg.AddEntry( hist, trigs[iitrig], 'f')
    hs.Draw('hist')
    c.SetLogy()
    hs.SetMinimum(1e-1)
    leg.Draw()
    stacks.append(hs)
    canvs.append(c)
    legs.append(leg)
    c.Print(options.hist + '_raw_eta_' + str(iieta) + '.png', 'png')
    c.Print(options.hist + '_raw_eta_' + str(iieta) + '.pdf', 'pdf')
