#! /usr/bin/env python
import os
from math import *

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--pt', metavar='F', type='string', action='store',
                  default='low',
                  dest='pt',
                  help='low or high')
parser.add_option('--mass', metavar='F', type='string', action='store',
                  default='std',
                  dest='mass',
                  help='low or high')


parser.add_option('--etabin', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'etabin',
                  help		=	'range1 range2 or all')



(options, args) = parser.parse_args()

argv = []

etastring = ''
if options.etabin == 'range1':
	etastring = '_eta_range1'
if options.etabin == 'range2':
	etastring = '_eta_range2'



import ROOT
ROOT.gROOT.Macro("rootlogon.C")

import sys

fData = ROOT.TFile("TTSemilepAnalyzer_19invfb_TTWeight_type1"+etastring+".root")

#fTopMC = ROOT.TFile("TTSemilepAnalyzer_v9_TTJets_antibtag_w_mucut_withDR_loosenedType2Top_FULL_withPU.root")
fTopFL = ROOT.TFile("TTSemilepAnalyzer_TTJetsLeptonic_TTWeight_ptWeighted_type1"+etastring+".root") 
fTopSL = ROOT.TFile("TTSemilepAnalyzer_TTJets_TTWeight_ptWeighted_type1"+etastring+".root")



fWMC = ROOT.TFile("TTSemilepAnalyzer_WJets_TTWeight_ptWeighted_type1"+etastring+".root")
fZJetsMC = ROOT.TFile("TTSemilepAnalyzer_ZJets_TTWeight_ptWeighted_type1"+etastring+".root")
fSingletop = [
ROOT.TFile("TTSemilepAnalyzer_ST_t_TTWeight_ptWeighted_type1"+etastring+".root"),
ROOT.TFile("TTSemilepAnalyzer_ST_tB_TTWeight_ptWeighted_type1"+etastring+".root"),
ROOT.TFile("TTSemilepAnalyzer_ST_tW_TTWeight_ptWeighted_type1"+etastring+".root"),
ROOT.TFile("TTSemilepAnalyzer_ST_tWB_TTWeight_ptWeighted_type1"+etastring+".root"),
ROOT.TFile("TTSemilepAnalyzer_ST_s_TTWeight_ptWeighted_type1"+etastring+".root"),
ROOT.TFile("TTSemilepAnalyzer_ST_sB_TTWeight_ptWeighted_type1"+etastring+".root"),
]


hists = []
canvs = []

nEvents = [
    25424818.,
    57653686.,
    30404232., 
    12043695.,
    ]
stnEvents = [
    3748155.,
    1930185.,
    495559.,
    491463.,
    259176.,
    139604.,
]
xs = [
    103.0 * 0.97 * 0.93,
    37509.0 * 0.97 * 0.93,
    3503.71 * 0.97 * 0.93,
    24.8 * 0.97 * 0.93,
    ]
stxs=[
    56.4 * 0.97 * 0.93,
    30.7 * 0.97 * 0.93,
    11.1 * 0.97 * 0.93,
    11.1 * 0.97 * 0.93,
    3.79 * 0.97 * 0.93,
    1.76 * 0.97 * 0.93,
]
colors = [
    #ROOT.kRed-3,
    ROOT.TColor.GetColor(255, 80, 80),
    ROOT.kGreen,
    ROOT.kYellow
    ]
qcdFactor = [
    0.00957248,0.00957248,0.00957248,0.00957248
    ]

lumi = 19748.
#15379.91 * 1.066
#lumi = 4921.


if options.pt == 'high':
	t1titles = ["t1MinimumPairwiseMasshighpt","t1TopMasshighpt","t1Nsubjetshighpt"]
else:
	if options.mass == 'ug':
		t1titles = ["t1MinimumPairwiseMass","t1TopMassgroomed","t1Nsubjets","t1Tau32groomed","t1BMaxgroomed"]		
	else:
		t1titles = ["t1MinimumPairwiseMass","t1TopMass","t1Nsubjets","t1Tau32","t1BMax"]		

