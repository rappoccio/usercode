#!/bin/python


# ===================================================
#             plotJetSpectrum.py
#
# ===================================================
# ===================================================


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFileMC', metavar='F', type='string', action='append',
                  default=[ 'QCD_pythia6_z2_plots_nominal',
                            'QCD_pythia8_4c_plots_nominal',
                            'QCD_herwigpp_23_plots_nominal'
                            ],
                  dest='inputFileMC',
                  help='Input file for MC')


parser.add_option('--hist', metavar='H', type='string', action='store',
                  default='histAK7MjetGenVsPtAvg',
                  dest='hist',
                  help='Histogram to plot')


parser.add_option('--title', metavar='H', type='string', action='store',
                  default='AK7 Jets, MC Truth',
                  dest='title',
                  help='Histogram to plot')


parser.add_option('--groom', metavar='H', type='string', action='store',
                  default=None,
                  dest='groom',
                  help='Histogram to plot')


parser.add_option('--outname', metavar='D', type='string', action='store',
                  default='trueMCDists',
                  dest='outname',
                  help='Output name')


(options, args) = parser.parse_args()

argv = []

from ROOT import *

gROOT.Macro("rootlogon.C")



xs = [ 2.21000008E10, 2.50999992E10, 2.31000003E10]
ntot = [ 10960800., 1060650. , 10430351. ]
lum = 4960. #4067.


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
  [ 125., 150.],
  [ 150., 220.],
  [ 220., 300.],
  [ 300., 450.],
  [ 450., 500.],
  [ 500., 600.],
  [ 600., 800.],
  [ 800.,1000.],
  [1000.,1500.],
  [1500.,7000.]
  ]

colors = [ 2, 8, 4 ]

titles = ['PYTHIA6', 'PYTHIA8', 'HERWIG++']

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

    # MC
    print '{0:6.0f} : '.format( iipt ),
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
        hMC = mchist2D.ProjectionX( options.inputFileMC[iMC] + '_pt' + str(iipt), mcbin0, mcbin1 )
        if iMC < len(colors) :
            #hMC.SetFillColor(17)
            hMC.SetLineColor( colors[iMC]  )
            hMC.SetLineWidth(3)

        if hMC.Integral() > 0.0 :
            #hMC.Scale( 1.0 / hMC.Integral() )
            hMC.Scale( xs[iMC] * lum / ntot[iMC] )
        hists.append( hMC )

        if iMC < len(colors) :
            hMC.Draw('hist same')
            leg.AddEntry( hMC, titles[iMC], 'l')
        histsToWrite.append(hMC)
        hMCs.append(hMC)
        files.append(fMC)
        print ' {0:6.2e}, '.format(hMC.Integral() ),
    print ''


fout.cd()

for ihist in histsToWrite :
    ihist.Write()

#fout.Close()
