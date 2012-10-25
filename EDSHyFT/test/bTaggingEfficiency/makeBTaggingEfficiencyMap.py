#!/usr/bin/env python

import os, sys
from ROOT import gROOT, TFile, TH2D
from array import array

gROOT.SetBatch(1)

#----------------------------------------------------------------------------------
# Configurable parameters

datasets = [
  # Background
  [
    '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/jpilot-TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola-Summer12_DR53X-PU_S10-fe5dcf8cf2a24180bf030f68a7d97dda/USER', # dataset name
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for b jets
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],  # jet Pt and |eta| bins for c jets
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},  # jet Pt and |eta| bins for udsg jets
    'TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_CA8PrunedPF_CSVM'  # output filename
  ],
  [
    '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]]},
    'WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball_CA8PrunedPF_CSVM'
  ],
  [
    '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/bazterra-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
    {'b':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 120., 1000.],[0., 0.6, 1.2, 2.4]]},
    'DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_CA8PrunedPF_CSVM'
  ],
  [
    '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 120., 240., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]]},
    'T_s-channel_TuneZ2star_8TeV-powheg-tauola_CA8PrunedPF_CSVM'
  ],
  [
    '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 1000.],[0., 0.6, 1.2, 2.4]]},
    'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola_CA8PrunedPF_CSVM'
  ],
  [
    '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/agarabed-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 1000.],[0., 0.6, 1.2, 2.4]]},
    'T_t-channel_TuneZ2star_8TeV-powheg-tauola_CA8PrunedPF_CSVM'
  ],
  [
    '/WW_TuneZ2star_8TeV_pythia6_tauola/mmhl-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'WW_TuneZ2star_8TeV_pythia6_tauola_CA8PrunedPF_CSVM'
  ],
  [
    '/WZ_TuneZ2star_8TeV_pythia6_tauola/bcalvert-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'WZ_TuneZ2star_8TeV_pythia6_tauola_CA8PrunedPF_CSVM'
  ],
  # Signal
  [
    '/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M450_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph_CA8PrunedPF_CSVM'
  ],
  [
    '/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph_CA8PrunedPF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph_CA8PrunedPF_CSVM'
  ],
  [
    '/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph_CA8PrunedPF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 400., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 300., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph_CA8PrunedPF_CSVM'
  ],
  [
    '/BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHBHinc_M800_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2-fe5dcf8cf2a24180bf030f68a7d97dda/USER',
    {'b':    [[0., 40., 60., 80., 100., 150., 200., 300., 500., 1000.],[0., 0.6, 1.2, 2.4]],
     'c':    [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]],
     'udsg': [[0., 40., 60., 80., 100., 150., 200., 1000.],[0., 0.6, 1.2, 2.4]]},
    'BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph_CA8PrunedPF_CSVM'
  ]
]

pathToInputFiles = 'CRAB_Jobs'
inputFileSubdirectory = 'bTaggingEffAnalyzer'
outputFileSuffix = 'bTaggingEfficiencyMap'

#----------------------------------------------------------------------------------

def produceEfficiencyMaps(dataset, inputPath, subdirectory, suffix):

  inputFilename = os.path.join(inputPath, dataset[0].lstrip('/').replace('/','__') + '.root')
  inputFile = TFile(inputFilename, 'READ')

  outputFilename = dataset[2] + '_' + suffix + '.root'
  outputFile = TFile(outputFilename, 'RECREATE')

  for partonFlavor in ['b', 'c', 'udsg']:

    denominatorHisto = subdirectory + '/h2_BTaggingEff_Denom_' + partonFlavor
    numeratorHisto = subdirectory + '/h2_BTaggingEff_Num_' + partonFlavor

    denominatorIn = inputFile.Get(denominatorHisto)
    numeratorIn = inputFile.Get(numeratorHisto)

    xShift = denominatorIn.GetXaxis().GetBinWidth(1)/2.
    yShift = denominatorIn.GetYaxis().GetBinWidth(1)/2.

    binsX = array('d', dataset[1][partonFlavor][0])
    binsY = array('d', dataset[1][partonFlavor][1])

    denominatorOut = TH2D('denominator_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)
    numeratorOut   = TH2D('numerator_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)
    efficiencyOut  = TH2D('efficiency_' + partonFlavor, '', (len(binsX)-1), binsX, (len(binsY)-1), binsY)

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
	  print 'Warning! Bin(%i,%i) for %s jets has a b-tagging efficiency of %.3f'%(i,j,partonFlavor,efficiency)

    # set efficiencies in overflow bins
    for i in range(1,denominatorOut.GetXaxis().GetNbins()+1):
      efficiencyOut.SetBinContent(i, denominatorOut.GetYaxis().GetNbins()+1, efficiencyOut.GetBinContent(i, denominatorOut.GetYaxis().GetNbins()))

    for j in range(1,denominatorOut.GetYaxis().GetNbins()+2):
      efficiencyOut.SetBinContent(denominatorOut.GetXaxis().GetNbins()+1, j, efficiencyOut.GetBinContent(denominatorOut.GetXaxis().GetNbins(), j))

    outputFile.cd()

    denominatorOut.Write()
    numeratorOut.Write()
    efficiencyOut.Write()

  outputFile.Close()

  print 'b-tagging efficiency map for'
  print dataset[0]
  print 'successfully created and stored in %s'%outputFilename
  print ''


def main():

  for dataset in datasets:
    produceEfficiencyMaps(dataset, pathToInputFiles, inputFileSubdirectory, outputFileSuffix)

if __name__ == "__main__":
  main()
