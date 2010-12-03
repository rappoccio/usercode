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
#                                    'file:/uscms_data/d2/rappocc/analysis/SHyFT/CMSSW_3_8_3_SHyFT/src/Analysis/EDSHyFT/test/syncex_shyft_382_mc.root'
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/InclusiveMu15/shyft_38xOn35x_v1/91f2fc34c53b68691c104fb43fa3e9f4/shyft_382_mc_1_1_rw3.root'
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v2/b8014e49c41bd22a9b4664626194b599/shyft_382_mc_1_1_fU1.root'
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_100_1_DBn.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_101_1_Lpm.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_102_1_goD.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_103_1_fHI.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_104_1_GLp.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_10_1_rr9.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_11_1_rXZ.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_12_1_TUg.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_13_1_4GA.root',
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/WJets-madgraph/shyft_38xOn35x_v5/c0e35ba6e48486ab759b591ebe1227c6/shyft_382_mc_14_1_HVv.root',


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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(3000) )

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
                                        reweightBTagEff = cms.bool(True),
                                        useCustomPayload = cms.bool(True),
                                        bcEffScale = cms.double(1.00),
                                        lfEffScale = cms.double(0.87),
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
                                         reweightBTagEff = cms.bool(True),
                                         useCustomPayload = cms.bool(True),
                                         bcEffScale = cms.double(1.00),
                                         lfEffScale = cms.double(0.87),                                         
                                        )
                                     
                                     )




process.pfShyftAnaMC = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF MC'),
        simpleSFCalc = cms.bool(False),
        reweightBTagEff = cms.bool(False),
        useCustomPayload = cms.bool(False),  
        )
    )

process.pfShyftAnaReweightedUnity = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted, unity'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                      
        bcEffScale = cms.double(1.00),
        lfEffScale = cms.double(1.00),        
        )
    )

process.pfShyftAnaReweightedBTag080 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 080'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                   
        bcEffScale = cms.double(0.80),
        lfEffScale = cms.double(0.87),        
        )
    )

process.pfShyftAnaReweightedBTag090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 090'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),
        bcEffScale = cms.double(0.90),
        lfEffScale = cms.double(0.87),        
        )
    )


process.pfShyftAnaReweightedBTag110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 110'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        bcEffScale = cms.double(1.10),
        lfEffScale = cms.double(0.87),        
        )
    )

process.pfShyftAnaReweightedBTag120 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 120'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        bcEffScale = cms.double(1.20),
        lfEffScale = cms.double(0.87),        
        )
    )







process.pfShyftAnaReweightedLFTag074 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 074'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        lfEffScale = cms.double(0.74),
        bcEffScale = cms.double(1.00),        
        )
    )

process.pfShyftAnaReweightedLFTag080 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 080'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        lfEffScale = cms.double(0.80),
        bcEffScale = cms.double(1.00),        
        )
    )


process.pfShyftAnaReweightedLFTag094 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 094'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                    
        lfEffScale = cms.double(0.94),
        bcEffScale = cms.double(1.00),        
        )
    )

process.pfShyftAnaReweightedLFTag100 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 100'),
        reweightBTagEff = cms.bool(True),
        useCustomPayload = cms.bool(True),                                                       
        lfEffScale = cms.double(1.00),
        bcEffScale = cms.double(1.00),        
        )
    )


# JES up and down with MET Cut

process.pfShyftAnaJES095 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('PFJES095')
        )
    )

process.pfShyftAnaJES105 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
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
process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF No MET'),
        metMin = cms.double(0.0)
        )
    )


process.jptShyftAnaNoMET = process.jptShyftAna.clone(
    shyftAnalysis = process.jptShyftAna.shyftAnalysis.clone(
        identifier = cms.string('JPT No MET'),
        metMin = cms.double(0.0)
        )
    )

process.pfShyftAnaJES095NoMET = process.pfShyftAnaNoMET.clone(
    shyftAnalysis = process.pfShyftAnaNoMET.shyftAnalysis.clone(
        jetScale = cms.double(0.95),
        identifier = cms.string('PFJES095')
        )
    )

process.pfShyftAnaJES105NoMET = process.pfShyftAnaNoMET.clone(
    shyftAnalysis = process.pfShyftAnaNoMET.shyftAnalysis.clone(
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
    process.jptShyftAna*
    process.pfShyftAnaJES095*    
    process.pfShyftAnaJES105*
    process.jptShyftAnaJES095*    
    process.jptShyftAnaJES105*
    process.pfShyftAnaNoMET*
    process.jptShyftAnaNoMET*
    process.pfShyftAnaJES095NoMET*    
    process.pfShyftAnaJES105NoMET*
    process.jptShyftAnaJES095NoMET*    
    process.jptShyftAnaJES105NoMET*    
    process.pfShyftAnaReweightedUnity*
    process.pfShyftAnaReweightedBTag080*
    process.pfShyftAnaReweightedBTag090*
    process.pfShyftAnaReweightedBTag110*
    process.pfShyftAnaReweightedBTag120*
    process.pfShyftAnaReweightedLFTag074*
    process.pfShyftAnaReweightedLFTag080*
    process.pfShyftAnaReweightedLFTag094*
    process.pfShyftAnaReweightedLFTag100*
    process.pfShyftAnaMC

    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
