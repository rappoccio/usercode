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


options.register('ignoreTrigger',
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")


options.parseArguments()

print options

import sys

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v6_Run2011-May10ReReco-submit3/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_100_0_3mi.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v6_Run2011-May10ReReco-submit3/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_101_0_K0t.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v6_Run2011-May10ReReco-submit3/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_102_0_u1E.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v6_Run2011-May10ReReco-submit3/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_103_0_TBf.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v6_Run2011-May10ReReco-submit3/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_104_0_4Xn.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v6_Run2011-May10ReReco-submit3/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_105_0_aup.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v6_Run2011-May10ReReco-submit3/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_106_0_2fG.root',
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v6_Run2011-May10ReReco-submit3/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_107_0_uDm.root',

)
)



## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Analysis.SHyFT.shyftPFSelection_cfi import shyftPFSelection as shyftPFSelectionInput



process.pfShyftProducer = cms.EDFilter('EDSHyFTPFSelector',
                                    shyftPFSelection = shyftPFSelectionInput.clone(
                                           
                                             # replace things here if you want
                                        )
                                    )


## std sequence to produce the kinematic fit for semi-leptonic events
process.load('TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Muons_cfi')

process.kinFitTtSemiLepEvent.jets = cms.InputTag("pfShyftProducer", "jets")
process.kinFitTtSemiLepEvent.mets = cms.InputTag("pfShyftProducer", "MET")
process.kinFitTtSemiLepEvent.leps = cms.InputTag("pfShyftProducer", "muons")

process.load("TopQuarkAnalysis.TopKinFitter.TtSemiLepKinFitProducer_Muons_cfi")



## configure output module
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents   = cms.untracked.PSet(SelectEvents = cms.vstring('p') ),                               
    fileName = cms.untracked.string('ttSemiLepKinFitProducer.root'),
    outputCommands = cms.untracked.vstring('drop *')
)
process.out.outputCommands += ['keep *_kinFitTtSemiLepEvent_*_*']



process.pfShyftTupleJets = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "jets"),
    lazyParser = cms.untracked.bool(True),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("mass"),
            quantity = cms.untracked.string("mass")
            ),
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("secvtxMass"),
            quantity = cms.untracked.string("userFloat('secvtxMass')")
            ),
        )  
    )


process.pfShyftTupleMuons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "muons"),
    lazyParser = cms.untracked.bool(True),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('PfAllParticleIso')")
            ),
        )  
    )


process.pfShyftTupleElectrons = cms.EDProducer(
    "CandViewNtpProducer", 
    src = cms.InputTag("pfShyftProducer", "electrons"),
    lazyParser = cms.untracked.bool(True),
    variables = cms.VPSet(
        cms.PSet(
            tag = cms.untracked.string("pt"),
            quantity = cms.untracked.string("pt")
            ),
        cms.PSet(
            tag = cms.untracked.string("eta"),
            quantity = cms.untracked.string("eta")
            ),
        cms.PSet(
            tag = cms.untracked.string("phi"),
            quantity = cms.untracked.string("phi")
            ),
        cms.PSet(
            tag = cms.untracked.string("pfiso"),
            quantity = cms.untracked.string("userIsolation('PfAllParticleIso')")
            ),
        )  
    )


process.p = cms.Path(
    process.pfShyftProducer *
    process.kinFitTtSemiLepEvent *
    process.pfShyftTupleJets*
    process.pfShyftTupleMuons*
    process.pfShyftTupleElectrons
    )


process.MessageLogger.cerr.FwkReport.reportEvery = 1000


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("shyft_ultraslim.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_pfShyftProducer_*_*',
                                                                      'keep *_pfShyftTuple*_*_*',
                                                                      'keep *_kinFitTtSemiLepEvent_*_*'
                                                                      ) 
                               )
process.outpath = cms.EndPath(process.out)

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.out.dropMetaData = cms.untracked.string("DROPPED")
