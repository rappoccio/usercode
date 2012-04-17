import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")


process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V24::All'
process.load("Configuration.StandardSequences.MagneticField_cff")


process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
                                    [
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_90_1_HYu.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_90_1_M3X.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_90_1_ua7.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_91_1_15a.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_91_1_S7o.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_91_1_erN.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_91_1_ias.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_91_1_oDm.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_92_1_6s8.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_92_1_7Th.root',
                                    '/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_92_1_E1g.root'
                                    ]
                                )
                            )



## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


mytrigs = [
    'HLT_Jet*_v*',
    ]
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
process.hltSelection1 = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
process.hltSelection1.throw = False
process.hltSelection = cms.Sequence( process.hltSelection1 )

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.pvCount = cms.EDFilter(
    "EDPileupAna",
    src=cms.InputTag('goodOfflinePrimaryVertices')
    )

# Select only triggers we want, write them out, and their prescales
process.dijetTriggerFilter = cms.EDFilter(
    "EDDijetTriggerFilter",
    src = cms.InputTag("patTriggerEvent"),
    trigs = cms.vstring( [
        'HLT_Jet60',
        'HLT_Jet110',
        'HLT_Jet190',
        'HLT_Jet240',
        'HLT_Jet370'
        ])
    )

process.patseq = cms.Sequence(
    process.pvCount *
    process.hltSelection *
    process.patTriggerDefaultSequence*
    process.dijetTriggerFilter
    )


process.p0 = cms.Path(
    process.patseq
    )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('ttbsm_v10beta_tuple_42x_data.root'),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p0') ),
                               outputCommands = cms.untracked.vstring(
                                   'drop *',
                                   'keep *_*Lite*_*_*',
                                   'keep *_pvCount_*_*',
                                   'keep double_kt6PFJets_*_*',
                                   'keep *_dijetTriggerFilter_*_*'
                                   #'keep *_patTrigger*_*_*'
                                   ),
                               dropMetaData = cms.untracked.string("DROPPED")
                               )
process.outpath = cms.EndPath(process.out)


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )


process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )
