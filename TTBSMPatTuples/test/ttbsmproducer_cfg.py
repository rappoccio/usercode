import FWCore.ParameterSet.Config as cms

process = cms.Process("TTBSM")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/Run2010B-Nov4ReReco_v1_ttbsm_387_v2/8919c3a29409d26fe513538bb627487e/ttbsm_386_10_1_eNq.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/Run2010B-Nov4ReReco_v1_ttbsm_387_v2/8919c3a29409d26fe513538bb627487e/ttbsm_386_11_1_V4g.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/Run2010B-Nov4ReReco_v1_ttbsm_387_v2/8919c3a29409d26fe513538bb627487e/ttbsm_386_12_1_XCD.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/Run2010B-Nov4ReReco_v1_ttbsm_387_v2/8919c3a29409d26fe513538bb627487e/ttbsm_386_13_1_Btc.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/Run2010B-Nov4ReReco_v1_ttbsm_387_v2/8919c3a29409d26fe513538bb627487e/ttbsm_386_14_1_yR4.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/Run2010B-Nov4ReReco_v1_ttbsm_387_v2/8919c3a29409d26fe513538bb627487e/ttbsm_386_15_1_7Gg.root',
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/Jet/Run2010B-Nov4ReReco_v1_ttbsm_387_v2/8919c3a29409d26fe513538bb627487e/ttbsm_386_16_1_aDK.root'
    )
)

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
from Analysis.BoostedTopAnalysis.CATopTagParams_cfi import caTopTagParams
from Analysis.BoostedTopAnalysis.BoostedTopWTagParams_cfi import boostedTopWTagParams


process.anaselectedAK5PFJets = cms.EDFilter("CandViewShallowCloneProducer",
                                   src = cms.InputTag('selectedPatJets'),
                                   cut = cms.string('pt > 40 & abs(eta) < 2.4')
                                   )


process.jetFilter = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("anaselectedAK5PFJets"),
                                 minNumber = cms.uint32(0),
                                 maxNumber = cms.uint32(6),
                                 filter=cms.bool(True)
                                  )

process.ttbsmAna = cms.EDFilter('TTBSMProducer',
                                wTagSrc = cms.InputTag('selectedPatJetsCA8PrunedPF'),
                                topTagSrc = cms.InputTag('selectedPatJetsCATopTagPF'),
                                pfJetIdParams = pfJetIDSelector.clone(),
                                topTagParams = caTopTagParams.clone(
                                    tagName = cms.string('CATop')
                                    ),
                                wTagParams = boostedTopWTagParams.clone()                                
)


process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.p = cms.Path(
    process.anaselectedAK5PFJets*
    process.jetFilter*
    process.ttbsmAna
    )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("ttbsm_ultraslim.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_ttbsmAna_*_*' ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
