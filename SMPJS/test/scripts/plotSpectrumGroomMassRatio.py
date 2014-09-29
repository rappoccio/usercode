#!/bin/python


# ===================================================
#             plotJetSpectrum.py
#
# ===================================================
# ===================================================


from optparse import OptionParser


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
                  default='histAK7PtAvgVsMjetGroomOverReco',
                  dest='hist',
                  help='Histogram to plot')


parser.add_option('--title', metavar='H', type='string', action='store',
                  default='AK7 Jets, Data/PYTHIA6',
                  dest='title',
                  help='Histogram to plot')


parser.add_option('--grooms', metavar='H', type='string', action='append',
                  default=['Filtered', 'Trimmed', 'Pruned'],
                  dest='grooms',
                  help='Histogram to plot')


parser.add_option('--outname', metavar='D', type='string', action='store',
                  default='ratioPlots',
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

profs = []

fMC = TFile( options.inputFileMC + '.root' )

firstPlot = True
leg = TLegend(0.3, 0.6, 0.5, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)
for igroom in xrange(len(options.grooms)) :

    groom = options.grooms[igroom]

    print 'Processing groom = ' + groom

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
        hDatas.append(hist2D)

    hData2D = hDatas[0]
    for ihist in range(1,len(hDatas)):
        hData2D.Add( hDatas[ihist] )

    #hData2D.Draw("box")
    hData = hData2D.ProjectionX()
    hData.SetName(groom + '_datapfx')
    hData.Scale( 1.0 / hData.Integral() )

    #hData.SetMarkerStyle(20 + igroom)
    hData.SetMarkerStyle(1)
    hData.SetLineColor( colors[igroom] )
    hData.SetMarkerColor( colors[igroom] )
    hData.SetTitle( ';m_{jet}^{Groom} / m_{jet};Fraction')
    #for ibin in xrange(hData.GetNbinsX()) :
    #    hData.SetBinError(ibin, 0.001 )
    if firstPlot is True :
        hData.Draw('e hist')
        firstPlot = False
    else :
        hData.Draw('e hist same')
    hData.SetMinimum(0.0)
    hData.SetMaximum(0.14)
    hData.GetXaxis().SetRangeUser(0.0, 0.999)

    if groom == '' :
        mchist2D = fMC.Get(options.hist)
    else :
        mchist2D = fMC.Get(options.hist + '_' + groom)

    mchist2D.Sumw2()
    hMC = mchist2D.ProjectionX(  )
    hMC.Scale(1.0 / hMC.Integral() )
    hMC.SetName(groom + '_mcpx')

    #hMC.SetMarkerStyle(24 + igroom)
    hMC.SetMarkerStyle(1)
    hMC.SetLineColor( colors[igroom] )
    hMC.SetMarkerColor( colors[igroom] )
    hMC.SetLineStyle(2)
    hMC.SetLineWidth(2)
    hMC.Draw('e hist same')
    hMC.SetName(groom + '_mcpfx')
    profs.append( [hData, hMC] )
    leg.AddEntry( hData, groom + ' data', 'l')
    leg.AddEntry( hMC, groom + ' MC', 'l')
    leg.Draw()

text1 = TLatex()
text1.SetNDC()
text1.SetTextFont(42)
text1.DrawLatex(0.13,0.86, "#scale[1.0]{CMS Preliminary, L = 5 fb^{-1} at  #sqrt{s} = 7 TeV}")
texts.append(text1)


c.Print(options.hist + '_' + options.outname + '.png', 'png')
c.Print(options.hist + '_' + options.outname + '.pdf', 'pdf')

