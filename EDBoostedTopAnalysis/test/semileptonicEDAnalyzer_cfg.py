import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'dcap:///pnfs/cms/WAX/11/store/user/srappocc/WJets-madgraph/ttbsm_361_v1/6e46b5e195f4b3b727488919472b1913/ttbsm_361_9_1_zpm.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Analysis.BoostedTopAnalysis.semileptonicAnalysis_cfi import semileptonicAnalysis as inputSemileptonicAnalysis




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("boostedTopSemileptonicStudies_pt_gt25.root")
                                   )

process.semileptonicAna = cms.EDAnalyzer('EDSemileptonicAnalysis',
                                  inputSemileptonicAnalysis.clone()
                                     )


process.p = cms.Path(
    process.semileptonicAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
