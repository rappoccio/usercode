#!/usr/bin/env python

import sys
from ROOT import gROOT, TFile, TH2D
from array import array

gROOT.SetBatch(1)

#----------------------------------------------------------------------------------
# Configurable parameters

# Choose parton flavor (b, c, or udsg)
partonFlavor = 'b'

inputFilename = 'BprimeBprimeToTWTWinc_bTaggingEfficiency.root'
outputFilename = 'BprimeBprimeToTWTWinc_bTaggingEfficiencyMap.root'

binsX = array('d', [0., 50., 100., 200., 400., 1000.])
binsY = array('d', [0., 0.6, 1.2, 2.4])

#----------------------------------------------------------------------------------

denominatorHisto = 'bTaggingEffAnalyzer/h2_BTaggingEff_Denom_' + partonFlavor
numeratorHisto = 'bTaggingEffAnalyzer/h2_BTaggingEff_Num_' + partonFlavor

inputFile = TFile(inputFilename, 'READ')

denominatorIn = inputFile.Get(denominatorHisto)
numeratorIn = inputFile.Get(numeratorHisto)

xShift = denominatorIn.GetXaxis().GetBinWidth(1)/2.
yShift = denominatorIn.GetYaxis().GetBinWidth(1)/2.

denominatorOut = TH2D('denominator', '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)
numeratorOut   = TH2D('numerator', '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)
efficiencyOut  = TH2D('efficiency', '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)

# loop over all bins
for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
  for j in range(1,denominatorOut.GetYaxis().GetNbins()+1):

    binXMin = denominatorIn.GetXaxis().FindBin(denominatorOut.GetXaxis().GetBinLowEdge(i)+xShift)
    binXMax = denominatorIn.GetXaxis().FindBin(denominatorOut.GetXaxis().GetBinUpEdge(i)-xShift)
    binYMinPos = denominatorIn.GetYaxis().FindBin(denominatorOut.GetYaxis().GetBinLowEdge(j)+yShift)
    binYMaxPos = denominatorIn.GetYaxis().FindBin(denominatorOut.GetYaxis().GetBinUpEdge(j)-yShift)
    binYMinNeg = denominatorIn.GetYaxis().FindBin(-denominatorOut.GetYaxis().GetBinUpEdge(j)+yShift)
    binYMaxNeg = denominatorIn.GetYaxis().FindBin(-denominatorOut.GetYaxis().GetBinLowEdge(j)-yShift)
    
    denominator = denominatorIn.Integral(binXMin,binXMax,binYMinPos,binYMaxPos)
    denominator = denominator + denominatorIn.Integral(binXMin,binXMax,binYMinNeg,binYMaxNeg)
    numerator = numeratorIn.Integral(binXMin,binXMax,binYMinPos,binYMaxPos)
    numerator = numerator + numeratorIn.Integral(binXMin,binXMax,binYMinNeg,binYMaxNeg)

    denominatorOut.SetBinContent(i,j,denominator)
    numeratorOut.SetBinContent(i,j,numerator)
    if(denominator>0.): efficiencyOut.SetBinContent(i,j,numerator/denominator)

# check if there are any bins with 0 or 100% efficiency
for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
  for j in range(1,denominatorOut.GetYaxis().GetNbins()+1):

    efficiency = efficiencyOut.GetBinContent(i,j)
    if(efficiency==0. or efficiency==1.):
      print 'Warning. Bin(%i,%i) has a b-tagging efficiency of %f'%(i,j,efficiency)

# set efficiencies in overflow bins
for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
  efficiencyOut.SetBinContent(i, denominatorOut.GetYaxis().GetNbins()+1, efficiencyOut.GetBinContent(i, denominatorOut.GetYaxis().GetNbins()))

for j in range(1,denominatorOut.GetYaxis().GetNbins()+2):
  efficiencyOut.SetBinContent(denominatorOut.GetXaxis().GetNbins()+1, j, efficiencyOut.GetBinContent(denominatorOut.GetXaxis().GetNbins(), j))


outputFilename = outputFilename.replace('.root','_' + partonFlavor + '.root')
outputFile = TFile(outputFilename, 'RECREATE')
outputFile.cd()

denominatorOut.Write()
numeratorOut.Write()
efficiencyOut.Write()

outputFile.Close()

print 'b-tagging efficiency map successfully created and stored in %s'%outputFilename
