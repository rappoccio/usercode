#!/usr/bin/env python
# ==============================================================================
#  File and Version Information:
#       $Id: RooUnfoldExample.py 302 2011-09-30 20:39:20Z T.J.Adye $
#
#  Description:
#       Simple example usage of the RooUnfold package using toy MC.
#
#  Author: Tim Adye <T.J.Adye@rl.ac.uk>
#
# ==============================================================================


from optparse import OptionParser

parser = OptionParser()


############################################
#            Job steering                  #
############################################


parser.add_option('--gray', metavar='F', action='store_true',
                  default=False,
                  dest='gray',
                  help='Plot in grayscale')


parser.add_option('--groom', metavar='F', type='string', action='store',
                  default=None,
                  dest='groom',
                  help='Groom value')

parser.add_option('--allsys', metavar='F', action='store_true',
                  default=False,
                  dest='allsys',
                  help='Plot all systematic contributions')



(options, args) = parser.parse_args()


from ROOT import *

gROOT.Macro("rootlogon.C")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
# from ROOT import RooUnfoldSvd
# from ROOT import RooUnfoldTUnfold

from array import *

from RooUnfoldMjjObject import RooUnfoldMjjObject
from RooUnfoldMjjTruthObject import RooUnfoldMjjTruthObject
from RooUnfoldMjjUnfoldedMeasurement import RooUnfoldMjjUnfoldedMeasurement


ptBins = array('d', [0., 50., 125., 150., 220., 300., 450., 500., 600., 800., 1000., 1500., 7000.])
maxes = [1.0e+1] * len(ptBins)
mins  = [1.0e-7] * len(ptBins)

if options.groom is None :
  groom = ''
  groomStr = ''
  groomAppend = ''
else :
  groom = '_' + options.groom
  groomStr = options.groom + ' '
  groomAppend = '_' + options.groom


with open('texTemplateUnfolded.tex', 'r') as ftex :
    texStr = ftex.read()
ftex.closed

ftexout = open('unfoldedFigures.tex', 'a')
fdebugout = open('debug.txt', 'a')

nominalName = 'QCD_pythia6_z2_plots_nominal'

mcNonsymSysNames = [
[ 'QCD_pythia6_z2_plots_jerup', 'QCD_pythia6_z2_plots_jerdn', 'JER', 'Energy resolution uncertainty'],
[ 'QCD_pythia6_z2_plots_jecup', 'QCD_pythia6_z2_plots_jecdn', 'JEC', 'Energy uncertainty'],
[ 'QCD_pythia6_z2_plots_jarup', 'QCD_pythia6_z2_plots_jardn', 'JAR', 'Angular resolution uncertainty'],
[ 'QCD_pythia6_z2_plots_puUp',  'QCD_pythia6_z2_plots_puDn', 'PU', 'Pileup uncertainty'],
  ]

mcSymSysNames = [
['QCD_herwigpp_23_plots_nominal', 'Herwig++']
]


trueNames =dict({
  'Pythia6' :'QCD_pythia6_z2_plots_nominal',
  'Pythia8' :'QCD_pythia8_4c_plots_nominal',
  'Herwig++':'QCD_herwigpp_23_plots_nominal'
  })


nominalObj = RooUnfoldMjjObject( nbins=11,
                                ptBins=ptBins,
                                responseFileName='response_full.root',
                                obsFileName='rawDataMCComparisons_histAK7MjetVsPtAvg' + groom + '.root',
                                responseName='response_' + nominalName + groom,
                                mcHistName=nominalName)

truthObj = RooUnfoldMjjTruthObject( nbins=11,
                                   ptBins=ptBins,
                                   trueFileName='trueMCDists_histAK7MjetGenVsPtAvg' + groom + '.root',
                                   trueNames=trueNames
                                   )

