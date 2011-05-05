import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useTrigger',  True,
                  VarParsing.multiplicity.singleton, VarParsing.varType.int,
                  "Use trigger" )

options.register( 'jetPD',    1,
                  VarParsing.multiplicity.singleton, VarParsing.varType.int, "Jet PD" )

options.register( 'htPD',    -1,
                  VarParsing.multiplicity.singleton, VarParsing.varType.int, "HT PD" )

options.parseArguments()

print options

###############################
########## Trigger ############
###############################
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if options.useTrigger :
    process.jetTrig = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_Jet370_*"])
    process.htTrig  = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["HLT_HT500_*"])

    process.jetTrig.throw= cms.bool(False)
    process.htTrig.throw= cms.bool(False)

    if options.jetPD > 0 :
        process.trigs = cms.Sequence( process.jetTrig )
    elif options.jetPD < 0 and options.htPD > 0 :
        process.trigs = cms.Sequence( ~process.jetTrig *
                                      process.htTrig )
    elif options.htPD > 0 :
        process.trigs = cms.Sequence( process.htTrig )
else :
    process.alltrig = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT", HLTPaths = ["*"])
    process.trigs = cms.Sequence( process.alltrig )



## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    #'file:/uscms_data/d2/guofan/patTuples/boostedTop/CMSSW_3_8_7/src/pickEvents/pickEvents_ReReco.root'
    #'file:/uscms/home/guofan/work/boostedTop/hadronicAnalysis/CMSSW_3_8_7/src/pickEvents/crab_0_110128_214641/res/pickevents_1_1_1Cp.root'
    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_10_1_RKm.root',
    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_11_1_it1.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

from Analysis.BoostedTopAnalysis.MistagMaker_cfi import *




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("Mistag.root")
                                   )

process.mistagAna = cms.EDAnalyzer('EDMistagMaker',
                                    MistagMakerParams
                                  )


process.p = cms.Path(
  process.trigs*process.mistagAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                      mistagAna = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      )

)

