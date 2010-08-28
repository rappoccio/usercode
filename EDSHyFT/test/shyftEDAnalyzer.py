import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
                                'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn356_v2/efe53b645403790e1d3a86e1908711f6/shyft_382_pat_10_1_b1r.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies.root")
                                   )


process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                  shyftAnalysis = inputShyftAnalysis.clone(
                                      muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                      electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                      metSrc = cms.InputTag('patMETsPFlow'),
                                      jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                      jetClonesSrc = cms.InputTag('goodPFJets'),
                                      jetPtMin = cms.double(25.0),
                                      minJets = cms.int32(1),
                                      useJetClones = cms.bool(False)
                                      )
                                  
                                  )

process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                  shyftAnalysis = inputShyftAnalysis.clone(
                                      jetClonesSrc = cms.InputTag('goodCaloJets'),
                                      jetPtMin = cms.double(30.0),
                                      minJets = cms.int32(1),
                                      useJetClones = cms.bool(False)
                                      )
                                  
                                  )


process.p = cms.Path(
    process.pfShyftAna*process.caloShyftAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
