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
                  default='sysComparisons',
                  dest='outname',
                  help='Output name')


(options, args) = parser.parse_args()

argv = []

from ROOT import *

gROOT.Macro("rootlogon.C")

xs = [ 2.21000008E10, 
      2.21000008E10,2.21000008E10,
      2.21000008E10,2.21000008E10,
      2.21000008E10,2.21000008E10,
      2.21000008E10,2.21000008E10,2.21000008E10
      ]

ntot = [ 10960800., 
        10960800.,10960800.,
        10960800.,10960800.,
        10960800.,10960800.,
        10960800.,10960800.,10960800.
        ]
lum = 4960. #4067.

fData = TFile( options.inputFileData )

if options.groom is None :
    fout = TFile(options.outname + '_' + options.hist + '.root', 'recreate')
    groomStr = ''
    groomAppend = ''
else :
    fout = TFile(options.outname + '_' + options.hist + '_' + options.groom + '.root', 'recreate')
    groomStr = options.groom + ' '
    groomAppend = '_' + options.groom

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
  [1000.,1500.],
  [1500.,7000.]
  ]

colors = [ 1, 2, 4 ]
widths = [ 1, 1, 2 ]
styles = [ 1, 2, 3 ]

titles = ['PYTHIA6']




for iipt in range(0,len(pts)-1):

    ipt = pts[iipt]


    c = TCanvas('c' + str(iipt), 'c' + str(iipt),200,10,960,800)
    p1 = TPad("p1" + str(iipt),"p1" + str(iipt),0.0,0.3,1.0,0.97)
    p1.SetBottomMargin(0.05)
    p1.SetNumber(1)
    p2 = TPad("p2" + str(iipt),"p2" + str(iipt),0.0,0.00,1.0,0.3)
    p2.SetNumber(2)
    p2.SetTopMargin(0.05)
    p2.SetBottomMargin(0.30)
    pads.append( [p1,p2] )


    c.cd()
    p1.Draw()
    p1.cd()




    leg = TLegend(0.7, 0.86, 1.0, 1.0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)




    if options.hist.find('Mjet') < 0 :
        massStr = 'm_{jj}'
    else :
        massStr = 'm_{jet}'

    # Data
    prependstr = ''
    if options.groom is not None :
        prependstr = options.groom + ' '
    hs = THStack( options.hist + '_hs', ';' + massStr + ' (GeV);Number')
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
    hData.SetTitle( ';' + massStr + ' (GeV);Number')
    hData.Draw('e')
    leg.AddEntry( hData, 'Data', 'p')
    histsToWrite.append(hData)
    hData.GetXaxis().SetLabelSize(0)
    
    # MC
    hMCs = []
    hMCRatios = []
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

        if hMC.Integral() > 0.0 :
            #hMC.Scale( hData.Integral() / hMC.Integral() )
            hMC.Scale( xs[iMC] * lum / ntot[iMC] )
            #hMC.Scale( hData.Integral() / mcNorms[iMC] )

        hMCRatio = hMC.Clone()
        hMCRatio.SetName( options.inputFileMC[iMC] + '_ptRatio' + str(iipt) )
        hMCRatio.SetTitle( ';m_{jet} (GeV);MC/Data')
        hMCRatio.UseCurrentStyle()
        if iMC < len(colors) :
            #hMC.SetFillColor(17)
            hMC.SetLineColor( colors[iMC] )
            hMC.SetLineWidth( widths[iMC] )
            hMC.SetLineStyle( styles[iMC])
            hMCRatio.SetLineColor( colors[iMC] )
            hMCRatio.SetLineWidth( widths[iMC] )
            hMCRatio.SetLineStyle( styles[iMC])

        hMCRatio.Divide( hData )
        hists.append( hMC )

        if iMC < len(colors) :
            hMC.Draw('hist same')
            leg.AddEntry( hMC, titles[iMC], 'l')
        histsToWrite.append(hMC)
        histsToWrite.append(hMCRatio)
        hMCs.append(hMC)
        hMCRatios.append( hMCRatio )
        files.append(fMC)
        


    text1 = TLatex()
    text1.SetNDC()
    text1.SetTextFont(42)
    text1.DrawLatex(0.13,0.86, "#scale[1.0]{CMS Preliminary, L = 5 fb^{-1} at  #sqrt{s} = 7 TeV}")
    texts.append(text1)

    text2 = TLatex()
    text2.SetNDC()
    text2.SetTextFont(42)
    text2.SetTextSize(0.05)
    text2.DrawLatex( 0.45, 0.75, str(pts[iipt][0]) + ' < p_{T}^{AVG} < ' + str(pts[iipt+1][0])  )
    p1.RedrawAxis()

    p1.cd()
    p1.SetLogy()
    hData.Draw("e same")
    hData.SetMinimum(1e-1)
    leg.Draw()




    c.cd()
    p2.Draw()
    p2.cd()
    for iMC in range(0, len(options.inputFileMC) ):
        hMCRatios[iMC].SetMaximum(2.0)
        hMCRatios[iMC].SetMinimum(0.0)
        hMCRatios[iMC].GetYaxis().SetNdivisions(2,4,0,False)
        if iMC == 0 :
            hMCRatios[iMC].Draw('hist')
        elif iMC < 3 :
            hMCRatios[iMC].Draw('hist same')
            



    c.cd()
    c.Update()
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
