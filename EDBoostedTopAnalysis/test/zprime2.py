import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'dcap:////pnfs/cms/WAX/11/store/user/guofan/Zprime_M2000GeV_W20GeV-madgraph/ttbsm_387_v2/8527abb9a688648f7e111642276a1842/ttbsm_387_10_1_yc9.root',
'dcap:////pnfs/cms/WAX/11/store/user/guofan/Zprime_M2000GeV_W20GeV-madgraph/ttbsm_387_v2/8527abb9a688648f7e111642276a1842/ttbsm_387_11_1_6ZN.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

from Analysis.BoostedTopAnalysis.Type11SelectionParams_cfi import *
from Analysis.BoostedTopAnalysis.Type22SelectionParams_cfi import *




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("Zprime.root")
                                   )

process.type22QCDAna15 = cms.EDAnalyzer('EDCombinedQCDEstimation',
                                  Type11QCDEstimationParams,
                                  Type22QCDEstimationParams
                                     )

#process.type22QCDAna10 = process.type22QCDAna15.clone( Probability = cms.double(0.10) )
#process.type22QCDAna5 = process.type22QCDAna15.clone( Probability = cms.double(0.05) )
#process.type22QCDAna33 = process.type22QCDAna15.clone( Probability = cms.double(0.33) )

process.p = cms.Path(
  process.type22QCDAna15#*process.type22QCDAna10*process.type22QCDAna5*process.type22QCDAna33
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                      type22QCDAna15 = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      ),
                      type22QCDAna10 = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      ),
                      type22QCDAna5 = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      ),
                      type22QCDAna33 = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      )

)

