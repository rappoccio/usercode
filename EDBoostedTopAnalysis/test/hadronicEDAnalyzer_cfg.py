import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'/store/user/srappocc/MinimumBias/ttbsmAug10_381on36x_r1/4e8cc640dce80838a57cdc6e0cf49d2e/ttbsm_381_1_1_qpg.root',
'/store/user/srappocc/MinimumBias/ttbsmAug10_381on36x_r1/4e8cc640dce80838a57cdc6e0cf49d2e/ttbsm_381_19_1_ZCG.root',
'/store/user/srappocc/MinimumBias/ttbsmAug10_381on36x_r1/4e8cc640dce80838a57cdc6e0cf49d2e/ttbsm_381_18_1_MDf.root',
'/store/user/srappocc/MinimumBias/ttbsmAug10_381on36x_r1/4e8cc640dce80838a57cdc6e0cf49d2e/ttbsm_381_17_1_fkw.root'

    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

from Analysis.BoostedTopAnalysis.hadronicAnalysis_cfi import hadronicAnalysis as inputHadronicAnalysis




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("boostedTopHadronicStudies_pt_gt25.root")
                                   )


process.hadronicAna = cms.EDAnalyzer('EDHadronicAnalysis',
                                     hadronicAnalysis = inputHadronicAnalysis.clone(
                                         dijetSelectorParams = inputHadronicAnalysis.dijetSelectorParams.clone(
                                             pfMetSrc = cms.InputTag('patMETsPFlow'),
                                             ptMin = cms.double(50.0)
                                             ),
                                         trig = cms.string('HLT_Jet30U')
                                         )
                                     )

process.hadronicAnaUnweighted = process.hadronicAna.clone( )

process.hadronicAna.plotOptions = cms.PSet(
    plotTracks = cms.bool(True),
    reweightHistoFile = cms.string('reweight_histo.root'),
    reweightHistoName = cms.string('ratio')
            )

process.hadronicAnaUnweighted.plotOptions = cms.PSet(
    plotTracks = cms.bool(True)
    )

process.p = cms.Path(
#    process.hadronicAna*
    process.hadronicAnaUnweighted
    )

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                      hadronicAnaUnweighted = cms.PSet(
                      initialSeed = cms.untracked.uint32(157)
                      )
)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
