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
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('triggerName',
                 'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Electron trigger to run")

options.register('ttbsmPAT',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "If running on ttbsm PAT tuples"
                 )
options.register('use42X',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "PAT tuplese done in 4_2_2"
                 )

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
    JSONfile = 'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON.txt'
    myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0  and options.ttbsmPAT > 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/lpctlbsm/srappocc/SingleElectron/ttbsm_v6_Run2011-May10ReReco/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_9_1_fbP.root',
        '/store/user/lpctlbsm/srappocc/SingleElectron/ttbsm_v6_Run2011-May10ReReco/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_99_0_fMQ.root',
        '/store/user/lpctlbsm/srappocc/SingleElectron/ttbsm_v6_Run2011-May10ReReco/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_98_0_CMU.root',
        '/store/user/lpctlbsm/srappocc/SingleElectron/ttbsm_v6_Run2011-May10ReReco/7e150b77ce1bf887c7a9afa63377fb1c/ttbsm_42x_data_97_0_87b.root',
        )
                                )
    
elif len(options.inputFiles) == 0  and options.ttbsmPAT == 0 and not options.use42X :  
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


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V12::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')


from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputRootFile)
                                   )
if options.ttbsmPAT > 0 and options.use42X > 0:
    process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                        shyftAnalysis = inputShyftAnalysis.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        ePlusJets = cms.bool( True ),
        muPlusJets = cms.bool( False ),
        eleTrig = cms.string(options.triggerName),	
        useEleMC = cms.bool(False),
        useAntiSelection = cms.bool(False),
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(5),
        metMin = cms.double(20.0),
        useData = cms.bool( not inputDoMC ),
        heavyFlavour = cms.bool( useFlavorHistory ),
        doMC = cms.bool( inputDoMC),
        sampleName = cms.string(inputSampleName),
        identifier = cms.string('PF'),
        cutsToIgnore=cms.vstring(inputCutsToIgnore),
        
        pvSelector = cms.PSet(
        pvSrc = cms.InputTag('goodOfflinePrimaryVertices'),
        minNdof = cms.double(4.0),
        maxZ = cms.double(15.0),
        maxRho = cms.double(2.0)
        ),
        
        muonIdTight = cms.PSet(
        version = cms.string('FALL10'),
        Chi2 = cms.double(10.0),
        D0 = cms.double(0.02),
        ED0 = cms.double(999.0),
        SD0 = cms.double(999.0),
        NHits = cms.int32(11),
        NValMuHits = cms.int32(0),
        ECalVeto = cms.double(999.0),
        HCalVeto = cms.double(999.0),
        RelIso = cms.double(0.05),
        LepZ = cms.double(1.0),
        nPixelHits = cms.int32(1),
        nMatchedStations=cms.int32(1),
        cutsToIgnore = cms.vstring('ED0', 'SD0', 'ECalVeto', 'HCalVeto'),
        RecalcFromBeamSpot = cms.bool(False),
        beamLineSrc = cms.InputTag("offlineBeamSpot"),
        pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
        ),
        
        muonIdLoose = cms.PSet(
        version = cms.string('FALL10'),
        Chi2 = cms.double(999.0),
        D0 = cms.double(999.0),
        ED0 = cms.double(999.0),
        SD0 = cms.double(999.0),
        NHits = cms.int32(-1),
        NValMuHits = cms.int32(-1),
        ECalVeto = cms.double(999.0),
        HCalVeto = cms.double(999.0),
        RelIso = cms.double(0.2),
        LepZ = cms.double(1.0),
        nPixelHits = cms.int32(1),
        nMatchedStations=cms.int32(1),        
        cutsToIgnore = cms.vstring('Chi2', 'D0', 'ED0', 'SD0', 'NHits','NValMuHits','ECalVeto','HCalVeto','LepZ','nPixelHits','nMatchedStations'),
        RecalcFromBeamSpot = cms.bool(False),
        beamLineSrc = cms.InputTag("offlineBeamSpot"),
        pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
        ),
        
        )
                                        )
    
elif options.ttbsmPAT == 0 and options.use42X == 0:
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
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(5),
        metMin = cms.double(20.0),
        useData = cms.bool( not inputDoMC ),
        heavyFlavour = cms.bool( useFlavorHistory ),
        doMC = cms.bool( inputDoMC),
        useTTBSMPat = cms.bool(False),
        sampleName = cms.string(inputSampleName),
        identifier = cms.string('PF'),
        cutsToIgnore=cms.vstring(inputCutsToIgnore)
        )                                    
                                        )
    
process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    identifier = cms.string('PF no MET')
    )
    )

process.pfShyftAnaMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    metMax = cms.double(20.),
    identifier = cms.string('PF MET < 20')
    )
    )

process.pfShyftAnaDataQCDLoose = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
	useAntiSelection = cms.bool(True),
	eRelIso = cms.double(0.15),
    identifier = cms.string('PF QCD Loose')     
    )
    )

process.pfShyftAnaNoMETDataQCDLoose = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
	useAntiSelection = cms.bool(True),
	eRelIso = cms.double(0.15),
    metMin = cms.double(0.0),
    identifier = cms.string('PF QCD Loose no MET')     
    )
    )

process.pfShyftAnaMETMax20DataQCDLoose = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
	useAntiSelection = cms.bool(True),
	eRelIso = cms.double(0.15),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    identifier = cms.string('PF QCD Loose MET < 20')     
    )
    )

process.p = cms.Path(
    process.patTriggerDefaultSequence*
    process.pfShyftAna*
    process.pfShyftAnaNoMET*              
    process.pfShyftAnaMETMax20

    ##__________my lost beloved QCD extraction method :(_____________
    #process.pfShyftAnaDataQCDLoose*       
    #process.pfShyftAnaNoMETDataQCDLoose*  
    #process.pfShyftAnaMETMax20DataQCDLoose 
    )

#suppress the L1 trigger error messages
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit =
cms.untracked.int32(0) )
