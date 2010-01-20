import FWCore.ParameterSet.Config as cms

process = cms.Process("FWDREF")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_3_3_0/RelValTTbar/GEN-SIM-RECO/STARTUP31X_V8-v1/0001/3291E09D-67B7-DE11-9ED6-003048678C9A.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


## fwdref test
process.fwdref = cms.EDFilter("FwdRefTest",
                              jetSrc = cms.InputTag("ak5CaloJets")
)

process.fwdrefcheck = cms.EDAnalyzer("FwdRefCheck",
                                     jetSrc1 = cms.InputTag("ak5CaloJets"),
                                     jetSrc2 = cms.InputTag("fwdref"),
                                     refVecSrc = cms.InputTag("fwdref"),
                                     jetIDSrc = cms.InputTag("ak5JetID")
)

process.p = cms.Path( process.fwdref * process.fwdrefcheck )

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('fwdref_test.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_fwdref_*_*',
                                                                      'keep *_ak5JetID_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)
