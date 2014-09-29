import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_1.root',
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_2.root',
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_3.root',
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_4.root',
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_5.root',
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_6.root',
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_7.root',
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_8.root',
    '/store/user/rappocc/SinglePiPt100/PFRecHitTimingNoPUStep3/140925_161155/0000/step3_9.root',
                                )
                                )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('pionPFAnalyzer.root')
                                   )



process.load('Analysis.PionPFAnalyzer.pionPFAnalyzer_cfi')

process.p = cms.Path(
    process.pionPFAnalyzer
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