t1axis = ["Minimum Pairwise Mass (GeV/c^{2})","m(top) (GeV/c^{2})","Number of Subjets","Tau3/Tau2","CSV"]
if options.mass == 'ug':
	t1int = [[50.0,149.99],[150.0,229.99],[3.0,10.0],[0.0,0.599],[0.679,0.999]]
	t1aint1 = [[0.0,49.99],[0.0,149.99],[0.0,2.0],[0.6,1.5],[0.0,0.679]]
	t1aint2 = [[0.0,0.0],[230.0,600.0],[-0.5,-0.5],[0.0,0.0],[0.0,0.0]]
else:
	t1int = [[50.0,149.99],[140.0,249.99],[3.0,10.0],[0.0,0.599],[0.679,0.999]]
	t1aint1 = [[0.0,49.99],[0.0,139.99],[0.0,2.0],[0.6,1.5],[0.0,0.679]]
	t1aint2 = [[0.0,0.0],[250.0,600.0],[-0.5,-0.5],[0.0,0.0],[0.0,0.0]]

t1rebins = [10,5,1,5,5]
i=0
		    
if options.pt == 'high':
	t1hists = ["minPairHisthighpt","topTagMassHistpremasshighpt","nsjhighpt"]
else:
	if options.mass == 'ug':	
		t1hists = ["minPairHist","topcandugmasspostminmass","nsj","topTagugmtau32Hist","topTagugmBMaxHist"]
	else:
		t1hists = ["minPairHist","topTagMassHistpremass","nsj","topTagtau32Hist","topTagBMaxHist"]