mcNonsymSysObjs = []
for isys in xrange(len(mcNonsymSysNames)) :
  sysup = RooUnfoldMjjObject (nbins=11,
                              ptBins=ptBins,
                              responseFileName='response_full.root',
                              obsFileName='rawDataMCComparisons_histAK7MjetVsPtAvg' + groom + '.root',
                              responseName='response_' + mcNonsymSysNames[isys][0] + groom,
                              mcHistName=mcNonsymSysNames[isys][0]
                              )
  sysdn = RooUnfoldMjjObject (nbins=11,
                              ptBins=ptBins,
                              responseFileName='response_full.root',
                              obsFileName='rawDataMCComparisons_histAK7MjetVsPtAvg' + groom + '.root',
                              responseName='response_' + mcNonsymSysNames[isys][1] + groom,
                              mcHistName=mcNonsymSysNames[isys][1]
                              )
  name=mcNonsymSysNames[isys][2]
  title=mcNonsymSysNames[isys][3]
  mcNonsymSysObjs.append( [sysup, sysdn, name, title] )

mcSymSysObjs = []
for isys in xrange(len(mcSymSysNames)) :
  sys = RooUnfoldMjjObject (nbins=11,
                            ptBins=ptBins,
                            responseFileName='response_full.root',
                            obsFileName='rawDataMCComparisons_histAK7MjetVsPtAvg' + groom + '.root',
                            responseName='response_' + mcSymSysNames[isys][0] + groom,
                            mcHistName=mcSymSysNames[isys][0]
                            )
  name=mcSymSysNames[isys][1]
  mcSymSysObjs.append( [sys, name] )


toKeep = []
canvs = []
legs = []
texts = []
pads = []


# A little histogram customization

gStyle.SetTitleFont(43)
gStyle.SetTitleFontSize(18)
gStyle.SetTitleFont(43, "XYZ")
gStyle.SetTitleSize(30, "XYZ")
gStyle.SetTitleOffset(3.5, "X")
gStyle.SetLabelFont(43, "XYZ")
gStyle.SetLabelSize(24, "XYZ")


#gStyle.SetTitleOffset(1.5, "X")
#gStyle.SetTitleOffset(1.5, "Y")

if options.allsys :
  sysDescription = 'The statistical uncertainty is shown in light yellow,' + \
      ' the uncertainties due to the jet-energy resolution, jet-energy scale, and jet-angular resolution are shown in shades of brown,' + \
      ' the uncertainty due to pile-up is shown in green,' + \
      ' and the uncertainty due to the parton shower are shown in dark yellow.'
  sysAppend = '_allsys'
else :
  sysDescription = 'The statistical uncertainty is shown in light yellow (light gray),' + \
      ' and the statistical plus systematic uncertainty is shown in dark yellow (dark gray).'
  sysAppend = ''


