#!/bin/python


# ===================================================
#             doSimpleFit.py
#
#  Do a simple 1-d fit to a single variable,
#  in this case, secvtx mass.
#  There are a number of command line options for some
#  W+HF variation studies. 
# ===================================================
# ===================================================

from ROOT import *

def distort( hist, version, flavor ) :
    if version == 'adhoc10' :
        m = 0.01
        b = 1.0
        # y = mx + b
        for ibin in range(1, hist.GetNbinsX() + 1):
            corr = (m*hist.GetXaxis().GetBinLowEdge(ibin) + b)
            print ' corr = ' + str(corr)
            hist.SetBinContent( ibin,
                                hist.GetBinContent(ibin) * corr )
    
    elif version == 'adhoc20' :
        m = -0.01
        b = 1.1
        # y = mx + b
        for ibin in range(1, hist.GetNbinsX() + 1):
            corr = (m*hist.GetXaxis().GetBinLowEdge(ibin) + b)
            print ' corr = ' + str(corr)
            hist.SetBinContent( ibin,
                                hist.GetBinContent(ibin) * corr )


    elif version == 'jetsmearing' :
        f = TFile('jetsmearing_ratios.root')
        h1 = f.Get('secvtxMassB1_ratio')
        h2 = f.Get('secvtxMassC1_ratio')
        h3 = f.Get('secvtxMassP1_ratio')
        if flavor == 'B' :
            h = h1
        elif flavor == 'C' :
            h = h2
        else :
            h = h3
        for ibin in range(1, hist.GetNbinsX() + 1):
            corr = h.GetBinContent( ibin )
            print ' corr = ' + str(corr)
            hist.SetBinContent( ibin,
                                hist.GetBinContent(ibin) * corr )

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFile', metavar='F', type='string', action='store',
                  default='shyftPlots_stitched_pfShyftAna_35pb_387v1data_387v1mc.root',
                  dest='inputFile',
                  help='input file tag to be used')

parser.add_option('--wqqQ2Variation', metavar='S', type='string', action='store',
                  default='nominal',
                  dest='wqqQ2Variation',
                  help='very simple W+QQ Q^2 variation, taken from 3-jet, 1-tag sample. Options are nominal, up, down.')

parser.add_option('--wcxQ2Variation', metavar='S', type='string', action='store',
                  default='nominal',
                  dest='wcxQ2Variation',
                  help='very simple W+c+X Q^2 variation, taken from 3-jet, 1-tag sample. Options are nominal, up, down.')

parser.add_option('--wbxQ2Variation', metavar='S', type='string', action='store',
                  default='nominal',
                  dest='wbxQ2Variation',
                  help='very simple W+b+X Q^2 variation, taken from 3-jet, 1-tag sample. Options are nominal, up, down.')

parser.add_option('--secVtxBMassVariation', metavar='V', type='string', action='store',
                  default='nominal',
                  dest='secVtxBMassVariation',
                  help='B-jet secondary vertex mass variation. One of (nominal,adhoc10,adhoc20)')

parser.add_option('--secVtxCMassVariation', metavar='V', type='string', action='store',
                  default='nominal',
                  dest='secVtxCMassVariation',
                  help='C-jet secondary vertex mass variation. One of (nominal,adhoc10,adhoc20)')

parser.add_option('--secVtxQMassVariation', metavar='V', type='string', action='store',
                  default='nominal',
                  dest='secVtxQMassVariation',
                  help='Q-jet secondary vertex mass variation. One of (nominal,adhoc10,adhoc20)')


# Option to just print out the pre-fit numbers
parser.add_option('--noFit', action='store_true',
                  default=False,
                  dest='noFit',
                  help='ignore the fit')


parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='simpleFit',
                  dest='outLabel',
                  help='output label')

(options, args) = parser.parse_args()

argv = []



from array import *

gROOT.Macro("rootlogon.C")