SFarray=[]
at1array=[]
at2array=[]
bt1array=[]
bt2array=[]
SFerrorarray=[]
for t1hist in t1hists:
	t1data= fData.Get(t1hist)
	t1data.Sumw2()
	t1ttbarFL= fTopFL.Get(t1hist)	
	t1ttbarSL= fTopSL.Get(t1hist)	
	t1ttbarFL.Sumw2()
	t1ttbarSL.Sumw2()
	t1ttbarFL.Scale(xs[3]*lumi/nEvents[3])
	t1ttbarSL.Scale(xs[0]*lumi/nEvents[0])		
	t1wjets= fWMC.Get(t1hist)
	t1wjets.Sumw2()
	t1wjets.Scale(xs[1]*lumi/nEvents[1])
	t1zjets= fZJetsMC.Get(t1hist)
	t1zjets.Sumw2()

	singletopt1temp = fSingletop[0].Get(t1hist)
	singletopt1temp.Sumw2()
	singletopt1temp.Scale((stxs[0] / stnEvents[0]) * lumi)
	singletopt1 = singletopt1temp.Clone("singletopt1")
	for ifile in range(1,len(fSingletop)):
		singletopt1temp = fSingletop[ifile].Get(t1hist)
		singletopt1temp.Sumw2()
		singletopt1temp.Scale((stxs[ifile] / stnEvents[ifile]) * lumi)
		singletopt1.Add(singletopt1temp)
	singletopt1.SetMarkerStyle( 0 )
	singletopt1.SetFillColor( 6 )


	#t1ttbar.Scale(xs[0]*lumi/nEvents[0])
	t1ttbarFL.Scale(1.)
	t1ttbarSL.Scale(1.)
        t1zjets.Scale(xs[2]*lumi/nEvents[2])



	t1ttbarSL.SetFillColor( colors[0] )
	t1ttbarFL.SetFillColor( 7 )
	t1wjets.SetFillColor( colors[1] )
	t1data.SetMarkerStyle( 8 ) 

	t1ttbarFL.SetMarkerStyle( 0 )
	t1ttbarSL.SetMarkerStyle( 0 )
	t1wjets.SetMarkerStyle( 0 )
	t1zjets.SetFillColor( 30 )
	t1zjets.SetMarkerStyle( 0 )
	if i==0:
		leg = ROOT.TLegend( 0.65, 0.65, 0.84, 0.84)
		leg.AddEntry( t1data,  'Data', 'p')
		leg.AddEntry( t1ttbarSL, 'Semi-Leptonic t#bar{t}', 'f')
		leg.AddEntry( t1ttbarFL, 'Fully-Leptonic t#bar{t}', 'f')
		leg.AddEntry( t1wjets, 'W+Jets', 'f')
		leg.AddEntry( t1zjets, 'Z+Jets', 'f')
		leg.AddEntry( singletopt1, 'Singletop', 'f')
		leg.SetFillColor(0)
		leg.SetBorderSize(0)

	hs = ROOT.THStack( 't1 BkgStack', 't1')
	

	hs.Add( t1zjets )
	hs.Add( singletopt1 )
	hs.Add( t1wjets )
	hs.Add( t1ttbarFL )
	hs.Add( t1ttbarSL )
	
	temphist = t1zjets.Clone()
	temphist.Add( singletopt1 )
	temphist.Add( t1wjets )
	temphist.Add( t1ttbarFL )
	temphist.Add( t1ttbarSL )

		
	print t1hist
    	t1bin1 = t1data.GetXaxis().FindBin(t1int[i][0])
    	t1bin2 = t1data.GetXaxis().FindBin(t1int[i][1]) 

    	at1 = float(t1data.Integral( t1bin1, t1bin2))
   	bt1 = float(t1data.Integral())

	temp=0.
	#print "Data"
    	#for ibin in range(t1bin1,t1bin2+1):
	#	print str(t1data.GetBinLowEdge(ibin)) + " To " + str(t1data.GetBinLowEdge(ibin)+t1data.GetBinWidth(ibin))
	#	print "Content " + str(float(t1data.GetBinContent(ibin)))
	#	temp+=float(t1data.GetBinContent(ibin))
	#print "total" + str(temp)

    	ft1 = at1 / bt1
    	dft1 = sqrt(ft1 * (1-ft1) / bt1)
	
	#print "lbin " + str(t1bin1)
	#print "hbin " + str(t1bin2)
	#print "data int 1 "+str(at1)
	#print "data int 2 "+str(bt1)
	
    	at2 = float(hs.GetStack().Last().Integral( t1bin1, t1bin2))
    	bt2 = float(hs.GetStack().Last().Integral())

	sigmaNa = ROOT.Double(0.0)
	sigmaNt1 = ROOT.Double(0.0)
	sigmaNt2 = ROOT.Double(0.0)

    	t1a1bin1 = t1data.GetXaxis().FindBin(t1aint1[i][0])
    	t1a1bin2 = t1data.GetXaxis().FindBin(t1aint1[i][1])

    	t1a2bin1 = t1data.GetXaxis().FindBin(t1aint2[i][0])
    	t1a2bin2 = t1data.GetXaxis().FindBin(t1aint2[i][1])  

	Nt1 = temphist.IntegralAndError(t1a1bin1,t1a1bin2,sigmaNt1)
	Nt2 = temphist.IntegralAndError(t1a2bin1,t1a2bin2,sigmaNt2)
	
	sigmaNt = sqrt(sigmaNt1*sigmaNt1 + sigmaNt2*sigmaNt2)

	REDUND = temphist.IntegralAndError(t1bin1, t1bin2,sigmaNa)

	N=bt2
	Na=at2
	Nt=N-Na 

	sigmaNa = sqrt(Na)
	sigmaNt = sqrt(Nt)

	#dft2 = sqrt((1.0/(N*N*N*N))*((Nt*sigmaNa)*(Nt*sigmaNa)+(Na*sigmaNt)*(Na*sigmaNt)))

    	ft2 = at2 / bt2
    	dft2 = sqrt(ft2 * (1-ft2) / bt2)
	at1array.append(at1)
	at2array.append(at2)
	bt1array.append(bt1)
	bt2array.append(bt2)
	#print "mc int 1 "+str(at2)
	#print "mc int 2 "+str(bt2)
	temp=0.
	#print "Monte Carlo"
    	#for ibin in range(t1bin1,t1bin2+1):
	#	print str(hs.GetStack().Last().GetBinLowEdge(ibin)) + " To " + str(hs.GetStack().Last().GetBinLowEdge(ibin)+hs.GetStack().Last().GetBinWidth(ibin))
	#	print "Content " + str(float(hs.GetStack().Last().GetBinContent(ibin)))
	#	temp+=float(hs.GetStack().Last().GetBinContent(ibin))
	#print "total" + str(temp)
	SF = ft1/ft2
	SFerror = sqrt((dft1/ft1)**2+(dft2/ft2)**2)*SF
	#print t1hist
	print "-----------------------------------------"
	print "Data = "+str(ft1) +" +/- "+str(dft1)
	print "MC = "+str(ft2) +" +/- "+str(dft2)
	print "SF = "+str(SF)+" +/- "+str(SFerror)
	singletopt1.Rebin(t1rebins[i])
	t1wjets.Rebin(t1rebins[i])
	t1zjets.Rebin(t1rebins[i])
	t1ttbarSL.Rebin(t1rebins[i])
	t1ttbarFL.Rebin(t1rebins[i])
	t1data.Rebin(t1rebins[i])
	hs = ROOT.THStack( 't1 BkgStack', 't1')
	hs.Add( t1zjets )
	hs.Add( singletopt1 )
	hs.Add( t1wjets )
	hs.Add( t1ttbarFL )
	hs.Add( t1ttbarSL )
	SFarray.append(SF)

	SFerrorarray.append(SFerror)

	c = ROOT.TCanvas('ct1'+t1hist, 'ct1'+t1hist)
	t1data.SetTitle(';'+t1axis[i]+';Events')
	t1data.SetStats(0)
	t1data.Draw('e')

	t1data.SetMaximum( 1.8 * t1data.GetMaximum() )
	hs.Draw('same hist')
	t1data.GetYaxis().SetTitleOffset(0.8)
	t1data.Draw('e same')
		
	leg.Draw()
	prelim = ROOT.TLatex()
	prelim.SetTextFont(42)
	prelim.SetNDC()
	prelim.DrawLatex( 0.15, 0.91, "#scale[1.0]{CMS Preliminary #sqrt{s} = 8 TeV, 19.7 fb^{-1}}" )


	c.Print( 'semiLepMass_'+t1titles[i]+etastring+'_TTWeight.root', 'root')
	c.Print( 'semiLepMass_'+t1titles[i]+etastring+'_TTWeight.pdf', 'pdf')
	i+=1
