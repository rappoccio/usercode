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

inputDoMC=True

inputSampleName = options.sampleNameInput

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'file:shyft_mc.root'
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/InclusiveMu15/shyft_38xOn35x_v1/91f2fc34c53b68691c104fb43fa3e9f4/shyft_382_mc_1_1_rw3.root'
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v2/b8014e49c41bd22a9b4664626194b599/shyft_382_mc_1_1_fU1.root'
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
										#useAntiSelection = cms.bool(False),
										#eleTrig = cms.string('HLT_Ele10_LW_L1R'),
										#useEleMC = cms.bool(True) ,
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),                                        
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PFlow'),
                                        jetAlgo = cms.string("pf"),
                                        simpleSFCalc = cms.bool(True),                                                       
                                        bcEffScale = cms.double(0.88),
                                        lfEffScale = cms.double(0.87),
                                        )                                    
                                    )

process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PFlow No MET'),
        metMin = cms.double(0.0)
        )
    )


process.pfRecoShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuons'),
                                        electronSrc = cms.InputTag('selectedPatElectrons'),
                                        metSrc = cms.InputTag('patMETsPF'),
                                        jetSrc = cms.InputTag('selectedPatJetsAK5PF'),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
										jetAlgo = cms.string("pf"),
                                        simpleSFCalc = cms.bool(True),                                                       
                                        bcEffScale = cms.double(0.88),
                                        lfEffScale = cms.double(0.87),
                                        )                                    
                                    )

process.pfRecoShyftAnaNoMET = process.pfRecoShyftAna.clone(
    shyftAnalysis=process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('PF no MET')
        )
    )

process.jptShyftAna = cms.EDAnalyzer('EDSHyFT',
                                     shyftAnalysis = inputShyftAnalysis.clone(
                                         metSrc = cms.InputTag('patMETsTC'),
                                         jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),                                         
                                         jetPtMin = cms.double(30.0),
                                         metMin = cms.double(20.0),
                                         minJets = cms.int32(5),
                                         heavyFlavour = cms.bool( useFlavorHistory ),
                                         doMC = cms.bool( inputDoMC),
                                         sampleName = cms.string(inputSampleName),
                                         identifier = cms.string('JPT'),
                                         jetAlgo = cms.string("jpt"),
                                         simpleSFCalc = cms.bool(True),                                                  
                                         bcEffScale = cms.double(0.88),
                                         lfEffScale = cms.double(0.87),                                         
                                        )
                                     
                                     )


process.jptShyftAnaNoMET = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        identifier = cms.string('JPT No MET'),
        metMin = cms.double(0.0)
        )
    )


if inputDoMC :
    caloBTag = 'simpleSecondaryVertexBJetTags'
else :
    caloBTag = 'simpleSecondaryVertexHighEffBJetTags'

process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                      shyftAnalysis = inputShyftAnalysis.clone(
	                                      jetPtMin = cms.double(30.0),
                                          metMin = cms.double(30.0),
                                          minJets = cms.int32(5),
                                          heavyFlavour = cms.bool( useFlavorHistory ),
                                          doMC = cms.bool( inputDoMC),
                                          sampleName = cms.string(inputSampleName),
                                          btaggerString = cms.string(caloBTag),
                                          identifier = cms.string('CALO'),
										  simpleSFCalc = cms.bool(True),                                                  
										  bcEffScale = cms.double(0.88),
										  lfEffScale = cms.double(0.87),
                                          )                                      
                                      )


process.caloShyftAnaNoMET = process.caloShyftAna.clone(
    shyftAnalysis=process.caloShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('CALO no MET')
        )
    )


process.pfRecoShyftAnaMC = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF MC'),
        simpleSFCalc = cms.bool(False)
        )
    )

process.pfRecoShyftAnaReweightedUnity = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted, unity'),
        simpleSFCalc = cms.bool(True),                                                       
        bcEffScale = cms.double(1.0),
        lfEffScale = cms.double(1.0),        
        )
    )

