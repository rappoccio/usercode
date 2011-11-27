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
                  default='shyft_fwlite',
                  dest='outname',
                  help='output name')

# Sample name
parser.add_option('--sampleName', metavar='F', type='string', action='store',
                  default='Top',
                  dest='sampleName',
                  help='output name')


# This will use the loose selections, and negate the isolation
# criteria
parser.add_option('--useLoose', metavar='F', action='store_true',
                  default=False,
                  dest='useLoose',
                  help='use loose leptons (exclusive from tight)')

# Using data or not. For MC, truth information is accessed.
parser.add_option('--useData', metavar='F', action='store_true',
                  default=False,
                  dest='useData',
                  help='use data')

# JEC systematics
parser.add_option('--jecSys', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='jecSys',
                  help='JEC Systematic variation. Options are "nominal, up, down"')

# BTag systematics
parser.add_option('--btagSys', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='btagSys',
                  help='BTag Systematic variation. Options are "nominal, up, down"')

# LFTag systematics
parser.add_option('--lftagSys', metavar='F', type='string', action='store',
                  default='nominal',
                  dest='lftagSys',
                  help='LFTag Systematic variation. Options are "nominal, up, down"')


(options, args) = parser.parse_args()

argv = []

# Import everything from ROOT
import ROOT
ROOT.gROOT.Macro("rootlogon.C")

# Import stuff from FWLite
import sys
from DataFormats.FWLite import Events, Handle

from Analysis.SHyFTScripts.combinations import *

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
nMuons = ROOT.TH1F("nMuons",         "Number of Muons, p_{T} > 45 GeV;N_{Muons};Number",               5, -0.5, 4.5 )
nElectrons = ROOT.TH1F("nElectrons",         "Number of Electrons, p_{T} > 60 GeV;N_{Jets};Number",               5, -0.5, 4.5 )

ptMu = ROOT.TH1F("ptMu", "p_{T} of Muon", 200, 0., 200.)
ptEle= ROOT.TH1F("ptEle", "p_{T} of Electron", 200, 0., 200.)
ptJet0 = ROOT.TH1F("ptJet0", "p_{T} Of Leading Jet", 300, 0., 600.)

secvtxMassPlots = []
lepEtaPlots = []
centralityPlots = []
sumPtPlots = []

maxJets = 5
maxTags = 2
flavors = ['_b','_c','_q','']

allVarPlots = [
    secvtxMassPlots,
    lepEtaPlots,
    centralityPlots,
    sumPtPlots
    ]
names = ['secvtxMass','lepEta','centrality','sumPt']
titles = ['SecVtx Mass','Lepton #eta','Centrality','#sum p_{T}']
bounds = [ [40,0.,10.],
           [40,0.,2.5],
           [40,0.,1.0],
           [50,0.,500.] ]

for iplot in range(0,len(allVarPlots)) :
    varPlots = allVarPlots[iplot]
    for ijet in range(0,maxJets+1):
        varPlots.append( [] )
        for itag in range(0,maxTags+1):
            if itag > ijet :
                continue
            varPlots[ijet].append( [] )
            for iflav in range(0,len(flavors)) :
                flav = flavors[iflav]
                varPlots[ijet][itag].append( ROOT.TH1F( options.sampleName + "_" + names[iplot] + "_" + str(ijet) + 'j_' + str(itag) + 't' + flav,
                                                        titles[iplot] + ", njets = " + str(ijet) + ', ntags = ' + str(itag),
                                                        bounds[iplot][0], bounds[iplot][1], bounds[iplot][2])
                                             )


############################################
#     Jet energy scale uncertainties       #
############################################


jecParStr = ROOT.std.string('Jec11_V3_Uncertainty_AK5PFchs.txt')
jecUnc = ROOT.JetCorrectionUncertainty( jecParStr )



############################################
# Physics level parameters for systematics #
############################################

# Kinematic cuts:
jetPtMin = 30.0
muonPtMin = 45.0
electronPtMin = 45.0
looseMuonIsoMax = 0.2
looseElectronIsoMax = 0.2
ssvheCut = 2.74

