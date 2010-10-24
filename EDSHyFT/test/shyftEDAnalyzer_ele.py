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

options.register('outputRootFile',
                 'shyftStudies.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Output root file name")

options.register('useTrigger',
				 0,
				 VarParsing.multiplicity.singleton,
				 VarParsing.varType.int,
				 "Use trigger only for dats")
				 
options.register ('useRange135821to139980',
				  0,
				  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 135821-139980 for HLT_Ele10_LW_L1R")

options.register ('useRange140058to143962',
				  0,
				  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
				  "Selected run range 140058_143962 for HLT_Ele15_SW_L1R")

options.register ('useRange144010to146421',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Selected run range 144010_146421 for HLT_Ele15_SW_CaloEleId_L1R")

options.register ('useRange146428to147116',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Selected run range 146428_147116 for HLT_Ele17_SW_CaloEleId_L1R")

options.register ('useRange147196to148002',
				  0,
				  VarParsing.multiplicity.singleton,
				  VarParsing.varType.int,
				  "Selected run range 147196_148002 for HLT_Ele17_SW_TightEleId_L1R")

options.parseArguments()

print options

import sys

# require trigger only if data
useTrigger = options.useTrigger
# check triggers for different run era
useRange135821to139980 = options.useRange135821to139980
useRange140058to143962 = options.useRange140058to143962
useRange144010to146421 = options.useRange144010to146421
useRange146428to147116 = options.useRange146428to147116
useRange147196to148002 = options.useRange147196to148002

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False

if options.doMC > 0 :
    inputDoMC = True
else :
    inputDoMC = False
    # get JSON file correctly parced
    JSONfile = 'Cert_132440-147454_7TeV_StreamExpress_Collisions10_JSON.txt'
    myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


inputSampleName = options.sampleNameInput

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'file:shyft_mc.root'
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
                                   fileName = cms.string(options.outputRootFile)
                                   )

if useTrigger == True :
	useMC = False
	
	if useRange135821to139980 :
		triggerName = "HLT_Ele10_LW_L1R"
	elif useRange140058to143962 :
		triggerName = "HLT_Ele15_SW_L1R"
	elif useRange144010to146421 :
		triggerName = "HLT_Ele15_SW_CaloEleId_L1R"
	elif useRange146428to147116 :
		triggerName = "HLT_Ele17_SW_CaloEleId_L1R"
	elif useRange147196to148002 :
		triggerName = "HLT_Ele17_SW_TightEleId_L1R"
	else :
	    triggerName = "HLT_Ele10_LW_L1R"
	    useMC = True #protection, no trigger requirement then
		
else : #By default no trigger will be used in the selector if useMC == true
	triggerName = "HLT_Ele10_LW_L1R" 
        useMC = True

process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
										eleTrig = cms.string(triggerName),
										useEleMC = cms.bool(useMC),
										useAntiSelection = cms.bool(False),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PFlow')
                                        )                                    
                                    )


process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('PFlow no MET')
        )
    )


process.pfShyftAnaDataQCD = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
	    useAntiSelection = cms.bool(True),
        identifier = cms.string('PFlow QCD')     
        )
    )

process.pfShyftAnaNoMETDataQCD = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
	    useAntiSelection = cms.bool(True),
		metMin = cms.double(0.0),
        identifier = cms.string('PFlow QCD no MET')      
        )
    )


process.pfRecoShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuons'),
                                        electronSrc = cms.InputTag('selectedPatElectrons'),
                                        metSrc = cms.InputTag('patMETsPF'),
                                        jetSrc = cms.InputTag('selectedPatJetsAK5PF'),
										eleTrig = cms.string(triggerName),	
										useEleMC = cms.bool(useMC),
										useAntiSelection = cms.bool(False),
                                        jetPtMin = cms.double(25.0),
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF')
                                        )                                    
                                    )

process.pfRecoShyftAnaNoMET = process.pfRecoShyftAna.clone(
    shyftAnalysis=process.pfRecoShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('PF no MET')
        )
    )


process.pfRecoShyftAnaDataQCD = process.pfRecoShyftAna.clone(
    shyftAnalysis=process.pfRecoShyftAna.shyftAnalysis.clone(
	    useAntiSelection = cms.bool(True),
        identifier = cms.string('PF QCD')     
        )
    )

