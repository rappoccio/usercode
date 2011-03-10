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

if not options.useData :
    #mytrigs = ['HLT_Jet100U*']
    mytrigs = ['HLT_Jet30U*']
    inputJetCorrLabel = ('AK5PF', ['L2Relative', 'L3Absolute'])
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring( 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6/pileupstudies_387_v1/354f7f597ac7df252a905f080fd28889/pileupstudies_387_1_1_qxF.root'
                                    )
                                )
else :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/Run2010B-Nov4ReReco_v1_pileupstudies_387_v2/9f1aaecf6c0c99a7f05a653bbea518c1/pileupstudies_387_1_1_IPn.root'
                                    )
                                )


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


print options

import sys

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.pvSel = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')    
    )

process.pvCount = cms.EDFilter(
    "EDPileupAna",
    src=cms.InputTag('pvSel')
    )

process.ak5Def = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("goodPatJetsPFlowAK5"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(True),
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
    src = cms.InputTag("goodPatJetsPFlowPUSubAK5"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(True),
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


process.genJets = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("ak5GenJets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(True),
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
    process.pvSel *
    process.pvCount*
    process.ak5Def *
    process.ak5CHS *
    process.genJets
    )


process.p0 = cms.Path(
    process.patseq
    )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('pileuptuple_387.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p0') ),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep *_ak5CHS_*_*',
                                   'keep *_ak5Def_*_*',
                                   'keep *_pvCount_*_*',
                                   'keep double_*PFlow*_*_*',
                                   'keep double_*kt6*_*_*'
                                   ),
                               dropMetaData = cms.untracked.string("DROPPED")
                               )
process.outpath = cms.EndPath(process.out)


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )



