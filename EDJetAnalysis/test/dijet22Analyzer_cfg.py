import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

import FWCore.PythonUtilities.LumiList as LumiList

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")


options.parseArguments()

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# get JSON file correctly parced
#JSONfile = 'Cert_161079-161352_7TeV_PromptReco_Collisions11_JSON_noESpbl_v2.txt'
#myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')

mytrigs = ['HLT_Jet370*']

from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if mytrigs is not None :
    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
    process.hltSelection.throw = False


#if options.useData :
histFileName = 'dijet22AnalyzerJet2011A.root'
## Source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring([
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v6_Run2011-May10ReReco/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_26_0_4mM.root'
                                ]
                                                              )#,
                            #        lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )
                            )



## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(histFileName)
                                   )


from Analysis.JetAnalysis.simpleSubstructureSelector_cfi import simpleSubstructureSelector as simpleSubstructureSelectorInput

process.ca8PrunedAnalyzer = cms.EDAnalyzer('EDDijet22Analyzer',
                                           simpleSubstructureSelector = simpleSubstructureSelectorInput.clone(
                                               ptCut = cms.double(400)
                                               )
                                           )


process.p = cms.Path(
    process.hltSelection*
    process.ca8PrunedAnalyzer
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
