import FWCore.ParameterSet.Config as cms

process = cms.Process("TTBSM")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
       fileNames = cms.untracked.vstring(
#       'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/jdolen/Zprime_M1000GeV_W10GeV-madgraph/ttbsm_v8_Summer11-PU_S4_-START42_V11-v2/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_10_1_Mmd.root'
                                'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/jdolen/Zprime_M2000GeV_W20GeV-madgraph/ttbsm_v8_Summer11-PU_S4_-START42_V11-v2/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_10_1_rPv.root'
       #'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/weizou/WprimeToTBbar_M-2000_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_-START42_V11-v1/2bcf344afee8f9cb5489a05cc32c05cf/ttbsm_42x_mc_1_1_J1v.root'
                                    )
                                )



## Geometry and Detector Conditions (needed for a few patTuple production steps)
#process.load("Configuration.StandardSequences.Geometry_cff")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = 'GR_R_42_V12::All'
#process.load("Configuration.StandardSequences.MagneticField_cff")


process.boostedTopTrigger = cms.EDAnalyzer('BoostedTopTrigger',
                                           jetTag1 = cms.untracked.InputTag("goodPatJetsCATopTagPF")
                                           , jetTag2 = cms.untracked.InputTag("goodPatJetsCA8PrunedPF")
                                           , TargetTrigger = cms.untracked.string("HLT_Jet240_v1")
                                           #, Verbose = cms.untracked.bool(True)
                                         )




process.MessageLogger.cerr.FwkReport.reportEvery = 100

print 'Making the path'

process.p = cms.Path(
    #process.patTriggerDefaultSequence*
    #process.hltSelection*
    process.boostedTopTrigger
    #*process.pdfWeights
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

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
##process.out.dropMetaData = cms.untracked.string("DROPPED")