f = TFile(options.inputFile)

# the various samples
species = [
    'QCD_B',
    'Zbx',  
    'Zcx',  
    'Zqq',  
    'Wbx',  
    'Wcx',  
    'Wqq',   
    'SingleTop',
    'Top',
    'Data'
    ]

# histogram cache
hists = []

# Loop over the species.
# For each, get the mass. Sum the >=3 jet, >=1 tag sample together.
for ispecies in species :
#    print 'processing species ' + ispecies
    jetbinhists = []
    for ijet in range(3,6):
        tagbinhists = []
        for itag in range(1,3):
            if itag > ijet :
                continue
            if itag is not 1 and ispecies is 'QCD_B' :
                continue
            h = f.Get( ispecies + '_secvtxMass_' + str(ijet) + 'j_' + str(itag) + 't').Clone()
            tagbinhists.append(h)
        tagbinhist = tagbinhists[0]
        if ispecies is not 'QCD_B' :
            tagbinhist.Add( tagbinhists[1] )
        jetbinhists.append(tagbinhist)
    jetbinhist = jetbinhists[0]
    jetbinhist.Add( jetbinhists[1] )
    jetbinhist.Add( jetbinhists[2] )    
    hists.append(jetbinhist)


# Optionally distort the secondary vertex mass distribution
# for b, c, q separately
if options.secVtxBMassVariation != 'nominal' :
    distort(hists[1], options.secVtxBMassVariation, 'B') # Z+b
    distort(hists[4], options.secVtxBMassVariation, 'B') # W+b
    distort(hists[7], options.secVtxBMassVariation, 'B') # Single top
    distort(hists[8], options.secVtxBMassVariation, 'B') # Top

if options.secVtxCMassVariation != 'nominal' :
    distort(hists[2], options.secVtxCMassVariation, 'C') # Z+c
    distort(hists[5], options.secVtxCMassVariation, 'C') # W+c

if options.secVtxQMassVariation != 'nominal' :
    distort(hists[3], options.secVtxQMassVariation, 'Q') # Z+q
    distort(hists[6], options.secVtxQMassVariation, 'Q') # W+q

plothists = [hists[0].Clone(),
             hists[1].Clone(),
             hists[4].Clone(),
             hists[5].Clone(),
             hists[6].Clone(),
             hists[7].Clone(),
             hists[8].Clone(),
             hists[9].Clone()]

# Add Z+Jets together
plothists[1].Add( hists[2] )
plothists[1].Add( hists[3] )

# Do a simple Q^2 variation
wbxDict = dict ( {'down':0.28, 'nominal':1.0, 'up':1.24 } )
wcxDict = dict ( {'down':0.46, 'nominal':1.0, 'up':2.00 } )
wqqDict = dict ( {'down':0.80, 'nominal':1.0, 'up':1.82 } )

# Scale the histograms by Q^2 variation
bscale = wbxDict[options.wbxQ2Variation]
cscale = wcxDict[options.wcxQ2Variation]
lfscale = wqqDict[options.wqqQ2Variation]

# Add the W+Jets together
#plothists[2].Scale( bscale )
#plothists[2].Add( hists[5], cscale )
#plothists[2].Add( hists[6], lfscale )


print '--------------------------------------------------------------'
print 'NHF              : Wbx = {0:6.2f}, Wcx = {1:6.2f}, Wqq = {2:6.2f}'.format(
#    bscale * hists[4].Integral(), cscale * hists[5].Integral(), lfscale * hists[6].Integral()
    hists[4].Integral(), hists[5].Integral(), hists[6].Integral()
    )
print 'Number of events : Top = {0:6.2f}, Single Top = {1:6.2f}, W+LF = {2:6.2f}, W+C = {3:6.2f}, W+B = {4:6.2f}, Zjets = {5:6.2f}, QCD = {6:6.2f}'.format(
    plothists[6].Integral(),
    plothists[5].Integral(),
    plothists[4].Integral(),
    plothists[3].Integral(),
    plothists[2].Integral(),
    plothists[1].Integral(),
    plothists[0].Integral(),
    )
