#!/usr/bin/env python

import time
from optparse import OptionParser
parser = OptionParser()


parser.add_option('--file', metavar='F', type='string', action='store',
                  default='run_theta/histos-mle-2d-CT10_nom.root',
                  dest='file',
                  help='Input file name')


(options, args) = parser.parse_args()

argv = []

from ROOT import gRandom, TH1, TH1D, cout, TFile, gSystem, TCanvas, TPad, gROOT, gStyle, THStack, TLegend, TLatex, TColor, gDirectory

gROOT.Macro("rootlogon.C")

gStyle.SetOptTitle(0);
gStyle.SetOptStat(0);
gStyle.SetOptFit(0);

gStyle.SetOptStat(000000)

gStyle.SetTitleFont(43)
#gStyle.SetTitleFontSize(0.05)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(1.0, "X")
gStyle.SetTitleOffset(1.0, "Y")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(20, "XYZ")

f = TFile(options.file)
keys = f.GetListOfKeys()

samples = ['QCD', 'SingleTop', 'WJets', 'TTbar_nonSemiLep', 'TTbar' ]
colors = {'TTbar':TColor.kRed,
          'TTbar_nonSemiLep':TColor.kOrange,
          'WJets':TColor.kGreen,
          'SingleTop':TColor.kMagenta,
          'QCD':TColor.kYellow
          }

files = {
    'etaAbsLep4':'NormalizedHists_CT10_nom/normalized2d_mujets_etaAbsLep6_subtracted_from_etaAbsLep4.root',    
    'etaAbsLep6':'NormalizedHists_CT10_nom/normalized2d_mujets_etaAbsLep7_subtracted_from_etaAbsLep6.root',
    'vtxMass7':'NormalizedHists_CT10_nom/normalized2d_mujets_vtxMass7.root'
    }
	

hists = {}
variables = []

for key in keys :
    keyname = key.GetName()
    keyssplit = keyname.split('__')
    variable = keyssplit[0]
    if variable not in variables : 
        variables.append(variable)
    sample = keyssplit[1]
    hist = gDirectory.Get( keyname )
    hist.SetFillColor( colors[sample] )
    if variable in hists : 
        hists[variable][sample] = hist
    else :
        hists.update( {variable:{sample:hist}} )


print hists
print variables 
canvs = []
stacks = []
f_datas = []
h_datas = []
ivar = 0

maxes = [40, 40, 600]
# Post-fit plots
i=0
for variable in variables :
    imax = maxes[i]
    f_data = TFile( files[ variable ] )
    h_data = f_data.Get( variable + '__DATA' )
    c = TCanvas(variable, variable)
    canvs.append(c)
    hs = THStack( variable, variable )
    isum = 0.0    
    for sample in samples :
        hist = hists[variable][sample]
        hs.Add( hist )
        print '{0:40s} {1:20s} {2:6.2f}'.format( variable, sample, hist.Integral() )
        isum += hist.Integral()
    print 'Total : {0:6.2f}'.format( isum )

    h_data.UseCurrentStyle()
    h_data.Draw('e')
    hs.Draw('hist same')
    h_data.Draw('e same')    
    h_data.SetMaximum(imax)
    f_datas.append(f_data)
    h_datas.append(h_data)
    stacks.append(hs)
    print 'Data : {0:6.2f}'.format( h_data.Integral() )
    c.Print(variable + '.png')
    c.Print(variable + '.pdf')
    i+= 1


# Pre-fit plots
i=0
for variable in variables :
    imax = maxes[i]
    f_data = TFile( files[ variable ] )
    h_data = f_data.Get( variable + '__DATA' )
    cpre = TCanvas(variable + 'pre', variable + 'pre')
    canvs.append(cpre)
    hs = THStack( variable+'pre', variable+'pre' )
    isum = 0.0
    for sample in samples :
        hist = f_data.Get( variable + '__' + sample )
        hs.Add( hist )
        print '{0:40s} {1:20s} {2:6.2f}'.format( variable, sample, hist.Integral() )
        isum += hist.Integral()
    print 'Total : {0:6.2f}'.format( isum )

    h_data.UseCurrentStyle()
    h_data.Draw('e')
    hs.Draw('hist same')
    h_data.Draw('e same')    
    h_data.SetMaximum(imax)
    f_datas.append(f_data)
    h_datas.append(h_data)
    stacks.append(hs)
    print 'Data : {0:6.2f}'.format( h_data.Integral() )
    cpre.Print(variable + 'p_re.png')
    cpre.Print(variable + '_pre.pdf')
    i+= 1
    
