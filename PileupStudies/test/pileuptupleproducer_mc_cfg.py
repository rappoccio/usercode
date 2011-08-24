import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.parseArguments()


process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                'file:patTuple.root'
                                )
                            )



## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


print options

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
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("jetArea"),
            quantity = cms.untracked.string("jetArea")
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



