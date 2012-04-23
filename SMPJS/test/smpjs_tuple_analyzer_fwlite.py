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

# Print verbose information
parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Print verbose information')

# job splitting
parser.add_option('--nsplit', type='int', action='store',
                  default=None,
                  dest='nsplit',
                  help='Number of split jobs')
parser.add_option('--isplit', type='int', action='store',
                  default=None,
                  dest='isplit',
                  help='Index of job (0...nsplit)')

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

files = []
# Get the file list.
if options.files.find('.txt') >= 0 :
    infile = open( options.files, 'r')
    tmpfiles = infile.readlines()
    for ifile in tmpfiles :
        s = ifile.rstrip()
        print s
        files.append( s )

elif options.nsplit is None :
    files = glob.glob( options.files )
    for ifile in files:
        print ifile
elif options.nsplit is not None :


    tmpfiles = glob.glob( options.files )
    print 'All files : '  + str(len(tmpfiles))
    for ifile in tmpfiles :
        print ifile

    tot = len(tmpfiles)
    nsplit = options.nsplit
    isplit = options.isplit
    msplit = tot / nsplit
    print 'Splitting into ' + str(nsplit) + ' jobs with ' + str(msplit) + ' elements each, this job is index ' + str(isplit)
    end = min( tot, (isplit + 1) * msplit )
    for i in range( isplit * msplit, end ) :
        files.append( tmpfiles[i] )
    print 'Selected files : '
    for ifile in files :
        print ifile

if len(files) == 0 :
    print 'No files, exiting'
    exit(0)

# Create the output file. 
f = ROOT.TFile(options.outname + ".root", "recreate")
f.cd()


# Make histograms
print "Creating histograms"

nJets = ROOT.TH1F("nJets",         "Number of Jets, p_{T} > 30 GeV;N_{Jets};Number",               20, -0.5, 19.5 )


############################################
#     Jet energy scale and uncertainties   #
############################################


if options.useMC :
    jecStr = [
        'GR_R_42_V23_L1FastJet_AK7PFchs.txt',
        'GR_R_42_V23_L2Relative_AK7PFchs.txt',
        'GR_R_42_V23_L3Absolute_AK7PFchs.txt',
    ]
else :
    jecStr = [
        'GR_R_42_V23_L1FastJet_AK7PFchs.txt',
        'GR_R_42_V23_L2Relative_AK7PFchs.txt',
        'GR_R_42_V23_L3Absolute_AK7PFchs.txt',
        'GR_R_42_V23_L2L3Residual_AK7PFchs.txt',
    ]

jecPars = ROOT.std.vector(ROOT.JetCorrectorParameters)()

for ijecStr in jecStr :
    ijec = ROOT.JetCorrectorParameters( ijecStr )
    jecPars.push_back( ijec )
    

jec = ROOT.FactorizedJetCorrector(jecPars)

jecUncStr = ROOT.std.string('GR_R_42_V23_Uncertainty_AK7PFchs.txt')
jecUnc = ROOT.JetCorrectionUncertainty( jecUncStr )


############################################
#     Trigger information                  #
############################################
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
[[0.0, 0.5], [ 178.,  324.,  533.,  663.,  970., 7000.] ],
[[0.5, 1.0], [ 240.,  390.,  645.,  820., 1218., 7000.] ],
[[1.0, 1.5], [ 369.,  615.,  998., 1261., 1904., 7000.] ],
[[1.5, 2.0], [ 530.,  920., 1590., 1985., 3107., 7000.] ],
[[2.0, 2.5], [ 913., 1549., 2665., 3700., 4000., 7000.] ]
    ]


############################################
# Physics level parameters for systematics #
############################################

# Kinematic cuts:
jetPtMin = 30.0
jetEtaMax = 2.5



ak7DefPxHandle         = Handle( "std::vector<float>" )
ak7DefPxLabel          = ( "ak7Lite",   "px" )
ak7DefPyHandle         = Handle( "std::vector<float>" )
ak7DefPyLabel          = ( "ak7Lite",   "py" )
ak7DefPzHandle         = Handle( "std::vector<float>" )
ak7DefPzLabel          = ( "ak7Lite",   "pz" )
ak7DefEnergyHandle     = Handle( "std::vector<float>" )
ak7DefEnergyLabel      = ( "ak7Lite",   "energy" )
ak7DefJetAreaHandle    = Handle( "std::vector<float>" )
ak7DefJetAreaLabel     = ( "ak7Lite",   "jetArea" )
ak7DefJecFactorHandle  = Handle( "std::vector<float>" )
ak7DefJecFactorLabel   = ( "ak7Lite",   "jecFactor" )