process.pfRecoShyftAnaReweightedBTag076 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        bcEffScale = cms.double(0.76),
        lfEffScale = cms.double(0.87),        
        )
    )

process.pfRecoShyftAnaReweightedBTag082 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        bcEffScale = cms.double(0.82),
        lfEffScale = cms.double(0.87),        
        )
    )


process.pfRecoShyftAnaReweightedBTag094 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        bcEffScale = cms.double(0.94),
        lfEffScale = cms.double(0.87),        
        )
    )

process.pfRecoShyftAnaReweightedBTag100 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        bcEffScale = cms.double(1.00),
        lfEffScale = cms.double(0.87),        
        )
    )


process.pfRecoShyftAnaReweightedLFTag074 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        lfEffScale = cms.double(0.74),
        bcEffScale = cms.double(0.88),        
        )
    )

process.pfRecoShyftAnaReweightedLFTag080 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        lfEffScale = cms.double(0.80),
        bcEffScale = cms.double(0.88),        
        )
    )


process.pfRecoShyftAnaReweightedLFTag094 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        lfEffScale = cms.double(0.94),
        bcEffScale = cms.double(0.88),        
        )
    )

process.pfRecoShyftAnaReweightedLFTag100 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted'),
        simpleSFCalc = cms.bool(True),                                                       
        lfEffScale = cms.double(1.00),
        bcEffScale = cms.double(0.88),        
        )
    )


# JES up and down with MET Cut

process.pfRecoShyftAnaJES095 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('PFJES095')
        )
    )

process.pfRecoShyftAnaJES105 = process.pfRecoShyftAna.clone(
    shyftAnalysis = process.pfRecoShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('PFJES105')
        )
    )

process.jptShyftAnaJES095 = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('JPTJES095')
        )
    )

process.jptShyftAnaJES105 = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('JPTJES105')
        )
    )




# Nominal, JES up and down without MET Cut

process.pfRecoShyftAnaJES095NoMET = process.pfRecoShyftAnaNoMET.clone(
    shyftAnalysis = process.pfRecoShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('PFJES095')
        )
    )

process.pfRecoShyftAnaJES105NoMET = process.pfRecoShyftAnaNoMET.clone(
    shyftAnalysis = process.pfRecoShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('PFJES105')
        )
    )

process.jptShyftAnaJES095NoMET = process.jptShyftAnaNoMET.clone(
    shyftAnalysis = process.jptShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('JPTJES095')
        )
    )

process.jptShyftAnaJES105NoMET = process.jptShyftAnaNoMET.clone(
    shyftAnalysis = process.jptShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(1.05),
        identifier = cms.string('JPTJES105')
        )
    )




process.p = cms.Path(
    process.pfShyftAna*
    process.pfShyftAnaNoMET*
	process.pfRecoShyftAna*
	process.pfRecoShyftAnaNoMET*
    process.jptShyftAna*
	process.jptShyftAnaNoMET*
	process.caloShyftAna*
	process.caloShyftAnaNoMET

    #process.pfRecoShyftAnaJES095*    
    #process.pfRecoShyftAnaJES105*
    #process.jptShyftAnaJES095*    
    #process.jptShyftAnaJES105*   
    #process.pfRecoShyftAnaJES095NoMET*    
    #process.pfRecoShyftAnaJES105NoMET*
    #process.jptShyftAnaJES095NoMET*    
    #process.jptShyftAnaJES105NoMET*    
    #process.pfRecoShyftAnaReweightedUnity*
    #process.pfRecoShyftAnaReweightedBTag076*
    #process.pfRecoShyftAnaReweightedBTag082*
    #process.pfRecoShyftAnaReweightedBTag094*
    #process.pfRecoShyftAnaReweightedBTag100*
    #process.pfRecoShyftAnaReweightedLFTag074*
    #process.pfRecoShyftAnaReweightedLFTag080*
    #process.pfRecoShyftAnaReweightedLFTag094*
    #process.pfRecoShyftAnaReweightedLFTag100*
    #process.pfRecoShyftAnaMC

    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
