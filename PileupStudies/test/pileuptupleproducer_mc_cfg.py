import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/pileupstudies_424_v2/a9c957deb24827efe91ad47274317b2d/patTuple_78_1_P9G.root'
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

process.ak5Def = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("goodPatJets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("correctedJet(0).pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("correctedJet(0).jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("correctedJet(0).eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("correctedJet(0).phi")
            ), 
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("correctedJet(0).mass")
            ), 
        )  
    )

process.ak5CHS = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("goodPatJetsPFlow"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("correctedJet(0).pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("correctedJet(0).jetArea")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("correctedJet(0).eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("correctedJet(0).phi")
            ), 
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("correctedJet(0).mass")
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
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ), 
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            ), 
        )  
    )



process.patseq = cms.Sequence(
    process.pvCount*
    process.ak5Def *
    process.ak5CHS *
    process.ak5Gen
    )


process.p0 = cms.Path(
    process.patseq
    )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('pileuptuple_424.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p0') ),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep *_ak5CHS_*_*',
                                   'keep *_ak5Gen_*_*',
                                   'keep *_ak5Def_*_*',
                                   'keep *_pvCount_*_*',
                                   'keep double_*PFlow*_*_*',
                                   'keep double_*kt6*_*_*',
                                   'keep double_fixed*_*_*',
                                   'keep *_addPileupInfo_*_*'
                                   ),
                               dropMetaData = cms.untracked.string("DROPPED")
                               )
process.outpath = cms.EndPath(process.out)


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )



