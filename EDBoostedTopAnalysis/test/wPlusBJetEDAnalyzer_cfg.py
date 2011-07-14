import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    'dcap:///pnfs/cms/WAX/11/store/user/guofan/QCD6Jets_Pt280to500-alpgen/ttbsm_38onRedigi36/cb1594198a28dea2154e88b47479a871/ttbsm_381_2_1_C9K.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

from Analysis.BoostedTopAnalysis.wPlusBJetAnalysis_cfi import *




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("wPlusBJetAnalysis.root")
                                   )

process.wPlusBJetAna = cms.EDAnalyzer('EDWPlusBJetAnalysis',
                                   wPlusBJetAnalysis.clone()
                                     )

process.wPlusBJetAna.WPlusBJetEventSelection.leadJetPtCut = cms.double(100)
process.wPlusBJetAna.WPlusBJetEventSelection.secondJetPtCut = cms.double(30)
process.wPlusBJetAna.WPlusBJetEventSelection.thirdJetPtCut = cms.double(30)
process.wPlusBJetAna.WPlusBJetEventSelection.fourthJetPtCut = cms.double(30)
process.wPlusBJetAna.WPlusBJetEventSelection.mistagFileName = "mistag_6jets_alljets_medium.root"
process.wPlusBJetAna.WPlusBJetEventSelection.bTagOP =  3.3 #1.7  loose point
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

