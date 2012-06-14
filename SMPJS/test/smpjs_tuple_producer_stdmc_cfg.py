import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                [
'/store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/9AF32315-EC97-E011-8B25-0026189438B3.root',
'/store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/18F1D3EA-E597-E011-8452-00304867BFBC.root'

                        ]
                                )
                            )



## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


import sys

# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')
# Modify defaults setting to avoid an over-efficiency in the presence of OFT PU
process.HBHENoiseFilter.minIsolatedNoiseSumE = cms.double(999999.)
process.HBHENoiseFilter.minNumIsolatedNoiseChannels = cms.int32(999999)
process.HBHENoiseFilter.minIsolatedNoiseSumEt = cms.double(999999.)

process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )

pvSrc = 'offlinePrimaryVertices'

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0),
                                     minNdof = cms.double(4.0) # this is >= 4
                                     ),
    src=cms.InputTag(pvSrc)
    )


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag("goodOfflinePrimaryVertices"),
                                           minimumNDOF = cms.uint32(3) , # this is > 3
                                           maxAbsZ = cms.double(24), 
                                           maxd0 = cms.double(2) 
                                           )


process.load("RecoJets.Configuration.GenJetParticles_cff")
from RecoJets.Configuration.RecoGenJets_cff import ak5GenJetsNoNu
process.ak5GenJetsNoNu = ak5GenJetsNoNu.clone()

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJets = kt4PFJets.clone(
    rParam = cms.double(0.6),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.pvCount = cms.EDFilter(
    "EDPileupAna",
    src=cms.InputTag('goodOfflinePrimaryVertices')
    )

process.pvCountAll = cms.EDFilter(
    "EDPileupAna",
    src=cms.InputTag('offlinePrimaryVertices')
    )

process.ak5Lite = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("ak5PFJets"),
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

process.patseq = cms.Sequence(
    process.scrapingVeto*
    process.HBHENoiseFilter*
    process.goodOfflinePrimaryVertices*
    process.primaryVertexFilter*
    process.pvCount *
    process.pvCountAll *
    process.ak5Lite *
    process.genParticlesForJetsNoNu*
    process.kt6PFJets*
    process.ak5GenJetsNoNu*
    process.ak5Gen
    )


process.p0 = cms.Path(
    process.patseq
    )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('ttbsm_v10beta_tuple_42x_stdmc.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p0') ),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep *_*Lite*_*_*',
                                   'keep *_ak5Gen_*_*',
                                   'keep *_pvCount*_*_*',
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