ak7GenPxHandle         = Handle( "std::vector<float>" )
ak7GenPxLabel          = ( "ak7Gen",   "px" )
ak7GenPyHandle         = Handle( "std::vector<float>" )
ak7GenPyLabel          = ( "ak7Gen",   "py" )
ak7GenPzHandle         = Handle( "std::vector<float>" )
ak7GenPzLabel          = ( "ak7Gen",   "pz" )
ak7GenEnergyHandle     = Handle( "std::vector<float>" )
ak7GenEnergyLabel      = ( "ak7Gen",   "energy" )


rhoHandle = Handle("double")
rhoLabel = ( "kt6PFJets", "rho")


puHandle = Handle("std::vector<PileupSummaryInfo>")
puLabel = ( "addPileupInfo", "")


generatorHandle = Handle("GenEventInfoProduct")
generatorLabel = ( "generator", "")


trigHandle = Handle("std::vector<std::string>")
trigLabel = ( "dijetTriggerFilter", 'jetPaths')


histAK7MjjVsEtaMax = ROOT.TH2F('histAK7MjjVsEtaMax', 'AK7 m_{jj} Versus #eta_{max};m_{jj} (GeV);#eta_{max}(radians)', 700, 0., 7000., 5, 0.0, 2.5)
histAK7MjetVsEtaMax = ROOT.TH2F('histAK7MjetVsEtaMax', 'AK7 <m_{jet}> Versus #eta_{max};<m_{jet}> (GeV);#eta_{max}(radians)', 300, 0., 300., 5, 0.0, 2.5)

# TO DO:::: DO this for each trigger!
histAK7MjjVsEtaMaxTrigs = []
histAK7MjetVsEtaMaxTrigs = []

for trig in trigsToKeep :
    histAK7MjjVsEtaMaxTrigs.append(  ROOT.TH2F('histAK7MjjVsEtaMax_' + trig,
                                                'AK7 m_{jj} Versus #eta_{max}' + trig +';m_{jj} (GeV);#eta_{max}(radians)',
                                                700, 0., 7000., 5, 0.0, 2.5) )
    histAK7MjetVsEtaMaxTrigs.append( ROOT.TH2F('histAK7MjetVsEtaMax_' + trig,
                                                'AK7 <m_{jet}> Versus #eta_{max};<m_{jet}> (GeV)' + trig + ';#eta_{max}(radians)',
                                                300, 0., 300., 5, 0.0, 2.5) )


histAK7MjjResponseVsEtaMax = ROOT.TH3F('histAK7MjjResponseVsEtaMax', 'AK7 m_{jj} Response;m_{jj} (GeV);#eta_{max}(radians)',
                                       70, 0., 7000., 20, 0.5, 1.5, 5, 0.0, 2.5)
histAK7MjetResponseVsEtaMax = ROOT.TH3F('histAK7MjetResponseVsEtaMax', 'AK7 <m_{jet}> Versus #eta_{max};<m_{jet}> (GeV);#eta_{max}(radians)',
                                        30, 0., 300., 20, 0.5, 1.5, 5, 0.0, 2.5)


histAK7PtResponse  = ROOT.TH2F('histAK7PtResponse',  ';p_{T}^{GEN} (GeV);p_{T}^{RECO} / p_{T}^{GEN}', 50, 0., 500., 20, 0.5, 1.5)
histAK7EtaResponse = ROOT.TH2F('histAK7EtaResponse', ';#eta^{GEN} (GeV);p_{T}^{RECO} / p_{T}^{GEN}', 50, -5.0, 5.0, 20, 0.5, 1.5)

