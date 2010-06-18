import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/ttbsm_361_v1/a5033698d5913844267be726de0ea95f/ttbsm_361_10_1.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

from Analysis.BoostedTopAnalysis.hadronicAnalysis_cfi import hadronicAnalysis as inputHadronicAnalysis




process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("boostedTopHadronicStudies_pt_gt50.root")
                                   )


process.hadronicAna = cms.EDAnalyzer('EDHadronicAnalysis',
                                  hadronicAnalysis = inputHadronicAnalysis.clone()
                                     )
process.hadronicAna.hadronicAnalysis.dijetSelectorParams.ptMin = cms.double(50.0) 

#process.hadronicAna.hadronicAnalysis.dijetSelectorParams.cutsToIgnore = cms.vstring(['Calo Jet ID', 'PF Jet ID'])
process.hadronicAna.hadronicAnalysis.cutsToIgnore = cms.vstring(['Trigger'])


process.hadronicAnaUnweighted = process.hadronicAna.clone( )

process.hadronicAna.plotOptions = cms.PSet(
    plotTracks = cms.bool(True),
    reweightHistoFile = cms.string('reweight_histo.root'),
    reweightHistoName = cms.string('ratio')
            )

process.hadronicAnaUnweighted.plotOptions = cms.PSet(
    plotTracks = cms.bool(True)
    )

process.p = cms.Path(
    process.hadronicAna*
    process.hadronicAnaUnweighted
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
