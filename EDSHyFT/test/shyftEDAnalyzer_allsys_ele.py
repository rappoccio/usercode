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
                 'Wjets',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register ('allSys',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run all systematics (1) or just the central one (0)")

options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('ttbsmPAT',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "If running on ttbsm PAT tuples"
                 )
options.register('use42X',
                 0,
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

if options.use42X > 0:
   use42XMC = True
else: use42XMC = False

inputDoMC=True

inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 and options.ttbsmPAT > 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/lpctlbsm/skhalil/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_9_1_gsY.root',
        '/store/user/lpctlbsm/skhalil/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/ttbsm_v7_Spring11-PU_S1_-START311_V1G1-v1/6a29f0fac22a95bcd534f59b8047bd70/ttbsm_41x_mc_99_1_AgZ.root',
        )
                                )                           
elif len(options.inputFiles) == 0 and options.ttbsmPAT == 0:
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/makouski/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/shyft_414_v1/4102b2143a05266d07e3ed7d177f56c8/shyft_414patch1_mc_9_1_Z8F.root',
        '/store/user/makouski/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/shyft_414_v1/4102b2143a05266d07e3ed7d177f56c8/shyft_414patch1_mc_99_1_yiR.root',
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

#_____________________________________PF__________________________________________________

if options.ttbsmPAT > 0:
    
    process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                        shyftAnalysis = inputShyftAnalysis.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        ePlusJets = cms.bool( True ),
        muPlusJets = cms.bool(False),        
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(5),
        metMin = cms.double(20.0),
        use42X  = cms.bool(use42XMC),
        heavyFlavour = cms.bool( useFlavorHistory ),
        doMC = cms.bool( inputDoMC),
        sampleName = cms.string(inputSampleName),
        identifier = cms.string('PF'),
        jetAlgo = cms.string("pf"),
        simpleSFCalc = cms.bool(False),                                        
        reweightBTagEff = cms.bool(True),
        weightSFCalc = cms.bool(True),                                        
        useCustomPayload = cms.bool(False),
        bcEffScale = cms.double(1.00),
        lfEffScale = cms.double(1.00),
        jetSmear = cms.double(0.1),
        cutsToIgnore=cms.vstring(inputCutsToIgnore),
        
       ##  pvSelector = cms.PSet(
##         pvSrc = cms.InputTag('goodOfflinePrimaryVertices'),
##         minNdof = cms.double(4.0),
##         maxZ = cms.double(15.0),
##         maxRho = cms.double(2.0)
##         ),
        
##         muonIdTight = cms.PSet(
##         version = cms.string('FALL10'),
##         Chi2 = cms.double(10.0),
##         D0 = cms.double(0.02),
##         ED0 = cms.double(999.0),
##         SD0 = cms.double(999.0),
##         NHits = cms.int32(11),
##         NValMuHits = cms.int32(0),
##         ECalVeto = cms.double(999.0),
##         HCalVeto = cms.double(999.0),
##         RelIso = cms.double(0.05),
##         LepZ = cms.double(1.0),
##         nPixelHits = cms.int32(1),
##         nMatchedStations=cms.int32(1),
##         cutsToIgnore = cms.vstring('ED0', 'SD0', 'ECalVeto', 'HCalVeto'),
##         RecalcFromBeamSpot = cms.bool(False),
##         beamLineSrc = cms.InputTag("offlineBeamSpot"),
##         pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
##         ),
        
##         muonIdLoose = cms.PSet(
##         version = cms.string('FALL10'),
##         Chi2 = cms.double(999.0),
##         D0 = cms.double(999.0),
##         ED0 = cms.double(999.0),
##         SD0 = cms.double(999.0),
##         NHits = cms.int32(-1),
##         NValMuHits = cms.int32(-1),
##         ECalVeto = cms.double(999.0),
##         HCalVeto = cms.double(999.0),
##         RelIso = cms.double(0.2),
##         LepZ = cms.double(1.0),
##         nPixelHits = cms.int32(1),
##         nMatchedStations=cms.int32(1),        
##         cutsToIgnore = cms.vstring('Chi2', 'D0', 'ED0', 'SD0', 'NHits','NValMuHits','ECalVeto','HCalVeto','LepZ','nPixelHits','nMatchedStations'),
##         RecalcFromBeamSpot = cms.bool(False),
##         beamLineSrc = cms.InputTag("offlineBeamSpot"),
##         pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
##         ),    
        
        )                                    
                                        )
    
elif options.ttbsmPAT == 0 :    
    process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                        shyftAnalysis = inputShyftAnalysis.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
        ePlusJets = cms.bool(True),
        muPlusJets = cms.bool(False),
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(5),
        metMin = cms.double(20.0),                                        
        heavyFlavour = cms.bool( useFlavorHistory ),
        doMC = cms.bool( inputDoMC),
        sampleName = cms.string(inputSampleName),
        identifier = cms.string('PF'),
        jetAlgo = cms.string("pf"),
        simpleSFCalc = cms.bool(False),                                        
        reweightBTagEff = cms.bool(True),
        weightSFCalc = cms.bool(True),                                        
        useCustomPayload = cms.bool(False),
        useTTBSMPat = cms.bool(False),
        bcEffScale = cms.double(1.00),
        lfEffScale = cms.double(1.00),
        jetSmear = cms.double(0.1),
        cutsToIgnore=cms.vstring(inputCutsToIgnore)
        )                                    
                                        )

