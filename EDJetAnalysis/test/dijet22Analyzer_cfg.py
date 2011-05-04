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
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_10_1_03g.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_10_1_RKm.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_11_1_AbM.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_11_1_it1.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_12_1_HJA.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_12_1_bZB.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_13_1_2NJ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_13_1_EWJ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_14_1_9Sm.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_14_1_xLk.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_15_1_0WI.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_15_1_o5A.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_16_1_5iA.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_16_1_enr.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_17_1_5bK.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_17_1_CTW.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_18_1_Fpd.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_18_2_Vbo.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_18_2_etz.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_19_1_VFl.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_19_1_nkE.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_1_1_JWP.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_1_1_ne2.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_20_1_NFp.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_20_1_ja8.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_21_1_PUR.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_21_1_h8z.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_22_1_VGm.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_22_1_VYg.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_23_1_JeO.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_23_1_kJj.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_24_1_E7H.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_24_1_b2S.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_25_1_Pzy.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_25_1_owb.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_26_1_2hC.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_26_1_qex.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_27_1_htR.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_27_1_sqe.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_28_1_TcF.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_28_1_YJm.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_29_1_0hU.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_29_1_U9q.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_2_1_ByU.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_2_1_qtt.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_30_1_YgH.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_30_1_kNj.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_31_1_96Q.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_31_1_UyJ.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_32_1_4Yw.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_32_1_zog.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_33_1_OLG.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_33_1_uuh.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_34_1_qJd.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_34_1_s8b.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_35_1_fY4.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_36_1_pgq.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_3_1_MEt.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_3_1_sTv.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_4_1_dtf.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_4_1_t8p.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_5_1_075.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_5_1_EQP.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_6_1_5uN.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_6_1_zgM.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_7_1_SWx.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_7_1_nN3.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_8_1_SPw.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_8_1_Szj.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_9_1_Ylg.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/ttbsm_v2_Run2011A-PromptReco-v1/84471d8a18e499e217065966b63862b9/ttbsm_414_data_9_1_vii.root'
                                
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
