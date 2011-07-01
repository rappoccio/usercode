import FWCore.ParameterSet.Config as cms

process = cms.Process("TTBSM")


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')




options.register ('sample',
                  'Jet',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Sample to use.")




options.parseArguments()

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )



## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V12::All'
process.load("Configuration.StandardSequences.MagneticField_cff")


from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
from Analysis.BoostedTopAnalysis.CATopTagParams_cfi import caTopTagParams
from Analysis.BoostedTopAnalysis.BoostedTopWTagParams_cfi import boostedTopWTagParams


if options.sample == 'Jet' :
    process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
                                fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_100_1_w3O.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_101_1_5y4.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_102_1_en8.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_103_1_JMP.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_104_1_MbI.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_105_1_P6i.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_106_1_RqH.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_107_1_kRA.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_108_1_IJb.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v8_Run2011-May10ReReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_109_1_b9J.root'

                                    )
                                )

    
    mytrigs = [
        'HLT_Jet190_v*',
        'HLT_Jet240_v*',
        'HLT_Jet300_v*',
        'HLT_Jet370_v*'
        ]
    from HLTrigger.HLTfilters.hltHighLevel_cfi import *
    process.hltSelection1 = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
    process.hltSelection1.throw = False
    process.hltSelection = cms.Sequence( process.hltSelection1 )
elif options.sample == 'HT' :

    process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
                                fileNames = cms.untracked.vstring(
                                    'file:ttbsm_42x_mc.root'
#'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/guofan/HT/ttbsm_v5_Run2011A-May10ReReco-v1/66893cf1a11d0e3066e5097c4fdc37a6/ttbsm_42x_data_74_1_PRV.root',
                                    )
                                )
    
    mytrigs1 = ['HLT_Jet240_v1',
                'HLT_Jet300_v*',
                'HLT_Jet370_v*']
    mytrigs2 = ['HLT_HT500*']
    from HLTrigger.HLTfilters.hltHighLevel_cfi import *
    process.hltSelection1 = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs1)
    process.hltSelection1.throw = False
    process.hltSelection2 = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs2)
    process.hltSelection2.throw = False
    process.hltSelection = cms.Sequence( ~process.hltSelection1 * process.hltSelection2 )

    
# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')


myAnaTrigs = [
    'HLT_Jet190_v1',
    'HLT_Jet190_v2',
    'HLT_Jet190_v3',
    'HLT_Jet190_v4',
    'HLT_Jet190_v5',
    'HLT_Jet190_v6',
    'HLT_Jet190_v7',
    'HLT_Jet240_v1',
    'HLT_Jet240_v2',
    'HLT_Jet240_v3',
    'HLT_Jet240_v4',
    'HLT_Jet240_v5',
    'HLT_Jet240_v6',
    'HLT_Jet240_v7',
    'HLT_Jet300_v1',
    'HLT_Jet300_v2',
    'HLT_Jet300_v3',
    'HLT_Jet300_v4',
    'HLT_Jet300_v5',
    'HLT_Jet300_v6',
    'HLT_Jet300_v7',
    'HLT_Jet370_v1',
    'HLT_Jet370_v2',
    'HLT_Jet370_v3',
    'HLT_Jet370_v4',
    'HLT_Jet370_v5',
    'HLT_Jet370_v6',
    'HLT_Jet370_v7'
    ]
process.ttbsmAna = cms.EDFilter('TTBSMProducer',
                                wTagSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                topTagSrc = cms.InputTag('goodPatJetsCATopTagPF'),
                                trigSrc = cms.InputTag('patTriggerEvent'),
                                rhoSrc = cms.InputTag('kt6PFJetsPFlow', 'rho'),
                                pvSrc = cms.InputTag('goodOfflinePrimaryVertices'),
                                trigs = cms.vstring(
                                    myAnaTrigs
                                    ),
                                topTagParams = caTopTagParams.clone(
                                    tagName = cms.string('CATop')
                                    ),
                                wTagParams = boostedTopWTagParams.clone(
                                    yCut = cms.double(0.0)
                                    ),
                                readTrig = cms.bool(True),
                                jetScale = cms.double(0.0),   #
                                jetPtSmear = cms.double(0.0), # note these three are fractional
                                jetEtaSmear = cms.double(0.0),#
                                jecPayloads = cms.vstring([
                                    'Jec11_V3_L1FastJet_AK5PFchs.txt',
                                    'Jec11_V3_L2Relative_AK5PFchs.txt',
                                    'Jec11_V3_L3Absolute_AK5PFchs.txt',
                                    'Jec11_V3_L2L3Residual_AK5PFchs.txt',
                                    'Jec11_V3_Uncertainty_AK5PFchs.txt'
                                    ]),
                                pdfSet = cms.string("")
)





process.MessageLogger.cerr.FwkReport.reportEvery = 100

print 'Making the path'

process.p = cms.Path(
    process.hltSelection*
    process.patTriggerDefaultSequence*
    process.ttbsmAna
    )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("ttbsm_ultraslim.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_ttbsmAna_*_*'
                                                                      #, 'keep *_goodPatJetsCA8PrunedPF_*_*'
                                                                      #, 'keep *_goodPatJetsCATopTagPF_*_*'
                                                                      #, 'keep recoPFJets_*_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )
#process.MessageLogger.destinations.remove( 'errors' )