#___________Special case of MET < 20 GeV_________________
process.pfShyftAnaMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MET <20'),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    )
    )
    
#_____________QCD WP95_______________________
process.pfShyftAnaQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF MET, WP95')
    )
    )

process.pfShyftAnaMETMax20QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MET <20, WP95'),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    eRelIso = cms.double(0.15),
    )
    )
#___________no MET cut________________
process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    identifier = cms.string('PF no MET')
    )
    )

process.pfShyftAnaQCDWP95NoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF no MET, WP95')
    )
    )

#______________To extract secvtx shapes and >=3 tag jets count _____________________

process.pfShyftAnaMC = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    )
    )

process.pfShyftAnaMCNoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC no MET'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    )
    )


process.pfShyftAnaMCQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC WP95'),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    eRelIso = cms.double(0.15),
    )
    )

process.pfShyftAnaMCQCDWP95NoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC WP95, NoMET'),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    eRelIso = cms.double(0.15),
    metMin = cms.double(0.0),
    )
    )

process.pfShyftAnaMCMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC MET < 20'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    )
    )
process.pfShyftAnaMCMETMax20QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC MET < 20, WP95'),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    eRelIso = cms.double(0.15),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    )
    )






################################################
#_______________Systematics__________________
#################################################

#________________________btagging Systematics ____________________________

##HF

process.pfShyftAnaReweightedBTag080 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 080'),
        bcEffScale = cms.double(0.80),        
        )
    )

process.pfShyftAnaReweightedBTag090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 090'),
        bcEffScale = cms.double(0.90),
        )
    )


process.pfShyftAnaReweightedBTag110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 110'),
        bcEffScale = cms.double(1.10),
        )
    )

process.pfShyftAnaReweightedBTag120 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 120'),
        bcEffScale = cms.double(1.20),
        )
    )


##LF

process.pfShyftAnaReweightedLFTag080 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 080'),
        lfEffScale = cms.double(0.80),
        )
    )

process.pfShyftAnaReweightedLFTag090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 090'),        
        lfEffScale = cms.double(0.90),
        )
    )

process.pfShyftAnaReweightedLFTag110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 110'),     
        lfEffScale = cms.double(1.10),
        )
    )

process.pfShyftAnaReweightedLFTag120 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 120'),
        lfEffScale = cms.double(1.20)
        )
    )

#____________________JES up and down _______________________

process.pfShyftAnaJES095 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(-1.0),
        jetUncertainty = cms.double(0.00),
        identifier = cms.string('PFJES095')
        )
    )

process.pfShyftAnaJES105 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.0),
        jetUncertainty = cms.double(0.00),
        identifier = cms.string('PFJES105')
        )
    )

#____________________JER _______________________
process.pfShyftAnaJER000 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetSmear = cms.double(0.00),
        identifier = cms.string('PFJER000')
        )
    )

process.pfShyftAnaJER020 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetSmear = cms.double(0.20),
        identifier = cms.string('PFJER020')
        )
    )

#____________________MET Resolution _______________________
process.pfShyftAnaMETRES090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        unclMetScale = cms.double( 0.90 ),
        identifier = cms.string('PFMETRES090')
        )
    )

process.pfShyftAnaMETRES110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        unclMetScale = cms.double( 1.10 ),
        identifier = cms.string('PFMETRES110')
        )
    )

process.pfShyftAnaEleEEPt125 =  process.pfShyftAna.clone(
     shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        ePtScale = cms.double(1.0),
        ePtUncertaintyEE = cms.double( 0.025),
        identifier = cms.string('PFEleEEPt125')
        )
    )

process.pfShyftAnaEleEEPt075 =  process.pfShyftAna.clone(
     shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        ePtScale = cms.double(-1.0),
        ePtUncertaintyEE = cms.double( 0.025),
        identifier = cms.string('PFEleEEPt075')
        )
    )

process.s = cms.Sequence(
   process.pfShyftAna*                 
   process.pfShyftAnaNoMET*
   
   process.pfShyftAnaJES095*    
   process.pfShyftAnaJES105*
   process.pfShyftAnaMETRES090*
   process.pfShyftAnaMETRES110*
   process.pfShyftAnaJER000*
   process.pfShyftAnaJER020*
   process.pfShyftAnaEleEEPt125*
   process.pfShyftAnaEleEEPt075*
   process.pfShyftAnaMC*
   process.pfShyftAnaMCNoMET*   
   process.pfShyftAnaMETMax20*
   process.pfShyftAnaMCMETMax20*
   process.pfShyftAnaReweightedBTag080*
   process.pfShyftAnaReweightedBTag090*
   process.pfShyftAnaReweightedBTag110*
   process.pfShyftAnaReweightedBTag120*
   process.pfShyftAnaReweightedLFTag080*
   process.pfShyftAnaReweightedLFTag090*
   process.pfShyftAnaReweightedLFTag110*
   process.pfShyftAnaReweightedLFTag120*
   
   process.pfShyftAnaQCDWP95*
   process.pfShyftAnaQCDWP95NoMET*
   process.pfShyftAnaMCQCDWP95*
   process.pfShyftAnaMCQCDWP95NoMET*
   process.pfShyftAnaMETMax20QCDWP95*
   process.pfShyftAnaMCMETMax20QCDWP95
   )

process.p = cms.Path(
    process.pfShyftAna*
    process.pfShyftAnaMC
    )

if options.allSys == 1 :
    process.p *= process.s

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
