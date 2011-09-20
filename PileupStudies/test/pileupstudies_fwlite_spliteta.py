#! /usr/bin/env python
import os
import glob
import math

from optparse import OptionParser

parser = OptionParser()


############################################
#            Job steering                  #
############################################

# Input files to use. This is in "glob" format, so you can use wildcards.
# If you get a "cannot find file" type of error, be sure to use "\*" instead
# of "*" to make sure you don't confuse the shell. 
parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')

# Output name to use. 
parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='pileupstudies_fwlite_spliteta',
                  dest='outname',
                  help='output name')


# Output name to use. 
parser.add_option('--max', metavar='M', type='int', action='store',
                  default=-1,
                  dest='max',
                  help='Maximum number of events to process, default = all')


(options, args) = parser.parse_args()

argv = []

# Import everything from ROOT
import ROOT
ROOT.gROOT.Macro("rootlogon.C")

# Import stuff from FWLite
import sys
from DataFormats.FWLite import Events, Handle

ROOT.gSystem.Load('libCondFormatsJetMETObjects')

#from CondFormats.JetMETObjects import *


def findGenJet( recoJet0, genJets ) :
    minDR = 0.5
    for genJet in genJets :
        dR = recoJet.DeltaR( genJet )
        if dR < minDR :
            return genJet


print 'Getting files from this dir: ' + options.files

# Get the file list. 
files = glob.glob( options.files )
print files


# Create the output file. 
f = ROOT.TFile(options.outname + ".root", "recreate")
f.cd()


# Make histograms
print "Creating histograms"

nJets = ROOT.TH1F("nJets",         "Number of Jets, p_{T} > 30 GeV;N_{Jets};Number",               20, -0.5, 19.5 )


############################################
#     Jet energy scale and uncertainties   #
############################################



jecStr = [
    'Jec11_V3_L1FastJet_AK5PFchs.txt',
    'Jec11_V3_L2Relative_AK5PFchs.txt',
    'Jec11_V3_L3Absolute_AK5PFchs.txt',
    ]

jecPars = ROOT.std.vector(ROOT.JetCorrectorParameters)()

for ijecStr in jecStr :
    ijec = ROOT.JetCorrectorParameters( ijecStr )
    jecPars.push_back( ijec )
    

jec = ROOT.FactorizedJetCorrector(jecPars)

jecUncStr = ROOT.std.string('Jec11_V3_Uncertainty_AK5PFchs.txt')
jecUnc = ROOT.JetCorrectionUncertainty( jecUncStr )



############################################
# Physics level parameters for systematics #
############################################

# Kinematic cuts:
jetPtMin = 30.0


print 'Creating events...',
events = Events (files)
print 'Done'

jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "ak5CHS",   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "ak5CHS",   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "ak5CHS",   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "ak5CHS",   "mass" )
jetAreaHandle         = Handle( "std::vector<float>" )
jetAreaLabel    = ( "ak5CHS",   "jetArea" )


genJetPtHandle         = Handle( "std::vector<float>" )
genJetPtLabel    = ( "ak5Gen",   "pt" )
genJetEtaHandle         = Handle( "std::vector<float>" )
genJetEtaLabel    = ( "ak5Gen",   "eta" )
genJetPhiHandle         = Handle( "std::vector<float>" )
genJetPhiLabel    = ( "ak5Gen",   "phi" )
genJetMassHandle         = Handle( "std::vector<float>" )
genJetMassLabel    = ( "ak5Gen",   "mass" )

puHandle = Handle("std::vector<PileupSummaryInfo>")
puLabel = ( "addPileupInfo", "")

rhoLabels = [
    ( "fixedGridRhoCentralCHS", "" ),
    ( "fixedGridRhoForwardCHS", "" )
    ]


irhoLabel = "fixedGridRhoMixedCHS"
etaRatioHists = ROOT.TH3F('etaRatio_' + irhoLabel, 'etaRecoRatio_' + irhoLabel, 50, -5.0, 5.0, 200, 0., 2.0, 5, 0, 25)
ptRatioHists = ROOT.TH3F('ptRatio_' + irhoLabel, 'ptRecoRatio_' + irhoLabel, 50, 0., 500., 200, 0., 2.0, 5, 0, 25)