for ptBin in range(1,len(ptBins)-2):


  texStrOut = texStr.replace( 'PTBIN', str(ptBin) )
  texStrOut = texStrOut.replace( 'PTMIN', str(ptBins[ptBin]) )
  texStrOut = texStrOut.replace( 'PTMAX', str(ptBins[ptBin+1]) )
  texStrOut = texStrOut.replace( 'GROOMSTRING', groomStr )
  texStrOut = texStrOut.replace( 'GROOMAPPEND', groomAppend )
  texStrOut = texStrOut.replace( 'STATSTRING', sysDescription )
  texStrOut = texStrOut.replace( 'SYSAPPEND', sysAppend )
  
  ftexout.write(texStrOut + '\n\n')

  unfoldedMeasurement = RooUnfoldMjjUnfoldedMeasurement(ptBin,
                                                        nominalObj,
                                                        mcNonsymSysObjs,
                                                        mcSymSysObjs,
                                                        truthObj )

  
  unfoldedMeasurement.doAllUnfolding()
  unfoldedMeasurement.calcMeasurement()
  c = TCanvas('c' + str(ptBin), 'c' + str(ptBin),200,10,960,800)
  p1 = TPad("p1" + str(ptBin),"p1" + str(ptBin),0.0,0.3,1.0,0.97)
  p1.SetBottomMargin(0.05)
  p1.SetNumber(1)
  p2 = TPad("p2" + str(ptBin),"p2" + str(ptBin),0.0,0.00,1.0,0.3)
  p2.SetNumber(2)
  p2.SetTopMargin(0.05)
  p2.SetBottomMargin(0.30)
  pads.append( [p1,p2] )
    
  [stat,statsysE,statsys,py6,py8,hpp,stat_f,statsysE_f,statsys_f,py6_f,py8_f,hpp_f,raw,py6raw] = unfoldedMeasurement.graphs


  sdebug = '{0:6.0f} : {1:6.2e}\n'.format( ptBin, py6.Integral() )
  fdebugout.write(sdebug)

  c.cd()
  p1.Draw()
  p1.cd()
  statsys.Draw('a2p')
  if options.allsys :
    for iistatsysE in xrange(len(statsysE)-1,-1,-1) :
      istatsysE = statsysE[iistatsysE]
      istatsysE.Draw('2p same')
  stat.Draw('2p same')
  py6.Draw('hist same')
  py8.Draw('hist same')
  hpp.Draw('hist same')
  if raw is not None :
    raw.Draw('p same')
  if py6raw is not None :
    py6raw.Draw('hist same')
  statsys.GetHistogram().SetTitle( ';;#frac{1}{#hat{#sigma}} #frac{d#hat{#sigma}}{dm_{J}^{AVG}} #left(#frac{1}{GeV}#right)')
  statsys.GetYaxis().SetTitleOffset(1.5)
  toKeep.append( unfoldedMeasurement )
  p1.SetLogy()
  statsys.GetHistogram().SetMaximum(maxes[ptBin])
  statsys.GetHistogram().SetMinimum(mins[ptBin])
  statsys.GetHistogram().GetXaxis().SetLabelSize(0)




  leg = TLegend(0.6, 0.56, 0.84, 0.84)
  leg.SetFillColor(0)
  leg.SetBorderSize(0)
  if raw is not None :
    leg.AddEntry( raw, 'Raw data', 'p')
  leg.AddEntry( stat, 'Unfolded Data', 'p')
  leg.AddEntry( stat, 'Statistical Uncertainty', 'f')
  if options.allsys :
    for isys in xrange(len(statsysE)):
      istatsysE = statsysE[isys]
      leg.AddEntry( istatsysE, mcNonsymSysNames[isys][3], 'f')
    leg.AddEntry( statsys, 'Parton Shower Uncertainty', 'f')
  else :
    leg.AddEntry( statsys, 'Total Uncertainty', 'f')
  leg.AddEntry( py6, 'Pythia6, Z2', 'l')
  leg.AddEntry( py8, 'Pythia8, 4c', 'l')
  leg.AddEntry( hpp, 'Herwig++, 23', 'l')
  leg.Draw()
  legs.append(leg)


  text1 = TLatex()
  text1.SetNDC()
  text1.SetTextFont(42)
  text1.DrawLatex(0.13,0.86, "#scale[1.0]{CMS Preliminary, L = 5 fb^{-1} at  #sqrt{s} = 7 TeV}")
  texts.append(text1)

  text2 = TLatex()
  text2.SetNDC()
  text2.SetTextFont(42)
  text2.SetTextSize(0.05)
  text2.DrawLatex( 0.25, 0.75, str(ptBins[ptBin]) + ' < p_{T}^{AVG} < ' + str(ptBins[ptBin+1])  )
  p1.RedrawAxis()

  c.cd()
  p2.Draw()
  p2.cd()
  statsys_f.Draw('a2p')
  if options.allsys :
    for iistatsysE_f in xrange(len(statsysE_f)-1,-1,-1) :
      istatsysE_f = statsysE_f[iistatsysE_f]
      istatsysE_f.Draw('2p same')
  stat_f.Draw('2p same')
  py6_f.Draw('hist same')
  py8_f.Draw('hist same')
  hpp_f.Draw('hist same')
  statsys_f.GetHistogram().SetTitle( ';m_{J}^{AVG} (GeV);MC/Data')
  statsys_f.GetHistogram().SetMaximum(2.0)
  statsys_f.GetHistogram().SetMinimum(0.0)

  statsys_f.GetHistogram().GetYaxis().SetNdivisions(4,2,0,False)


  p2.RedrawAxis()
  c.cd()
  c.RedrawAxis()
  appendstr = ''
  if options.groom is not None :
    appendstr += groom
  if options.gray :
    appendstr += '_gray'
    c.SetGrayscale()
  if options.allsys :
    appendstr += '_allsys'
  c.Update()  
  canvs.append(c)
  c.Print('unfoldedMeasurementDijets_' + str(ptBin) + appendstr + '.png', 'png')
  c.Print('unfoldedMeasurementDijets_' + str(ptBin) + appendstr + '.pdf', 'pdf')
  
