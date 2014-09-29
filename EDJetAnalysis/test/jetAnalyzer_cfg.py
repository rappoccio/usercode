import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V12::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

## import CondCore.DBCommon.CondDBCommon_cfi
## process.l1GtTriggerMenu = cms.ESSource( "PoolDBESSource"
## , CondCore.DBCommon.CondDBCommon_cfi.CondDBCommon
## , toGet   = cms.VPSet(
##     cms.PSet(
##         record  = cms.string( 'L1GtTriggerMenuRcd' ),
##         tag     = cms.string( 'L1GtStableParameters_CRAFT09_hlt' )  # L1 menu for Fall10 REDIGI (CMSSW_3_8_7)
##     )
##   )
## )
## process.preferL1GtTriggerMenu = cms.ESPrefer( "PoolDBESSource", "l1GtTriggerMenu" )


import FWCore.PythonUtilities.LumiList as LumiList

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.register ('doBinPtTrig',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Bin the data in HLT paths by pt")

options.register ('semimuTriggers',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use the semimuonic triggers")

options.parseArguments()

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# get JSON file correctly parced
JSONfile = 'Cert_160404-163869_7TeV_PromptReco_Collisions11_JSON.txt'
myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


if options.useData :
    histFileName = 'jetStudiesJet2011A.root'
    jecLevels = [ 'Jec11_V1_AK5PFchs_L1FastJet.txt',
                  'Jec11_V1_AK5PFchs_L2Relative.txt',
                  'Jec11_V1_AK5PFchs_L3Absolute.txt',
                  'Jec10V1_Uncertainty_AK5PF.txt']

    print 'Processing these JEC: '
    print jecLevels
    ## Source
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/lpctlbsm/srappocc/Jet/ttbsm_v6_Run2011-May10ReReco/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_26_0_4mM.root'
        ),
        lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )
    )
else :
    histFileName = 'jetStudiesQCDFlat.root'
    jecLevels = [ 'Jec11_V1_AK5PFchs_L1FastJet.txt',
                  'Jec11_V1_AK5PFchs_L2Relative.txt',
                  'Jec11_V1_AK5PFchs_L3Absolute.txt',
                  'Jec10V1_Uncertainty_AK5PF.txt']
   
    ## Source
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt-15to3000_TuneZ2_Flat_7TeV_pythia6/ttbsm_v6_Summer11-PU_S3_-START42_V11-v2/83fc13450c5d7926fa1f909d95a68741/ttbsm_42x_mc_62_1_BvN.root'

        )
    )    
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from Analysis.JetAnalysis.jetStudies2011_cfi import jetStudies2011 as jetStudies2011

from PhysicsTools.SelectorUtils.pfMuonSelector_cfi import pfMuonSelector

if options.semimuTriggers :
    itrigs = cms.vstring( ['HLT_Mu24_v1' ] )
else :
    itrigs = jetStudies2011.trigs

print 'Talking to tfileservice'
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(histFileName)
                                   )

print 'Making analyzers'

process.ak5Analyzer = cms.EDAnalyzer('EDJetStudies2011',
                                     jetStudies2011.clone(
                                         binPtTrig = cms.bool( options.doBinPtTrig == 1 ),
                                         trigs = itrigs,
                                         jecPayloads = cms.vstring( jecLevels )
                                         )
                                     )

process.ca8Analyzer = cms.EDAnalyzer('EDJetStudies2011',
                                     jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCA8PF'),
                                                           useCA8GenJets = cms.bool(True),
                                                           binPtTrig = cms.bool( options.doBinPtTrig == 1 ),
                                                           trigs = itrigs,
                                                           jecPayloads = cms.vstring( jecLevels )
                                                           )
                                     )

process.ca8PrunedAnalyzer = cms.EDAnalyzer('EDJetStudies2011',
                                           jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                                                 useCA8BasicJets = cms.bool(True),
                                                                 genJetsSrc = cms.InputTag('caPrunedGen', ''),
                                                                 binPtTrig = cms.bool( options.doBinPtTrig == 1 ),
                                                                 trigs = itrigs,
                                                                 jecPayloads = cms.vstring( jecLevels )
                                                                 )
                                           )

process.ca8PrunedAnalyzerBTagSearch = cms.EDAnalyzer('EDJetStudies2011',
                                                     jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                                                           useCA8GenJets = cms.bool(True),
                                                                           useBTags = cms.bool(True),
                                                                           orderByMass =cms.bool(True),
                                                                           trigs = itrigs,
                                                                           jecPayloads = cms.vstring( jecLevels ),
                                                                           muonSrc = cms.InputTag('selectedPatMuonsLoosePFlow'),
                                                                           rCut = cms.double(0.8),
                                                                           muonInJetSelector = pfMuonSelector.clone(
                                                                               cutsToIgnore = cms.vstring(['PFIso', 'D0'])
                                                                               )
                                                                           )
                                                     )

process.ca8PrunedAnalyzerBTagMuSearch = cms.EDAnalyzer('EDJetStudies2011',
                                                     jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCA8PrunedPF'),
                                                                           useCA8GenJets = cms.bool(True),
                                                                           useBTags = cms.bool(True),
                                                                           orderByMass = cms.bool(True),
                                                                           trigs = cms.vstring([
                                                                               'HLT_Mu24_v1'
                                                                               ]),
                                                                           jecPayloads = cms.vstring( jecLevels ),
                                                                           muonSrc = cms.InputTag('selectedPatMuonsLoosePFlow'),
                                                                           rCut = cms.double(0.8),
                                                                           muonInJetSelector = pfMuonSelector.clone(
                                                                               cutsToIgnore = cms.vstring(['PFIso', 'D0'])
                                                                               )
                                                                           )
                                                     )


process.ca8TopTagAnalyzer = cms.EDAnalyzer('EDJetStudies2011',
                                           jetStudies2011.clone( jetSrc = cms.InputTag('goodPatJetsCATopTagPF'),
                                                                 useCA8GenJets = cms.bool(True),
                                                                 binPtTrig = cms.bool( options.doBinPtTrig == 1 ),
                                                                 trigs = itrigs,
                                                                 jecPayloads = cms.vstring( jecLevels )
                                                                 )
                                           )

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

#process.patTrigger.addL1Algos = False

print 'Making the path'
process.p = cms.Path(
    process.patTriggerDefaultSequence*
    process.ak5Analyzer*
    process.ca8Analyzer*
    process.ca8PrunedAnalyzer*
    process.ca8TopTagAnalyzer*
    process.ca8PrunedAnalyzerBTagSearch*
    process.ca8PrunedAnalyzerBTagMuSearch
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.MessageLogger.suppressWarning.append('patTrigger')
