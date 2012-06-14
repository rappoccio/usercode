import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList


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
    # get JSON file correctly parced
    JSONfile = 'Cert_132440-144114_7TeV_StreamExpress_Collisions10_JSON_v2.txt'
    myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


inputSampleName = options.sampleNameInput

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/InclusiveMu15/shyft_38xOn35x_v1/91f2fc34c53b68691c104fb43fa3e9f4/shyft_382_mc_1_1_rw3.root'
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v2/b8014e49c41bd22a9b4664626194b599/shyft_382_mc_1_1_fU1.root'
                                    )
                                )
else :
    filelist = open( options.inputFiles[0], 'r' )
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    filelist.readlines()
                                    )
                                )

if inputDoMC == False :
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

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
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),                                        
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
                                        jetAlgo = cms.string("pf"),                                        
                                        )                                    
                                    )

process.pfShyftAnaReweightedUnity = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted, unity'),
        simpleSFCalc = cms.bool(True),                                                       
        bcEffScale = cms.double(1.0),
        lfEffScale = cms.double(1.0),        
        )
    )


process.pfShyftAnaReweighted = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        bcEffScale = cms.double(0.88),
        lfEffScale = cms.double(0.87),        
        )
    )



process.p = cms.Path(
    process.pfShyftAna*
    process.pfShyftAnaReweightedUnity*
    process.pfShyftAnaReweighted
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
