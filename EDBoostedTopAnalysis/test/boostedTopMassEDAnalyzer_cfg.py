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
JSONfile = 'Cert_161079-161352_7TeV_PromptReco_Collisions11_JSON_noESpbl_v2.txt'
myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


if options.useData :
    histFileName = 'wPlusBJetPlotsSingleMu.root'
    
    ## Source
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(  
 'dcap:///pnfs/cms/WAX/11/store/user/rappocc/SingleMu/ttbsm_v1_Run2011A-PromptReco-v1/3dc70b6acc7a164ec5660c65e5f36a85/ttbsm_413_17_1_ACA.root'                 
        ),
        lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )
    )
else :
    histFileName = 'wPlusBJetPlotsTTJets.root'
    ## Source
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTJets_TuneZ2_7TeV-madgraph-tauola/ttbsm_v1_Spring11-PU_S1_START311_V1G1-v1/3900271fc94df2539ec6b7c2deffc3db/ttbsm_413_1_1_7nH.root',
        )
    )    
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Analysis.BoostedTopAnalysis.boostedTopMassAnalysis_cfi import boostedTopMassAnalysis


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(histFileName)
                                   )

process.ca8PrunedAnalyzer = cms.EDAnalyzer('EDBoostedTopMassAnalysis',
                                           boostedTopMassAnalysis.clone(
                                               shyftSelection = cms.PSet( boostedTopMassAnalysis.shyftSelection.clone(
                                                   jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),                                                   
                                                   ) )
                                               )
                                           )


process.p = cms.Path(
    process.ca8PrunedAnalyzer
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
