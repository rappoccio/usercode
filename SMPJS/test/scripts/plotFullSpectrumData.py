#!/bin/python


# ===================================================
#             plotJetSpectrum.py
#
# ===================================================
# ===================================================


from optparse import OptionParser

from array import *

parser = OptionParser()

parser.add_option('--inputFileData', metavar='F', type='string', action='store',
                  default='Jet_plots_nominal.root',
                  dest='inputFileData',
                  help='Input file for data')

parser.add_option('--inputFileMC', metavar='F', type='string', action='store',
                  default='QCD_pythia6_z2_plots_nominal',
                  dest='inputFileMC',
                  help='Input file for MC')


parser.add_option('--hist', metavar='H', type='string', action='store',
                  default='histAK7MjetVsNvtx',
                  dest='hist',
                  help='Histogram to plot')


parser.add_option('--title', metavar='H', type='string', action='store',
                  default='AK7 Jets, Data/PYTHIA6',
                  dest='title',
                  help='Histogram to plot')


parser.add_option('--grooms', metavar='H', type='string', action='append',
                  default=['', 'Filtered', 'Trimmed', 'Pruned'],
                  dest='grooms',
                  help='Histogram to plot')


parser.add_option('--outname', metavar='D', type='string', action='store',
                  default='nvtxPlots',
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

normalizations = [
#    10439., 647., 28.9, 8.6, 1.0
    12300, 690, 32.9, 9.6, 1.0
    ]



fData = TFile( options.inputFileData )


hists2D = []
mchists2D = []
hists = []
canvs = []
legs = []
stacks = []
files = []
pads = []
texts = []

histsToWrite = []

gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
#gStyle.SetTitleFontSize(0.05)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(3.5, "X")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")

c = TCanvas('c', 'c')

colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen + 2 ]
markersData = [20,21,22,29]
markersMC = [24,25,26,30] 
profs = []

fMC = TFile( options.inputFileMC + '.root' )

graphs = []

firstPlot = True
leg = TLegend(0.86, 0.3, 1.0, 0.84 )
leg.SetFillColor(0)
leg.SetBorderSize(0)
#for igroom in xrange(len(options.grooms)) :
for igroom in range(0,4) :

    groom = options.grooms[igroom]

    print 'Processing groom = ' + groom

    xvals =  array('d', [])
    exvals =  array('d', [])
    yvals_data =  array('d', [])
    eyvals_data =  array('d', [])
    yvals_mc =  array('d', [])
    eyvals_mc =  array('d', [])

    hDatas = []
    for iitrig in xrange(len(trigs) -1, -1, -1) :
        itrig = trigs[iitrig]
        if groom != '':
            hist2D = fData.Get(options.hist + '_' + itrig + '_' + groom)
        else:
            hist2D = fData.Get(options.hist + '_' + itrig )
        hists2D.append( hist2D )
        hist2D.Sumw2()
        hist2D.Scale( normalizations[iitrig] )


    hData2D = hists2D[0]
    for ihist in range(1,len(hists2D)):
        hData2D.Add( hists2D[ihist] )

    
    hData2D.Scale( 1.0 / hData2D.Integral() )
    #hData2D.Draw("box")
    hData = hData2D.ProjectionY()
    hData.SetName( groom + '_datapfx')

    if groom == '' :
        mchist2D = fMC.Get(options.hist)
    else :
        mchist2D = fMC.Get(options.hist + '_' + groom)

    mchist2D.Sumw2()
    mchist2D.Scale( 1.0 / mchist2D.Integral() )
    hMC = mchist2D.ProjectionY()
    
    hMC.SetName( groom + '_mcpfx' )

    hData.SetLineColor(igroom + 1)
    hMC.SetLineColor(igroom + 1)

    hData.SetLineStyle(1)
    hMC.SetLineStyle(2)

    if igroom == 0 :
        hData.Draw('hist')
    else :
        hData.Draw('hist same')
    hMC.Draw('hist same')
        
