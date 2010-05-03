import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt100to250-madgraph/shyft_35x_v1/7d6b33b2c5d85d3512a9f559ea910755/multijets_1_1.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

from Analysis.JetAnalysis.multijetStudies_cfi import jetStudies as inputJetStudies
from Analysis.JetAnalysis.multijetStudies_cfi import pfJetStudies as inputPFJetStudies

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector as inputPFJetIDSelector
from PhysicsTools.SelectorUtils.jetIDSelector_cfi import jetIDSelector as inputJetIDSelector

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("multijetStudies.root")
                                   )


process.multijetAna = cms.EDAnalyzer('EDMultijetAnalysis',
                                     pfJetIDSelector = inputPFJetIDSelector.clone(),
                                     jetIDSelector = inputJetIDSelector.clone(),
                                     jetStudies = inputJetStudies.clone(ptMin = cms.double(50.0)),
                                     pfJetStudies = inputPFJetStudies.clone(ptMin = cms.double(50.0)),
                                     plotParameters = cms.PSet ( doTracks = cms.bool(False),
                                                                 useMC = cms.bool(False)
                                                                 )
                                     )


process.p = cms.Path(
    process.multijetAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
