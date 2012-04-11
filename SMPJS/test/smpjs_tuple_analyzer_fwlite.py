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
                  default='smpjs_fwlite',
                  dest='outname',
                  help='output name')

# Use MC information, otherwise use trigger information
parser.add_option('--useMC', action='store_true',
                  default=False,
                  dest='useMC',
                  help='Use MC Weight (True) or weight by trigger prescale (False)')

# Output name to use. 
parser.add_option('--max', metavar='M', type='int', action='store',
                  default=-1,
                  dest='max',
                  help='Maximum number of events to process, default = all')



# Print verbose information
parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Print verbose information')

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
        dR = recoJet0.DeltaR( genJet )
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


jecUncStr = ROOT.std.string('Jec11_V3_Uncertainty_AK5PFchs.txt')
jecUnc = ROOT.JetCorrectionUncertainty( jecUncStr )



############################################
# Physics level parameters for systematics #
############################################

# Kinematic cuts:
jetPtMin = 30.0
jetEtaMax = 2.5


print 'Creating events...',
events = Events (files)
print 'Done'


ak7DefPxHandle         = Handle( "std::vector<float>" )
ak7DefPxLabel          = ( "ak7Lite",   "px" )
ak7DefPyHandle         = Handle( "std::vector<float>" )
ak7DefPyLabel          = ( "ak7Lite",   "py" )
ak7DefPzHandle         = Handle( "std::vector<float>" )
ak7DefPzLabel          = ( "ak7Lite",   "pz" )
ak7DefEnergyHandle     = Handle( "std::vector<float>" )
ak7DefEnergyLabel      = ( "ak7Lite",   "energy" )


ak5DefPxHandle         = Handle( "std::vector<float>" )
ak5DefPxLabel          = ( "ak5Lite",   "px" )
ak5DefPyHandle         = Handle( "std::vector<float>" )
ak5DefPyLabel          = ( "ak5Lite",   "py" )
ak5DefPzHandle         = Handle( "std::vector<float>" )
ak5DefPzLabel          = ( "ak5Lite",   "pz" )
ak5DefEnergyHandle     = Handle( "std::vector<float>" )
ak5DefEnergyLabel      = ( "ak5Lite",   "energy" )

ak5FilteredPxHandle         = Handle( "std::vector<float>" )
ak5FilteredPxLabel          = ( "ak5FilteredLite",   "px" )
ak5FilteredPyHandle         = Handle( "std::vector<float>" )
ak5FilteredPyLabel          = ( "ak5FilteredLite",   "py" )
ak5FilteredPzHandle         = Handle( "std::vector<float>" )
ak5FilteredPzLabel          = ( "ak5FilteredLite",   "pz" )
ak5FilteredEnergyHandle     = Handle( "std::vector<float>" )
ak5FilteredEnergyLabel      = ( "ak5FilteredLite",   "energy" )

ak5PrunedPxHandle         = Handle( "std::vector<float>" )
ak5PrunedPxLabel          = ( "ak5PrunedLite",   "px" )
ak5PrunedPyHandle         = Handle( "std::vector<float>" )
ak5PrunedPyLabel          = ( "ak5PrunedLite",   "py" )
ak5PrunedPzHandle         = Handle( "std::vector<float>" )
ak5PrunedPzLabel          = ( "ak5PrunedLite",   "pz" )
ak5PrunedEnergyHandle     = Handle( "std::vector<float>" )
ak5PrunedEnergyLabel      = ( "ak5PrunedLite",   "energy" )

ak5TrimmedPxHandle         = Handle( "std::vector<float>" )
ak5TrimmedPxLabel          = ( "ak5TrimmedLite",   "px" )
ak5TrimmedPyHandle         = Handle( "std::vector<float>" )
ak5TrimmedPyLabel          = ( "ak5TrimmedLite",   "py" )
ak5TrimmedPzHandle         = Handle( "std::vector<float>" )
ak5TrimmedPzLabel          = ( "ak5TrimmedLite",   "pz" )
ak5TrimmedEnergyHandle     = Handle( "std::vector<float>" )
ak5TrimmedEnergyLabel      = ( "ak5TrimmedLite",   "energy" )




ak7GenPxHandle         = Handle( "std::vector<float>" )
ak7GenPxLabel          = ( "ak7Gen",   "px" )
ak7GenPyHandle         = Handle( "std::vector<float>" )
ak7GenPyLabel          = ( "ak7Gen",   "py" )
ak7GenPzHandle         = Handle( "std::vector<float>" )
ak7GenPzLabel          = ( "ak7Gen",   "pz" )
ak7GenEnergyHandle     = Handle( "std::vector<float>" )
ak7GenEnergyLabel      = ( "ak7Gen",   "energy" )

ak5GenPxHandle         = Handle( "std::vector<float>" )
ak5GenPxLabel          = ( "ak5Gen",   "px" )
ak5GenPyHandle         = Handle( "std::vector<float>" )
ak5GenPyLabel          = ( "ak5Gen",   "py" )
ak5GenPzHandle         = Handle( "std::vector<float>" )
ak5GenPzLabel          = ( "ak5Gen",   "pz" )
ak5GenEnergyHandle     = Handle( "std::vector<float>" )
ak5GenEnergyLabel      = ( "ak5Gen",   "energy" )

