
# import configurations
import FWCore.ParameterSet.Config as cms

print "About to process"

# define the process
process = cms.Process("CATopJets")

print "Creating message logger"
# input message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.include( "SimGeneral/HepPDTESSource/data/pythiapdt.cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATLayer0Summary')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default          = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    PATLayer0Summary = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

print "Setting variables"

outputdir = './'
algorithm = 'ca'
output_dst = True
nevents = 1000
idtag = '_slim_223'


outputfile = outputdir + algorithm + '_pat' + idtag + '.root'

print "Output file : " + outputfile

# this defines the input files

from TopQuarkAnalysis.TopPairBSM.RecoInput_ZPrime3000_w30_cfi import *

# define the source, from reco input
process.source = RecoInput()

# get generator sequences
#process.load("Configuration.StandardSequences.Generator_cff")
process.load("RecoJets.Configuration.GenJetParticles_cff")

# Load geometry
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('IDEAL_V9::All')
process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.StandardSequences.GeometryPilot1_cff")

# Kt6 jets
process.load("RecoJets.JetProducers.kt6CaloJets_cff")
process.load("RecoJets.JetProducers.antikt6CaloJets_cff")
process.load("RecoJets.JetProducers.cambridge6CaloJets_cff")
process.load("RecoJets.JetProducers.sisCone7CaloJets_cff")

# CATopJets
process.load("TopQuarkAnalysis.TopPairBSM.caTopJets_cff")
process.load("TopQuarkAnalysis.TopPairBSM.CATopJetTagger_cfi")

# turn off sum-et dependent stuff.
process.caTopJetsProducer.ptBins = cms.vdouble(0,10e9)
process.caTopJetsProducer.rBins  = cms.vdouble(0.8,0.8)
process.caTopJetsProducer.ptFracBins = cms.vdouble(0.05,0.05)
process.caTopJetsProducer.nCellBins = cms.vint32(1,1)


print "About to input pat sequences"

# input pat sequences
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
process.load("PhysicsTools.PatAlgos.patLayer1_cff")

## Necessary fixes to run 2.2.X on 2.1.X data
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run22XonSummer08AODSIM
run22XonSummer08AODSIM(process)

# switch jet collection to our juets
from PhysicsTools.PatAlgos.tools.jetTools import *

print "About to switch jet collection"






## ==== Example with CaloJets
switchJetCollection(process, 
        'caTopJetsProducer',   # Jet collection; must be already in the event when patLayer0 sequence is executed
        layers=[0,1],          # If you're not runnint patLayer1, set 'layers=[0]' 
        runCleaner="BasicJet", # =None if not to clean
        doJTA=True,            # Run Jet-Track association & JetCharge
        doBTagging=True,       # Run b-tagging
        #jetCorrLabel=('KT6', 'Calo'),   # example jet correction name; set to None for no JEC
        jetCorrLabel=None,     # Turn this off, do it by hand. This tool doesn't work with new JEC
        doType1MET=False)      # recompute Type1 MET using these jets

# now set JEC by hand
process.jetCorrFactors.jetSource = cms.InputTag("kt6CaloJets")
process.jetCorrFactors.L1Offset  = cms.string('none')
process.jetCorrFactors.L2Relative= cms.string('Summer08_L2Relative_KT6Calo')
process.jetCorrFactors.L3Absolute= cms.string('Summer08_L3Absolute_KT6Calo')
process.jetCorrFactors.L4EMF     = cms.string('none')
process.jetCorrFactors.L5Flavor  = cms.string('none')
process.jetCorrFactors.L6UE      = cms.string('none')                           
process.jetCorrFactors.L7Parton  = cms.string('none')

# Place appropriate jet cuts (NB: no cut on number of constituents)
process.selectedLayer1Jets.cut = cms.string('pt > 250. & abs(rapidity) < 5.0')
process.selectedLayer1Muons.cut = cms.string('pt > 50. & abs(rapidity) < 2.5 && caloIso < 3.0')
process.selectedLayer1Electrons.cut = cms.string('pt > 50. & abs(rapidity) < 2.5 && caloIso < 3.0')
process.selectedLayer1METs.cut = cms.string('pt > 150.0')
process.selectedLayer1Photons.cut = cms.string('pt > 50. & abs(rapidity) < 5.0')
# Turn off resolutions, they don't mean anything here
process.allLayer1Jets.addResolutions = cms.bool(False)
# Add CATopTag info... piggy-backing on b-tag functionality
process.layer0TagInfos.associations.append ( cms.InputTag("CATopJetTagger") )
process.allLayer1Jets.addBTagInfo = cms.bool(True)
process.allLayer1Jets.addTagInfoRefs = cms.bool(True)
process.allLayer1Jets.tagInfoNames = cms.vstring('CATopJetTagger')
process.allLayer1Jets.addDiscriminators = cms.bool(False)
# Add parton match to quarks and gluons
process.allLayer1Jets.addGenPartonMatch = cms.bool(True)
process.allLayer1Jets.embedGenPartonMatch = cms.bool(True)
process.allLayer1Jets.embedCaloTowers = cms.bool(True)
#process.allLayer1Muons.addGenPartonMatch = cms.bool(True)
#process.allLayer1Muons.embedGenPartonMatch = cms.bool(True)
process.jetPartons.withTop = cms.bool(True)
process.jetPartonAssociation.coneSizeToAssociate = cms.double(0.8)
process.jetPartonAssociation.doPriority = cms.bool(True)
process.jetPartonAssociation.priorityList = cms.vint32(6)
process.jetFlavourAssociation.definition = cms.int32(4)
process.jetFlavourAssociation.physicsDefinition = cms.bool(False)

