import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                [
'/store/user/smpjs/jpilot/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/a326ba49a16ab761c492392538b61378/ttbsm_42x_mc_5_1_JIQ.root',
'/store/user/smpjs/jpilot/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/a326ba49a16ab761c492392538b61378/ttbsm_42x_mc_60_1_UoA.root'
]
                                )
                            )



## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


import sys

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.pvCount = cms.EDFilter(
    "EDPileupAna",
    src=cms.InputTag('goodOfflinePrimaryVertices')
    )

process.ca8Lite = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("goodPatJetsCA8PF"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("px"),
            quantity = cms.untracked.string("px()")
            ),
        cms.PSet(
            tag = cms.untracked.string("py"),
            quantity = cms.untracked.string("py()")
            ),
        cms.PSet(
            tag = cms.untracked.string("pz"),
            quantity = cms.untracked.string("pz()")
            ),
        cms.PSet(
            tag = cms.untracked.string("energy"),
            quantity = cms.untracked.string("energy()")
            ),
        cms.PSet(
            tag = cms.untracked.string("jecFactor"),
            quantity = cms.untracked.string("jecFactor(0)")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea()")
            ),
        )  
    )


process.ak5Gen = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("ak5GenJetsNoNu"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("px"),
            quantity = cms.untracked.string("px()")
            ),
        cms.PSet(
            tag = cms.untracked.string("py"),
            quantity = cms.untracked.string("py()")
            ),
        cms.PSet(
            tag = cms.untracked.string("pz"),
            quantity = cms.untracked.string("pz()")
            ),
        cms.PSet(
            tag = cms.untracked.string("energy"),
            quantity = cms.untracked.string("energy()")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea()")
            ),
        )  
    )

process.ak8Gen = process.ak5Gen.clone(
    src = cms.InputTag("ak8GenJetsNoNu")
    )

process.ak7Gen = process.ak5Gen.clone(
    src = cms.InputTag("ak7GenJetsNoNu")
    )

process.ca8Gen = process.ak5Gen.clone(
    src = cms.InputTag("ca8GenJetsNoNu")
    )


process.patseq = cms.Sequence(
    process.pvCount *
    process.ca8Lite *
    process.ak5Gen *
    process.ak7Gen *
    process.ak8Gen *
    process.ca8Gen
    )


process.p0 = cms.Path(
    process.patseq
    )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('ttbsm_v10beta_tuple_42x_mc.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p0') ),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep *_*Lite*_*_*',
                                   'keep *_ak5Gen_*_*',
                                   'keep *_ak7Gen_*_*',
                                   'keep *_ak8Gen_*_*',
                                   'keep *_ca8Gen_*_*',
                                   'keep *_pvCount_*_*',
                                   'keep double_kt6PFJets_*_*',
                                   'keep *_addPileupInfo_*_*',
                                   'keep *_generator_*_*'
                                   ),
                               dropMetaData = cms.untracked.string("DROPPED")
                               )
process.outpath = cms.EndPath(process.out)


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )


