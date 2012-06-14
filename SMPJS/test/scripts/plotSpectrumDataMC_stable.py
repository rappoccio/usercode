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

parser.add_option('--inputFileMC', metavar='F', type='string', action='append',
                  default=[ 'QCD_pythia6_z2_plots_nominal',
                            'QCD_pythia8_4c_plots_nominal',
                            'QCD_herwigpp_23_plots_nominal',
                            'QCD_pythia6_z2_plots_jardn',
                            'QCD_pythia6_z2_plots_jarup',
                            'QCD_pythia6_z2_plots_jecdn',
                            'QCD_pythia6_z2_plots_jecup',
                            'QCD_pythia6_z2_plots_jerdn',
                            'QCD_pythia6_z2_plots_jerup',
                            'QCD_pythia6_z2_plots_puDn',
                            'QCD_pythia6_z2_plots_puNominal',
                            'QCD_pythia6_z2_plots_puUp'
                            ],
                  dest='inputFileMC',
                  help='Input file for MC')


parser.add_option('--hist', metavar='H', type='string', action='store',
                  default='histAK7MjetVsPtAvg',
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

xs = [ 2.21000008E10, 2.50999992E10, 2.31000003E10]
ntot = [ 10960800., 1060650. , 10430351. ]
lum = 4067.

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

pts = [
  [   0.,  50.],
  [  50., 125.],
  [ 125., 200.],
  [ 200., 300.],
  [ 300., 400.],
  [ 400., 500.],
  [ 500., 600.],
  [ 600., 800.],
  [ 800.,1000.],
  [1000.,1500.]
  ]

colors = [ 1, 2, 4 ]
widths = [ 1, 1, 2 ]
styles = [ 1, 2, 3 ]

titles = ['PYTHIA6', 'PYTHIA8', 'HERWIG++']

mcNorms = []


for iipt in range(0,len(pts)):

    ipt = pts[iipt]

    leg = TLegend(0.7, 0.86, 1.0, 1.0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)



    c = TCanvas('c' + str(iipt), 'c' + str(iipt))
    if options.hist.find('Mjet') < 0 :
        massStr = 'm_{jj}'
    else :
        massStr = 'm_{jet}'

    # Data
    prependstr = ''
    if options.groom is not None :
        prependstr = options.groom + ' '
    hs = THStack( options.hist + '_hs', prependstr + options.title + ', ' + str(ipt[0]) + ' < p_{T}^{AVG} < ' + str(ipt[1]) + ';' + massStr + ' (GeV);Number')
    hDatas = []
    for iitrig in xrange(len(trigs) -1, -1, -1) :
        itrig = trigs[iitrig]
        if options.groom is not None:
            hist2D = fData.Get(options.hist + '_' + itrig + '_' + options.groom)
        else:
            hist2D = fData.Get(options.hist + '_' + itrig )
        hists2D.append( hist2D )
        bin0 = hist2D.GetYaxis().FindBin( ipt[0] )
        bin1 = hist2D.GetYaxis().FindBin( ipt[1] ) - 1
        print 'Integrating trigger ' + itrig + ', bin0 = ' + str(bin0) + ', bin1 = ' + str(bin1)
        hist = hist2D.ProjectionX( hist2D.GetName() + str(iipt), bin0, bin1 )
        hist.Scale( normalizations[iitrig] )
        hists.append(hist)
        hDatas.append(hist)
        

    hData = hDatas[0]
    for ihist in range(1,len(hDatas)):
        hData.Add( hDatas[ihist] )
    hData.SetMarkerStyle(20)
    hData.SetName('jetdata_pt' + str(iipt))
    hData.SetTitle(prependstr +  options.title + ', ' + str(ipt[0]) + ' < p_{T}^{AVG} < ' + str(ipt[1])  + ';' + massStr + ' (GeV);Number')
    hData.Draw('e')
    leg.AddEntry( hData, 'Data', 'p')
    histsToWrite.append(hData)
    
    # MC
    hMCs = []
    for iMC in range(0,len(options.inputFileMC)) :
        fMC = TFile( options.inputFileMC[iMC] + '.root' )
        if options.groom is None :
            mchist2D = fMC.Get(options.hist)
        else :
            mchist2D = fMC.Get(options.hist + '_' + options.groom)
        mchists2D.append( mchist2D )
        mcbin0 = mchist2D.GetYaxis().FindBin( ipt[0] )
        mcbin1 = mchist2D.GetYaxis().FindBin( ipt[1] ) - 1
        print 'Integrating MC ' + options.inputFileMC[iMC] + ', bin0 = ' + str(bin0) + ', bin1 = ' + str(bin1)
        hMC = mchist2D.ProjectionX( options.inputFileMC[iMC] + '_pt' + str(iipt), mcbin0, mcbin1 )
        if iMC < len(colors) :
            #hMC.SetFillColor(17)
            hMC.SetLineColor( colors[iMC] )
            hMC.SetLineWidth( widths[iMC] )
            hMC.SetLineStyle(styles[iMC])

        if hMC.Integral() > 0.0 :
            hMC.Scale( hData.Integral() / hMC.Integral() )
            #hMC.Scale( xs[iMC] * lum / ntot[iMC] )
        hists.append( hMC )

        if iMC < len(colors) :
            hMC.Draw('hist same')
            leg.AddEntry( hMC, titles[iMC], 'l')
        histsToWrite.append(hMC)
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
        c.Print(options.hist + '_' + options.outname + '_pt_' + str(iipt) + '.png', 'png')
        c.Print(options.hist + '_' + options.outname + '_pt_' + str(iipt) + '.pdf', 'pdf')
    else :
        c.Print(options.hist + '_' + options.outname + '_pt_' + str(iipt) + '_' + options.groom + '.png', 'png')
        c.Print(options.hist + '_' + options.outname + '_pt_' + str(iipt) + '_' + options.groom + '.pdf', 'pdf')


fout.cd()

for ihist in histsToWrite :
    ihist.Write()

#fout.Close()