count = 0
for ifile in files :

    ifiles = [ ifile ]

    events = Events (ifiles)

    print "Start looping on file " + ifiles[0]
    for event in events:

        # Histogram filling weight
        weight = 1.0

        # Histogram index for data (Jet60,110,190,240,370)
        iTrigHist = None

        if count % 10000 == 0 :
            print 'Processing event ' + str(count)

        count += 1

        # Event-level variables:
        npv = -1         # Number of Primary Vertices observed
        npu = -1         # Number of pileup interactions simulated
        mjjReco = None   # reconstructed dijet mass
        mjjGen = None    # particle-level dijet mass
        mjetReco = None  # reconstructed average jet mass
        mjetGen = None   # generated average jet mass
        etaMax = None    # maximum eta of the dijet system


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
        event.getByLabel( ak7DefJetAreaLabel, ak7DefJetAreaHandle )
        ak7DefJetAreas = ak7DefJetAreaHandle.product()
        event.getByLabel( ak7DefJecFactorLabel, ak7DefJecFactorHandle )
        ak7DefJecFactors = ak7DefJecFactorHandle.product()


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


        event.getByLabel( rhoLabel, rhoHandle )
        rho = rhoHandle.product()[0]

        ak7Def = []
        ak7GenMatched = []
        found = True
        for idef in range(0,len(ak7DefPxs)):
            jdefRaw = ROOT.TLorentzVector(
                ak7DefPxs[idef] * ak7DefJecFactors[idef],
                ak7DefPys[idef] * ak7DefJecFactors[idef],
                ak7DefPzs[idef] * ak7DefJecFactors[idef],
                ak7DefEnergys[idef] * ak7DefJecFactors[idef]
                )

            jec.setJetEta(jdefRaw.Eta())
            jec.setJetPt(jdefRaw.Perp())
            jec.setJetA(ak7DefJetAreas[idef])
            jec.setRho(rho)
            factor = jec.getCorrection()


            jdef = ROOT.TLorentzVector(
                jdefRaw.Px() * factor,
                jdefRaw.Py() * factor,
                jdefRaw.Pz() * factor,
                jdefRaw.Energy() * factor
                )
            
            if jdef.Perp() > jetPtMin and abs(jdef.Eta()) < jetEtaMax:
                ak7Def.append( jdef )
                if options.useMC :
                    jgen = findGenJet( jdef, ak7Gen )
                    if jgen is None :
                        found = False
                    else :
                        ak7GenMatched.append( jgen )
                if options.verbose :
                    print ' raw jet {0:4.0f}, (pt,eta,phi,m) = ({1:6.2f},{2:6.2f},{3:6.2f},{4:6.2f})'.format( idef, jdefRaw.Perp(), jdefRaw.Eta(), jdefRaw.Phi(), jdefRaw.M() )
                    print ' corrjet {0:4.0f}, (pt,eta,phi,m) = ({1:6.2f},{2:6.2f},{3:6.2f},{4:6.2f})'.format( idef, jdef.Perp(), jdef.Eta(), jdef.Phi(), jdef.M() )
                    if options.useMC and jgen is not None :
                        print ' gen jet {0:4.0f}, (pt,eta,phi,m) = ({1:6.2f},{2:6.2f},{3:6.2f},{4:6.2f})'.format( idef, jgen.Perp(), jgen.Eta(), jgen.Phi(), jgen.M() )

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
            trigs = trigHandle.product()
            acceptedPaths = []
            trigPassedName = None
            passMjjTrig = False

            # If there are any accepted paths, cache them. Then match to the lookup table "trigThresholds" to see if
            # the event is in the correct mjj bin for the trigger in question.
            if len( trigs ) > 0 :
                for ipath in xrange( len(trigs)-1, -1, -1) :
                    path = trigs[ipath]
                    for ikeep in xrange(len(trigsToKeep)-1, -1, -1) :
                        if options.verbose :
                            print '   ----- checking trigger ' + trigsToKeep[ikeep] + ' : mjjThreshold = ' + str(mjjThresholds[ikeep])
                        if path.find( trigsToKeep[ikeep] ) >= 0 and mjjReco >= mjjThresholds[ikeep] and mjjReco < mjjThresholds[ikeep + 1]:
                            trigPassedName = path
                            iTrigHist = ikeep
                            passMjjTrig = True
                            if options.verbose :
                                print '    -----------> Joy and elation, it worked! trigger = ' + trigsToKeep[iTrigHist]
                            break
                    if passMjjTrig == True :
                        break

            passEvent = passMjjTrig

        if passEvent :
            if options.verbose :
                print 'event passed! OH happy day!'

            if options.useMC :
                histAK7MjjVsEtaMax.Fill( mjjReco, etaMax, weight )
                histAK7MjetVsEtaMax.Fill( mjetReco, etaMax, weight )
            elif iTrigHist is not None :
                if options.verbose :
                    print ' Filling histogram ' + str(iTrigHist) + ' which corresponds to trigger ' + trigsToKeep[iTrigHist]
                histAK7MjjVsEtaMaxTrigs[iTrigHist].Fill( mjjReco, etaMax, weight )
                histAK7MjetVsEtaMaxTrigs[iTrigHist].Fill( mjetReco, etaMax, weight )                
            else :
                print 'Error in trigger assignment!'
                continue

            if options.useMC :
                response0 = ak7Def[0].Perp() / ak7GenMatched[0].Perp()
                mjjResponse = mjjReco / mjjGen
                mjetResponse = mjetReco / mjetGen
                ptGen0 = ak7GenMatched[0].Perp()
                etaGen0 = ak7GenMatched[0].Eta()
                histAK7PtResponse.Fill( ptGen0, response0 )
                histAK7EtaResponse.Fill( etaGen0, response0 )
                histAK7MjjResponseVsEtaMax.Fill( mjjGen, mjjResponse, etaMax )
                histAK7MjetResponseVsEtaMax.Fill( mjetGen, mjetResponse, etaMax )


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
