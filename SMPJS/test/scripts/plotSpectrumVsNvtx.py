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
for igroom in xrange(len(options.grooms)) :

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
    ## hData2D.FitSlicesY(0)
    ## hData = gDirectory.Get( hData2D.GetName() + '_1' )
    ## hData.SetName(groom + '_datapfx')
    ## eData = gDirectory.Get( hData2D.GetName() + '_2' )
    ## eData.SetName(groom + '_edatapfx')
    hData = hData2D.ProfileX( groom + '_datapfx', -1, -1, 'g')
    

    for ibin in xrange(hData.GetNbinsX()) :
        if hData.GetBinContent(ibin) == 0.0 :
            continue
        xvals.append( hData.GetXaxis().GetBinLowEdge(ibin) )
        exvals.append( hData.GetXaxis().GetBinCenter(ibin) - hData.GetXaxis().GetBinLowEdge(ibin) )
        yvals_data.append( hData.GetBinContent(ibin) )
        eyvals_data.append( 0.1 ) #eData.GetBinContent(ibin) )
    

    if groom == '' :
        mchist2D = fMC.Get(options.hist)
    else :
        mchist2D = fMC.Get(options.hist + '_' + groom)

    mchist2D.Sumw2()
    mchist2D.Scale( 1.0 / mchist2D.Integral() )
    ## mchist2D.FitSlicesY(0)
    ## hMC = gDirectory.Get( mchist2D.GetName() + '_1' )
    ## eMC = gDirectory.Get( mchist2D.GetName() + '_2' )
    ## hMC.SetName( groom + '_mcpfx' )
    ## eMC.SetName( groom + '_emcpfx' )
    hMC = mchist2D.ProfileX(  groom + '_mcpfx', -1, -1, 'g' )
    mchist2D.SetLineColor(2)
    for ibin in xrange(hMC.GetNbinsX()) :
        if hMC.GetBinContent(ibin) == 0.0 :
            continue
        yvals_mc.append( hMC.GetBinContent(ibin) )
        eyvals_mc.append( 0.1 ) #eMC.GetBinContent(ibin) )

    #mchist2D.Draw("box same")


    gr_data = TGraphErrors( len(xvals), xvals, yvals_data, exvals, eyvals_data )

    gr_data.SetMarkerStyle( markersData[igroom] )
    gr_data.SetLineColor( colors[igroom] )
    gr_data.SetFillColor( colors[igroom] )
    gr_data.SetMarkerColor( colors[igroom] )
    gr_data.SetTitle( ';N_{PV};<m_{J}^{AVG}> (GeV)')    

    gr_mc = TGraphErrors( len(xvals), xvals, yvals_mc, exvals, eyvals_mc )
    if igroom == 0 :
        gr_data.Draw('a3')
    else :
        gr_data.Draw('3')

    gr_mc.SetMarkerStyle( markersMC[igroom])
    gr_mc.SetLineColor( colors[igroom] )
    gr_mc.SetFillStyle( 3001 )
    gr_mc.SetFillColor( colors[igroom] )
    gr_mc.SetMarkerColor( colors[igroom] )


    gr_mc.Draw('3')
    profs.append( [hData, hMC] )
    graphs.append( [gr_data, gr_mc] )
    leg.AddEntry( gr_data, groom + ' data', 'f')
    leg.AddEntry( gr_mc, groom + ' MC', 'f')
    gr_data.GetHistogram().GetXaxis().SetRangeUser(0., 20.)
    gr_data.GetHistogram().SetMinimum(0.0)
    gr_data.GetHistogram().SetMaximum(30.0)


leg.Draw()
    



text1 = TLatex()
text1.SetNDC()
text1.SetTextFont(42)
text1.DrawLatex(0.13,0.86, "#scale[1.0]{CMS Preliminary, L = 5 fb^{-1} at  #sqrt{s} = 7 TeV}")
texts.append(text1)


c.Print(options.hist + '_' + options.outname + '.png', 'png')
c.Print(options.hist + '_' + options.outname + '.pdf', 'pdf')