rhoHandle         = Handle( "double" )
    
# loop over events
count = 0
ntotal = events.size()
if options.max > 0 :
    ntotal = options.max
percentDone = 0.0
ipercentDone = 0
ipercentDoneLast = -1
print "Start looping"
for event in events:
    ipercentDone = int(percentDone)
    if ipercentDone != ipercentDoneLast :
        ipercentDoneLast = ipercentDone
        print 'Processing {0:10.0f}/{1:10.0f} : {2:5.0f}%'.format(
            count, ntotal, ipercentDone )
    count = count + 1
    percentDone = float(count) / float(ntotal) * 100.0


    if options.max > 0 and count > options.max :
        break

    event.getByLabel( jetPtLabel, jetPtHandle )
    jetPts = jetPtHandle.product()

    njet = 0
    for jetPt in jetPts :
        if jetPt > 30.0 :
            njet += 1
    if njet < 2 :
        continue



    event.getByLabel( genJetPtLabel, genJetPtHandle )
    genJetPts = genJetPtHandle.product()

    ngenjet = 0
    for jetPt in genJetPts :
        if jetPt > 30.0 :
            ngenjet += 1
    if ngenjet < 2 :
        continue


    event.getByLabel( puLabel, puHandle )
    puInfos = puHandle.product()

    npu = puInfos[0].getPU_NumInteractions()

#    print '======================================'
#    print 'NPU = ' + str(npu)


    
    event.getByLabel( jetEtaLabel, jetEtaHandle )
    jetEtas = jetEtaHandle.product()
    event.getByLabel( jetPhiLabel, jetPhiHandle )
    jetPhis = jetPhiHandle.product()
    ## event.getByLabel( jetMassLabel, jetMassHandle )
    ## jetMasses = jetMassHandle.product()
    event.getByLabel( jetAreaLabel, jetAreaHandle )
    jetAreas = jetAreaHandle.product()



    event.getByLabel( genJetEtaLabel, genJetEtaHandle )
    genJetEtas = genJetEtaHandle.product()
    event.getByLabel( genJetPhiLabel, genJetPhiHandle )
    genJetPhis = genJetPhiHandle.product()
    ## event.getByLabel( genJetMassLabel, genJetMassHandle )
    ## genJetMasses = genJetMassHandle.product()

    #print 'got all products'

    genJets = []
    for igen in range(0,len(genJetPts)):
        if genJetPts[igen] < 30.0 :
            continue
        jgen = ROOT.TLorentzVector()
        jgen.SetPtEtaPhiM(
            genJetPts[igen],
            genJetEtas[igen],
            genJetPhis[igen],
            0.0 #genJetMasses[igen],
            )
        genJets.append( jgen )


    for ijet in range(0,2):

        if jetPts[ijet] < 30.0 :
            continue

        recoJet = ROOT.TLorentzVector()
        recoJet.SetPtEtaPhiM(
            jetPts[ijet],
            jetEtas[ijet],
            jetPhis[ijet],
            0.0 #jetMasses[ijet] 
            )

        #print 'getting gen jet matched'
        genJet = findGenJet( recoJet,
                             genJets )


        region = 0
        if abs(recoJet.Eta()) > 2.1 :
            region = 1


        rhoLabel = rhoLabels[region]
        event.getByLabel( rhoLabel, rhoHandle )
        rho = rhoHandle.product()[0]


        jec.setJetEta(jetEtas[ijet])
        jec.setJetPt(jetPts[ijet])
        jec.setJetA(jetAreas[ijet])
        jec.setRho(rho)
        factor = jec.getCorrection()

        if genJet is not None  :
            ptRatioHists .Fill( genJet.Pt(),  factor * recoJet.Pt() /genJet.Pt(),  npu )
            etaRatioHists.Fill( genJet.Eta(), factor * recoJet.Pt() /genJet.Pt(),  npu )


f.cd()
f.Write()
f.Close()
