import FWCore.ParameterSet.Config as cms

process = cms.Process("FWDREFCHECK")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:fwdref_test.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.fwdrefcheck = cms.EDAnalyzer("FwdRefCheck",
                                     jetSrc1 = cms.InputTag("ak5CaloJets"),
                                     jetSrc2 = cms.InputTag("fwdref"),
                                     refVecSrc = cms.InputTag("fwdref"),
                                     jetIDSrc = cms.InputTag("ak5JetID")
)

process.p = cms.Path( process.fwdrefcheck )

