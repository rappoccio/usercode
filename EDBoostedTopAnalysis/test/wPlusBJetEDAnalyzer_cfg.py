import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    'dcap://cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/guofan/Zprime_M750GeV_W7500MeV-madgraph/ttbsm_38on35/bb725c5f06fa9bd285bf64e68c9e6c07/ttbsm_381_7_1_Ugj.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(6000) )

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

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                      wPlusBJetAna = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      )
)


process.MessageLogger.cerr.FwkReport.reportEvery = 1000
