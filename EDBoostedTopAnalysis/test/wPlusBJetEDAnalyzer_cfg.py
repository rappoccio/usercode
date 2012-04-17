import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    'file:/uscms_data/d2/guofan/TTbarJets-madgraph/ttbsm_361_10_1.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

from Analysis.BoostedTopAnalysis.wPlusBJetAnalysis_cfi import *




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("wPlusBJetAnalysis.root")
                                   )

process.wPlusBJetAna = cms.EDAnalyzer('EDWPlusBJetAnalysis',
                                   wPlusBJetAnalysis.clone()
                                     )


process.p = cms.Path(
    process.wPlusBJetAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
