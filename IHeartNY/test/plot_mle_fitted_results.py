#!/usr/bin/env python

import time
from optparse import OptionParser
parser = OptionParser()


parser.add_option('--file', metavar='F', type='string', action='store',
                  default='histfiles/histos-mle.root',
                  dest='file',
                  help='Input file name')

parser.add_option('--pattern', metavar='p', type='string', action='store',
                  default='histfiles/normalized_mujets_',
                  dest='pattern',
                  help='Input file name patterns for root files containing data')


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
gStyle.SetTitleOffset(2.0, "X")
gStyle.SetTitleOffset(1.25, "Y")
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

for variable in variables :
    f_data = TFile( options.pattern + variable + '.root' )
    h_data = f_data.Get( variable + '__DATA' )
    c = TCanvas(variable, variable)
    canvs.append(c)
    hs = THStack( variable, variable )    
    for sample in samples :
        hist = hists[variable][sample]
        hs.Add( hist )

    h_data.Draw('e')
    hs.Draw('hist same')
    h_data.Draw('e same')
    f_datas.append(f_data)
    h_datas.append(h_data)
    stacks.append(hs)
    c.Print(variable + '.png')
    c.Print(variable + '.pdf')
