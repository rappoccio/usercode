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
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_100_1_Fkn.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_102_1_CCu.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_10_1_Ztf.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_10_1_fis.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_11_1_73y.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_11_1_AyF.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_12_1_HQd.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_12_1_b0q.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_13_1_7Eb.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_13_1_GiP.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_14_1_8zV.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_14_1_w3t.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_15_1_F2F.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_15_1_v2E.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_16_1_TC6.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_16_1_t9h.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v3_Run2011-PromptReco/dc97efd01703e3edbb5420e49bf35fb4/ttbsm_41x_data_17_1_8AI.root',

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
