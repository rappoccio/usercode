import FWCore.ParameterSet.Config as cms

process = cms.Process("EDMNtuple")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
import sys
#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')


options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")
options.register ('runData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "if running over data (1) else (0)")
options.register('eleEt',
                  25.,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.float,
                 "electron et threshold")
options.register('runLoose',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Run extra sequence(1) for loose selction  or ignore them (0)")

options.register('btagMap',
		 'Analysis/EDSHyFT/data/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph',
		 VarParsing.multiplicity.singleton,
		 VarParsing.varType.string,
		 "BTag Efficiency Map File")
                 
options.parseArguments()

print options

if options.runData == 1:
    runData = True
else: runData  = False

runNoEleID = options.runLoose

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source    
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    '/store/user/lpctlbsm/cjenkins/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_B/c04f3b4fa74c8266c913b71e0c74901d/tlbsm_53x_v2_mc_10_1_0GF.root',
    )
                            )                           

## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

if runData:
    process.GlobalTag.globaltag = 'GR_P_V40_AN1::All'
else:
    process.GlobalTag.globaltag = 'START53_V7F::All'

process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

# apply the JEC on fly
payloads = [
    'Jec12_V2_L1FastJet_AK5PFchs.txt',
    'Jec12_V2_L2Relative_AK5PFchs.txt', 
    'Jec12_V2_L3Absolute_AK5PFchs.txt',
    'Jec12_V2_L2L3Residual_AK5PFchs.txt',
    'Jec12_V2_Uncertainty_AK5PFchs.txt',   
]

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis
#_______________________________BTagging SF and Pileup________________________________________

if not runData:
    process.pileupReweightingProducer = cms.EDProducer("PileupReweightingPoducer",
                                         FirstTime = cms.untracked.bool(False),
                                         oneDReweighting = cms.untracked.bool(True),
                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
                                         PileupDataFile = cms.untracked.string('PUData_finebin_dist.root')
                                                       )

    # creates value maps to jets as userInt index:
    #-1 -- ignore, 1 -- right out of the box, 2 -- Nominal SF, 4 -- SF up, 8 -- SF down.
    print options.btagMap+'_AK5PF_CSVM_bTaggingEfficiencyMap.root'
    process.goodPatJetsPFSF = cms.EDProducer("BTaggingSFProducer",
        JetSource = cms.InputTag('goodPatJetsPFlow'),
        DiscriminatorTag = cms.string('combinedSecondaryVertexBJetTags'),
        DiscriminatorValue = cms.double(0.679),
        EffMapFile = cms.string(options.btagMap+'_AK5PF_CSVM_bTaggingEfficiencyMap.root')
    )

    process.goodPatJetsCA8PrunedPFSF = cms.EDProducer("BTaggingSFProducer",
        JetSource = cms.InputTag('goodPatJetsCA8PrunedPF'),
        DiscriminatorTag = cms.string('combinedSecondaryVertexBJetTags'),
        DiscriminatorValue = cms.double(0.679),
        EffMapFile = cms.string(options.btagMap+'_CA8PrunedPF_CSVM_bTaggingEfficiencyMap.root')
    )

    process.GenInfo = cms.EDProducer('BoostedParticles')

#_____________________________________PF__________________________________________________


from Analysis.SHyFT.shyftselection_cfi import wplusjetsAnalysis as shyftSelectionInput

## electron+jets decay mode
## ========================
process.pfTupleEle = cms.EDFilter('EDSHyFTSelector',
    shyftSelection = shyftSelectionInput.clone(
	muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
	electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
	metSrc = cms.InputTag('patMETsPFlow'),
	jetSrc = cms.InputTag('goodPatJetsPFSF'),
	pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
	ePlusJets = cms.bool( True ),
	muPlusJets = cms.bool( False ),
	eEt = cms.double( 25.0 ),
    muPtMin = cms.double( 25.0 ),
	jetPtMin = cms.double(25.0),
	minJets = cms.int32(1),
    eRelIso = cms.double( 0.2 ), #loose iso
    muRelIso = cms.double( 0.2), #loose iso
	useNoPFIso = cms.bool(False),
	useNoID  = cms.bool(False), # use eMVA > 0
	useData = cms.bool(runData),
	identifier = cms.string('AK5 PF'),
	cutsToIgnore=cms.vstring(inputCutsToIgnore),
	jecPayloads = cms.vstring( payloads ),
    ),
    matchByHand = cms.bool(False),
    useData = cms.bool(runData)                              
)

## e+jets with loose collections
process.pfTupleEleLoose = process.pfTupleEle.clone()
process.pfTupleEleLoose.shyftSelection.muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose')
process.pfTupleEleLoose.shyftSelection.electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose')
process.pfTupleEleLoose.shyftSelection.eRelIso = cms.double( 0.5)
process.pfTupleEleLoose.shyftSelection.useNoID  = cms.bool(True)
process.pfTupleEleLoose.shyftSelection.identifier = cms.string('AK5 PF Loose electrons')

