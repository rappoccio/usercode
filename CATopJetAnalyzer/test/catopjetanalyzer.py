# import configurations
import FWCore.ParameterSet.Config as cms

# define the process
process = cms.Process("CATopJets")

# input message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.include( "SimGeneral/HepPDTESSource/data/pythiapdt.cfi")

# this defines the input files
from Analysis.CATopJetAnalyzer.RecoInput_QCD_3000_3500_RelVal_cfi import *

# get generator sequences
#process.load("Configuration.StandardSequences.Generator_cff")
process.load("RecoJets.Configuration.GenJetParticles_cff")

# Get some geometry
process.load("Configuration.StandardSequences.GeometryPilot1_cff")

# input Jet Reco sequences
process.load("RecoJets.JetProducers.caTopJets_cff")
process.load("RecoJets.JetProducers.iterativeCone5CaloJets_cff")

# pythia output
process.printList = cms.EDAnalyzer( "ParticleListDrawer",
                                src = cms.InputTag( "genParticles" ),
                                maxEventsToPrint = cms.untracked.int32( 10 )
)

# request a summary at the end of the file
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# define the source, from reco input
process.source = RecoInput()

# set the number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5000)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('histo2.root')
)

process.topquarks = cms.EDProducer("PdgIdAndStatusCandViewSelector",
                                   src = cms.InputTag("genParticles"),
                                   pdgId = cms.vint32(6),
                                   status = cms.vint32(3)
                                   )


process.jetAna = cms.EDAnalyzer("CATopJetAnalyzer",
                                genericQCD = cms.bool(True),
                                TopMass = cms.double(171),
                                WMass = cms.double(80.4),
                                verbose = cms.bool(False)
                                )

                                     
# produce Z to mu mu candidates
process.zToJJ = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string('caTopJets caTopJets'),
    checkCharge = cms.bool(False),
    cut = cms.string('0.0 < mass < 20000.0'),
    name = cms.string('zToJJ'),
    roles = cms.vstring('jet1', 'jet2')
)


# define event selection to be that which satisfies 'p'
process.EventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p')
    )
)

# setup event content
process.EventContent = cms.PSet(
    outputCommands = cms.untracked.vstring('drop *',
                                           'keep *_genParticles_*_*',
                                           'keep *_topquarks_*_*',
                                           'keep *_genParticlesForJets_*_*',
                                           'keep *_caTopJetsProducer_*_*',
                                           'keep *_zToJJ_*_*'
                                           )
    )
    

# define event selection to be that which satisfies 'p'
process.EventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('p')
    )
    )

# talk to output module
process.out = cms.OutputModule("PoolOutputModule",
                               process.EventSelection,
                               process.EventContent,
                               verbose = cms.untracked.bool(False),
                               fileName = cms.untracked.string('/uscms_data/d1/rappocc/topjets2.root')
                               )

# define path 'p'
process.p = cms.Path(process.genParticlesForJets*
                     process.caTopJetsProducer*
                     process.topquarks*
                     #process.zToJJ*
                     process.jetAna
                     )
# define output path
process.outpath = cms.EndPath(process.out)
# Set the threshold for output logging to 'info'
process.MessageLogger.cerr.threshold = 'INFO'