print 'RMS              : Top = {0:6.2f}, Single Top = {1:6.2f}, W+LF = {2:6.2f}, W+C = {3:6.2f}, W+B = {4:6.2f}, Zjets = {3:6.2f}, QCD = {4:6.2f}'.format(
    plothists[6].GetRMS(),
    plothists[5].GetRMS(),
    plothists[4].GetRMS(),
    plothists[3].GetRMS(),    plothists[2].GetRMS(),
    plothists[1].GetRMS(),
    plothists[0].GetRMS(),    
    )
print '--------------------------------------------------------------'

colors = [
    TColor.kYellow,
    TColor.kAzure-2,
    TColor.kGreen-3,
    TColor.kGreen-2,
    TColor.kGreen-1,
    TColor.kMagenta,
    TColor.kRed+1,
    TColor.kBlack
    ]
names = [
    'QCD',
    'Z/#gamma*#rightarrowl^{+}l^{-}',
    'W#rightarrowl#nu+b',
    'W#rightarrowl#nu+c',
    'W#rightarrowl#nu+q',    
    'Single Top',
    't#bar{t}'
    ]

leg = TLegend(0.5, 0.5, 0.8, 0.8)
leg.SetFillColor(0)
leg.SetBorderSize(0)
stack = THStack('hs','hs')
for hist in range(0, len(plothists)-1):
    plothists[hist].SetFillStyle(1001)
    plothists[hist].SetFillColor(colors[hist])
    stack.Add( plothists[hist] )
    leg.AddEntry( plothists[hist], names[hist], 'f')

plothists[len(plothists)-1].SetMarkerStyle(20)
plothists[len(plothists)-1].Draw('e')
plothists[len(plothists)-1].SetName('data_1jets_1tags')
plothists[len(plothists)-1].SetTitle('Secondary Vertex Mass, >=3 Jets, >=1 Tags;Vertex Mass (GeV/c^{2});Number of events')
stack.Draw('hist same')
plothists[len(plothists)-1].Draw('e same')
leg.Draw()

c2 = TCanvas('c2', 'c2')
stack2 = THStack('hs','hs')
for hist in range(0, len(hists)-1):    
    stack2.Add( hists[hist] )

hists[len(hists)-1].SetMarkerStyle(20)
hists[len(hists)-1].Draw('e')
hists[len(hists)-1].SetName('data_1jets_1tags')
hists[len(hists)-1].SetTitle('Secondary Vertex Mass, >=3 Jets, >=1 Tags;Vertex Mass (GeV/c^{2});Number of events')
stack2.Draw('hist same')
hists[len(hists)-1].Draw('e same')

c1.Print( options.outLabel + 'mcExp1jet.png', 'png')
c1.Print( options.outLabel + 'mcExp1jet.pdf', 'pdf')