## e+jets with ca8jets
process.pfTupleEleCA8Pruned = process.pfTupleEle.clone()
process.pfTupleEleCA8Pruned.shyftSelection.jetSrc = cms.InputTag('goodPatJetsCA8PrunedPFSF')
process.pfTupleEleCA8Pruned.shyftSelection.identifier = cms.string('CA8 Prunded PF')
process.pfTupleEleCA8Pruned.matchByHand = cms.bool(True)

## e+jets MET unclus systematics
process.pfTupleEleMetRes090 =  process.pfTupleEle.clone()
process.pfTupleEleMetRes090.shyftSelection.jetSmear = cms.double(0.1)
process.pfTupleEleMetRes090.shyftSelection.unclMetScale = cms.double( 0.90 )
process.pfTupleEleMetRes090.shyftSelection.identifier = cms.string('PFMETRES090')

process.pfTupleEleMetRes110 =  process.pfTupleEle.clone()
process.pfTupleEleMetRes110.shyftSelection.jetSmear = cms.double(0.1)
process.pfTupleEleMetRes110.shyftSelection.unclMetScale = cms.double( 1.10 )
process.pfTupleEleMetRes110.shyftSelection.identifier = cms.string('PFMETRES110')

## mu+jets decay mode
## =================
process.pfTupleMu = process.pfTupleEle.clone()
process.pfTupleMu.ePlusJets = cms.bool( False )
process.pfTupleMu.muPlusJets = cms.bool( True )

## mu+jets with loose collections
process.pfTupleMuLoose = process.pfTupleMu.clone()
process.pfTupleMuLoose.shyftSelection.muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose')
process.pfTupleMuLoose.shyftSelection.electronSrc = cms.InputTag('selectedPatElectronsPFlowLoose')
process.pfTupleMuLoose.shyftSelection.muRelIso = cms.double(0.5)
process.pfTupleMuLoose.shyftSelection.identifier = cms.string('AK5 PF Loose muons')

## mu+jets with ca8jets
process.pfTupleMuCA8Pruned = process.pfTupleMu.clone()
process.pfTupleMuCA8Pruned.shyftSelection.jetSrc = cms.InputTag('goodPatJetsCA8PrunedPFSF')
process.pfTupleMuCA8Pruned.shyftSelection.identifier = cms.string('CA8 Prunded PF')
process.pfTupleMuCA8Pruned.matchByHand = cms.bool(True)

## mu+jets MET unclus systematics
process.pfTupleMuMetRes090 =  process.pfTupleMu.clone()
process.pfTupleMuMetRes090.shyftSelection.jetSmear = cms.double(0.1)
process.pfTupleMuMetRes090.shyftSelection.unclMetScale = cms.double( 0.90 )
process.pfTupleMuMetRes090.shyftSelection.identifier = cms.string('PFMETRES090')

process.pfTupleMuMetRes110 =  process.pfTupleMu.clone()
process.pfTupleMuMetRes110.shyftSelection.jetSmear = cms.double(0.1)
process.pfTupleMuMetRes110.shyftSelection.unclMetScale = cms.double( 1.10 )
process.pfTupleMuMetRes110.shyftSelection.identifier = cms.string('PFMETRES110')

## configure output module
process.p0 = cms.Path( process.patTriggerDefaultSequence )
process.p1 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEle)
process.p2 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMu)
process.p3 = cms.Path( process.goodPatJetsCA8PrunedPFSF * process.pfTupleEleCA8Pruned)
process.p4 = cms.Path( process.goodPatJetsCA8PrunedPFSF * process.pfTupleMuCA8Pruned)
process.p5 = cms.Path( process.goodPatJetsPFSF * process.pfTupleEleLoose)
process.p6 = cms.Path( process.goodPatJetsPFSF * process.pfTupleMuLoose)
process.p7 = cms.Path()

if not runData:
    process.p7 = cms.Path( process.pileupReweightingProducer * process.GenInfo *
                           process.pfTupleEleMetRes090 * process.pfTupleEleMetRes110 *
                           process.pfTupleMuMetRes090 * process.pfTupleMuMetRes110)

process.out = cms.OutputModule("PoolOutputModule",
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring( 'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7') ),
                               fileName =  cms.untracked.string('edmTest.root'),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_pfTuple*_*_*',
                                                                      'drop *_pfTuple*CA8Pruned_*_*',
                                                                      'keep *_pfTuple*CA8Pruned_jets_*',
                                                                      'keep *_pfTuple*CA8Pruned_MET_*',
                                                                      'keep *_patTriggerEvent_*_*',
                                                                      'keep *_patTrigger_*_*',
                                                                      'keep *_kt6PFJetsForIsolation_rho_*',
                                                                      'keep *_goodOfflinePrimaryVertices_*_*',
                                                                      'keep *_caPrunedPFlow_SubJets_*'
                                                                      ),
                               )
if not runData:
    process.out.outputCommands += [
                                'drop *_pfTuple*Loose_*_*',
                                'drop *_pfTuple*MetRes*_*_*',
                                'keep *_pfTuple*MetRes*_MET_*',
                                'keep *_GenInfo*_*_*',
                                'keep *_*_pileupWeights_*',
                                'keep PileupSummaryInfos_*_*_*',
                                ]
 
## output path
process.outpath = cms.EndPath(process.out)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

open('junk.py','w').write(process.dumpPython())