# Per-jet scale factors:
sfB = 1.00
sfC = 1.00
sfQ = 1.00
if options.btagSys == 'up' :
    sfB = 1.10
    sfC = 1.10
elif options.btagSys == 'down' :
    sfB = 0.90
    sfC = 0.90
if options.lftagSys == 'up' :
    sfQ = 1.10
elif options.lftagSys == 'down' :
    sfQ = 0.90

# JEC scales
jecScale = 0.0
if options.jecSys == 'up' :
    jecScale = 1.0
elif options.jecSys == 'down' :
    jecScale = -1.0
flatJecUnc = 0.05



events = Events (files)

# Make the entirety of the handles required for the
# analysis. 
postfix = ""
if options.useLoose :
    postfix = "Loose"

jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJets" + postfix,   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJets" + postfix,   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJets" + postfix,   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJets" + postfix,   "mass" )
jetSecvtxMassHandle         = Handle( "std::vector<float>" )
jetSecvtxMassLabel    = ( "pfShyftTupleJets" + postfix,   "secvtxMass" )
jetSSVHEHandle         = Handle( "std::vector<float>" )
jetSSVHELabel    = ( "pfShyftTupleJets" + postfix,   "ssvhe" )
jetFlavorHandle         = Handle( "std::vector<float>" )
jetFlavorLabel    = ( "pfShyftTupleJets" + postfix,   "flavor" )

muonPtHandle         = Handle( "std::vector<float>" )
muonPtLabel    = ( "pfShyftTupleMuons" + postfix,   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuons" + postfix,   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuons" + postfix,   "phi" )
muonPfisoHandle         = Handle( "std::vector<float>" )
muonPfisoLabel    = ( "pfShyftTupleMuons" + postfix,   "pfiso" )

electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectrons" + postfix,   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectrons" + postfix,   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectrons" + postfix,   "phi" )
electronPfisoHandle         = Handle( "std::vector<float>" )
electronPfisoLabel    = ( "pfShyftTupleElectrons" + postfix,   "pfiso" )