if options.noFit is False:

    x = RooRealVar('x', 'x', 0., 10.0)

    h_rf_data = RooDataHist("vtxMass", "vtxMass", RooArgList(x), plothists[len(plothists)-1] )

    h_rf_qcd   =RooDataHist ("h_rf_qcd",   "h_rf_qcd",   RooArgList(x), plothists[0] )
    pdf_qcd_bare =RooHistPdf  ("pdf_qcd",    "pdf_qcd",    RooArgSet(x), h_rf_qcd)
    qcdfrac = RooRealVar('qcdfrac','QCD Fraction', plothists[0].Integral(), 0.0, 10000.0)
    constraint_qcd = RooGaussian("constraint_qcd","constraint_qcd",qcdfrac,
                                 RooFit.RooConst(plothists[0].Integral()),
                                 RooFit.RooConst(plothists[0].Integral() * 1.0)
                                 )
    pdf_qcd = RooProdPdf("sumc","sum with constraint",RooArgList(pdf_qcd_bare, constraint_qcd), 0.)

    h_rf_zjets   =RooDataHist ("h_rf_zjets",   "h_rf_zjets",   RooArgList(x), plothists[1] )
    pdf_zjets    =RooHistPdf  ("pdf_zjets",    "pdf_zjets",    RooArgSet(x), h_rf_zjets)




    h_rf_wb   =RooDataHist ("h_rf_wb",   "h_rf_wb",   RooArgList(x), plothists[2] )
    pdf_wb_bare =RooHistPdf  ("pdf_wb",    "pdf_wb",    RooArgSet(x), h_rf_wb)
    wbfrac = RooRealVar('wbfrac','WB Fraction', plothists[2].Integral(), 0.0, 10000.0)
    constraint_wb = RooGaussian("constraint_wb","constraint_wb",wbfrac,
                                 RooFit.RooConst(plothists[2].Integral()),
                                 RooFit.RooConst(plothists[2].Integral() * 2.0)
                                 )
    pdf_wb = RooProdPdf("sumwb","sum with constraint",RooArgList(pdf_wb_bare, constraint_wb), 0.)

#    h_rf_wb   =RooDataHist ("h_rf_wb",   "h_rf_wb",   RooArgList(x), plothists[2] )
#    pdf_wb    =RooHistPdf  ("pdf_wb",    "pdf_wb",    RooArgSet(x), h_rf_wb)

    h_rf_wc   =RooDataHist ("h_rf_wc",   "h_rf_wc",   RooArgList(x), plothists[3] )
    pdf_wc    =RooHistPdf  ("pdf_wc",    "pdf_wc",    RooArgSet(x), h_rf_wc)

    h_rf_wq   =RooDataHist ("h_rf_wq",   "h_rf_wq",   RooArgList(x), plothists[4] )
    pdf_wq    =RooHistPdf  ("pdf_wq",    "pdf_wq",    RooArgSet(x), h_rf_wq)



    h_rf_singletop   =RooDataHist ("h_rf_singletop",   "h_rf_singletop",   RooArgList(x), plothists[5] )
    pdf_singletop_bare =RooHistPdf  ("pdf_singletop",    "pdf_singletop",    RooArgSet(x), h_rf_singletop)
    singletopfrac = RooRealVar('singletopfrac','SINGLETOP Fraction', plothists[5].Integral(), 0.0, 10000.0)
    constraint_singletop = RooGaussian("constraint_singletop","constraint_singletop",singletopfrac,
                                 RooFit.RooConst(plothists[5].Integral()),
                                 RooFit.RooConst(plothists[5].Integral() * 0.3)
                                 )
    pdf_singletop = RooProdPdf("sumd","sum with constraint",RooArgList(pdf_singletop_bare, constraint_singletop), 0.)


    h_rf_top   =RooDataHist ("h_rf_top",   "h_rf_top",   RooArgList(x), plothists[6] )
    pdf_top    =RooHistPdf  ("pdf_top",    "pdf_top",    RooArgSet(x), h_rf_top)




    zjetsfrac = RooRealVar('zjetsfrac','Z+jets Fraction',plothists[1].Integral(), 0.0, 10000.0)
#    wbfrac = RooRealVar('wbfrac','W+jets Fraction',plothists[2].Integral(), 0.0, 10000.0)    
    wcfrac = RooRealVar('wcfrac','W+jets Fraction',plothists[3].Integral(), 0.0, 10000.0)
    wqfrac = RooRealVar('wqfrac','W+jets Fraction',plothists[4].Integral(), 0.0, 10000.0)