process.jetPartonMatch.mcPdgId = cms.vint32(1,2,3,4,5,6,21)
process.jetPartonMatch.maxDeltaR = cms.double(0.8)
#process.allLayer1Jets.genPartonMatch = cms.InputTag("CAJetPartonMatcher")
# Add jet MC flavour (custom built to capture tops)
process.allLayer1Jets.getJetMCFlavour = cms.bool(True)

#turn off all trigger info
process.allLayer1Jets.addTrigMatch = cms.bool(False)
process.allLayer1Electrons.addTrigMatch = cms.bool(False)
process.allLayer1Muons.addTrigMatch = cms.bool(False)
process.allLayer1Taus.addTrigMatch = cms.bool(False)
process.allLayer1METs.addTrigMatch = cms.bool(False)
process.allLayer1Photons.addTrigMatch = cms.bool(False)

#process.allLayer1Jets.JetPartonMapSource = cms.InputTag("CAJetFlavourIdentifier")

print "Done switching jet collection"

# input pat analyzer sequence
process.load("TopQuarkAnalysis.TopPairBSM.CATopJetKit_cfi")

# load the pat layer 1 event content
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")


#process.L2L3JetCorrectorFKt6 = cms.ESSource("JetCorrectionServiceChain",
#    correctors = cms.vstring('L2RelativeJetCorrectorFKt6', 
#        'L3AbsoluteJetCorrectorFKt6'),
#    label = cms.string('L2L3JetCorrectorFKt6')
#)
#process.es_prefer_L2L3JetCorrectorFKt6 = cms.ESPrefer("JetCorrectionServiceChain","L2L3JetCorrectorFKt6")
#process.L2JetCorJetFKt6.src = cms.InputTag("kt6CaloJets")


# Reduce number of tracks in the output file
process.goodTracks = cms.EDProducer("TrackViewCandidateProducer",
    src = cms.InputTag("generalTracks"),
    particleType = cms.string('pi+'),
    cut = cms.string('pt > 10')
)

# only keep events that have at least one jet
process.jetFilter = cms.EDFilter("CandViewCountFilter",
                                  src = cms.InputTag("selectedLayer1Jets"),
                                  minNumber = cms.uint32( 1 )
                                  )

if algorithm == 'kt' :
    process.caTopJetsProducer.algorithm = cms.int32(0)
elif algorithm == 'ca' :
    process.caTopJetsProducer.algorithm = cms.int32(1)
elif algorithm == 'antikt' :
    process.caTopJetsProducer.algorithm = cms.int32(2)

# pythia output
process.printList = cms.EDAnalyzer( "ParticleListDrawer",
                                src = cms.InputTag( "genParticles" ),
                                maxEventsToPrint = cms.untracked.int32( 0 )
)



# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(nevents)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('histo_' + '_' + algorithm + '_2110.root')
)


# setup event content
process.patEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring('drop *')
    )

# extend event content to include PAT objects
process.patEventContent.outputCommands.extend(process.patLayer1EventContent.outputCommands)
process.patEventContent.outputCommands.extend(['drop *_genParticles_*_*',
                                               'keep *_genEventScale_*_*',
                                               'drop *_generalTracks_*_*',
                                               'keep *_goodTracks_*_*',
                                               #'keep *_kt6Calojets_*_*',
                                               #'keep *_antikt6Calojets_*_*',
                                               #'keep *_cambridge6Calojets_*_*',
                                               #'keep *_sisCone7Calojets_*_*',
                                               #'drop *_towerMaker_*_*',
                                               'keep *_caTopJetsProducer_*_*',
                                               'keep *_CATopJetTagger_*_*',
                                               'drop *_selectedLayer1Taus_*_*',
                                               'drop *_selectedLayer1Hemispheres_*_*',
                                               'drop *_selectedLayer1Photons_*_*'
                                               #'keep *_CAJetPartonMatcher_*_*',
                                               #'keep *_CAJetFlavourIdentifier_*_*'
                                               ]
                                              )


# define event selection to be that which satisfies 'p'
process.patEventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('p')
    )
    )

# talk to output module
process.out = cms.OutputModule("PoolOutputModule",
                               process.patEventSelection,
                               process.patEventContent,
                               verbose = cms.untracked.bool(False),
                               dropMetaDataForDroppedData = cms.untracked.bool(True),
                               fileName = cms.untracked.string(outputfile)
                               )

# define path 'p'
process.p = cms.Path(process.kt6CaloJets*
                     process.antikt6CaloJets*
                     process.cambridge6CaloJets*
                     process.sisCone7CaloJets*
                     process.printList*
                     process.goodTracks*
                     process.caTopJetsProducer*
                     process.CATopJetTagger*
                     process.patLayer0_withoutTrigMatch*
                     process.patLayer1*
                     process.jetFilter
#                     process.CATopJetKit
                     )


                     
# define output path
if output_dst == True :
    process.outpath = cms.EndPath(process.out)

# Set the threshold for output logging to 'info'
process.MessageLogger.cerr.threshold = 'INFO'


#print process.dumpPython()