metHandle = Handle( "std::vector<float>" )
metLabel = ("pfShyftTupleMET" + postfix,   "pt" )
metPhiHandle = Handle( "std::vector<float>" )
metPhiLabel = ("pfShyftTupleMET" + postfix,   "phi" )




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
    

    #Require exactly one lepton (e or mu)

    lepType = 0 # Let 0 = muon, 1 = electron    
    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
        continue
    muonPts = muonPtHandle.product()

    event.getByLabel (muonEtaLabel, muonEtaHandle)
    muonEtas = muonEtaHandle.product()
    event.getByLabel (muonPhiLabel, muonPhiHandle)
    muonPhis = muonPhiHandle.product()


    
    event.getByLabel (electronPtLabel, electronPtHandle)
    if not electronPtHandle.isValid():
        continue
    electronPts = electronPtHandle.product()
    event.getByLabel (electronEtaLabel, electronEtaHandle)
    electronEtas = electronEtaHandle.product()
    event.getByLabel (electronPhiLabel, electronPhiHandle)
    electronPhis = electronPhiHandle.product()


    # Get the isolation values if needed
    if options.useLoose :
        event.getByLabel (muonPfisoLabel, muonPfisoHandle)
        if not muonPfisoHandle.isValid():
            continue
        muonPfisos = muonPfisoHandle.product()
        event.getByLabel (electronPfisoLabel, electronPfisoHandle)
        if not electronPfisoHandle.isValid():
            continue
        electronPfisos = electronPfisoHandle.product()


    

    nMuonsVal = 0
    for imuonPt in range(0,len(muonPts)):
        muonPt = muonPts[imuonPt]
        if muonPt > muonPtMin :
            if options.useLoose :
                if muonPfisos[imuonPt] / muonPt < looseMuonIsoMax :
                    continue
                else :
                    nMuonsVal += 1
                    lepType = 0
            else :
                nMuonsVal += 1
                lepType = 0                
                    
    nMuons.Fill( nMuonsVal )
    if nMuonsVal > 0 :
        ptMu.Fill( muonPts[0] )

    event.getByLabel (electronPtLabel, electronPtHandle)
    electronPts = electronPtHandle.product()

    nElectronsVal = 0
    if nMuonsVal == 0 :
        for ielectronPt in range(0,len(electronPts)):
            electronPt = electronPts[ielectronPt]
            if electronPt > electronPtMin :
                if options.useLoose :
                    if electronPfisos[ielectronPt] / electronPt < looseElectronIsoMax :
                        continue
                    else :
                        nElectronsVal += 1
                        lepType = 1
                else :
                    nElectronsVal += 1
                    lepType = 1
                        
    nElectrons.Fill( nElectronsVal )


    # Require exactly one lepton
    if nMuonsVal + nElectronsVal != 1 :
        continue

    lepEta = -999.0
    if nMuonsVal > 0 :
        lepEta = muonEtas[0]
    else :
        lepEta = electronEtas[0]

    # Now get the number of jets
    event.getByLabel( jetPtLabel, jetPtHandle )
    jetPts = jetPtHandle.product()
    event.getByLabel( jetEtaLabel, jetEtaHandle )
    jetEtas = jetEtaHandle.product()
    event.getByLabel( jetPhiLabel, jetPhiHandle )
    jetPhis = jetPhiHandle.product()
    event.getByLabel( jetMassLabel, jetMassHandle )
    jetMasses = jetMassHandle.product()

    event.getByLabel( metLabel, metHandle )
    metRaw = metHandle.product()[0]
    event.getByLabel( metPhiLabel, metPhiHandle )
    metPhiRaw = metPhiHandle.product()[0]


    jets = []
    met_px = metRaw * math.cos( metPhiRaw )
    met_py = metRaw * math.sin( metPhiRaw )


    for ijet in range(0,len(jetPts) ):
        jetScale = 1.0
        if abs(jecScale) > 0.0001 :
            #print 'Modifying jet pts according to jecScale = ' + str(jecScale)
            jecUnc.setJetEta( jetEtas[ijet] )
            jecUnc.setJetPt( jetPts[ijet] )

            upOrDown = bool(jecScale > 0.0)

            unc1 = abs(jecUnc.getUncertainty(upOrDown))
            unc2 = flatJecUnc
            unc = math.sqrt(unc1*unc1 + unc2*unc2)
            #print 'Correction = ' + str( 1 + unc * jecScale)
            jetScale = 1 + unc * jecScale

        thisJet = ROOT.TLorentzVector()
        thisJet.SetPtEtaPhiM(jetPts[ijet],
                             jetEtas[ijet],
                             jetPhis[ijet],
                             jetMasses[ijet])


        met_px = met_px + thisJet.Px()
        met_py = met_py + thisJet.Py()
        thisJet = thisJet * jetScale
        met_px = met_px - thisJet.Px()
        met_py = met_py - thisJet.Py()
        jets.append( thisJet )


    met = math.sqrt(met_px*met_px + met_py*met_py)

    njets = 0
    for jet in jets :
        if jet.Pt() > jetPtMin :
            njets += 1


    if njets < 1 :
        continue


    # Now get the number of SSVHEM tags and vertex mass.
    # If using MC, get the jet flavor also
    event.getByLabel (jetSSVHELabel, jetSSVHEHandle)
    jetSSVHEs = jetSSVHEHandle.product()
    event.getByLabel( jetSecvtxMassLabel, jetSecvtxMassHandle )
    jetSecvtxMasses = jetSecvtxMassHandle.product()
    if not options.useData :
        event.getByLabel( jetFlavorLabel, jetFlavorHandle )
        jetFlavors = jetFlavorHandle.product()

    # Compute the number of tags, the secondary vertex mass,
    # and the jet flavor (MC only)
    ntags = 0
    secvtxMass = 0.0
    flavorIndex = -1
    numB = 0
    numC = 0
    numQ = 0
    sumEt = 0.
    sumPt = 0.
    sumE = 0.
    effs = []
    # The vertex mass for the event is the vertex mass
    # of the first tagged jet (ordered by pt).
    # The flavor for the event is the highest flavor
    # in the event out of b, c, and light flavor.
    for ijet in range(0,len(jets)) :
        jetP4 = jets[ijet]
        if jetP4.Pt() < jetPtMin :
            continue
        sumEt = sumEt + jetP4.Et()
        sumPt = sumPt + jetP4.Pt()
        sumE = sumE + jetP4.E()
        ssvhe = jetSSVHEs[ijet]
        isf = 1.0
        iflavor = -1
        if not options.useData :
            jetFlavor = jetFlavors[ijet]
            
            #print 'jet flavor = ' + str(jetFlavor)
            if abs(jetFlavor) == 5 :
                numB = numB + 1
                isf = sfB
                iflavor = 0
            elif abs(jetFlavor) == 4 :
                numC = numC + 1
                isf = sfC
                iflavor = 1
            else :
                numQ = numQ + 1
                isf = sfQ
                iflavor = 2
        # Only consider tagged jets for the vertex mass
        if ssvhe > ssvheCut :
            ntags += 1
            # The
            if secvtxMass <= 0.0001 : # Stop at the first nontrivial secvtx mass
                secvtxMass = jetSecvtxMasses[ijet]



        # For the SF weighting, use :
        # the scale factors if tagged
        # zero if not tagged
        if not options.useData :
            if ssvhe > ssvheCut :
                effs.append( EffInfo(ijet, isf, iflavor) )
            else :
                effs.append( EffInfo(ijet, 0.0, iflavor) )

    if numB > 0 :
        flavorIndex = 0
    elif numC > 0 :
        flavorIndex = 1
    else :
        flavorIndex = 2



    nJets.Fill( njets )

    if njets > maxJets :
        njets = maxJets
    if ntags > maxTags :
        ntags = maxTags

    #if not options.useData :
    #    print 'Njets = {0:6.0f}, Ntags = {1:6.0f}, flavorIndex = {2:3.0f}, histname = {3:12s}'.format(
    #        njets, ntags, flavorIndex, secvtxMassPlots[njets][ntags][flavorIndex].GetName() )
        
    #else :
    #    print 'Njets = {0:6.0f}, Ntags = {1:6.0f}, histname = {2:12s}'.format(
    #        njets, ntags, secvtxMassPlots[njets][ntags][3].GetName() )

    # Now fill discriminator variables

    if options.useData :
        # always fill the "total" 
        secvtxMassPlots[njets][ntags][3].Fill( secvtxMass ) 
        lepEtaPlots[njets][ntags][3].Fill( lepEta )
        centralityPlots[njets][ntags][3].Fill( sumEt / sumE )
        sumPtPlots[njets][ntags][3].Fill( sumPt )

        if flavorIndex >= 0 :
            secvtxMassPlots[njets][ntags][flavorIndex].Fill( secvtxMass ) # Fill each jet flavor individually
            lepEtaPlots[njets][ntags][flavorIndex].Fill( lepEta )
            centralityPlots[njets][ntags][flavorIndex].Fill( sumEt / sumE )
            sumPtPlots[njets][ntags][flavorIndex].Fill( sumPt )
    else :

        # otherwise, loop over all of the SF combinatorics to tag itag out of njet jets
        # and weight the distributions by the resultant probability. 
        effCombos = EffInfoCombinations( effs, verbose=False )

        for itag in range(0,njets) :
            pTag = effCombos.pTag( itag )
            jtag = itag
            if jtag > maxTags :
                jtag = maxTags
            # always fill the "total"
            if jtag > 0 :
                secvtxMassPlots[njets][jtag][3].Fill( secvtxMass, pTag ) 
            lepEtaPlots[njets][jtag][3].Fill( lepEta, pTag )
            centralityPlots[njets][jtag][3].Fill( sumEt / sumE, pTag )
            sumPtPlots[njets][jtag][3].Fill( sumPt, pTag )

            if flavorIndex >= 0 :
                if jtag > 0 :
                    secvtxMassPlots[njets][jtag][flavorIndex].Fill( secvtxMass, pTag ) # Fill each jet flavor individually
                lepEtaPlots[njets][jtag][flavorIndex].Fill( lepEta, pTag )
                centralityPlots[njets][jtag][flavorIndex].Fill( sumEt / sumE, pTag )
                sumPtPlots[njets][jtag][flavorIndex].Fill( sumPt, pTag )


f.cd()
f.Write()
f.Close()
