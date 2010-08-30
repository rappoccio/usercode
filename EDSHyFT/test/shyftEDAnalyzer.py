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

options.register ('useFlavorHistory',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Flavor History Mode")

options.register ('doMC',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use MC truth")

options.register('sampleNameInput',
                 'top',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.parseArguments()

print options

import sys

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False

if options.doMC > 0 :
    inputDoMC = True
else :
    inputDoMC = False

inputSampleName = options.sampleNameInput

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v1/91f2fc34c53b68691c104fb43fa3e9f4/shyft_382_mc_1_1_qow.root'
    )
)
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies.root")
                                   )


process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                        jetClonesSrc = cms.InputTag('goodPFJets'),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(1),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        useJetClones = cms.bool(False)
                                        )                                    
                                    )

process.jptShyftAna = cms.EDAnalyzer('EDSHyFT',
                                     shyftAnalysis = inputShyftAnalysis.clone(
                                         metSrc = cms.InputTag('patMETsTC'),
                                         jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),                                         
                                         jetClonesSrc = cms.InputTag('goodJPTJets'),
                                         jetPtMin = cms.double(25.0),
                                         minJets = cms.int32(1),
                                         heavyFlavour = cms.bool( useFlavorHistory ),
                                         doMC = cms.bool( inputDoMC),
                                         sampleName = cms.string(inputSampleName),
                                         useJetClones = cms.bool(False)
                                        )
                                     
                                     )

process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                      shyftAnalysis = inputShyftAnalysis.clone(
                                          jetClonesSrc = cms.InputTag('goodCaloJets'),
                                          jetPtMin = cms.double(30.0),
                                          minJets = cms.int32(1),
                                          heavyFlavour = cms.bool( useFlavorHistory ),
                                          doMC = cms.bool( inputDoMC),
                                          sampleName = cms.string(inputSampleName),
                                          useJetClones = cms.bool(False),
                                          btaggerString = cms.string('simpleSecondaryVertexBJetTags')
                                          )                                      
                                      )


process.p = cms.Path(
    #process.pfShyftAna*process.jptShyftAna*process.caloShyftAna
    process.jptShyftAna
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
