import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    'file:/uscms_data/d2/guofan/patTuples/boostedTop/CMSSW_3_8_7/src/pickEvents/pickEvents_ReReco.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

from Analysis.BoostedTopAnalysis.wPlusBJetAnalysis_cfi import *




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("wPlusBJetAnalysis.root")
                                   )

process.wPlusBJetAna = cms.EDAnalyzer('EDWPlusBJetAnalysis',
                                   wPlusBJetAnalysis.clone(runOnData=True)
                                     )

process.wPlusBJetAna.WPlusBJetEventSelection.trig = cms.string("HLT_Jet70U")
process.wPlusBJetAna.WPlusBJetEventSelection.cutsToIgnore = cms.vstring("Trigger")
process.wPlusBJetAna.WPlusBJetEventSelection.leadJetPtCut = cms.double(160)
process.wPlusBJetAna.WPlusBJetEventSelection.secondJetPtCut = cms.double(100)
process.wPlusBJetAna.WPlusBJetEventSelection.BoostedTopWJetParameters.jetPtMin = 200
process.wPlusBJetAna.WPlusBJetEventSelection.bTagOP = 3.3

#process.wPlusBJetAna2 = process.wPlusBJetAna.clone( )
#process.wPlusBJetAna2.WPlusBJetEventSelection.leadJetPtCut = cms.double(80)
#process.wPlusBJetAna3 = process.wPlusBJetAna.clone( )
#process.wPlusBJetAna3.WPlusBJetEventSelection.leadJetPtCut = cms.double(100)
#process.wPlusBJetAna4 = process.wPlusBJetAna.clone( )
#process.wPlusBJetAna4.WPlusBJetEventSelection.leadJetPtCut = cms.double(120)


process.p = cms.Path(
    process.wPlusBJetAna#*process.wPlusBJetAna2*process.wPlusBJetAna3*process.wPlusBJetAna4
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                      wPlusBJetAna = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      )
)