puHandle = Handle("std::vector<PileupSummaryInfo>")
puLabel = ( "addPileupInfo", "")


generatorHandle = Handle("GenEventInfoProduct")
generatorLabel = ( "generator", "")


trigHandle = Handle("pat::TriggerEvent")
trigLabel = ( "patTriggerEvent", '')

histAK7MjjVsEtaMax = ROOT.TH2F('histAK7MjjVsEtaMax', 'AK7 m_{jj} Versus #eta_{max};m_{jj} (GeV);#eta_{max}(radians)', 300, 0., 3000., 5, 0.0, 2.5)
histAK7MjetVsEtaMax = ROOT.TH2F('histAK7MjetVsEtaMax', 'AK7 <m_{jet}> Versus #eta_{max};<m_{jet}> (GeV);#eta_{max}(radians)', 300, 0., 300., 5, 0.0, 2.5)


# Use the same trigger thresholds as QCD-11-004 in AN-364-v4 Table 8
trigsToKeep = [
    'HLT_Jet60',
    'HLT_Jet110',
    'HLT_Jet190',
    'HLT_Jet240',
    'HLT_Jet370',
    ]
# Here are the trigger thresholds for the various eta bins.
# In the following, each entry is an eta bin. The
# two fields are then [etamin,etamax], and the
# list of mjj thresholds for HLT_Jet60,110,190,240,370.
trigThresholds = [
[[0.0, 0.5], [ 178.,  324.,  533.,  663.,  970.] ],
[[0.5, 1.0], [ 240.,  390.,  645.,  820., 1218.] ],
[[1.0, 1.5], [ 369.,  615.,  998., 1261., 1904.] ],
[[1.5, 2.0], [ 530.,  920., 1590., 1985., 3107.] ],
[[2.0, 2.5], [ 913., 1549., 2665., 3700., 4000.] ]
    ]


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
    weight = 1.0
    ipercentDone = int(percentDone)
    if ipercentDone != ipercentDoneLast :
        ipercentDoneLast = ipercentDone
        print 'Processing {0:10.0f}/{1:10.0f} : {2:5.0f}%'.format(
            count, ntotal, ipercentDone )
    count = count + 1
    percentDone = float(count) / float(ntotal) * 100.0


    if options.max > 0 and count > options.max :
        break


    # Event-level variables:
    npv = -1         # Number of Primary Vertices observed
    npu = -1         # Number of pileup interactions simulated
    mjjReco = None   # reconstructed dijet mass
    mjjGen = None    # particle-level dijet mass
    mjetReco = None  # reconstructed average jet mass
    mjetGen = None   # generated average jet mass
    etaMax = None    # maximum eta of the dijet system



    if options.verbose :
        print '------------ Event ' + str(count) + ', NPU = ' + str(npu) + ', Weight = ' + str(weight)

    # First get the jets.
    # For data, only reco (obviously).
    # For MC, both reco and gen.
    event.getByLabel( ak7DefPxLabel, ak7DefPxHandle )
    ak7DefPxs = ak7DefPxHandle.product()
    event.getByLabel( ak7DefPyLabel, ak7DefPyHandle )
    ak7DefPys = ak7DefPyHandle.product()
    event.getByLabel( ak7DefPzLabel, ak7DefPzHandle )
    ak7DefPzs = ak7DefPzHandle.product()
    event.getByLabel( ak7DefEnergyLabel, ak7DefEnergyHandle )
    ak7DefEnergys = ak7DefEnergyHandle.product()


    if options.useMC :
        event.getByLabel( ak7GenPxLabel, ak7GenPxHandle )
        ak7GenPxs = ak7GenPxHandle.product()
        event.getByLabel( ak7GenPyLabel, ak7GenPyHandle )
        ak7GenPys = ak7GenPyHandle.product()
        event.getByLabel( ak7GenPzLabel, ak7GenPzHandle )
        ak7GenPzs = ak7GenPzHandle.product()
        event.getByLabel( ak7GenEnergyLabel, ak7GenEnergyHandle )
        ak7GenEnergys = ak7GenEnergyHandle.product()

        ak7Gen = []
        for igen in range(0,len(ak7GenPxs)):
            jgen = ROOT.TLorentzVector(
                ak7GenPxs[igen],
                ak7GenPys[igen],
                ak7GenPzs[igen],
                ak7GenEnergys[igen]
                )
            ak7Gen.append( jgen )


    ak7Def = []
    ak7GenMatched = []
    found = True
    for idef in range(0,len(ak7DefPxs)):
        jdef = ROOT.TLorentzVector(
            ak7DefPxs[idef],
            ak7DefPys[idef],
            ak7DefPzs[idef],
            ak7DefEnergys[idef]
            )
        if jdef.Perp() > jetPtMin and abs(jdef.Eta()) < jetEtaMax:
            ak7Def.append( jdef )
            if options.useMC :
                jgen = findGenJet( jdef, ak7Gen )
                if jgen is None :
                    found = False
                else :
                    ak7GenMatched.append( jgen )
                
    if found == False :
        continue

    if len(ak7Def) < 2 :
        continue

    dijetCandReco = ak7Def[0] + ak7Def[1]


    mjetReco = (ak7Def[0].M() + ak7Def[1].M()) * 0.5

    mjjReco = dijetCandReco.M()
    etaMax = abs(ak7Def[0].Eta())
    if abs(ak7Def[0].Eta()) < abs(ak7Def[1].Eta()) :
        etaMax = abs(ak7Def[1].Eta())

    trigEtaBin = -1
    for ibin in range(0, len(trigThresholds)) :
        if etaMax >= trigThresholds[ibin][0][0] and etaMax < trigThresholds[ibin][0][1] :
            trigEtaBin = ibin
            break

    mjjThresholds = trigThresholds[ibin][1]
    if options.verbose :
        print 'mjjReco = ' + str(mjjReco) + ', etaMax = ' + str(etaMax) + ', trig eta bin = ' + str(trigEtaBin)
        print 'mjj thresholds : '
        print mjjThresholds


    dijetCandGen  = None
    mjjGen = None
    mjetGen = None

    if options.useMC :
        dijetCandGen  = ak7GenMatched[0] + ak7GenMatched[1]
        mjjGen = dijetCandGen.M()
        mjetGen = (ak7Def[0].M() + ak7Def[1].M()) * 0.5


    #------------------------------------------
    # Now get the event weight.
    #
    # For MC:
    #   - Weight by the generator weight (cross section for this event)
    # For Data:
    #   - Weight by trigger prescale of *highest* pt-threshold jet trigger that passed
    #------------------------------------------
    passEvent = False
    if options.useMC :
        # Get the generator product
        event.getByLabel( generatorLabel, generatorHandle )
        if generatorHandle.isValid() :
            generatorInfo = generatorHandle.product()
            # weight is the generator weight
            weight *= generatorInfo.weight()
            if options.verbose :
                print 'generator info weight = ' + str(weight)
            passEvent = True

        # Also get the number of simulated pileup interactions
        event.getByLabel( puLabel, puHandle )
        puInfos = puHandle.product()

        npu = puInfos[0].getPU_NumInteractions()


    else :
        # Get the pat::TriggerEvent
        event.getByLabel( trigLabel, trigHandle )
        acceptedPaths = []
        trigPassedName = None
        passMjjTrig = False
        if trigHandle.isValid() :
            trig = trigHandle.product()
            # IF any triggers were run and were accepted, loop over the paths and get HLT_Jet* (ignoring the one without jet ID)
            if trig.wasRun() and trig.wasAccept() :
                paths = trig.paths()
                for path in paths :
                    if path.wasRun() and path.wasAccept() and path.name().find('HLT_Jet') >= 0 and path.name().find('NoJetID') < 0 :
                        acceptedPaths.append( path )
        # If there are any accepted paths, cache them. Then match to the lookup table "trigThresholds" to see if
        # the event is in the correct mjj bin for the trigger in question.
        if len( acceptedPaths) > 0 :
            for ipath in xrange( len(acceptedPaths)-1, -1, -1) :
                path = acceptedPaths[ipath]
                if options.verbose:
                    print '  --- considering path : ' + str(path.index()) + ', name = ' + str(path.name()) + ', prescale = ' + str(path.prescale() )
                for ikeep in xrange(len(trigsToKeep)-1, -1, -1) :
                    if options.verbose :
                        print '   ----- checking trigger ' + trigsToKeep[ikeep] + ' : mjjThreshold = ' + str(mjjThresholds[ikeep])
                    if path.name().find( trigsToKeep[ikeep] ) >= 0 and mjjReco > mjjThresholds[ikeep] :
                        weight = path.prescale()
                        trigPassedName = path.name()
                        passMjjTrig = True
                        if options.verbose :
                            print '    -----------> Joy and elation, it worked!'
                        break
                if passMjjTrig == True :
                    break

        passEvent = passMjjTrig

    if passEvent :
        if options.verbose :
            print 'event passed! OH happy day!'
        histAK7MjjVsEtaMax.Fill( mjjReco, etaMax, weight )
        histAK7MjetVsEtaMax.Fill( mjetReco, etaMax, weight )





#        histAK7DefPt.Fill( jdef.Perp(), weight )
        #print 'getting gen jet matched'
#        igen = findGenJet( jdef,
#                           ak7Gen )
#        if igen is not None :
#            ptResponse = jdef.Perp() / igen.Perp()
#            print 'jet {0:6.0f} : pt(def) / pt(gen) = {1:6.2f} / {2:6.2f} = {3:6.2f}'.format(
#                idef, jdef.Perp(), igen.Perp(), ptResponse
#                )



f.cd()
f.Write()
f.Close()
