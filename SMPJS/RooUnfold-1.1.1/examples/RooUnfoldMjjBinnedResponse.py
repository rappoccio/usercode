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

from ROOT import *

gROOT.Macro("rootlogon.C")

from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
# from ROOT import RooUnfoldSvd
# from ROOT import RooUnfoldTUnfold

from array import *

# ==============================================================================
#  Example Unfolding
# ==============================================================================


fResponse = TFile("QCD_pythia6_z2_v10beta_plots.root")

fData = TFile('rawDataMCComparisons_histAK7MjetVsPtAvg.root')

obsStr = 'jetdata_'

sResponse3D = 'histAK7MjetGenVsRecoVsPtAvg'
sTrue = 'histAK7MjetGenVsPtAvg'
sClosure = 'histAK7MjetVsPtAvg'

ptBins =[
  [125.,200.],
  [200.,300.],
  [300.,400.],
  [400.,500.]
  ]

canvs = []
hists = []
responses = []
legs = []
hists3D = []

response3DAll = fResponse.Get(sResponse3D)
response2DAll=response3DAll.Project3D('xy')
response2DAll.SetName( response3DAll.GetName() + 'all')
response2DAll.Scale(1.0 / response2DAll.Integral() )
responseRUAll = RooUnfoldResponse(0,0,response2DAll, 'responseAll', 'responseAll')
crall = TCanvas('crall', 'crall')
response2DAll.Draw('colz')

for iptBin in xrange(len(ptBins)) :
  ptBin = ptBins[iptBin]
  response3D = response3DAll.Clone()
  response3D.SetName( response3DAll.GetName() + str(iptBin) )
  bin0 = response3D.GetZaxis().FindBin( ptBin[0] )
  bin1 = response3D.GetZaxis().FindBin( ptBin[1] )
  print 'Looking at pt from ' + str(ptBin[0]) + ' to ' + str(ptBin[1]) + ', bins = ' + str(bin0) + ' - ' + str(bin1)
  response3D.GetZaxis().SetRange(bin0,bin1)
  response2D=response3D.Project3D('xy')
  response2D.SetName( response3D.GetName() + str(iptBin))

  c = TCanvas('response' + str(iptBin), 'response' + str(iptBin))
  response2D.Rebin2D(10,10)
  response2D.Sumw2()
  response2D.Scale(1.0 / response2D.Integral())

  response2D.Draw('colz')
  canvs.append(c)
  hists.append(response2D)

  responseRU = RooUnfoldResponse(0,0,response2D, 'response' + str(iptBin), 'response' + str(iptBin))
  responses.append(responseRU)


  #hMeas = fData.Get(obsStr + str(iptBin))

  hClosure2D = fResponse.Get(sClosure)
  ybin0 = hClosure2D.GetYaxis().FindBin(ptBins[iptBin][0])
  ybin1 = hClosure2D.GetYaxis().FindBin(ptBins[iptBin][1])
  hMeas = hClosure2D.ProjectionX( 'hClosure' + str(iptBin), ybin0, ybin1)
  hMeas.SetName( 'hClosure' + str(iptBin) )
  
  hMeas.SetMarkerStyle(28)
  #hMeas.Rebin(10)
  hists.append(hMeas)
                      
  hTrue2D = fResponse.Get(sTrue)
  ybin0 = hTrue2D.GetYaxis().FindBin(ptBins[iptBin][0])
  ybin1 = hTrue2D.GetYaxis().FindBin(ptBins[iptBin][1])
  hTrue = hTrue2D.ProjectionX( 'hTrue' + str(iptBin), ybin0, ybin1)
  hTrue.SetName( 'hTrue' + str(iptBin) )
  #hTrue.Rebin(10)
  hTrue.Scale( hMeas.Integral() / hTrue.Integral() )

  print "==================================== UNFOLD ==================================="
  #unfold= RooUnfoldBayes     (response, hMeas, 4);    #  OR
  # unfold= RooUnfoldSvd     (response, hMeas, 20);   #  OR
  # unfold= RooUnfoldTUnfold (response, hMeas);


  unfold= RooUnfoldBinByBin  (responseRU, hMeas)
  #unfold= RooUnfoldBinByBin  (responseRUAll, hMeas)

  #unfold= RooUnfoldSvd     (responseRU, hMeas, 20)
  hReco= unfold.Hreco()
  hReco.SetTitle( str(ptBin[0]) + ' < p_{T}^{AVG} < ' + str(ptBin[1])  + ';m_{jet} (GeV)')
  hReco.SetMarkerStyle(21)
  unfold.PrintTable (cout, hTrue)
  cu = TCanvas('cu' + str(iptBin), 'cu' + str(iptBin))
  hReco.Draw('e')
  hMeas.Draw('e same')
  hTrue.SetLineColor(8)
  hTrue.Draw("hist SAME")
  cu.SetLogy()

  leg = TLegend(0.6, 0.6, 0.84, 0.84)
  leg.SetFillColor(0)
  leg.SetBorderSize(0)
  leg.AddEntry( hMeas, 'Raw', 'p')
  leg.AddEntry( hTrue, 'Truth', 'f')
  leg.AddEntry( hReco, 'Unfolded', 'p')
  leg.Draw()
  legs.append(leg)

  canvs.append(cu)
  cu.Print('unfolded_mjet_' + str(iptBin) + '.png', 'png')
  cu.Print('unfolded_mjet_' + str(iptBin) + '.pdf', 'pdf')
