#! /usr/bin/env python
import os
from math import *

from optparse import OptionParser


parser = OptionParser()

#parser.add_option('--dim', metavar='F', type='string', action='store',
 #                 default='1D',
  #                dest='dim',
   #               help='2D or 1D')


parser.add_option('--set', metavar='F', type='string', action='store',
                  default='mcatnlo',
                  dest='set',
                  help='mcatnlo or powheg')

(options, args) = parser.parse_args()

argv = []


import ROOT
ROOT.gROOT.Macro("rootlogon.C")

import sys
DIM = ['','2D']
if options.set == 'mcatnlo':
	MCstring = "MCATNLO"
	print "using MC@NLO"
elif options.set == 'powheg':
	MCstring = "POWHEG"
	print "using Powheg"
else:
	MCstring = "MadGraph"	
	print "using MadGraph"



hists = []
canvs = []

if options.set == 'mcatnlo':
	nEvents = 32575025.

elif options.set == 'powheg':
	nEvents = 21560109.
else:
	nEvents = 25273288.
if options.set == 'mcatnlo' or options.set == 'powheg':
	xs = 234.0 * 0.97 * 0.93
else:
	xs = 103.0 * 0.97 * 0.93	

lumi = 19748.


t1titles = ["t1TopPtprekin","t1TopPtpostkin","t1TopPtpostnsj","t1TopPtpostminmass","t1TopPtposttopmass","t1TopPtposttau32","t1TopPtpostbmax"]
t1axis = ["pt(top) (GeV/c)","gen pt(top) (GeV/c)"]
t1rebins = 5
i=0
GENSTR = "gen"
t1hists = ["topcand"+GENSTR+"ptprekin","topcand"+GENSTR+"ptpostkin","topcand"+GENSTR+"ptpostnsj","topcand"+GENSTR+"ptpostminmass","topcand"+GENSTR+"ptposttopmass","topcand"+GENSTR+"ptposttau32","topcand"+GENSTR+"ptpostbmax"]
dimtitle = ["Isolation","2D Cut"]
leg = ROOT.TLegend( 0.65, 0.65, 0.84, 0.84)
fTopSL=[ROOT.TFile("GenPt_TTbar_"+MCstring+"_ptWeighted_type1.root"),ROOT.TFile("GenPt2D_TTbar_"+MCstring+"_ptWeighted_type1.root")]
colors1 =[2,4]
for t1hist in t1hists:
    c = ROOT.TCanvas('ct1'+t1hist, 'ct1'+t1hist)
    t1SLttbar = []

    for idim in range(0,len(DIM)):



	t1SLttbar.append(fTopSL[idim].Get(t1hist))
		
	t1SLttbar[idim].Scale(xs*lumi/nEvents)
	#t1SLttbar[idim].Scale(1./t1SLttbar[idim].Integral())
	t1SLttbar[idim].Rebin(t1rebins)

	t1SLttbar[idim].SetLineColor( colors1[idim] )
	t1SLttbar[idim].SetLineWidth( 2 )
	print t1SLttbar[idim].Integral()
	if i==0:
		leg.AddEntry( t1SLttbar[idim],  dimtitle[idim], 'l')
		leg.SetFillColor(0)
		leg.SetBorderSize(0)
	if idim == 0:
    		t1SLttbar[0].SetTitle(';'+t1axis[1]+';Events')
    		t1SLttbar[0].GetYaxis().SetTitleOffset(0.8)
    		t1SLttbar[0].GetXaxis().SetRangeUser(0.0,1500.0)
    		t1SLttbar[0].SetStats(0)
    		t1SLttbar[0].SetMaximum( 1.8 * t1SLttbar[idim].GetMaximum() )
    		t1SLttbar[0].Draw('hist')
    	else:
		t1SLttbar[1].Draw('samehist')
    leg.Draw()
    prelim = ROOT.TLatex()
    prelim.SetTextFont(42)
    prelim.SetNDC()
    prelim.DrawLatex( 0.15, 0.91, "#scale[1.0]{CMS Preliminary Simulation}" )


    c.Print( 'GenptComp_'+GENSTR+t1titles[i]+'_'+MCstring+'_TTWeight.root', 'root')
    c.Print( 'GenptComp_'+GENSTR+t1titles[i]+'_'+MCstring+'_TTWeight.pdf', 'pdf')
    i+=1

