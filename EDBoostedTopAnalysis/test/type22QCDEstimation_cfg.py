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

from Analysis.BoostedTopAnalysis.Type22SelectionParams_cfi import *




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("Type22QCDEstimation.root")
                                   )

process.type22QCDAna = cms.EDAnalyzer('EDType22QCDEstimation',
                              Type22Selection = cms.PSet( Type22SelectionParams )
                                     )

process.p = cms.Path(
  process.type22QCDAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
