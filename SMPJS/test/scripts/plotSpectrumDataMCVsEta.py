#!/bin/python


# ===================================================
#             plotJetSpectrum.py
#
# ===================================================
# ===================================================


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFileData', metavar='F', type='string', action='store',
                  default='Jet_Run2011_plots.root',
                  dest='inputFileData',
                  help='Input file for data')

parser.add_option('--inputFileMC', metavar='F', type='string', action='append',
                  default=['QCD_pythia6_z2_v10beta_plots.root'],
                  dest='inputFileMC',
                  help='Input file for MC')


parser.add_option('--hist', metavar='H', type='string', action='store',
                  default='histAK7MjjVsEtaMax',
                  dest='hist',
                  help='Histogram to plot')


parser.add_option('--title', metavar='H', type='string', action='store',
                  default='AK7 Jets, Data/PYTHIA6',
                  dest='title',
                  help='Histogram to plot')


parser.add_option('--groom', metavar='H', type='string', action='store',
                  default=None,
                  dest='groom',
                  help='Histogram to plot')


parser.add_option('--outname', metavar='D', type='string', action='store',
                  default='rawDataMCComparisons',
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

if options.groom is None :
    fout = TFile(options.outname + '_' + options.hist + '.root', 'recreate')
else :
    fout = TFile(options.outname + '_' + options.hist + '_' + options.groom + '.root', 'recreate')

hists2D = []
mchists2D = []
hists = []
canvs = []
legs = []
stacks = []
files = []

histsToWrite = []

gStyle.SetOptStat(000000)

etas = [
    [0.0,0.5],
    [0.5,1.0],
    [1.0,1.5],
    [1.5,2.0],
    [2.0,2.5],
    ]

colors = [ 2, 4 ]

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

    # Data
    prependstr = ''
    if options.groom is not None :
        prependstr = options.groom + ' '
    hs = THStack( options.hist + '_hs', prependstr + options.title + ', ' + str(ieta[0]) + ' < |#eta| < ' + str(ieta[1]) + ';' + massStr + ' (GeV);Number')
    hDatas = []
    for iitrig in xrange(len(trigs) -1, -1, -1) :
        itrig = trigs[iitrig]
        if options.groom is not None:
            hist2D = fData.Get(options.hist + '_' + itrig + '_' + options.groom)
        else:
            hist2D = fData.Get(options.hist + '_' + itrig )
        hists2D.append( hist2D )
        bin0 = hist2D.GetYaxis().FindBin( ieta[0] )
        bin1 = hist2D.GetYaxis().FindBin( ieta[1] )
        hist = hist2D.ProjectionX( hist2D.GetName() + str(iieta), bin0, bin0 )
        hist.Scale( normalizations[iitrig] )
        hists.append(hist)
        hDatas.append(hist)

    hData = hDatas[0]
    for ihist in range(1,len(hDatas)):
        hData.Add( hDatas[ihist] )
    hData.SetMarkerStyle(20)
    hData.SetName('jetdata_' + str(iieta))
    hData.SetTitle(prependstr +  options.title + ', ' + str(ieta[0]) + ' < |#eta_{max}| < ' + str(ieta[1])  + ';' + massStr + ' (GeV);Number')
    hData.Draw('e')
    histsToWrite.append(hData)
    
    # MC
    hMCs = []
    for iMC in range(0,len(options.inputFileMC)) :
        fMC = TFile( options.inputFileMC[iMC] )
        if options.groom is None :
            mchist2D = fMC.Get(options.hist)
        else :
            mchist2D = fMC.Get(options.hist + '_' + options.groom)
        mchists2D.append( mchist2D )
        mcbin0 = mchist2D.GetYaxis().FindBin( ieta[0] )
        mcbin1 = mchist2D.GetYaxis().FindBin( ieta[1] )
        hMC = mchist2D.ProjectionX( 'mcpx_' + str(iieta) + str(iMC), mcbin0, mcbin0 )
        hMC.SetFillColor(17)
        #hMC.SetLineColor( colors[iMC]  )
        #hMC.SetLineWidth(3)

        hMC.Scale( hData.Integral() / hMC.Integral() )
        hists.append( hMC )

        hMC.Draw('hist same')
        hMCs.append(hMC)
        files.append(fMC)

    c.SetLogy()
    hData.Draw("e same")
    hData.SetMinimum(1e-1)
    leg.Draw()
    canvs.append(c)
    legs.append(leg)
    stacks.append(hs)
    appendstr = ''
    if options.groom is None :
        c.Print(options.hist + '_' + options.outname + '_eta_' + str(iieta) + '.png', 'png')
        c.Print(options.hist + '_' + options.outname + '_eta_' + str(iieta) + '.pdf', 'pdf')
    else :
        c.Print(options.hist + '_' + options.outname + '_eta_' + str(iieta) + '_' + options.groom + '.png', 'png')
        c.Print(options.hist + '_' + options.outname + '_eta_' + str(iieta) + '_' + options.groom + '.pdf', 'pdf')


fout.cd()

for ihist in histsToWrite :
    ihist.Write()

#fout.Close()