temp=1.0
temperror=0.0
for iFac in range(0,len(SFarray)):
	temp*=SFarray[iFac]
	temperror+=(SFerrorarray[iFac]*SFerrorarray[iFac])/(SFarray[iFac]*SFarray[iFac])
	#temperror+=SFerrorarray[iFac]*SFerrorarray[iFac]
print ""
print "Top Tagging Scale Factor " +str(temp) + " +/- " + str(temp*sqrt(temperror))

SFtotnum = at1array[4] / bt1array[2]
SFtotnumerr = sqrt(SFtotnum * (1-SFtotnum) / bt1array[2])
SFtotden = at2array[4] / bt2array[2]
SFtotdenerr = sqrt(SFtotden * (1-SFtotden) / bt2array[2])
SFtot = SFtotnum/SFtotden
SFtoterr = sqrt((SFtotnumerr/SFtotnum)**2+(SFtotdenerr/SFtotden)**2)*SFtot

#print ""
#print "-----------------------------------------"
#print "Totals"
#print "-----------------------------------------"
#print "Data = "+str(SFtotnum) +" +/- "+str(SFtotnumerr)
#print "MC = "+str(SFtotden) +" +/- "+str(SFtotdenerr)
#print "SF = "+str(SFtot)+" +/- "+str(SFtoterr)
#print ""
	

