import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    #'file:/uscms_data/d2/guofan/patTuples/boostedTop/CMSSW_3_8_7/src/pickEvents/pickEvents_ReReco.root'
    #'file:/uscms/home/guofan/work/boostedTop/hadronicAnalysis/CMSSW_3_8_7/src/pickEvents/crab_0_110128_214641/res/pickevents_1_1_1Cp.root'
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_83_1_edc.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_82_1_0JR.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_81_1_MjO.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_80_1_10Z.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_7_1_NLO.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_79_1_xzO.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_78_1_gl0.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_77_1_VJA.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_76_1_2mG.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_75_1_8Os.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_74_1_NWT.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_73_1_RWQ.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_72_1_p20.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_71_1_FfP.root',
'dcap:///pnfs/cms/WAX/11/store/user/guofan/Jet/Run2010-Nov4ReReco_v1_ttbsm_387_v2/5a03e904833f2addf159ca9dd7167ab5/ttbsm_387_70_1_Gmc.root'
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
  process.mistagAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                      mistagAna = cms.PSet(
                      initialSeed = cms.untracked.uint32(81)
                      )

)