process.pfRecoShyftAnaNoMETDataQCD = process.pfRecoShyftAna.clone(
    shyftAnalysis=process.pfRecoShyftAna.shyftAnalysis.clone(
	    useAntiSelection = cms.bool(True),
		metMin = cms.double(0.0),
        identifier = cms.string('PF QCD no MET')      
        )
    )



process.jptShyftAna = cms.EDAnalyzer('EDSHyFT',
                                     shyftAnalysis = inputShyftAnalysis.clone(
                                         metSrc = cms.InputTag('patMETsTC'),
                                         jetSrc = cms.InputTag('selectedPatJetsAK5JPT'),
										 eleTrig = cms.string(triggerName),
										 useEleMC = cms.bool(useMC),
										 useAntiSelection = cms.bool(False),
                                         jetPtMin = cms.double(30.0),
                                         metMin = cms.double(20.0),
                                         minJets = cms.int32(5),
                                         heavyFlavour = cms.bool( useFlavorHistory ),
                                         doMC = cms.bool( inputDoMC),
                                         sampleName = cms.string(inputSampleName),
                                         identifier = cms.string('JPT')
                                        )
                                     
                                     )


process.jptShyftAnaNoMET = process.jptShyftAna.clone(
    shyftAnalysis=process.jptShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('JPT no MET')
        )
    )

process.jptShyftAnaDataQCD = process.jptShyftAna.clone(
    shyftAnalysis=process.jptShyftAna.shyftAnalysis.clone(
	    useAntiSelection = cms.bool(True),
        identifier = cms.string('JPT QCD')     
        )
    )

process.jptShyftAnaNoMETDataQCD = process.jptShyftAna.clone(
    shyftAnalysis=process.jptShyftAna.shyftAnalysis.clone(
	    useAntiSelection = cms.bool(True),
		metMin = cms.double(0.0),
        identifier = cms.string('JPT QCD no MET')      
        )
    )


if inputDoMC :
    caloBTag = 'simpleSecondaryVertexBJetTags'
else :
    caloBTag = 'simpleSecondaryVertexHighEffBJetTags'

process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                      shyftAnalysis = inputShyftAnalysis.clone(
	                                      eleTrig = cms.string(triggerName),
										  useEleMC = cms.bool(False),
										  useAntiSelection = cms.bool(False),
                                          jetPtMin = cms.double(30.0),
                                          metMin = cms.double(30.0),
                                          minJets = cms.int32(5),
                                          heavyFlavour = cms.bool( useFlavorHistory ),
                                          doMC = cms.bool( inputDoMC),
                                          sampleName = cms.string(inputSampleName),
                                          btaggerString = cms.string(caloBTag),
                                          identifier = cms.string('CALO')
                                          )                                      
                                      )


process.caloShyftAnaNoMET = process.caloShyftAna.clone(
    shyftAnalysis=process.caloShyftAna.shyftAnalysis.clone(
        metMin = cms.double(0.0),
        identifier = cms.string('CALO no MET')
        )
    )

process.caloShyftAnaDataQCD = process.caloShyftAna.clone(
    shyftAnalysis=process.caloShyftAna.shyftAnalysis.clone(
	    useAntiSelection = cms.bool(True),
        identifier = cms.string('CALO QCD')     
        )
    )

process.caloShyftAnaNoMETDataQCD = process.caloShyftAna.clone(
    shyftAnalysis=process.caloShyftAna.shyftAnalysis.clone(
	    useAntiSelection = cms.bool(True),
		metMin = cms.double(0.0),
        identifier = cms.string('CALO QCD no MET')      
        )
    )

process.p = cms.Path(
    process.pfShyftAna*
    process.pfShyftAnaNoMET*
    process.pfShyftAnaDataQCD*
    process.pfShyftAnaNoMETDataQCD*
    process.pfRecoShyftAna*
    process.pfRecoShyftAnaNoMET*
    process.pfRecoShyftAnaDataQCD*
    process.pfRecoShyftAnaNoMETDataQCD*
    process.jptShyftAna*
    process.jptShyftAnaNoMET*
    process.jptShyftAnaDataQCD*
	process.jptShyftAnaNoMETDataQCD*
    process.caloShyftAna*
    process.caloShyftAnaNoMET*
	process.caloShyftAnaDataQCD*
	process.caloShyftAnaNoMETDataQCD
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
