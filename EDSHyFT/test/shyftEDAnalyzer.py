import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'dcap:///pnfs/cms/WAX/11/store/user/lannon/TTbarJets-madgraph/SHYFT_pat357_skim/0aa0bf8c0747525f693ade731a97f67d/ljmet_skim_7_1.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies.root")
                                   )


process.shyftAna = cms.EDAnalyzer('EDSHyFT',
                                  shyftAnalysis = inputShyftAnalysis.clone()
                                     )


process.p = cms.Path(
    process.shyftAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
