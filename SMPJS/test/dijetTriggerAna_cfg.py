import FWCore.ParameterSet.Config as cms

process = cms.Process("TTBSM")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V24::All'
process.load("Configuration.StandardSequences.MagneticField_cff")



process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
       fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/smpjs/srappocc/Jet/ttbsm_v10beta_Run2011/68bf12ab4dfae5632a3177b3a9ce559d/ttbsm_42x_data_1_1_sNX.root'

                                    )
                                )


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("dijetTriggerAna.root")
                                   )


process.jet110Trigger = cms.EDAnalyzer('EDDijetTriggerAna',
                                       jetTag = cms.untracked.string("ak7Lite")
                                       , TargetTrigger = cms.untracked.string("HLT_Jet60_v")
                                       , threshold = cms.untracked.double(110.0)
                                       #, Verbose = cms.untracked.bool(True)
                                       )
process.jet190Trigger = cms.EDAnalyzer('EDDijetTriggerAna',
                                       jetTag = cms.untracked.string("ak7Lite")
                                       , TargetTrigger = cms.untracked.string("HLT_Jet110_v")
                                       , threshold = cms.untracked.double(190.0)
                                       )
process.jet240Trigger = cms.EDAnalyzer('EDDijetTriggerAna',
                                       jetTag = cms.untracked.string("ak7Lite")
                                       , TargetTrigger = cms.untracked.string("HLT_Jet190_v")
                                       , threshold = cms.untracked.double(240.0)
                                       )
process.jet370Trigger = cms.EDAnalyzer('EDDijetTriggerAna',
                                       jetTag = cms.untracked.string("ak7Lite")
                                       , TargetTrigger = cms.untracked.string("HLT_Jet240_v")
                                       , threshold = cms.untracked.double(370.0)
                                       )


process.MessageLogger.cerr.FwkReport.reportEvery = 10000

print 'Making the path'


mytrigs = [
        'HLT_Jet60_v*',
        'HLT_Jet110_v*',
        'HLT_Jet190_v*',
        'HLT_Jet240_v*',
        'HLT_Jet370_v*'
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
process.dijetTriggerFilter60 = cms.EDFilter(
    "EDDijetTriggerFilter",
    src = cms.InputTag("patTriggerEvent"),
    trigs = cms.vstring( [
        'HLT_Jet60_v',
        ])
    )

process.dijetTriggerFilter110 = process.dijetTriggerFilter60.clone(
    trigs = ['HLT_Jet110_v']
    )

process.dijetTriggerFilter190 = process.dijetTriggerFilter60.clone(
    trigs = ['HLT_Jet190_v']
    )

process.dijetTriggerFilter240 = process.dijetTriggerFilter60.clone(
    trigs = ['HLT_Jet240_v']
    )

process.dijetTriggerFilter370 = process.dijetTriggerFilter60.clone(
    trigs = ['HLT_Jet370_v']
    )

process.preseq = cms.Sequence(
    process.pvCount *
    process.hltSelection*
    process.patTriggerDefaultSequence
    )


process.jet110Path = cms.Path(
    process.preseq * process.dijetTriggerFilter60 * process.jet110Trigger
    )

process.jet190Path = cms.Path(
    process.preseq * process.dijetTriggerFilter110 * process.jet190Trigger
    )

process.jet240Path = cms.Path(
    process.preseq * process.dijetTriggerFilter190 * process.jet240Trigger
    )

process.jet370Path = cms.Path(
    process.preseq * process.dijetTriggerFilter240 * process.jet370Trigger
    )


## process.out = cms.OutputModule("PoolOutputModule",
##                                fileName = cms.untracked.string("ttbsm_ultraslim.root"),
##                                SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
##                                outputCommands = cms.untracked.vstring('drop *',
##                                                                       'keep *_ttbsmAna*_*_*'
##                                                                       ,'keep *_hltTriggerSummaryAOD_*_*'
##                                                                       #, 'keep *_goodPatJetsCA8PrunedPF_*_*'
##                                                                       #, 'keep *_goodPatJetsCATopTagPF_*_*'
##                                                                       #, 'keep recoPFJets_*_*_*'
##                                                                       ) 
##                                )
## process.outpath = cms.EndPath(process.out)

process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
##process.out.dropMetaData = cms.untracked.string("DROPPED")
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )
