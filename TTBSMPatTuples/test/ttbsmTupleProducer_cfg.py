import FWCore.ParameterSet.Config as cms

process = cms.Process("TTBSM")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v6_Run2011-May10ReReco/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_200_0_pIF.root',
    )
)

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
from Analysis.BoostedTopAnalysis.CATopTagParams_cfi import caTopTagParams
from Analysis.BoostedTopAnalysis.BoostedTopWTagParams_cfi import boostedTopWTagParams


mytrigs = ['HLT_Jet370*']
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
process.hltSelection.throw = False


process.ttbsmAna = cms.EDFilter('TTBSMProducer',
                                wTagSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                topTagSrc = cms.InputTag('goodPatJetsCATopTagPF'),
                                topTagParams = caTopTagParams.clone(
                                    tagName = cms.string('CATop')
                                    ),
                                wTagParams = boostedTopWTagParams.clone(
                                    yCut = cms.double(0.0)
                                    )
)


process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.p = cms.Path(
    process.hltSelection*
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