#    singletopfrac = RooRealVar('stopfrac','Single Top Fraction',plothists[5].Integral(), 0.0, 10000.0)
    topfrac = RooRealVar('topfrac','TTbar Fraction',plothists[6].Integral(), 0.0, 10000.0)

    #pdf_mass = RooAddPdf("pdf_mass", "pdf_mass",
    #                     RooArgList(pdf_qcd, pdf_zjets, pdf_wjets, pdf_singletop, pdf_top),
    #                     RooArgList(qcdfrac,zjetsfrac,wjetsfrac,singletopfrac,topfrac) )
    pdf_mass = RooAddPdf("pdf_mass", "pdf_mass",
                         RooArgList(pdf_qcd,pdf_wq,pdf_wc,pdf_wb,pdf_singletop,pdf_top),
                         RooArgList(qcdfrac,wqfrac,wcfrac,wbfrac,singletopfrac,topfrac) )



    r = pdf_mass.fitTo( h_rf_data, RooFit.Save(), RooFit.Extended(), RooFit.Constrain(RooArgSet(qcdfrac, singletopfrac, wbfrac)) )
    r.Print()

    xframe = x.frame(RooFit.Title("Secondary Vertex Mass, 1 jet, 1 tag;SecVtx Mass (GeV/c^2);Events")) ;

    RooAbsData.plotOn(h_rf_data, xframe, )
    #RooAddPdf.plotOn(pdf_mass, xframe, RooFit.LineColor(kBlack))
#    argset1 = RooArgSet(pdf_top,pdf_singletop,pdf_wq,pdf_wc,pdf_wb,pdf_qcd)
    argset1 = RooArgSet(pdf_top,pdf_wq,pdf_wc,pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset1), RooFit.FillColor(2), RooFit.LineColor(1), RooFit.DrawOption("F"))

    argset1a = RooArgSet(pdf_singletop,pdf_wq,pdf_wc,pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset1a), RooFit.FillColor(kMagenta), RooFit.LineColor(1), RooFit.DrawOption("F"))
    
    argset2 = RooArgSet(pdf_wq,pdf_wc,pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset2), RooFit.FillColor(kGreen-1), RooFit.LineColor(1), RooFit.DrawOption("F")) 

    argset3 = RooArgSet(pdf_wc,pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset3), RooFit.FillColor(kGreen-2), RooFit.LineColor(1), RooFit.DrawOption("F")) 

    argset4 = RooArgSet(pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset4), RooFit.FillColor(kGreen-3), RooFit.LineColor(1), RooFit.DrawOption("F")) 

    argset5 = RooArgSet(pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset5), RooFit.FillColor(kYellow), RooFit.LineColor(1), RooFit.DrawOption("F"))
    RooAbsData.plotOn(h_rf_data, xframe)
    #RooAbsPdf.plotOn(pdf_wjets, xframe, RooFit.LineColor(kGreen))
    #RooAbsPdf.plotOn(pdf_qcd, xframe, RooFit.LineColor(kYellow))

    #pdf_mass.plotOn(xframe, RooFit.Components(RooArgSet(pdf_top, pdf_wjets)), RooFit.LineColor(kMagenta) )
    #pdf_mass.plotOn(xframe, RooFit.Components(RooArgSet(pdf_wjets)), RooFit.LineColor(kRed) )



    c3 = TCanvas('c3', 'c3')
    xframe.Draw()

    c3.Print( options.outLabel + 'simplefit1jet.png','png')
    c3.Print( options.outLabel + 'simplefit1jet.pdf','pdf')


    pars = r.floatParsFinal()
    ntop = pars[2].getVal()
    dntop = pars[2].getError()


    # Get the xs and print it
    xs_top = ntop / plothists[6].Integral() * 157.
    dxs_top = dntop / ntop * xs_top



    print '--------------------------------------------------------------'
    print 'TTbar Cross Section = {0:9.2f} +- {1:9.2f} pb, % uncertainty = {2:6.2f}'.format(
        xs_top,
        dxs_top,
        dxs_top/xs_top
        )
    print '--------------------------------------------------------------'
    
# Bye!

