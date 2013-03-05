import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

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
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/jpilot/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/7305e6f2cb5c2c3444120cb6d446b6e4/ttbsm_52x_mc_80_1_rVD.root'
                                    )
                                )
    process.GlobalTag.globaltag = 'START53_V7G::All'
else :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/jpilot/JetHT/Run2012D-PromptReco-v1_TLBSM_53x_v2_b/e3fb55b810dc7a0811f4c66dfa2267c9/tlbsm_53x_v2_data_1_1_x2f.root'
                                    )
                                )
    process.GlobalTag.globaltag = 'GR_P_V42_AN4::All'


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


print options

import sys

process.pvCount = cms.EDFilter(
    "EDPileupAna",
    src=cms.InputTag('goodOfflinePrimaryVertices')
    )



###############################
###### AK 0.5 jets groomed ####
###############################

ak5JetSrc = cms.InputTag("selectedPatJetsPFlow","pfCandidates")

from RecoJets.JetProducers.ak5PFJetsTrimmed_cfi import ak5PFJetsTrimmed
process.ak5TrimmedPFlow = ak5PFJetsTrimmed.clone(
    src = ak5JetSrc,
    doAreaFastjet = cms.bool(True)
    )

from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsFiltered
process.ak5FilteredPFlow = ak5PFJetsFiltered.clone(
    src = ak5JetSrc,
    doAreaFastjet = cms.bool(True)
    )

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
process.ak5PrunedPFlow = ak5PFJetsPruned.clone(
    src = ak5JetSrc,
    doAreaFastjet = cms.bool(True)
    )


process.ak5Ungroomed = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("goodPatJetsPFlow"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string(""),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("correctedP4(0).pt()")
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
            quantity = cms.untracked.string("correctedP4(0).mass()")
            ), 
        )  
    )

process.ak5Trimmed = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("ak5TrimmedPFlow"),
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


process.ak5Filtered = process.ak5Trimmed.clone(
    src = cms.InputTag("ak5FilteredPFlow")
    )

process.ak5Pruned = process.ak5Trimmed.clone(
    src = cms.InputTag("ak5PrunedPFlow")
    )



# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')




process.patseq = cms.Sequence(
    process.patTriggerDefaultSequence*
    process.pvCount*
    process.ak5Ungroomed *
    process.ak5TrimmedPFlow *
    process.ak5PrunedPFlow *
    process.ak5FilteredPFlow *
    process.ak5Trimmed * 
    process.ak5Filtered *
    process.ak5Pruned 
    )


process.p0 = cms.Path(
    process.patseq
    )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('pileup_grooming_studies_tuple.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p0') ),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep *_pvCount_*_*',
                                   'keep floats_*_*_ANA',
                                   'keep double_kt6PF_*_*',
                                   'keep PileupSummaryInfos_*_*_*',
                                   'keep GenRunInfoProduct_generator_*_*',
                                   'keep GenEventInfoProduct_generator_*_*',
                                   'keep LumiSummary_lumiProducer_*_*',
                                   'keep *_goodOfflinePrimaryVertices*_*_*',
                                   #'keep *_TriggerResults_*_*',
                                   #'keep *_hltTriggerSummaryAOD_*_*',
                                   'keep *_patTriggerEvent_*_*'
                                   ),
                               dropMetaData = cms.untracked.string("DROPPED")
                               )
process.outpath = cms.EndPath(process.out)


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )



process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

