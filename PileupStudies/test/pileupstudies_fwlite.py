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
                  default='pileupstudies_fwlite',
                  dest='outname',
                  help='output name')


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




events = Events (files)

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

rhoHandle         = Handle( "double" )
rhoLabel    = ( "kt6PFJetsPFlow",   "rho" )


# loop over events
count = 0
ntotal = events.size()
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
    

    event.getByLabel( jetPtLabel, jetPtHandle )
    jetPts = jetPtHandle.product()
    event.getByLabel( jetEtaLabel, jetEtaHandle )
    jetEtas = jetEtaHandle.product()
    event.getByLabel( jetPhiLabel, jetPhiHandle )
    jetPhis = jetPhiHandle.product()
    event.getByLabel( jetMassLabel, jetMassHandle )
    jetMasses = jetMassHandle.product()
    event.getByLabel( jetAreaLabel, jetAreaHandle )
    jetAreas = jetAreaHandle.product()
    event.getByLabel( rhoLabel, rhoHandle )
    rho = rhoHandle.product()[0]


    jetP4s = []

    for ijet in range(0,len(jetPts)):

        jec.setJetEta(jetEtas[ijet])
        jec.setJetPt(jetPts[ijet])
        jec.setJetA(jetAreas[ijet])
        jec.setRho(rho)
        factor = jec.getCorrection()
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(
            jetPts[ijet],
            jetEtas[ijet],
            jetPhis[ijet],
            jetMasses[ijet] )
        jet *= factor
        jetP4s.append( jet )
        print 'Jet {0:3.0f}, pt = {1:6.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, area = {5:6.2f}'.format(
            ijet,
            jet.Pt(),
            jet.Eta(),
            jet.Phi(),
            jet.M(),
            jetAreas[ijet]
            )


f.cd()
f.Write()
f.Close()
