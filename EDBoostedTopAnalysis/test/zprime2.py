import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_10_1_RKm.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_11_1_it1.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_12_1_HJA.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_13_1_EWJ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_14_1_xLk.root',

    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

from Analysis.BoostedTopAnalysis.Type11SelectionParams_cfi import *
from Analysis.BoostedTopAnalysis.Type22SelectionParams_cfi import *




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("jetPD.root")
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

