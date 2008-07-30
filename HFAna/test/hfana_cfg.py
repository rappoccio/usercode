# Import configurations
import FWCore.ParameterSet.Config as cms

# set up process
process = cms.Process("HFANA")

flavor = 'wc'
histfile = flavor + 'Ana.root'
outfile = '/uscms_data/d1/rappocc/' + flavor + 'Skim.root'

# this defines the input files

if flavor == 'wbb' :
    from Analysis.HFAna.RecoInput_wbb_cfi import *
elif flavor == 'wcc' :
    from Analysis.HFAna.RecoInput_wcc_cfi import *
elif flavor == 'wc' :
    from Analysis.HFAna.RecoInput_wc_cfi import *
else :
    from Analysis.HFAna.RecoInput_wbb_cfi import *

    
# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.load('Configuration.StandardSequences.MagneticField_cff')

# input message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

# input MC stuff
process.load( "SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load( "PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load( "PhysicsTools.HepMCCandAlgos.genEventWeight_cfi")
process.load( "PhysicsTools.HepMCCandAlgos.genEventScale_cfi")

# input flavor history stuff
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryProducer_cfi")
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryFilter_cfi")

process.printList = cms.EDAnalyzer( "ParticleListDrawer",
                                    src =  cms.InputTag( "genParticles" ),
                                    maxEventsToPrint = cms.untracked.int32( 1 )
)

# input pat sequences
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
process.load("PhysicsTools.PatAlgos.patLayer1_cff")

process.selectedLayer1Jets.cut = cms.string('et > 20.0 & abs(eta) < 2.5 & nConstituents > 0')
process.selectedLayer1Muons.cut = cms.string('pt > 30.0 & abs(eta) < 5.0')
process.countLayer1Leptons.minNumber = cms.uint32(1)
#process.countLayer1Leptons.maxNumber = cms.uint32(1)



# input pat analyzer sequence
process.load("Analysis.HFAna.hfana_cfi")

process.wbbAna = process.hfAna.clone()
process.wccAna = process.hfAna.clone()
process.wcAna = process.hfAna.clone()


# load the pat layer 1 event content
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")

# request a summary at the end of the file
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# define the source, from reco input
process.source = RecoInput()

# talk to TFileService
process.TFileService = cms.Service("TFileService",
    fileName = cms.string(histfile)
)

# define event selection to be that which satisfies 'p'
process.patEventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)


# define path 'p'
process.p = cms.Path(
  process.genParticles *
  process.genEventWeight *
#  process.printDecay *
#  process.printList *
#  process.printTree *
  process.patLayer0*
  process.patLayer1*  
  process.bFlavorHistoryProducer*
  process.cFlavorHistoryProducer)

process.wbb = cms.Path(
    process.genParticles *
    process.genEventWeight *
    process.patLayer0*
    process.patLayer1*  
    process.bFlavorHistoryProducer*
    process.cFlavorHistoryProducer*
    process.wbb_me_flavorHistoryFilter*
    process.wbbAna )


process.wcc = cms.Path(
    process.genParticles *
    process.genEventWeight *
    process.patLayer0*
    process.patLayer1*  
    process.bFlavorHistoryProducer*
    process.cFlavorHistoryProducer*
    ~process.wbb_me_flavorHistoryFilter*
    process.wcc_me_flavorHistoryFilter*
    process.wccAna )


process.wc = cms.Path(
    process.genParticles *
    process.genEventWeight *
    process.patLayer0*
    process.patLayer1*  
    process.bFlavorHistoryProducer*
    process.cFlavorHistoryProducer*
    ~process.wbb_me_flavorHistoryFilter*
    ~process.wcc_me_flavorHistoryFilter*
    process.wc_fe_flavorHistoryFilter*
    process.wcAna )


# Set the threshold for output logging to 'info'
process.MessageLogger.cerr.threshold = 'INFO'
# extend event content to include pat analyzer kit objects
process.patLayer1EventContent.outputCommands.extend(['keep *_bFlavorHistoryProducer_*_*'])
process.patLayer1EventContent.outputCommands.extend(['keep *_cFlavorHistoryProducer_*_*'])


# talk to output module
process.out = cms.OutputModule("PoolOutputModule",
    process.patEventSelection,
    process.patLayer1EventContent,
    verbose = cms.untracked.bool(False),
    fileName = cms.untracked.string(outfile)
)


# define output path
process.outpath = cms.EndPath(process.out)
