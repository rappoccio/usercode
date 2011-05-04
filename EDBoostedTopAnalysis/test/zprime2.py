import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useTrigger',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events by trigger path")


options.register ('jetPD',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "use triggers from the Jet PD (1), ignore them (0), or veto them (-1), if useTrigger == 1")


options.register ('htPD',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "use triggers from the HT PD (1), ignore them (0), or veto them (-1), if useTrigger == 1")



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
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_10_1_RKm.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_11_1_it1.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_12_1_HJA.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_13_1_EWJ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_14_1_xLk.root',

    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

from Analysis.BoostedTopAnalysis.Type11SelectionParams_cfi import *
from Analysis.BoostedTopAnalysis.Type22SelectionParams_cfi import *




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("jetPD.root")
                                   )

process.cascadingQCDAna15 = cms.EDAnalyzer('EDCombinedQCDEstimation',
                                           Type11QCDEstimationParams.clone(
                                               caTopJetPtMin = cms.double(400)
                                               ),
                                           Type22QCDEstimationParams.clone(
                                               jetPt0 = cms.double(400)
                                               )
                                           )

#process.type22QCDAna10 = process.type22QCDAna15.clone( Probability = cms.double(0.10) )
#process.type22QCDAna5 = process.type22QCDAna15.clone( Probability = cms.double(0.05) )
#process.type22QCDAna33 = process.type22QCDAna15.clone( Probability = cms.double(0.33) )

process.p = cms.Path(
    process.trigs*
    process.cascadingQCDAna15
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                      cascadingQCDAna15 = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      )

)

