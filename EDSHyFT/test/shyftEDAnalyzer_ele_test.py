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

options.register ('sampleNameInput',
                  'top',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Sample name to give histograms")

options.register ('outputRootFile',
                  'shyftStudies.root',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Output root file name")

options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('triggerName',
                 'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v2',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Electron trigger to run")

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
    JSONfile = 'Cert_160404-163369_7TeV_PromptReco_Collisions11_JSON.txt'
    myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_9_1_drw.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_96_1_0fn.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_95_1_JQ3.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_94_1_58x.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_93_1_2Y9.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_92_1_ezw.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_91_1_iUf.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_90_1_JGA.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_8_1_d1I.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_89_1_eod.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_88_1_zha.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_87_1_odL.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_86_1_jGO.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_85_1_kNr.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_84_1_mnY.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_83_1_LnL.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_82_1_9tr.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_81_1_1f1.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_80_1_tyX.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_7_1_JR7.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_79_1_RRB.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_78_1_0Cw.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_77_1_mBd.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_76_1_WRY.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_75_1_svK.root',
                                '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_74_1_7zu.root',
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
#Det iso <0.1 with WP70 (default)
process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
                                        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
                                        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
                                        metSrc = cms.InputTag('patMETsPFlow'),
                                        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
                                        ePlusJets = cms.bool( True ),
                                        muPlusJets = cms.bool( False ),
                                        eleTrig = cms.string(options.triggerName),	
                                        useEleMC = cms.bool(False),
                                        useAntiSelection = cms.bool(False),
                                        jetPtMin = cms.double(25.0),##
                                        minJets = cms.int32(5),
                                        metMin = cms.double(20.0),
                                        useData = cms.bool( not inputDoMC ),
                                        heavyFlavour = cms.bool( useFlavorHistory ),
                                        doMC = cms.bool( inputDoMC),
                                        sampleName = cms.string(inputSampleName),
                                        identifier = cms.string('PF'),
                                        usePFIso = cms.bool(False),
                                        cutsToIgnore=cms.vstring(inputCutsToIgnore)
                                        )                                    
                                    )

process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    identifier = cms.string('PF no MET')
    )
    )

#switch to PF iso < 0.1 with WP70
process.pfShyftAnaPFIso = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    identifier = cms.string('PF Iso')
    )
    )

process.pfShyftAnaNoMETPFIso = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    metMin = cms.double(0.0),
    identifier = cms.string('PF Iso, no MET')
    )
    )

#relax PF iso < 0.15 with WP70
process.pfShyftAnaPFIso15WP70 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF Iso')
    )
    )

process.pfShyftAnaNoMETPFIso15WP70 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    metMin = cms.double(0.0),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF Iso, no MET')
    )
    )

#relax pfiso < 0.2 with WP70
process.pfShyftAnaPFIso20WP70 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    eRelIso = cms.double(0.20),
    identifier = cms.string('PF Iso')
    )
    )

process.pfShyftAnaNoMETPFIso20WP70 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    metMin = cms.double(0.0),
    eRelIso = cms.double(0.20),
    identifier = cms.string('PF Iso, no MET')
    )
    )

#switch to PF iso < 0.1 with WP80
process.pfShyftAnaPFIso10WP80 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    useWP80Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    identifier = cms.string('PF Iso')
    )
    )

process.pfShyftAnaNoMETPFIso10WP80 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    useWP80Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    metMin = cms.double(0.0),
    identifier = cms.string('PF Iso, no MET')
    )
    )
#relax pfiso < 0.15 with WP80
process.pfShyftAnaPFIso15WP80 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    useWP80Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF Iso')
    )
    )

process.pfShyftAnaNoMETPFIso15WP80 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    usePFIso = cms.bool(True),
    useWP80Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    metMin = cms.double(0.0),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF Iso, no MET')
    )
    )


process.p = cms.Path(
    process.pfShyftAna*
    process.pfShyftAnaNoMET*              
    process.pfShyftAnaPFIso*
    process.pfShyftAnaNoMETPFIso*
    process.pfShyftAnaPFIso15WP70*
    process.pfShyftAnaNoMETPFIso15WP70*
    process.pfShyftAnaPFIso20WP70*
    process.pfShyftAnaNoMETPFIso20WP70*
    process.pfShyftAnaPFIso10WP80*
    process.pfShyftAnaNoMETPFIso10WP80*
    process.pfShyftAnaPFIso15WP80*
    process.pfShyftAnaNoMETPFIso15WP80 
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 100
