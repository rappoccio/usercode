import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/ttbsm_383_Oct25_147146_148058/e6b092d68d75aab417dfeee8751d8b0a/ttbsm_381_1_1_Ieu.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

from Analysis.BoostedTopAnalysis.hadronicAnalysis_cfi import hadronicAnalysis as inputHadronicAnalysis




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("boostedTopHadronicStudies.root")
                                   )


process.hadronicAna = cms.EDAnalyzer('EDHadronicAnalysis',
                                     hadronicAnalysis = inputHadronicAnalysis.clone(
                                         dijetSelectorParams = inputHadronicAnalysis.dijetSelectorParams.clone(
                                             pfMetSrc = cms.InputTag('patMETsPFlow'),
                                             ptMin = cms.double(200)
                                             #ptMin = cms.double(220)
                                             ),
                                         trig = cms.string('HLT_Jet100U_v2'),
                                         cutsToIgnore = cms.vstring("Trigger")
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
                      ),
                      hadronic2 = cms.PSet( initialSeed = cms.untracked.uint32(11) )
)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
